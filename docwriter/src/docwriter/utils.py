import shutil as _shutil, os as _os
from ruamel.yaml import YAML as __YAML
from exceptions import DocumentNotFoundError as _DocumentNotFoundError, MkdocsIndexWriteError as _MkdocsIndexWriteError
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as DQ

_yaml = __YAML()
_yaml.preserve_quotes = True

def read_config(config_path: str, key: str = "") -> dict:
    try:
        with open(f'{config_path}', "r", encoding="utf-8") as f:
            config = _yaml.load(f)
        if not config:
            return {}
        if not key:
            return config
        config = config[f'{key}']
        if not config:
            return {}
        return config 
    except FileNotFoundError:
        raise _DocumentNotFoundError
    
    
def write_config(config_path: str, data: dict) -> None:    
    # Backup file before editing
    _shutil.copy2(config_path, "./" + _os.path.basename(config_path) + ".bkp")
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            _yaml.dump(data, f)
    except Exception:
        raise _MkdocsIndexWriteError(f"Ocorreu um erro durante a indexação na função {__name__}.write_config")
        
def quote_nav(obj):
    if isinstance(obj, dict):
        return {DQ(str(k)): quote_nav(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [quote_nav(item) for item in obj]
    else:
        return DQ(str(obj))
    
def russian_doll_list(l):
    if not l:
        return []
    nested = [l[-1]]
    print(nested)
    for i in reversed(l[:-1]):
        nested = [i, nested]
    return nested
    
    