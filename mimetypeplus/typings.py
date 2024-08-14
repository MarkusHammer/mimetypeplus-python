"""
typings

Contains commoly used types used for type checking and base classes
"""
#pylint:disable=unused-import,ungrouped-imports

try:
    from typing import Union #type:ignore
except ImportError:
    from typing_extensions import Union #type:ignore

try:
    from typing import Tuple #type:ignore
except ImportError:
    from typing_extensions import Tuple #type:ignore

try:
    from typing import List #type:ignore
except ImportError:
    from typing_extensions import List #type:ignore

try:
    from typing import Iterable #type:ignore
except ImportError:
    from typing_extensions import Iterable #type:ignore

try:
    from typing import Self #type:ignore
except ImportError:
    from typing_extensions import Self #type:ignore

try:
    from os import PathLike #type:ignore
except ImportError:
    from pathlib import PathLike #type:ignore

try:
    from typing import cast #type:ignore
except ImportError:
    from typing_extensions import cast #type:ignore

try:
    from typing import Callable #type:ignore
except ImportError:
    from typing_extensions import Callable #type:ignore

try:
    from typing import TypeAlias #type:ignore
except ImportError:
    from typing_extensions import TypeAlias #type:ignore

try:
    from typing import LiteralString #type:ignore
except ImportError:
    try:
        from typing_extensions import LiteralString #type:ignore
    except ImportError:
        LiteralString:TypeAlias = str #type:ignore

try:
    from types import NotImplementedType #type:ignore
except ImportError:
    try:
        from typing import Any #type:ignore
    except ImportError:
        from typing_extensions import Any #type:ignore
    NotImplementedType:TypeAlias = Any

try:
    from pathlib import Path #type:ignore
except ImportError:
    from pathlib2 import Path #type:ignore
