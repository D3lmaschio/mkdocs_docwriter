def nav_add(nav: list, path: str, file_path: str) -> list:
    """Adiciona um item à estrutura nav do mkdocs.yml."""
    keys = path.split('.')
    current = nav

    for i, key in enumerate(keys):
        found = None
        for item in current:
            if isinstance(item, dict) and key in item:
                found = item
                break

        if found:
            # Se o valor encontrado não for lista e ainda há níveis, substituir por lista
            if i < len(keys) - 1:
                if not isinstance(found[key], list):
                    found[key] = []
                current = found[key]
            else:
                # Último nível: atualizar o valor diretamente
                found[key] = file_path
        else:
            if i < len(keys) - 1:
                new_level = {key: []}
                if isinstance(current, list):
                    current.append(new_level)
                else:
                    raise TypeError(f"Nível '{key}' não é uma lista (type={type(current)})")
                current = new_level[key]
            else:
                if not isinstance(current, list):
                    raise TypeError(f"Nível final não é lista (type={type(current)})")
                current.append({key: file_path})

    return nav

def nav_remove(nav: list, path: str) -> list:
    """Remove um item da estrutura nav do mkdocs.yml, limpando níveis vazios."""
    keys = path.split('.')
    current = nav
    stack = []
    for key in keys:
        found = None
        parent = current
        for item in current:
            if isinstance(item, dict) and key in item:
                found = item
                break
        if not found:
            return nav
        stack.append((parent, found, key))
        if isinstance(found[key], list):
            current = found[key]
        else:
            break
    parent, found, key = stack.pop()
    parent.remove(found)
    while stack:
        parent, found, key = stack.pop()
        if not found[key]:
            parent.remove(found)
    return nav

def nav_update(nav: list, path: str, new_file: str) -> bool:
    """
    Atualiza o arquivo associado a um item existente em 'nav' sem recriar a hierarquia.
    Exemplo:
        path = "Aplicações.Teste.Brincadeira"
        new_file = "Aplicações/Teste/Brincadeira/novo.md"
    """
    keys = path.split('.')
    current = nav
    for i, key in enumerate(keys):
        found = None
        for item in current:
            if isinstance(item, dict) and key in item:
                found = item
                break
        if found is None:
            return False

        if i == len(keys) - 1:
            found[key] = new_file
            return True
        else:
            next_level = found[key]
            if not isinstance(next_level, list):
                return False
            current = next_level
    return False

def nav_get(nav: list, path: str) -> None | str | list:
    keys = path.split('.')
    current = nav
    for i, key in enumerate(keys):
        found = None
        for item in current:
            if isinstance(item, dict) and key in item:
                found = item[key]
                break
        if found is None:
            return None
        # se for o último nível, deve retornar somente se ele existir exatamente
        if i == len(keys) - 1:
            return found
        if not isinstance(found, list):
            return None
        current = found
    return None
