from pathlib import Path


class FileHandlerSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        csv_file: str = "",
        output_path=Path("."),
    ):
        if not hasattr(self, "initialized"):
            self.csv_file = csv_file
            self.output_path = output_path
            self.initialized = True

    def update_paths(self, csv_file: str, output_path: Path):
        self.csv_file = csv_file
        self.output_path = output_path
