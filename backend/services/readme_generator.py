from pathlib import Path


def generate_documentation_readme(
    project_analysis,
    project_overview
):
    """
    Build the main documentation README.

    The README combines:
    - AI-generated project overview
    - Repository structure
    - Python source files
    - Classes
    - Functions
    - Dependencies
    - Links to generated documentation
    """

    repository_name = project_analysis["repository"]

    structure = project_analysis["structure"]

    python_files = project_analysis["code"]["python_files"]

    dependencies = project_analysis["dependencies"]

    lines = []

    # --------------------------------
    # Title
    # --------------------------------

    lines.append(
        f"# {repository_name}"
    )

    lines.append("")

    lines.append(
        "## Project Overview"
    )

    lines.append("")

    lines.append(
        project_overview
    )

    lines.append("")

    # --------------------------------
    # Repository Structure
    # --------------------------------

    lines.append(
        "## Repository Structure"
    )

    lines.append("")

    lines.append(
        f"- **Files:** {structure['file_count']}"
    )

    lines.append(
        f"- **Directories:** {structure['directory_count']}"
    )

    lines.append("")

    if structure["files"]:

        lines.append(
            "### Files"
        )

        lines.append("")

        for file_name in structure["files"]:

            lines.append(
                f"- `{file_name}`"
            )

        lines.append("")

    # --------------------------------
    # Python Components
    # --------------------------------

    lines.append(
        "## Python Components"
    )

    lines.append("")

    if not python_files:

        lines.append(
            "No Python files were detected."
        )

        lines.append("")

    else:

        for file_analysis in python_files:

            file_name = file_analysis["file"]

            lines.append(
                f"### `{file_name}`"
            )

            lines.append("")

            classes = file_analysis["classes"]

            standalone_functions = (
                file_analysis["standalone_functions"]
            )

            if classes:

                lines.append(
                    "**Classes:**"
                )

                lines.append("")

                for class_info in classes:

                    class_name = class_info["name"]

                    lines.append(
                        f"- `{class_name}`"
                    )

                    methods = class_info["methods"]

                    if methods:

                        for method in methods:

                            lines.append(
                                f"  - `{method['name']}()`"
                            )

                lines.append("")

            if standalone_functions:

                lines.append(
                    "**Functions:**"
                )

                lines.append("")

                for function in standalone_functions:

                    lines.append(
                        f"- `{function['name']}()`"
                    )

                lines.append("")

            markdown_file = (
                Path(file_name)
                .with_suffix(".md")
                .name
            )

            lines.append(
                f"**Detailed documentation:** "
                f"[View `{file_name}` documentation]"
                f"(api/{markdown_file})"
            )

            lines.append("")

    # --------------------------------
    # Dependencies
    # --------------------------------

    lines.append(
        "## Dependencies"
    )

    lines.append("")

    if dependencies:

        for dependency in dependencies:

            source = dependency["source"]

            target = dependency["target"]

            lines.append(
                f"- `{source}` → `{target}`"
            )

    else:

        lines.append(
            "No internal file dependencies were detected."
        )

    lines.append("")

    # --------------------------------
    # Architecture
    # --------------------------------

    lines.append(
        "## Architecture"
    )

    lines.append("")

    lines.append(
        "The following diagram shows the detected "
        "dependencies between project files."
    )

    lines.append("")

    lines.append(
        "![Dependency Graph]"
        "(../dependency_graph.png)"
    )

    lines.append("")

    # --------------------------------
    # Documentation Index
    # --------------------------------

    lines.append(
        "## Documentation"
    )

    lines.append("")

    lines.append(
        "Detailed documentation is available for "
        "each detected Python source file:"
    )

    lines.append("")

    for file_analysis in python_files:

        file_name = file_analysis["file"]

        markdown_file = (
            Path(file_name)
            .with_suffix(".md")
            .name
        )

        lines.append(
            f"- [`{file_name}`](api/{markdown_file})"
        )

    lines.append("")

    return "\n".join(lines)