import shutil as _shutil, os as _os
from ruamel.yaml import YAML as __YAML
from exceptions import DocumentNotFoundError as _DocumentNotFoundError, MkdocsIndexingWriteError as _MkdocsIndexingWriteError
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as DQ

_yaml = __YAML()
_yaml.preserve_quotes = True


def read_config(config_path: str, key: str = "") -> dict | list:
    try:
        with open(f'{config_path}', "r", encoding="utf-8") as f:
            config = _yaml.load(f)
        if not config:
            return {} if not key else []
        if not key:
            return config
        value = config.get(key)
        return value if value is not None else []
    except FileNotFoundError:
        raise _DocumentNotFoundError
      
def write_config(config_path: str, data: dict) -> None:    
    # Backup file before editing
    _shutil.copy2(config_path, "./" + _os.path.basename(config_path) + ".bkp")
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            _yaml.dump(data, f)
    except Exception:
        raise _MkdocsIndexingWriteError(f"Ocorreu um erro durante a indexação na função {__name__}.write_config")