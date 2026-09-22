from pathlib import Path


def write_file(file_path: Path, content: str):
    """
    Write text content to a file.
    """

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    return {
        "success": True,
        "path": str(file_path)
    }


def write_project_documentation(
    repository_path: str,
    project_overview: str,
    file_documentation: list
):
    """
    Write generated documentation into the repository.
    """

    repository = Path(repository_path)

    if not repository.exists():

        return {
            "success": False,
            "message": "Repository does not exist"
        }

    docs_directory = repository / "docs"
    api_directory = docs_directory / "api"

    docs_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    api_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------
    # Project README
    # --------------------------------

    readme_path = docs_directory / "README.md"

    readme_result = write_file(
        readme_path,
        project_overview
    )

    if not readme_result["success"]:
        return readme_result

    # --------------------------------
    # File documentation
    # --------------------------------

    generated_files = []

    for documentation in file_documentation:

        file_name = documentation["file"]
        content = documentation["documentation"]

        markdown_name = (
            Path(file_name)
            .with_suffix(".md")
            .name
        )

        output_path = api_directory / markdown_name

        result = write_file(
            output_path,
            content
        )

        if not result["success"]:
            return result

        generated_files.append(
            str(output_path)
        )

    return {
        "success": True,
        "message": "Project documentation generated successfully",
        "readme": str(readme_path),
        "api_files": generated_files
    }