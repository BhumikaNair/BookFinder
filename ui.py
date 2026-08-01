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

def make_console() -> Console:
    return Console(theme=DARK_THEME, highlight=False)

def show_logo(console: Console) -> None:
    console.clear()
    console.print(LOGO)
    console.print(
        Panel(
            "[muted]Sources: Project Gutenberg  |  Standard Ebooks  |  "
            "Open Library  |  Internet Archive[/muted]",
            border_style="grey42",
            expand=False,
        )
    )

def ask_query(console: Console) -> str:
    console.print()
    return Prompt.ask("[accent]Search by title, author, or ISBN[/accent]").strip()

def _source_style(source: str) -> str:
    key = source.lower().replace(" ", "_")
    return (
        f"source.{key}"
        if key
        in {
            "source.gutenberg",
            "source.standard_ebooks",
            "source.open_library",
            "source.archive_org",
        }
        else "muted"
    )

def display_results(
    console: Console, books: List[Book], page: int, total_pages: int
) -> None:
    if not books:
        console.print(
            Panel("[warn]No results on this page.[/warn]", border_style="yellow")
        )
        return

    table = Table(
        title=f"Search Results (page {page}/{total_pages})",
        header_style="bold white on grey19",
        border_style="grey42",
        expand=True,
    )
    table.add_column("#", style="accent", width=3, justify="right")
    table.add_column("Title", style="title", overflow="fold")
    table.add_column("Author", style="white")
    table.add_column("Year", style="muted", width=6, justify="center")
    table.add_column("Formats", style="ok")
    table.add_column("Source")

    for i, book in enumerate(books, start=1):
        source_style = _source_style(book.source)
        table.add_row(
            str(i),
            book.title,
            book.author,
            book.year or "-",
            ", ".join(sorted(book.formats.keys())) or "-",
            Text(book.source, style=source_style),
        )
    console.print(table)

def prompt_selection(console: Console, max_index: int, allow_nav: bool = True) -> str:
    hint = f"1-{max_index}"
    if allow_nav:
        hint += ", [n]ext, [p]rev, [f]avorite <n>, [q]uit"
    return Prompt.ask(f"[accent]Select a book[/accent] ({hint})").strip().lower()

def select_format(
    console: Console, book: Book, preferred_order: List[str]
) -> Optional[str]:
    available = list(book.formats.keys())
    if not available:
        console.print("[err]This book has no downloadable formats.[/err]")
        return None
    if len(available) == 1:
        return available[0]

    ordered = [f for f in preferred_order if f in available] + [
        f for f in available if f not in preferred_order
    ]

    console.print(
        Panel(
            f"[title]{book.title}[/title]\n[muted]{book.author}[/muted]",
            border_style="cyan",
        )
    )
    for i, fmt in enumerate(ordered, start=1):
        console.print(f"  [accent]{i}[/accent]. {fmt}")
    choice = Prompt.ask(
        "[accent]Choose a format[/accent]",
        choices=[str(i) for i in range(1, len(ordered) + 1)],
        default="1",
    )
    return ordered[int(choice) - 1]

def confirm(console: Console, message: str, default: bool = True) -> bool:
    return Confirm.ask(f"[accent]{message}[/accent]", default=default)

def show_error(console: Console, message: str) -> None:
    console.print(f"[err]Error:[/err] {message}")

def show_success(console: Console, message: str) -> None:
    console.print(f"[ok]{message}[/ok]")

def show_info(console: Console, message: str) -> None:
    console.print(f"[muted]{message}[/muted]")
