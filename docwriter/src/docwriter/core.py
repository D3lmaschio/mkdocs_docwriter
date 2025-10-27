from config import MKDOCS_CONFIG_PATH as _MKDOCS_CONFIG_PATH, MKDOCS_DOC_ROOT_PATH as _MKDOCS_DOC_ROOT_PATH, DEFAULT_TEXT_FOR_NEW_SECTIONS as _DEFAULT_TEXT_FOR_NEW_SECTIONS
from utils import write_config as _write_config, read_config as _read_config, quote_nav as _quote_nav, russian_doll_list
from exceptions import MkdocsFileNotFoundError as _MkdocsFileNotFoundError, MkdocsIndexError as _MkdocsIndexError, MkdocsIndexWriteError as _MkdocsIndexWriteError
from pathlib import Path
import json

import os as _os

if not _MKDOCS_CONFIG_PATH:
    raise _MkdocsFileNotFoundError(f"MkDocs configuration file not found: {_MKDOCS_CONFIG_PATH}")

if not _MKDOCS_DOC_ROOT_PATH:
    raise _MkdocsFileNotFoundError(f"MkDocs Documentation folder not found: {_MKDOCS_DOC_ROOT_PATH}")

_mkdocs_config = _read_config(_MKDOCS_CONFIG_PATH)

def index(filename: str , where: str):
    """Index the documentation in mkdocs configuration file"""
    path = where.split('.')
    if not _mkdocs_config.get('nav'):
        _mkdocs_config['nav'] = []

    print(russian_doll_list(path))
    
    # Write the input in the file
    try: 
        _write_config(_MKDOCS_CONFIG_PATH, _mkdocs_config)
    except _MkdocsIndexWriteError:
        raise _MkdocsIndexError()
    
    _map_folders(filename, where)
        
    
def _map_folders(filepath: str, where: str):
    source_file = Path(filepath)
    
    if not source_file.exists():
        raise _MkdocsFileNotFoundError(f"MkDocs documentation file not found: {source_file}")
    
    keys = where.split('.')
    project_root = Path(_MKDOCS_DOC_ROOT_PATH)
    
    current_path = project_root
    
    for key in keys[:-1]:
        current_path = current_path / key
        current_path.mkdir(parents=True, exist_ok=True)
        index_file = current_path / "index.md"
        if not index_file.exists():
            index_file.write_text(f"# {key}\n\n{_DEFAULT_TEXT_FOR_NEW_SECTIONS}", encoding="utf-8")
            
    final_dir = current_path / keys[-1]
    final_dir.mkdir(parents=True, exist_ok=True)
    
    source_file = Path(filepath)
    target_file = final_dir / source_file.name
    target_file.write_bytes(source_file.read_bytes())