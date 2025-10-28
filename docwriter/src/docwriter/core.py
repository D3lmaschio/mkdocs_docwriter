import os as _os
from pathlib import Path as _Path
from yaml_io import write_config as _write_config, read_config as _read_config
from config import MKDOCS_CONFIG_PATH as _MKDOCS_CONFIG_PATH, MKDOCS_DOC_ROOT_PATH as _MKDOCS_DOC_ROOT_PATH, DEFAULT_TEXT_FOR_NEW_SECTIONS as _DEFAULT_TEXT_FOR_NEW_SECTIONS
from navtree import nav_get as _nav_get, nav_add as _nav_add, nav_remove as _nav_remove, nav_update as _nav_update
from exceptions import MkdocsFileNotFoundError as _MkdocsFileNotFoundError, MkdocsIndexingError as _MkdocsIndexingError, MkdocsIndexingWriteError as _MkdocsIndexingWriteError, MkdocsUtilsError as _MkdocsUtilsError, MkdocsUnindexingError as _MkdocsUnindexingError, MkdocsUnindexingWriteError as _MkdocsUnindexingWriteError
from utils import yamlpath_to_filepath as _yamlpath_to_filepath

if not _MKDOCS_CONFIG_PATH:
    raise _MkdocsFileNotFoundError(
        f"MkDocs configuration file not found: {_MKDOCS_CONFIG_PATH}")

if not _MKDOCS_DOC_ROOT_PATH:
    raise _MkdocsFileNotFoundError(
        f"MkDocs Documentation folder not found: {_MKDOCS_DOC_ROOT_PATH}")

cfg = _read_config(_MKDOCS_CONFIG_PATH)


def index(yaml_path: str, file_path: str):
    """
    Index the documentation in mkdocs configuration file
    path = path in yaml to index
    filepath = new file path to index
    """
    if not isinstance(cfg, dict):
        return False

    nav = cfg.get('nav')

    if not nav:
        nav = []

    found = _nav_get(nav, yaml_path)

    if isinstance(found, list):
        raise _MkdocsIndexingError(
            f"{yaml_path} já existe e é uma pasta, indique o nome do arquivo \"{yaml_path}.arquivo\" se a intenção for registrar dentro de {yaml_path}.")

    if found:
        item = found.split('/')[-1]
        if item.endswith('.md'):
            return False

    try:
        cfg['nav'] = _nav_add(
            nav=nav, path=yaml_path, file_path=_yamlpath_to_filepath(yaml_path, file_path))
    except _MkdocsUtilsError as ex:
        raise _MkdocsIndexingError(ex) from None

    # Write the input in the file
    try:
        _write_config(_MKDOCS_CONFIG_PATH, cfg)
        _map_folders(yaml_path, file_path)
    except (_MkdocsIndexingWriteError, _MkdocsFileNotFoundError) as ex:
        raise _MkdocsIndexingError(ex)

    return True

def unindex(yamlpath: str):
    if not isinstance(cfg, dict):
        return False
    nav = cfg.get('nav')
    if not nav:
        return False
    
    found = _nav_get(nav, yamlpath)

    if not found:
        return False
    
    try:
        cfg['nav'] = _nav_remove(nav, yamlpath)
    except Exception as ex:
        raise _MkdocsUnindexingError(f"Erro ao tentar desindexar {yamlpath}.")
    
    try:
        _write_config(_MKDOCS_CONFIG_PATH, cfg)
    except:
        raise _MkdocsUnindexingWriteError("Erro ao tentar escrever mudanças no arquivo de configuração.")
    
    return True

def _map_folders(path: str, filepath: str):
    source_file = _Path(filepath)

    if not source_file.exists():
        raise _MkdocsFileNotFoundError(
            f"MkDocs documentation file not found: {source_file}")

    keys = path.split('.')
    project_root = _Path(_MKDOCS_DOC_ROOT_PATH)

    current_path = project_root

    for key in keys[:-1]:
        current_path = current_path / key
        current_path.mkdir(parents=True, exist_ok=True)
        index_file = current_path / "index.md"
        if not index_file.exists():
            index_file.write_text(
                f"# {key}\n\n{_DEFAULT_TEXT_FOR_NEW_SECTIONS}", encoding="utf-8")

    final_dir = current_path / keys[-1]
    final_dir.mkdir(parents=True, exist_ok=True)

    source_file = _Path(filepath)
    target_file = final_dir / source_file.name
    target_file.write_bytes(source_file.read_bytes())

def get_nav() -> list | None:
    cf = _read_config(_MKDOCS_CONFIG_PATH)
    if not isinstance(cf, dict):
        return
    return cf['nav']