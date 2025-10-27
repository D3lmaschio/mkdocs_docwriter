from dotenv import load_dotenv as _load_dotenv
import os as _os

_load_dotenv()

MKDOCS_DOC_ROOT_PATH = _os.getenv("MKDOCS_DOC_ROOT_PATH")
MKDOCS_CONFIG_PATH = _os.getenv("MKDOCS_CONFIG_PATH")
DEFAULT_TEXT_FOR_NEW_SECTIONS = _os.getenv("DEFAULT_TEXT_FOR_NEW_SECTIONS")