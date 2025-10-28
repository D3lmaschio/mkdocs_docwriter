import os as _os
from exceptions import MkdocsUtilsError as _MkdocsUtilsError
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as DQ

def yamlpath_to_filepath(yaml_path: str, file_path: str):
    keys = yaml_path.split('.')
    filename = _os.path.basename(file_path)
    try:
        # remove o penúltimo nível se for igual ao último
        if len(keys) >= 2 and keys[-1] == keys[-2]:
            keys.pop(-2)
    except IndexError as ex:
        raise _MkdocsUtilsError(f"{yaml_path} é uma pasta, não é possível indexar uma documentação.") from None
        
    return '/'.join(keys) + '/' + filename

def quote_nav(obj):
    if isinstance(obj, dict):
        return {DQ(str(k)): quote_nav(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [quote_nav(item) for item in obj]
    else:
        return DQ(str(obj))

    
    