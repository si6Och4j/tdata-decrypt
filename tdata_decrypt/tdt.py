from io import BytesIO

class TDRawBytes:
    size = 0

    @classmethod
    def read(cls, data: BytesIO):
        return cls._read_value(data)

    @staticmethod
    def _read_value(data: BytesIO):
        return cls._read_bytes(data, cls.size)

    @staticmethod
    def _read_bytes(data: BytesIO, size: int):
        result = data.read(size)
        if len(result) != size:
            raise StopIteration()

        return result


class TDInteger(TDRawBytes):
    signed = False

    @classmethod
    def _read_value(cls, data: BytesIO):
        return int.from_bytes(
            cls._read_bytes(data, cls.size), 'big', signed=cls.signed
        )


class TDInt32(TDInteger):
    size = 4
    signed = True


class TDUInt32(TDInteger):
    size = 4
    signed = False


class TDInt64(TDInteger):
    size = 8
    signed = True


class TDUInt64(TDInteger):
    size = 8
    signed = False


class TDByteArray(TDRawBytes):
    @classmethod
    def _read_value(cls, data: BytesIO):
        size = TDInt32.read(data)
        if size <= 0:
            return b''

        return cls._read_bytes(data, size)


class TDBoolean(TDInt32):
    @classmethod
    def read(cls, data: BytesIO):
        return cls._read_value(data) == 1


class TDString(TDByteArray):
    @classmethod
    def read(cls, data: BytesIO):
        return cls._read_value(data).decode('utf16')
