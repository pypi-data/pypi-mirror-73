class NetFile:
    def __init__(self):
        pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def read(self, chunk_bytes: int = None) -> bytes:
        raise NotImplementedError()


class NetFileError(Exception):
    pass


class InvalidFileRequestError(NetFileError):
    pass


class FileUnavailableError(NetFileError):
    pass


class FileMissingError(InvalidFileRequestError):
    pass


class InvalidFileRangeError(InvalidFileRequestError):
    pass
