import ast
from pathlib import Path


def get_python_imports(file_path: Path):

    try:
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

    except (UnicodeDecodeError, SyntaxError):
        return []

    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):

            if node.module:
                imports.append(node.module)

    return imports


def analyze_dependencies(repository_path: str):

    repository = Path(repository_path)

    if not repository.exists():
        return {
            "success": False,
            "message": "Repository does not exist"
        }

    python_files = list(repository.rglob("*.py"))

    # Ignore virtual environments and other unnecessary directories
    python_files = [
        file for file in python_files
        if not any(
            part in {".git", "__pycache__", "venv", ".venv", "node_modules"}
            for part in file.parts
        )
    ]

    # Map Python module names to actual files
    module_map = {}

    for file in python_files:
        relative_path = file.relative_to(repository)

        module_name = str(relative_path.with_suffix("")).replace("\\", ".")

        module_map[module_name] = relative_path

    dependencies = []

    for file in python_files:

        relative_file = file.relative_to(repository)

        imports = get_python_imports(file)

        for imported_module in imports:

            imported_file = None

            # Direct module match
            if imported_module in module_map:
                imported_file = module_map[imported_module]

            # Match first part of import
            else:
                imported_name = imported_module.split(".")[0]

                for module_name, module_path in module_map.items():

                    if module_name.split(".")[0] == imported_name:
                        imported_file = module_path
                        break

            if imported_file:

                dependencies.append({
                    "source": str(relative_file),
                    "target": str(imported_file)
                })

    return {
        "success": True,
        "repository": repository.name,
        "dependencies": dependencies
    }