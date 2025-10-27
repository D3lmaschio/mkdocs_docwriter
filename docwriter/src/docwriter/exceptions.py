from config import MKDOCS_CONFIG_PATH

class ConfigFileNotFoundError(Exception): 
    """Base exception for missing configuration files."""
    pass

class MkdocsIndexError(Exception):
    pass
        
class MkdocsIndexWriteError(MkdocsIndexError):
     def __init__(self, message: str):
        super().__init__(message)
    
class DocumentNotFoundError(FileNotFoundError):
    def __init__(self):
        super().__init__(f"Arquivo de documentação não foi encontrado verifique o caminho e tente novamente.")

class MkdocsFileNotFoundError(ConfigFileNotFoundError):
    """Raised when MkDocs configuration file is not found."""
    def __init__(self, message: str = ""):
        super().__init__(message)