from __future__ import annotations

from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.theme import Theme

from providers.base import Book

DARK_THEME = Theme(
    {
        "brand": "bold cyan",
        "accent": "bold magenta",
        "muted": "grey58",
        "ok": "bold green",
        "warn": "bold yellow",
        "err": "bold red",
        "title": "bold white",
        "source.gutenberg": "green",
        "source.standard_ebooks": "cyan",
        "source.open_library": "yellow",
        "source.archive_org": "magenta",
    }
)

LOGO = r"""
[brand] ____              _   ______           _
|  _ \            | | |  ____|         | |
| |_) | ___   ___ | | | |__ _ _ __   __| | ___ _ __
|  _ < / _ \ / _ \| |/ /|  __| | '_ \ / _` |/ _ \ '__|
| |_) | (_) | (_) |   < | |    | | | | (_| |  __/ |
|____/ \___/ \___/|_|\_\|_|    |_| |_|\__,_|\___|_|[/brand]
[muted]        legal, open & public-domain ebook finder[/muted]
"""
