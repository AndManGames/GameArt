from pathlib import Path


class FileHandlerSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self._csv_file = ""
            self._output_path = Path(".").absolute()
            self.initialized = True

    @property
    def csv_file(self) -> str:
        return self._csv_file

    @csv_file.setter
    def csv_file(self, value: str):
        self._csv_file = value

    @property
    def output_path(self) -> Path:
        return self._output_path

    @output_path.setter
    def output_path(self, value: Path):
        self._output_path = value
