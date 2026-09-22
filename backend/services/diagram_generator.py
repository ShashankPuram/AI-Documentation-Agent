from pathlib import Path
import subprocess


def generate_dependency_graph(dependencies, output_path):

    output_path = Path(output_path)

    dot_lines = [
        "digraph dependencies {",
        '    rankdir=LR;',
        '    node [shape=box];'
    ]

    for dependency in dependencies:

        source = dependency["source"]
        target = dependency["target"]

        dot_lines.append(
            f'    "{source}" -> "{target}";'
        )

    dot_lines.append("}")

    dot_content = "\n".join(dot_lines)

    dot_file = output_path.with_suffix(".dot")

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
            "message": "Dependency graph generated successfully",
            "dot_file": str(dot_file),
            "image_file": str(output_path)
        }

    except subprocess.CalledProcessError as error:

        return {
            "success": False,
            "message": error.stderr
        }