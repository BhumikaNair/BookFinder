import ui

class BookFinderApp:
    def __init__(self) -> None:
        self.config = Config.load()
        self.console = ui.make_console()
        self.engine = SearchEngine(self.config)
        self.history = JsonListStore(Config.history_path(), max_items=200)
        self.favorites = JsonListStore(Config.favorites_path())

if __name__ == "__main__":
    main()
