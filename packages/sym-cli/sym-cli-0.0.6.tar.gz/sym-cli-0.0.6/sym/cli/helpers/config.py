from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, cast, Final, Iterator, Literal, TypedDict
import yaml, os

ConfigKey = Literal["org"]


XDG_CONFIG_HOME = os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")


class ConfigSchema(TypedDict, total=False):
    org: str


class Config(MutableMapping):
    __slots__ = ["path", "config"]

    path: Final[Path]
    config: Final[ConfigSchema]

    def __init__(self) -> None:
        self.path = Path(XDG_CONFIG_HOME) / "sym" / "config.yml"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            config = cast(
                ConfigSchema, yaml.load(self.path.open("r"), Loader=yaml.FullLoader)
            )
        except FileNotFoundError:
            config = ConfigSchema()
        self.config = config

    def __flush(self) -> None:
        yaml.dump(self.config, self.path.open("w"))

    def __getitem__(self, key: ConfigKey) -> Any:
        return self.config[key]

    def __delitem__(self, key: ConfigKey) -> None:
        del self.config[key]
        self.__flush()

    def __setitem__(self, key: ConfigKey, value: Any) -> None:
        self.config[key] = value
        self.__flush()

    def __iter__(self) -> Iterator[ConfigKey]:
        return cast(Iterator[ConfigKey], iter(self.config))

    def __len__(self) -> int:
        return len(self.config)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.path})"
