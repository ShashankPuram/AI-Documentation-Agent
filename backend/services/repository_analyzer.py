import ast
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "docs"
}


IGNORED_FILES = {
    "dependency_graph.dot",
    "dependency_graph.png"
}


def get_return_values(function_node):
    """
    Extract return expressions from a function or method.

    Examples:

        return True
        -> ["True"]

        return self.database.connect()
        -> ["self.database.connect()"]

        return str(user)
        -> ["str(user)"]
    """

    return_values = []

    for node in ast.walk(function_node):

        if isinstance(node, ast.Return):

            if node.value is None:

                return_values.append(
                    "None"
                )

            else:

                return_values.append(
                    ast.unparse(node.value)
                )

    return return_values


def get_function_calls(function_node):
    """
    Extract function and method calls from a function or method.

    Examples:

        Database()
        -> ["Database()"]

        self.database.connect()
        -> ["self.database.connect()"]

        format_user(user)
        -> ["format_user(user)"]
    """

    calls = []

    for node in ast.walk(function_node):

        if isinstance(node, ast.Call):

            try:

                call_expression = ast.unparse(
                    node
                )

                calls.append(
                    call_expression
                )

            except Exception:

                continue

    return calls


def analyze_python_file(file_path: Path):

    try:

        source_code = file_path.read_text(
            encoding="utf-8"
        )

        tree = ast.parse(
            source_code
        )

    except (UnicodeDecodeError, SyntaxError) as error:

        return {
            "success": False,
            "message": f"Unable to parse file: {error}"
        }

    classes = []

    standalone_functions = []

    imports = []

    for node in tree.body:

        if isinstance(
            node,
            ast.ClassDef
        ):

            class_docstring = ast.get_docstring(
                node
            )

            methods = []

            for class_node in node.body:

                if isinstance(
                    class_node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef
                    )
                ):

                    parameters = [
                        argument.arg
                        for argument in class_node.args.args
                    ]

                    docstring = ast.get_docstring(
                        class_node
                    )

                    return_values = get_return_values(
                        class_node
                    )

                    calls = get_function_calls(
                        class_node
                    )

                    methods.append({
                        "name": class_node.name,
                        "line": class_node.lineno,
                        "parameters": parameters,
                        "docstring": docstring,
                        "returns": return_values,
                        "calls": calls
                    })

            classes.append({
                "name": node.name,
                "line": node.lineno,
                "docstring": class_docstring,
                "methods": methods
            })

        elif isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        ):

            parameters = [
                argument.arg
                for argument in node.args.args
            ]

            docstring = ast.get_docstring(
                node
            )

            return_values = get_return_values(
                node
            )

            calls = get_function_calls(
                node
            )

            standalone_functions.append({
                "name": node.name,
                "line": node.lineno,
                "parameters": parameters,
                "docstring": docstring,
                "returns": return_values,
                "calls": calls
            })

        elif isinstance(
            node,
            ast.Import
        ):

            for alias in node.names:

                imports.append(
                    alias.name
                )

        elif isinstance(
            node,
            ast.ImportFrom
        ):

            module = node.module or ""

            for alias in node.names:

                imports.append(
                    f"{module}.{alias.name}"
                )

    return {
        "success": True,
        "source_code": source_code,
        "classes": classes,
        "standalone_functions": standalone_functions,
        "imports": imports
    }


def analyze_repository(
    repository_path: str
):

    repository = Path(
        repository_path
    )

    if not repository.exists():

        return {
            "success": False,
            "message": "Repository does not exist"
        }

    files = []

    directories = []

    python_files = []

    for path in repository.rglob("*"):

        if any(
            part in IGNORED_DIRECTORIES
            for part in path.parts
        ):
            continue

        relative_path = path.relative_to(
            repository
        )

        if path.is_file():

            if path.name in IGNORED_FILES:
                continue

            files.append(
                str(relative_path)
            )

            if path.suffix == ".py":

                python_files.append(
                    path
                )

        elif path.is_dir():

            directories.append(
                str(relative_path)
            )

    python_analysis = []

    for python_file in python_files:

        analysis = analyze_python_file(
            python_file
        )

        if analysis["success"]:

            relative_path = (
                python_file.relative_to(
                    repository
                )
            )

            python_analysis.append({
                "file": str(relative_path),
                "source_code": analysis[
                    "source_code"
                ],
                "classes": analysis[
                    "classes"
                ],
                "standalone_functions": analysis[
                    "standalone_functions"
                ],
                "imports": analysis[
                    "imports"
                ]
            })

    return {
        "success": True,
        "repository": repository.name,
        "files": sorted(files),
        "directories": sorted(directories),
        "file_count": len(files),
        "directory_count": len(directories),
        "python_files": python_analysis
    }