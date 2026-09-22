from pathlib import Path


def build_component_index(
    project_analysis
):
    """
    Build an index of classes, functions, and methods
    defined in the repository.
    """

    index = {}

    python_files = (
        project_analysis["code"]["python_files"]
    )

    for file_analysis in python_files:

        file_name = file_analysis["file"]

        # -----------------------------------------------------
        # Classes and methods
        # -----------------------------------------------------

        for class_info in file_analysis["classes"]:

            class_name = class_info["name"]

            index[class_name] = {
                "type": "class",
                "file": file_name
            }

            for method in class_info["methods"]:

                method_name = method["name"]

                qualified_name = (
                    f"{class_name}.{method_name}"
                )

                index[qualified_name] = {
                    "type": "method",
                    "file": file_name,
                    "class": class_name
                }

        # -----------------------------------------------------
        # Standalone functions
        # -----------------------------------------------------

        for function in file_analysis[
            "standalone_functions"
        ]:

            function_name = function["name"]

            index[function_name] = {
                "type": "function",
                "file": file_name
            }

    return index


def analyze_component_dependencies(
    project_analysis
):
    """
    Analyze relationships between source-code components.

    Relationships are inferred from AST call information
    and known repository components.
    """

    component_index = build_component_index(
        project_analysis
    )

    dependencies = []

    python_files = (
        project_analysis["code"]["python_files"]
    )

    for file_analysis in python_files:

        file_name = file_analysis["file"]

        # -----------------------------------------------------
        # Standalone functions
        # -----------------------------------------------------

        for function in file_analysis[
            "standalone_functions"
        ]:

            source_component = function["name"]

            for call in function["calls"]:

                target_component = _resolve_call(
                    call,
                    component_index
                )

                if target_component:

                    dependencies.append({
                        "source": source_component,
                        "source_file": file_name,
                        "target": target_component,
                        "relationship": "calls"
                    })

        # -----------------------------------------------------
        # Class methods
        # -----------------------------------------------------

        for class_info in file_analysis["classes"]:

            class_name = class_info["name"]

            for method in class_info["methods"]:

                source_component = (
                    f"{class_name}.{method['name']}"
                )

                for call in method["calls"]:

                    target_component = _resolve_call(
                        call,
                        component_index
                    )

                    if target_component:

                        dependencies.append({
                            "source": source_component,
                            "source_file": file_name,
                            "target": target_component,
                            "relationship": "calls"
                        })

    # ---------------------------------------------------------
    # Remove duplicate relationships
    # ---------------------------------------------------------

    unique_dependencies = []

    seen = set()

    for dependency in dependencies:

        key = (
            dependency["source"],
            dependency["target"],
            dependency["relationship"]
        )

        if key in seen:
            continue

        seen.add(key)

        unique_dependencies.append(
            dependency
        )

    return {
        "success": True,
        "components": component_index,
        "dependencies": unique_dependencies
    }


def _resolve_call(
    call_expression,
    component_index
):
    """
    Resolve a call expression against known repository
    components.
    """

    # ---------------------------------------------------------
    # Direct calls
    #
    # Examples:
    # Database()
    # UserService()
    # format_user(user)
    # ---------------------------------------------------------

    for component_name in component_index:

        if call_expression.startswith(
            f"{component_name}("
        ):
            return component_name

    # ---------------------------------------------------------
    # Method calls
    #
    # Examples:
    # service.get_user(1)
    # self.database.connect()
    # ---------------------------------------------------------

    if "." in call_expression:

        parts = call_expression.split(".")

        if len(parts) >= 2:

            method_name = (
                parts[-1]
                .split("(")[0]
                .strip()
            )

            for component_name, component in (
                component_index.items()
            ):

                if component["type"] != "method":
                    continue

                # component_name is something like:
                #
                # UserService.get_user
                #
                # Therefore compare the final part.
                indexed_method_name = (
                    component_name
                    .split(".")[-1]
                )

                if indexed_method_name == method_name:

                    return component_name

    return None