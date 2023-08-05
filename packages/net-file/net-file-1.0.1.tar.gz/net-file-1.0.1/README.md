# Net-file ranged read file access abstraction library

net-file allows you to access files by URL the same way for different types of storage: 
 * local files
 * files served by http(s) servers like Nginx
 * files on (S)FTP (future)
 * ...

Second major feature of net-file is ranged access. So you can download only part of file
starting from arbitrary position. 

## API

```python
    open_url(
        url: str,                   # File URL. For local file use file:///absolute/file/path
        start_bytes: int = None,    # For ranged access - the beginning of the range
        length: int = None          # For ranged access - range length
    ) -> NetFile
```

Opens URL returning `NetFile` object. To read from file use `context manager` or `open()` / `close()`
methods pair of `NetFile` object:

```python
    with open_url(
            url='http://test.domain/example.mp4',
            start_bytes=10000,
            length=20000,
    ) as open_file:
        content = open_file.read()
        while content:
            content = open_file.read()
```

![Speech Technology Center](https://gitlab.com/kraevs/net-file/-/raw/master/img/stc.png)