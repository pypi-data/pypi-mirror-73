from os import path

from net_file.net_file import open_url


def test_read_local_file():
    readme_file_path = path.normpath(path.join(path.abspath(path.dirname(__file__)), '..', 'examples', 'samples', 'test_file.txt'))

    parts = []
    with open_url(
            url=f'file://{readme_file_path}',
            start_bytes=20,
            length=30,
    ) as open_file:
        content = open_file.read(7)
        while content:
            parts.append(content)
            content = open_file.read(7)
    assert parts == [b'2222222', b'2223333', b'3333334', b'4444444', b'44']
