import base64
from urllib.parse import urlparse

from net_file.common import NetFile
from net_file.local_file import supported_schemas as local_schemas
from net_file.local_file import open_local_file
from net_file.http_file import supported_schemas as http_schemas
from net_file.http_file import open_http_url


_SCHEMA_HANDLERS = {
    local_schemas(): open_local_file,
    http_schemas(): open_http_url,
}


def open_url(
        url: str,
        start_bytes: int = None,
        length: int = None,
) -> NetFile:
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme.lower()
    for schemas, handler in _SCHEMA_HANDLERS.items():
        if scheme in schemas:
            return handler(
                url=url,
                start_bytes=start_bytes,
                length=length,
            )
    raise ValueError(f'Unknown schema {parsed_url.scheme}')
