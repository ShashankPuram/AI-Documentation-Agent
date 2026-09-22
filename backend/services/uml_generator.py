from pathlib import Path
import subprocess


def generate_class_diagram(
    project_analysis,
    output_path
):
    """
    Generate a UML-style class diagram from classes,
    methods, and detected class-level relationships.
    """

    output_path = Path(output_path)

    dot_lines = [
        "digraph classes {",
        '    rankdir=LR;',
        '    graph [pad="0.5", nodesep="0.8", ranksep="1.0"];',
        '    node [shape=plain];'
    ]

    class_names = set()

    # ---------------------------------------------------------
    # Generate class nodes
    # ---------------------------------------------------------

    for file_analysis in project_analysis["code"]["python_files"]:

        for class_info in file_analysis["classes"]:

            class_name = class_info["name"]

            class_names.add(class_name)

            rows = []

            rows.append(
                f'<TR><TD BGCOLOR="lightgray">'
                f'<B>{class_name}</B>'
                f'</TD></TR>'
            )

            for method in class_info["methods"]:

                parameters = [
                    parameter
                    for parameter in method["parameters"]
                    if parameter != "self"
                ]

                parameter_text = ", ".join(
                    parameters
                )

                method_text = (
                    f"+ {method['name']}"
                    f"({parameter_text})"
                )

                rows.append(
                    f'<TR><TD ALIGN="LEFT">'
                    f'{method_text}'
                    f'</TD></TR>'
                )

            label = (
                '<<TABLE BORDER="1" '
                'CELLBORDER="0" '
                'CELLSPACING="0" '
                'CELLPADDING="6">'
                + "".join(rows)
                + "</TABLE>>"
            )

            safe_name = class_name.replace(
                '"',
                '\\"'
            )

            dot_lines.append(
                f'"{safe_name}" [label={label}];'
            )

    # ---------------------------------------------------------
    # Detect class-level relationships
    # ---------------------------------------------------------

    class_relationships = set()

    python_files = (
        project_analysis["code"]["python_files"]
    )

    # Build method → class mapping.
    method_to_class = {}

    for file_analysis in python_files:

        for class_info in file_analysis["classes"]:

            class_name = class_info["name"]

            for method in class_info["methods"]:

                method_to_class[
                    f"{class_name}.{method['name']}"
                ] = class_name

    # Look at component dependencies.
    #
    # A method call such as:
    #
    # UserService.__init__ -> Database
    #
    # becomes:
    #
    # UserService -> Database
    #
    # A method call such as:
    #
    # UserService.get_user -> Database.connect
    #
    # becomes:
    #
    # UserService -> Database
    #

    for dependency in project_analysis.get(
        "component_dependencies",
        []
    ):

        source = dependency["source"]
        target = dependency["target"]

        source_class = _resolve_class(
            source,
            class_names,
            method_to_class
        )

        target_class = _resolve_class(
            target,
            class_names,
            method_to_class
        )

        if (
            source_class
            and target_class
            and source_class != target_class
        ):

            class_relationships.add(
                (
                    source_class,
                    target_class
                )
            )

    # ---------------------------------------------------------
    # Generate class relationships
    # ---------------------------------------------------------

    for source, target in sorted(
        class_relationships
    ):

        dot_lines.append(
            f'"{source}" -> "{target}" '
            '[label="uses"];'
        )

    dot_lines.append("}")

    dot_content = "\n".join(
        dot_lines
    )

    dot_file = output_path.with_suffix(
        ".dot"
    )

    dot_file.write_text(
        dot_content,
        encoding="utf-8"
    )

    try:

        subprocess.run(
            [
                "dot",
                "-Tpng",
                str(dot_file),
                "-o",
                str(output_path)
            ],
            check=True,
            capture_output=True,
            text=True
        )

        return {
            "success": True,
            "message": (
                "UML class diagram generated successfully"
            ),
            "dot_file": str(dot_file),
            "image_file": str(output_path)
        }

    except FileNotFoundError:

        return {
            "success": False,
            "message": (
                "Graphviz 'dot' executable was not found. "
                "Make sure Graphviz is installed and available "
                "in PATH."
            )
        }

    except subprocess.CalledProcessError as error:

        return {
            "success": False,
            "message": error.stderr
        }


def _resolve_class(
    component_name,
    class_names,
    method_to_class
):
    """
    Resolve a component name to its owning class.
    """

    if component_name in class_names:
        return component_name

    if component_name in method_to_class:
        return method_to_class[component_name]

    return None