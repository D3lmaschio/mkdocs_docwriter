import os as _os
from pathlib import Path as _Path
from docwriter.yaml_io import write_config as _write_config, read_config as _read_config
from docwriter.config import MKDOCS_CONFIG_PATH as _MKDOCS_CONFIG_PATH, MKDOCS_DOC_ROOT_PATH as _MKDOCS_DOC_ROOT_PATH, DEFAULT_TEXT_FOR_NEW_SECTIONS as _DEFAULT_TEXT_FOR_NEW_SECTIONS
from docwriter.navtree import nav_get as _nav_get, nav_add as _nav_add, nav_remove as _nav_remove, nav_update as _nav_update
from docwriter.exceptions import MkdocsFileNotFoundError as _MkdocsFileNotFoundError, MkdocsIndexingError as _MkdocsIndexingError, MkdocsIndexingWriteError as _MkdocsIndexingWriteError, MkdocsUtilsError as _MkdocsUtilsError, MkdocsUnindexingError as _MkdocsUnindexingError, MkdocsUnindexingWriteError as _MkdocsUnindexingWriteError
from docwriter.utils import yamlpath_to_filepath as _yamlpath_to_filepath

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

def unindex(yamlpath: str, file_path: str = "") -> bool:
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
        if file_path:
            _unmap_folders(yamlpath, file_path)
    except Exception as ex:
        raise _MkdocsUnindexingError(f"Erro ao tentar desindexar {yamlpath}.")
    
    try:
        _write_config(_MKDOCS_CONFIG_PATH, cfg)
    except:
        raise _MkdocsUnindexingWriteError("Erro ao tentar escrever mudanças no arquivo de configuração.")
    
    return True

def organize_nav_indexes(nav: list) -> list:
    """
    Reorganiza os indexes para que fiquem sempre como o primeiro item de cada pasta no nav.
    Exemplo:
    - CMES:
        - CMES: Aplicações/CMES/index.md
        - Outro: ...
    """
    def organize_node(node):
        if isinstance(node, dict):
            new_dict = {}
            for key, value in node.items():
                if isinstance(value, list):
                    # Separe indexes e outros
                    indexes = []
                    others = []
                    for item in value:
                        if isinstance(item, dict):
                            # Recursivo para subpastas
                            for subkey, subvalue in item.items():
                                if subkey == key and subvalue.endswith("index.md"):
                                    indexes.append(item)
                                else:
                                    others.append(organize_node(item))
                        elif isinstance(item, str) and item.endswith("index.md"):
                            # Index direto
                            indexes.append(item)
                        else:
                            others.append(item)
                    # Index do próprio diretório
                    dir_index = None
                    for item in value:
                        if isinstance(item, dict) and key in item and item[key].endswith("index.md"):
                            dir_index = item
                            break
                    # Reorganiza: index primeiro, depois outros
                    new_list = []
                    if dir_index:
                        new_list.append(dir_index)
                        # Remove duplicidade
                        others = [o for o in others if o != dir_index]
                    else:
                        new_list.extend(indexes)
                    new_list.extend(others)
                    new_dict[key] = new_list
                else:
                    new_dict[key] = value
            return new_dict
        return node

    organized_nav = []
    for item in nav:
        if isinstance(item, dict):
            organized_nav.append(organize_node(item))
        else:
            organized_nav.append(item)
    return organized_nav

def _map_folders(path: str, filepath: str):
    """
    Apenas cria a estrutura de pastas e copia o arquivo do documento.
    Não cria mais index.md automaticamente.
    """
    source_file = _Path(filepath)

    if not isinstance(cfg, dict):
        return False

    if not source_file.exists():
        raise _MkdocsFileNotFoundError(
            f"MkDocs documentation file not found: {source_file}")

    keys = path.split('.')
    project_root = _Path(_MKDOCS_DOC_ROOT_PATH)

    current_path = project_root
    for key in keys[:-1]:
        current_path = current_path / key
        current_path.mkdir(parents=True, exist_ok=True)

    final_dir = current_path / keys[-1]
    final_dir.mkdir(parents=True, exist_ok=True)

    target_file = final_dir / source_file.name
    target_file.write_bytes(source_file.read_bytes())
    
def _unmap_folders(path: str, filepath: str):
    """
    Remove a pasta física correspondente ao path da documentação, junto com o arquivo .md.
    """
    from pathlib import Path

    keys = path.split('.')
    project_root = Path(_MKDOCS_DOC_ROOT_PATH)
    final_dir = project_root.joinpath(*keys)

    source_file = Path(filepath)
    target_file = final_dir / source_file.name

    # Remove o arquivo de documentação, se existir
    if target_file.exists():
        target_file.unlink(missing_ok=True)
    # Remove a pasta da documentação se estiver vazia
    if final_dir.exists() and final_dir.is_dir() and not any(final_dir.iterdir()):
        final_dir.rmdir()
    
def index_folder(yaml_path: str):
    """
    Cria um arquivo index.md na pasta especificada por yaml_path e indexa esse arquivo no nav.
    Se não for uma pasta válida, retorna erro.
    """
    keys = yaml_path.split('.')
    folder_path = _Path(_MKDOCS_DOC_ROOT_PATH).joinpath(*keys)
    index_file = folder_path / "index.md"

    if not folder_path.exists() or not folder_path.is_dir():
        raise _MkdocsFileNotFoundError(f"Pasta não encontrada: {folder_path}")

    # Cria o index.md se não existir
    if not index_file.exists():
        index_file.write_text(f"# {keys[-1]}\n\n{_DEFAULT_TEXT_FOR_NEW_SECTIONS}", encoding="utf-8")

    if not isinstance(cfg, dict):
        return

    nav = cfg.get('nav')
    if not isinstance(nav, list):
        nav = []

    # Caminho relativo ao root para o mkdocs
    rel_path = "/".join(keys) + "/index.md"
    folder_name = keys[-1]

    # Remove qualquer index anterior para essa pasta
    from docwriter.navtree import nav_get, nav_remove, nav_add
    found = nav_get(nav, yaml_path)
    if isinstance(found, list):
        # Remove index.md anterior se houver
        found[:] = [item for item in found if not (isinstance(item, str) and item.endswith("index.md"))]
        found.append({folder_name: rel_path})
    else:
        nav_add(nav, yaml_path, rel_path)

    cfg['nav'] = organize_nav_indexes(cfg['nav'])
    _write_config(_MKDOCS_CONFIG_PATH, cfg)

    return True

def get_nav() -> list | None:
    cf = _read_config(_MKDOCS_CONFIG_PATH)
    if not isinstance(cf, dict):
        return
    return cf['nav']