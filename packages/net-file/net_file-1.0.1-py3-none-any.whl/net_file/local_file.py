from pathlib import Path
from typing import Tuple

from net_file.common import FileMissingError
from net_file.common import FileUnavailableError
from net_file.common import InvalidFileRangeError
from net_file.common import InvalidFileRequestError
from net_file.common import NetFile


class LocalFile(NetFile):
    def __init__(
            self,
            path: Path,
            start_bytes: int = None,
            length: int = None,
    ):
        super().__init__()
        if start_bytes < 0 or length < 0:
            raise InvalidFileRangeError()

        self._path = path
        self._start_bytes = start_bytes or 0
        self._length = length
        self._raw_file = None
        self._remaining_bytes = 0

    def read(self, chunk_bytes: int = None) -> bytes:
        assert chunk_bytes is None or chunk_bytes > 0

        if self.closed:
            raise InvalidFileRequestError('File is closed')

        content = b''
        if self._remaining_bytes:
            try:
                if chunk_bytes is not None:
                    content = self._raw_file.read(min(self._remaining_bytes, chunk_bytes))
                else:
                    content = self._raw_file.read(self._remaining_bytes)
            except IOError as exc:
                raise FileUnavailableError(f'File become unavailable ({exc})')

        self._remaining_bytes -= len(content)
        return content

    @property
    def closed(self) -> bool:
        return not self._raw_file or self._raw_file.closed

    def open(self) -> None:
        if self._raw_file and not self._raw_file.closed:
            return

        try:
            self._raw_file = self._path.open(mode='rb')
        except FileNotFoundError:
            raise FileMissingError(f'File {self._path} is missing')
        except IOError as exc:
            raise InvalidFileRequestError(f'Failed to open file ({exc})')

        file_size = self._path.stat().st_size
        if self._start_bytes or self._length:
            length = (self._length or file_size) - self._start_bytes
            self._remaining_bytes = self._length
            if self._start_bytes + length > file_size:
                raise InvalidFileRangeError(f'Invalid file length/start offset specified ({self._length}/{self._start_bytes}). File length: {file_size}')

        if self._start_bytes:
            try:
                self._raw_file.seek(self._start_bytes)
            except IOError:
                raise InvalidFileRangeError(f'Failed to seek file to {self._start_bytes} position')

    def close(self) -> None:
        if not self._raw_file or self._raw_file.closed:
            return

        try:
            self._raw_file.close()
        except IOError:
            pass
        finally:
            self._raw_file = None


def supported_schemas() -> Tuple[str, ...]:
    return 'file',


def open_local_file(
        url: str,
        start_bytes: int = None,
        length: int = None,
) -> NetFile:
    assert url.startswith('file:///')
    return LocalFile(
        path=Path(url[7:]),
        start_bytes=start_bytes,
        length=length,
    )
