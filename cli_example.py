from argparse import ArgumentParser
from sys import stdin
from pathlib import Path
from typing import Union
from mimetypeplus import MimeType


try:
    from sys import getdefaultencoding
except ImportError:
    DEFAULT_ENCODING = 'utf-8'
else:
    DEFAULT_ENCODING = getdefaultencoding()


PREFIX_CHARS: str
try:
    from sys import platform
except ImportError:
    PREFIX_CHARS = "-"
else:
    if platform == "win32":
        PREFIX_CHARS = "-/"
    else:
        PREFIX_CHARS = "-"

try:
    from os import EX_OK
except ImportError:
    EX_OK = 0  # type:ignore


def from_io(io, max_read: int|None) -> Union[MimeType, None]:
    enc = getattr(io, "encoding", None) or DEFAULT_ENCODING
    return MimeType.from_data(io.read(max_read), encoding=enc)


def main(progname:str, *args) -> int:
    parser = ArgumentParser(progname, prefix_chars=PREFIX_CHARS)
    mode_gr = parser.add_mutually_exclusive_group(required=True)
    mode_gr.add_argument('path', nargs='?', type = Path, default=None)
    mode_gr.add_argument('--literal', "-l", "--string", "--str",
                         nargs='+',
                         type = str,
                         default=""
                         )
    mode_gr.add_argument("--stdin", "-i", "--in", action="store_true")
    parser.add_argument("--max", "-m", "--maxread", "--mr", "-r", "--read",
                        type = int,
                        default = None
                        )

    parsed = parser.parse_args(args)

    mt = None

    if parsed.stdin:
        print("Parsing from stdin ...")
        mt = from_io(stdin, max_read = parsed.max)
    if parsed.literal:
        lit = " ".join(parsed.literal)
        if parsed.max:
            lit = lit[:min(parsed.max, len(lit))]
        print(f"Parsing provided argument data '{lit}' ...")
        mt = MimeType.from_data(lit, encoding = DEFAULT_ENCODING)
    else:
        print(f"Parsing {parsed.path} ...")
        mt = MimeType.from_path(parsed.path)

    print(mt)
    return EX_OK


def __main__():
    from sys import argv, exit as sys_exit
    sys_exit(main(*argv))


if __name__ == "__main__":
    __main__()
