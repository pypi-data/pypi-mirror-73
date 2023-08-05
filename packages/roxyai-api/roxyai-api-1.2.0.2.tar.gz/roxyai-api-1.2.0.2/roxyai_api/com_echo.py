# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
from .com_definition import COM_ECHO
from .com_base import BaseCommand


class EchoCommand(BaseCommand):
    code = COM_ECHO

    def __init__(self, data: bytes, connection=None):
        super().__init__(connection)
        # 要求データの設定
        self.data = data

    def recv(self):
        reply_data = super().recv()
        # 応答データの妥当性チェック
        if self.data != reply_data:
            raise RuntimeError(f'mismatched echo reply data')

    def __str__(self):
        string = (
            f'Echo({self.code:02x}) '
            f'Data: {self.data[:min(len(self.data), 128)]} '
            f'{len(self.data):,} bytes '
        )
        if self.recv_time:
            string += f'({self.get_process_time()} ms)'
        return string
