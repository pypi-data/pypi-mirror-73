import base64

from net_file.net_file import open_url


def tutorial():
    with open_url(
            url='http://10.16.10.131:8888/storage/prepared_datasets/27.12_bord_real/video/02d87f31-ab38-43ae-9d28-bb256c725192.mp4',
            start_bytes=10000,
            length=20000,
    ) as open_file:
        content = open_file.read()
        while content:
            print(len(content), base64.b64encode(content))
            content = open_file.read()

    with open_url(
            url='file:///opt/project/examples/samples/test_file.txt',
            start_bytes=20,
            length=30,
    ) as open_file:
        content = open_file.read(7)
        while content:
            print(content, end='')
            content = open_file.read(7)
        print()

    open_file = open_url(
            url='file:///opt/project/examples/samples/test_file.txt',
            start_bytes=30,
            length=20,
    )
    open_file.open()
    content = open_file.read()
    print(content)
    open_file.close()
    open_file.open()
    content = open_file.read(10000)
    print(content)


if __name__ == "__main__":
    tutorial()
