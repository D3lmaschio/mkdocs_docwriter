from docwriter.config import MKDOCS_CONFIG_PATH

class MkdocsUtilsError(Exception):
    """Base exception for utils package exceptions"""
    pass

class ConfigFileNotFoundError(Exception): 
    """Base exception for missing configuration files."""
    pass

class MkdocsIndexingError(Exception):
    pass

class MkdocsUnindexingError(Exception):
    pass

class MkdocsUnindexingWriteError(MkdocsUnindexingError):
    def __init__(self, message: str = ""):
        super().__init__(message)
        
class MkdocsIndexingWriteError(MkdocsIndexingError):
     def __init__(self, message: str = ""):
        super().__init__(message)

class DocumentNotFoundError(FileNotFoundError):
    def __init__(self):
        super().__init__(f"Arquivo de documentação não foi encontrado verifique o caminho e tente novamente.")

class MkdocsFileNotFoundError(ConfigFileNotFoundError):
    """Raised when MkDocs configuration file is not found."""
    def __init__(self, message: str = ""):
        super().__init__(message)