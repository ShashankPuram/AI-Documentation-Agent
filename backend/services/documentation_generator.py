from pathlib import Path
from services.project_analyzer import analyze_project
from services.documentation_service import (
    generate_project_overview
)
from services.documentation_agent import (
    generate_validated_documentation
)
from services.readme_generator import (
    generate_documentation_readme
)
from services.documentation_writer import (
    write_project_documentation
)
from services.repository_context import (
    build_repository_context
)
from services.component_dependency_analyzer import (
    analyze_component_dependencies
)
from services.architecture_diagram_generator import (
    generate_component_architecture_graph
)
from services.architecture_documentation import (
    generate_architecture_documentation
)
from services.uml_generator import (
    generate_class_diagram
)

def generate_project_documentation(
    repository_path: str
):
    """
    Generate complete project documentation.

    The pipeline performs repository analysis, component
    dependency analysis, architecture diagram generation,
    UML class diagram generation, architecture documentation,
    AI documentation generation, validation, quality scoring,
    and Markdown file generation.
    """

    # ---------------------------------------------------------
    # Analyze repository
    # ---------------------------------------------------------
    project_analysis = analyze_project(
        repository_path
    )
    if not project_analysis["success"]:
        return project_analysis
    # ---------------------------------------------------------
    # Build repository context
    # ---------------------------------------------------------
    repository_context = build_repository_context(
        project_analysis
    )
    if not repository_context["success"]:
        return repository_context
    # ---------------------------------------------------------
    # Component dependency analysis
    # ---------------------------------------------------------
    component_analysis = (
        analyze_component_dependencies(
            project_analysis
        )
    )
    if not component_analysis["success"]:
        return component_analysis
    # Store component dependencies inside the project
    # analysis so other generators can use them.
    project_analysis["component_dependencies"] = (
        component_analysis["dependencies"]
    )

    # ---------------------------------------------------------
    # Generate component architecture diagram
    # ---------------------------------------------------------

    architecture_path = (
        Path(repository_path)
        / "architecture_graph.png"
    )

    architecture_result = (
        generate_component_architecture_graph(
            component_analysis["dependencies"],
            architecture_path
        )
    )

    if not architecture_result["success"]:
        return architecture_result

    # ---------------------------------------------------------
    # Generate UML class diagram
    # ---------------------------------------------------------

    class_diagram_path = (
        Path(repository_path)
        / "class_diagram.png"
    )

    class_diagram_result = (
        generate_class_diagram(
            project_analysis,
            class_diagram_path
        )
    )

    if not class_diagram_result["success"]:
        return class_diagram_result

    # ---------------------------------------------------------
    # Generate architecture documentation
    # ---------------------------------------------------------

    architecture_documentation = (
        generate_architecture_documentation(
            project_analysis,
            component_analysis
        )
    )

    # ---------------------------------------------------------
    # Generate project overview
    # ---------------------------------------------------------

    overview_result = generate_project_overview(
        project_analysis
    )

    if not overview_result["success"]:
        return overview_result

    project_overview = (
        overview_result["response"]
    )

    # ---------------------------------------------------------
    # Generate documentation for every Python file
    # ---------------------------------------------------------

    file_documentation = []

    python_files = (
        project_analysis["code"]["python_files"]
    )

    total_files = len(python_files)

    for file_analysis in python_files:

        documentation_result = (
            generate_validated_documentation(
                file_analysis,
                repository_context
            )
        )

        if not documentation_result["success"]:

            return {
                "success": False,
                "message": (
                    "Documentation generation failed "
                    f"for {file_analysis['file']}"
                ),
                "details": documentation_result
            }

        file_documentation.append({
            "file": file_analysis["file"],
            "documentation": (
                documentation_result["documentation"]
            ),
            "validation": (
                documentation_result["validation"]
            ),
            "quality": (
                documentation_result["quality"]
            ),
            "attempts": (
                documentation_result["attempts"]
            )
        })

    # ---------------------------------------------------------
    # Generate documentation README
    # ---------------------------------------------------------

    documentation_readme = (
        generate_documentation_readme(
            project_analysis,
            project_overview
        )
    )

    # ---------------------------------------------------------
    # Write documentation
    # ---------------------------------------------------------

    write_result = write_project_documentation(
        repository_path,
        documentation_readme,
        file_documentation
    )

    if not write_result["success"]:
        return write_result

    # ---------------------------------------------------------
    # Write architecture documentation
    # ---------------------------------------------------------

    docs_directory = (
        Path(repository_path)
        / "docs"
    )

    architecture_documentation_path = (
        docs_directory
        / "architecture.md"
    )

    architecture_documentation_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    architecture_documentation_path.write_text(
        architecture_documentation,
        encoding="utf-8"
    )

    # ---------------------------------------------------------
    # Quality summary
    # ---------------------------------------------------------

    quality_summary = []

    for item in file_documentation:

        quality = item["quality"]

        quality_summary.append({
            "file": item["file"],
            "score": quality["score"],
            "max_score": quality["max_score"],
            "percentage": quality["percentage"],
            "attempts": item["attempts"],
            "valid": item["validation"]["valid"]
        })

    # ---------------------------------------------------------
    # Return complete result
    # ---------------------------------------------------------

    return {
        "success": True,
        "message": (
            "AI documentation generated successfully "
            "with architecture analysis, UML generation, "
            "architecture documentation, validation "
            "and quality scoring"
        ),
        "repository": (
            project_analysis["repository"]
        ),
        "files_processed": total_files,
        "architecture": {
            "components": (
                component_analysis["components"]
            ),
            "dependencies": (
                component_analysis["dependencies"]
            ),
            "component_diagram": architecture_result,
            "uml_class_diagram": class_diagram_result,
            "documentation": {
                "path": str(
                    architecture_documentation_path
                )
            }
        },
        "documentation": write_result,
        "quality_summary": quality_summary
    }