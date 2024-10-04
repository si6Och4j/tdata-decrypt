import hashlib
from io import BytesIO
from tdata_decrypt.settings import read_settings_blocks
from tdata_decrypt.crypto import create_local_key, create_legacy_local_key, decrypt_local
from tdata_decrypt.qt import read_qt_byte_array

class RawTDF:
    MAGIC = b'TDF$'

    class ParseError(Exception):
        pass

    def __init__(self):
        self.version = None
        self.encrypted_data = None
        self.hashsum = None
        self.path = None

    def get_size(self) -> int:
        return int.from_bytes(self.encrypted_data[0:4], 'big', True)

    def get_data(self) -> bytes:
        return self.encrypted_data[4:]

    def get_decrypted_data(self, local_key: bytes):
        return decrypt_local(self.get_data(), local_key)

    def get_stream(self) -> BytesIO:
        return BytesIO(self.encrypted_data)

    @classmethod
    def from_file(cls, path: str):
        for candidate in [path + 's', path]:
            with open(candidate, 'rb') as f:
                tdf = cls.from_bytes(f.read())
                tdf.path = candidate

                return tdf

        raise FileNotFoundError('Unable to locate TDF')

    @classmethod
    def from_bytes(cls, data: bytes):
        if data[:4] != cls.MAGIC:
            raise ParseError('Wrong magic. Not a TDF file?')

        tdf = cls()
        tdf.version = int.from_bytes(data[4:8], 'little')
        tdf.encrypted_data = data[8:-16]
        tdf.hashsum = data[-16:]

        checksum = hashlib.md5(
            tdf.encrypted_data +
            len(tdf.encrypted_data).to_bytes(4, 'little') +
            tdf.version.to_bytes(4, 'little') +
            cls.MAGIC
        ).digest()

        if checksum != tdf.hashsum:
            raise TdfParserError('Wrong hashsum. Corrupted file?')

        return tdf


class KeyTDF(RawTDF):
    def get_key(self, password: bytes = b''):
        stream = self.get_stream()

        salt = read_qt_byte_array(stream)
        key_sealed = read_qt_byte_array(stream)
        info_sealed = read_qt_byte_array(stream)

        key = create_local_key(password, salt)

        local_key = decrypt_local(key_sealed, key)
        index = decrypt_local(info_sealed, local_key)

        return local_key, index

    @classmethod
    def read_key(cls, path: str, password: str = ''):
        return cls.from_file(path).get_key(password.encode())


class SettingsTDF(RawTDF):
    def get_raw_settings(self, key: str = ''):
        stream = self.get_stream()
        salt = read_qt_byte_array(stream)
        data = read_qt_byte_array(stream)

        key = create_legacy_local_key(key, salt)

        return decrypt_local(data, key)

    def get_settings(self, key: str = '', extract_key: bool = True):
        if extract_key:
            data = self.get_raw_settings(key)
        else:
            data = self.get_decrypted_data(key)

        return read_settings_blocks(
            self.version,
            BytesIO(data),
        )

    @classmethod
    def read_settings(cls, path: str, key: bytes = b'', extract_key: bool = True):
        return cls.from_file(path).get_settings(key, extract_key)
