# (c) Roxy Corp. 2020-, CONFIDENTIAL
# Roxy AI Inspect-Server communication definition

# フレームのヘッダ定義
SIGN_CODE = 0x6941
HEADER_SIZE = 8

# ステータス定義
STS_REQUEST = 0x00
STS_REPLY_ACK = 0x01
ERR_INVALID_DATA_SIZE = 0x0D
ERR_UNKNOWN_EXCEPTION = 0x0E
ERR_INVALID_COMMAND = 0x0F
ERR_NOT_FOUND_PRODUCT = 0x11
ERR_NOT_FOUND_MODEL = 0x12
ERR_DENIED_PRODUCT = 0x13
ERR_FAILED_LOAD_CONFIG = 0x14
ERR_FAILED_INITIALIZE = 0x15
ERR_FAILED_LOGGING = 0x16
ERR_INVALID_MODEL_ID = 0x21
ERR_INVALID_IMG_FORMAT = 0x22
ERR_INVALID_IMG_DATA = 0x23
ERR_INVALID_JSON_DATA = 0x24
ERR_UNINITIALIZED = 0x25
ERR_OVERLAP_INSPECT_ID = 0x26
ERR_FAILED_INSPEC = 0x27

STATUS_LIST = {
    STS_REQUEST: 'Request',
    STS_REPLY_ACK: 'ACK',
    ERR_INVALID_DATA_SIZE: 'ERR: Invalid command data size',
    ERR_UNKNOWN_EXCEPTION: 'ERR: Unknown exception',
    ERR_INVALID_COMMAND: 'ERR: Unknown command',
    ERR_NOT_FOUND_PRODUCT: 'ERR: Cannot find product folder',
    ERR_NOT_FOUND_MODEL: 'ERR: Cannot find model data',
    ERR_DENIED_PRODUCT: 'ERR: Denied open additional product',
    ERR_FAILED_LOAD_CONFIG: 'ERR: Loading config file failed',
    ERR_FAILED_INITIALIZE: 'ERR: Model initialization failed',
    ERR_FAILED_LOGGING: 'ERR: Output inspection log failed',
    ERR_INVALID_MODEL_ID: 'ERR: Invalid model id',
    ERR_INVALID_IMG_FORMAT: 'ERR: Invalid image format id',
    ERR_INVALID_IMG_DATA: 'ERR: Invalid image data',
    ERR_INVALID_JSON_DATA: 'ERR: Invalid JSON data',
    ERR_UNINITIALIZED: 'ERR: Uninitialized',
    ERR_OVERLAP_INSPECT_ID: 'ERR: Overlapped inspect id',
    ERR_FAILED_INSPEC: 'ERR: Inspection failed',
}

# コマンドの定義
COM_ECHO = 0x10
COM_INITIALIZE = 0x11
COM_TERMINATE = 0x12
COM_INSPECT = 0x13

COM_LIST = {
    COM_ECHO: 'Echo',
    COM_INITIALIZE: 'Initialize',
    COM_TERMINATE: 'Terminate',
    COM_INSPECT: 'Inspect',
}


def get_status(status):
    return STATUS_LIST.get(status, 'Unknown Status')


def get_command(command):
    return COM_LIST.get(command, 'Unknown Command Code')
