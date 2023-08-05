from typing import Tuple

import requests

from net_file.common import FileUnavailableError
from net_file.common import InvalidFileRangeError
from net_file.common import InvalidFileRequestError
from net_file.common import NetFile


class HttpFile(NetFile):
    def __init__(
            self,
            url: str,
            start_bytes: int = None,
            length: int = None,
    ):
        super().__init__()
        if start_bytes < 0 or length < 0:
            raise InvalidFileRangeError()

        self._url = url
        self._start_bytes = start_bytes or 0
        self._length = length
        self._remaining_bytes = 0
        self._response = None
        self._response_generator = None

    def open(self) -> None:
        if self._response is not None:
            return

        response = requests.head(url=self._url, headers={'Accept-Encoding': 'identity'})
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise InvalidFileRequestError(str(exc))

        file_size = int(response.headers['Content-Length'])

        headers = {}
        if self._start_bytes or self._length:
            length = (self._length or file_size) - self._start_bytes
            self._remaining_bytes = self._length
            if self._start_bytes + length > file_size:
                raise InvalidFileRangeError(f'Invalid file length/start offset specified ({self._length}/{self._start_bytes}). File length: {file_size}')
            accept_ranges = response.headers.get('Accept-Ranges')
            if accept_ranges != 'bytes':
                raise InvalidFileRangeError(f"Server doesn't support ranges")

            range_from = self._start_bytes or 0
            range_to = (self._length + range_from - 1) if self._length else (file_size - 1)
            headers['Range'] = f'bytes={range_from}-{range_to}'

        self._response = requests.get(url=self._url, stream=True, headers=headers)
        try:
            self._response.raise_for_status()
        except requests.HTTPError as exc:
            raise InvalidFileRequestError(str(exc))

    def close(self) -> None:
        if not self._response:
            return
        self._response.close()
        self._response = None

    def read(self, chunk_bytes: int = None) -> bytes:
        if not self._response:
            raise InvalidFileRequestError('File is closed')

        def _generator():
            chunk_size = None if chunk_bytes is None else (chunk_bytes or 1024)
            try:
                for chunk in self._response.iter_content(chunk_size=chunk_size):
                    yield chunk
            except requests.RequestException:
                raise FileUnavailableError()

        if not self._response_generator:
            self._response_generator = _generator()

        try:
            return next(self._response_generator)
        except StopIteration:
            self._response_generator = None
            self._response.close()
            self._response = None


def supported_schemas() -> Tuple[str, ...]:
    return 'http', 'https'


def open_http_url(
        url: str,
        start_bytes: int = None,
        length: int = None,
) -> NetFile:
    return HttpFile(url=url, start_bytes=start_bytes, length=length)
