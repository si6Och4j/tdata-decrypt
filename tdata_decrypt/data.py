from __future__ import annotations
import os
import hashlib
from io import BytesIO
from tdata_decrypt.tdt import TDInt32, TDUInt64
from tdata_decrypt.tdf import SettingsTDF, KeyTDF
from tdata_decrypt.settings import (
    SettingsBlocks,
    Settings,
    read_key_data_accounts)

def compute_data_name_key(dataname: str):
    filekey = hashlib.md5(dataname.encode('utf8')).digest()[:8]

    return ''.join(f'{b:X}'[::-1] for b in filekey)

class MtpData:
    def __init__(self):
        self.user_id: int = None
        self.main_dc_id: int = None
        self.keys: dict[int, bytes] = None
        self.keys_to_destroy: dict[int, bytes] = None

    @classmethod
    def from_bytes(cls, data: bytes) -> MtpData:
        stream = BytesIO(data)

        mtp_data = cls()
        mtp_data.user_id = TDInt32.read(stream) # legacy_user_id
        mtp_data.main_dc_id = TDInt32.read(stream) # legacy_main_dc_id
        if mtp_data.user_id == -1 and mtp_data.main_dc_id == -1:
            mtp_data.user_id = TDUInt64.read(stream)
            mtp_data.main_dc_id = TDInt32.read(stream)

        def read_keys():
            return {
                TDInt32.read(stream): stream.read(256)
                for _ in range(TDInt32.read(stream))
            }

        mtp_data.keys = read_keys()
        mtp_data.keys_to_destroy = read_keys()

        return mtp_data


class Account:
    def __init__(self, base_path: str, index: int):
        self._base_path = base_path
        self.index = index

        self.account_name = 'data'
        if index > 0:
            self.account_name += f'#{index + 1}'

        self.dataname_key = compute_data_name_key(self.account_name)
        self.local_key = None
        self.mtp_data = None

    @classmethod
    def get_by_index(
            cls, base_path: str,
            index: int, local_key: bytes) -> Account:
        account = cls(base_path, index)
        account.local_key = local_key
        account.mtp_data = account.read_mtp_data(local_key)

        return account

    def read_mtp_data(self, local_key: bytes) -> MtpData:
        tdf = SettingsTDF.from_file(
            os.path.join(self._base_path, self.dataname_key))
        blocks = tdf.get_settings(local_key, False)

        return MtpData.from_bytes(
            blocks.get(SettingsBlocks.dbiMtpAuthorization))


class TData:
    def __init__(self, path: str, password: str = ''):
        self.local_key, self.accounts_index = KeyTDF.read_key(
            os.path.join(path, 'key_data'), password)

        self.path = path
        self.settings: Settings | None = None
        self.accounts: dict[int, Account] | None = None
        self.main_account: int | None = None

    def read_settings(self) -> Settings:
        if not self.settings is None:
            return self.settings

        self.settings = SettingsTDF.read_settings(
            os.path.join(path, 'settings'))

        return self.settings

    def read_accounts(self) -> dict[int, Account]:
        if not self.accounts is None:
            return self.accounts

        account_indexes, self.main_account = read_key_data_accounts(
            BytesIO(self.accounts_index))

        self.accounts = {}
        for index in account_indexes:
            self.accounts[index] = Account.get_by_index(
                self.path, index, self.local_key)

        return self.accounts

    def get_main_account(self) -> int:
        self.read_accounts()

        return self.main_account
