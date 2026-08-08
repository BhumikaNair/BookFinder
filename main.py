import ui

class BookFinderApp:
    def __init__(self) -> None:
        self.config = Config.load()
        self.console = ui.make_console()
        self.engine = SearchEngine(self.config)
        self.history = JsonListStore(Config.history_path(), max_items=200)
        self.favorites = JsonListStore(Config.favorites_path())

    async def run_interactive(self) -> None:
        ui.show_logo(self.console)
        while True:
            query = ui.ask_query(self.console)
            if not query:
                if ui.confirm(self.console, "Exit BookFinder?", default=True):
                    break
                continue

            books = await self._search_with_spinner(query)
            self.history.add({"query": query, "result_count": len(books)})

            if not books:
                ui.show_error(self.console, "No results found from any provider.")
                if not ui.confirm(self.console, "Search again?", default=True):
                    break
                continue

            await self._browse_and_download(books)

            if not ui.confirm(self.console, "Search again?", default=True):
                break

        ui.show_info(self.console, "Goodbye!")

    async def _search_with_spinner(self, query: str) -> List[Book]:
        with Status(
            f"[accent]Searching Gutenberg, Standard Ebooks, Open Library, "
            f"and Internet Archive for '{query}'...[/accent]",
            console=self.console,
            spinner="dots",
        ):
            return await self.engine.search(query)

    async def _browse_and_download(self, books: List[Book]) -> None:
        page = 1
        page_size = self.config.results_per_page

        while True:
            page_items, total_pages = paginate(books, page, page_size)
            ui.display_results(self.console, page_items, page, total_pages)
            choice = ui.prompt_selection(self.console, len(page_items))

            if choice == "q":
                return
            if choice == "n":
                page = min(page + 1, total_pages)
                continue
            if choice == "p":
                page = max(page - 1, 1)
                continue
            if choice.startswith("f "):
                await self._handle_favorite(choice, page_items)
                continue
            if not choice.isdigit() or not (1 <= int(choice) <= len(page_items)):
                ui.show_error(self.console, "Invalid selection.")
                continue

            book = page_items[int(choice) - 1]
            await self._download_flow(book)
            return

    async def _handle_favorite(self, choice: str, page_items: List[Book]) -> None:
        try:
            idx = int(choice.split()[1])
        except (IndexError, ValueError):
            ui.show_error(self.console, "Usage: f <number>")
            return
        if not (1 <= idx <= len(page_items)):
            ui.show_error(self.console, "Invalid favorite index.")
            return
        book = page_items[idx - 1]
        self.favorites.add(book)
        ui.show_success(self.console, f"Added '{book.title}' to favorites.")

    async def _download_flow(self, book: Book) -> None:
        fmt = ui.select_format(self.console, book, self.config.preferred_formats)
        if not fmt:
            return
        downloader = Downloader(self.config, self.console)
        try:
            path = await downloader.download(book, fmt)
            ui.show_success(self.console, f"Saved to {path}")
        except DownloadError as exc:
            ui.show_error(self.console, str(exc))

if __name__ == "__main__":
    main()
