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

if __name__ == "__main__":
    main()
