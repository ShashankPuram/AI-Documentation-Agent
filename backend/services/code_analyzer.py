import ast
from pathlib import Path


def analyze_python_file(file_path: str):

    path = Path(file_path)

    if not path.exists():
        return {
            "success": False,
            "message": "File does not exist"
        }

    try:
        source_code = path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

    except (UnicodeDecodeError, SyntaxError) as error:
        return {
            "success": False,
            "message": f"Unable to parse file: {error}"
        }

    classes = []
    functions = []
    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "line": node.lineno
            })

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parameters = [
                argument.arg
                for argument in node.args.args
            ]

            functions.append({
                "name": node.name,
                "line": node.lineno,
                "parameters": parameters
            })

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                imports.append(
                    f"{module}.{alias.name}"
                )

    return {
        "success": True,
        "file": path.name,
        "classes": classes,
        "functions": functions,
        "imports": imports
    }