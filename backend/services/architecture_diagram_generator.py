from pathlib import Path
import subprocess


def generate_component_architecture_graph(
    component_dependencies,
    output_path
):
    """
    Generate a Graphviz architecture diagram from
    component-level dependencies.
    """

    output_path = Path(output_path)

    dot_lines = [
        "digraph architecture {",
        "    rankdir=LR;",
        '    graph [pad="0.5", nodesep="0.6", ranksep="1.0"];',
        '    node [shape=box, style="rounded"];'
    ]

    # ---------------------------------------------------------
    # Add component nodes
    # ---------------------------------------------------------

    components = set()

    for dependency in component_dependencies:

        components.add(
            dependency["source"]
        )

        components.add(
            dependency["target"]
        )

    for component in sorted(components):

        safe_component = (
            component
            .replace("\\", "/")
        )

        dot_lines.append(
            f'    "{safe_component}";'
        )

    # ---------------------------------------------------------
    # Add relationships
    # ---------------------------------------------------------

    for dependency in component_dependencies:

        source = dependency["source"]
        target = dependency["target"]
        relationship = dependency["relationship"]

        dot_lines.append(
            f'    "{source}" -> "{target}" '
            f'[label="{relationship}"];'
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

    # ---------------------------------------------------------
    # Generate PNG
    # ---------------------------------------------------------

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
                "Component architecture graph "
                "generated successfully"
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