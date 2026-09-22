from pathlib import Path

from services.documentation_agent import (
    generate_validated_documentation
)


def regenerate_affected_documentation(
    repository_path,
    affected_files,
    project_analysis,
    repository_context
):
    """
    Regenerate documentation only for affected source files.
    """

    repository = Path(repository_path)

    python_files = (
        project_analysis["code"]["python_files"]
    )

    file_index = {
        file_analysis["file"]: file_analysis
        for file_analysis in python_files
    }

    regenerated_files = []

    skipped_files = []

    for file_name in affected_files:

        if file_name not in file_index:

            skipped_files.append({
                "file": file_name,
                "reason": (
                    "File is not a supported Python source file"
                )
            })

            continue

        file_analysis = file_index[file_name]

        result = generate_validated_documentation(
            file_analysis,
            repository_context
        )

        if not result["success"]:

            return {
                "success": False,
                "message": (
                    "Failed to regenerate documentation "
                    f"for {file_name}"
                ),
                "details": result
            }

        documentation_path = (
            repository
            / "docs"
            / "api"
            / Path(file_name).with_suffix(".md").name
        )

        documentation_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        documentation_path.write_text(
            result["documentation"],
            encoding="utf-8"
        )

        regenerated_files.append({
            "source_file": file_name,
            "documentation_file": str(
                documentation_path
            ),
            "quality": result["quality"],
            "validation": result["validation"],
            "attempts": result["attempts"]
        })

    return {
        "success": True,
        "message": (
            "Affected documentation regenerated successfully"
        ),
        "regenerated_files": regenerated_files,
        "skipped_files": skipped_files
    }