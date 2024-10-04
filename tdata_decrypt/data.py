import os
import hashlib
from typing import Tuple, List, Dict
from io import BytesIO
from tdata_decrypt.qt import read_qt_int32, read_qt_uint64
from tdata_decrypt.tdf import SettingsTDF, KeyTDF
from tdata_decrypt.settings import SettingsBlocks, read_key_data_accounts

def file_to_to_str(filekey: bytes):
    return ''.join(f'{b:X}'[::-1] for b in filekey)


def compute_data_name_key(dataname: str):
    filekey = hashlib.md5(dataname.encode('utf8')).digest()[:8]

    return file_to_to_str(filekey)


def compose_account_name(index: int):
    if index > 0:
        return f'data#{index+1}'

    return 'data'


class MtpData:
    def __init__(self):
        self.user_id: int = None
        self.main_dc_id: int = None
        self.keys: Dict[int, bytes] = None
        self.keys_to_destroy: Dict[int, bytes] = None

    @classmethod
    def from_bytes(cls, data: bytes):
        stream = BytesIO(data)

        mtp_data = cls()
        mtp_data.user_id = read_qt_int32(stream) # legacy_user_id
        mtp_data.main_dc_id = read_qt_int32(stream) # legacy_main_dc_id
        if mtp_data.user_id == -1 and mtp_data.main_dc_id == -1:
            mtp_data.user_id = read_qt_uint64(stream)
            mtp_data.main_dc_id = read_qt_int32(stream)

        def read_keys():
            return {
                read_qt_int32(stream): stream.read(256)
                for _ in range(read_qt_int32(stream)) # count
            }

        mtp_data.keys = read_keys()
        mtp_data.keys_to_destroy = read_keys()

        return mtp_data


class Account:
    def __init__(self, base_path: str, index: int):
        self._base_path = base_path
        self.index = index
        self.account_name = compose_account_name(index)
        self.dataname_key = compute_data_name_key(self.account_name)
        self.local_key = None
        self.mtp_data = None

    @classmethod
    def get_by_index(cls, base_path: str, index: int, local_key: bytes):
        account = cls(base_path, index)
        account.local_key = local_key
        account.mtp_data = account.read_mtp_data(local_key)

        return account

    def read_mtp_data(self, local_key: bytes) -> MtpData:
        tdf = SettingsTDF.from_file(
            os.path.join(self._base_path, self.dataname_key)
        )
        blocks = tdf.get_settings(local_key, False)

        return MtpData.from_bytes(
            blocks.get(SettingsBlocks.dbiMtpAuthorization)
        )


class TData:
    def __init__(self):
        self.settings = None
        self.local_key = None
        self.accounts: Dict[int, Account] = {}

    @classmethod
    def read_accounts(cls, path: str, password: str = ''):
        local_key, accounts_index = KeyTDF.read_key(
            os.path.join(path, 'key_data'),
            password
        )
        account_indexes, _ = read_key_data_accounts(BytesIO(accounts_index))

        tdata = cls()
        tdata.settings = SettingsTDF.read_settings(
            os.path.join(path, 'settings'),
        )
        tdata.local_key = local_key
        tdata.accounts = {}
        for index in account_indexes:
            tdata.accounts[index] = Account.get_by_index(
                path, index, local_key
            )

        return tdata
