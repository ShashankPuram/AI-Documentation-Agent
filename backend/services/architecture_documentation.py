def generate_architecture_documentation(
    project_analysis,
    component_analysis
):
    """
    Generate Markdown documentation describing the
    component-level architecture of the repository.
    """

    repository_name = project_analysis["repository"]

    components = component_analysis["components"]
    dependencies = component_analysis["dependencies"]

    lines = []

    lines.append("# System Architecture")
    lines.append("")
    lines.append(
        f"This document describes the component-level "
        f"architecture of `{repository_name}`."
    )
    lines.append("")

    # ---------------------------------------------------------
    # Components
    # ---------------------------------------------------------

    lines.append("## Components")
    lines.append("")

    if not components:

        lines.append(
            "No source-code components were detected."
        )

    else:

        for component_name in sorted(components):

            component = components[component_name]

            component_type = component["type"]
            file_name = component["file"]

            if component_type == "method":

                class_name = component.get(
                    "class",
                    "Unknown"
                )

                lines.append(
                    f"- `{component_name}` "
                    f"({component_type} of `{class_name}`) "
                    f"defined in `{file_name}`"
                )

            else:

                lines.append(
                    f"- `{component_name}` "
                    f"({component_type}) "
                    f"defined in `{file_name}`"
                )

    lines.append("")

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    lines.append("## Component Relationships")
    lines.append("")

    if not dependencies:

        lines.append(
            "No component relationships were detected."
        )

    else:

        for dependency in dependencies:

            source = dependency["source"]
            target = dependency["target"]
            relationship = dependency["relationship"]

            lines.append(
                f"- `{source}` "
                f"**{relationship}** "
                f"`{target}`"
            )

    lines.append("")

    # ---------------------------------------------------------
    # Architecture Diagram
    # ---------------------------------------------------------

    lines.append("## Architecture Diagram")
    lines.append("")

    lines.append(
        "The following diagram shows the detected "
        "relationships between source-code components."
    )

    lines.append("")

    lines.append(
        "![Component Architecture]"
        "(../architecture_graph.png)"
    )

    lines.append("")

    # ---------------------------------------------------------
    # Source Files
    # ---------------------------------------------------------

    lines.append("## Source Files")
    lines.append("")

    python_files = (
        project_analysis["code"]["python_files"]
    )

    if not python_files:

        lines.append(
            "No Python source files were detected."
        )

    else:

        for file_analysis in python_files:

            file_name = file_analysis["file"]

            class_count = len(
                file_analysis["classes"]
            )

            function_count = len(
                file_analysis["standalone_functions"]
            )

            lines.append(
                f"- `{file_name}` — "
                f"{class_count} class(es), "
                f"{function_count} standalone function(s)"
            )

    lines.append("")

    return "\n".join(lines)