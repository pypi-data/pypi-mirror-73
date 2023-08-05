# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
import time
from struct import pack, unpack

from .com_definition import (
    SIGN_CODE,
    HEADER_SIZE,
    STS_REQUEST,
    STS_REPLY_ACK,
    STATUS_LIST,
    get_status,
    get_command,
)

import logging.config
log = logging.getLogger(__name__)

# サーバの定義
HOST = '127.0.0.1'
PORT = 6945


class BaseCommand():
    code = None
    data = b''
    connection = None

    STATUS_SET = set(STATUS_LIST.keys())
    STATUS_SET.discard(STS_REQUEST)

    def __init__(self, connection=connection):
        """ 基底コマンドクラス
            Args:
                code        :   送信するコマンド番号
                connection  :   接続管理クラス（Option）
        """
        if connection:
            # 接続指定があればクラス変数ではなくインスタンス変数を利用
            self.connection = connection
        self.status = None
        self.send_time = None
        self.recv_time = None

    def send(self, extension: bytes = b''):
        """ コマンドの送信
        """
        data = self.data
        # 指定がなければ現在の接続を使う
        if self.connection is None:
            connection = self.current
        else:
            connection = self.connection

        code = self.code
        size = len(data) + len(extension)

        buffer = pack(f'< H L B B {len(data)}s', SIGN_CODE, size, code, STS_REQUEST, data)

        log.debug(
            f'Send command code:{code:02x}({get_command(code)}), '
            f'size: {size:,d} bytes'
        )

        self.send_time = time.time()
        self.recv_time = None
        connection.sock.sendall(buffer)
        if extension:
            connection.sock.sendall(extension)

    def recv(self):
        """ コマンドの送信
            Returns:
                status: int     返信コマンドステータス
                code:   int     返信コマンド番号
                data:   bytes   返信コマンドデータ
        """
        # 指定がなければ現在の接続を使う
        # if self.connection is None:
        #     connection = current
        # else:
        #     connection = self.connection

        # ヘッダの読み込み
        buf = self.connection.sock.recv(HEADER_SIZE)
        self.recv_time = time.time()
        if len(buf) == 0:
            # サーバによる切断
            raise ConnectionResetError

        if len(buf) < HEADER_SIZE:
            # ゴミ受信のため破棄
            raise RuntimeError(f'Receive invalid header size data: {len(buf)} bytes')

        sign, size, code, status = unpack('< H L B B', buf[0:HEADER_SIZE])
        if sign != SIGN_CODE:
            # パケット種別チェック
            raise RuntimeError(f'Receive invalid signe code: 0x{sign:04x}')

        # 受信ヘッダデータの検証
        if code != self.code:
            raise RuntimeError(f'Received command code:0x{code:02X} is mismatched 0x{self.code:02X}')

        if status not in self.STATUS_SET:
            raise RuntimeError(f'Receive invalid status: 0x{status:02x}')

        reply_data = b''
        while len(reply_data) < size:
            reply_data += self.connection.sock.recv(size - len(reply_data))

        log.debug(
            f'Receive command code:{code:02x}({get_command(code)}), '
            f'status:{status:02x}({get_status(status)}), '
            f'size: {size:,d} bytes'
        )

        self.status = status
        if self.status != STS_REPLY_ACK:
            reply_data = b''
        return reply_data

    def run(self):
        """ コマンドの送受信
            Returns:
                status: int     返信コマンドステータス
                data:   bytes   返信コマンドデータ
        """
        # コマンドの送信＆受信
        self.send()
        reply_data = self.recv()

        return reply_data

    def get_process_time(self):
        """ コマンドの要求～応答の処理時間 [ms]
        """
        process_time = None
        if self.send_time and self.recv_time:
            process_time = (self.recv_time - self.send_time) * 1000

        return process_time
