from pathlib import Path


def analyze_documentation_impact(
    changed_files,
    project_analysis
):
    """
    Determine which source files are affected by changes.

    A changed source file always affects its own documentation.

    Files that depend on a changed file are also considered
    affected because their documented relationships may have
    changed.
    """

    python_files = (
        project_analysis["code"]["python_files"]
    )

    known_files = {
        file_analysis["file"]
        for file_analysis in python_files
    }

    dependencies = project_analysis.get(
        "dependencies",
        []
    )

    affected_files = set()

    # ---------------------------------------------------------
    # Normalize changed files
    # ---------------------------------------------------------

    normalized_changes = []

    for change in changed_files:

        if isinstance(change, str):

            normalized_changes.append(
                change
            )

        elif isinstance(change, dict):

            file_name = change.get("file")

            if file_name:
                normalized_changes.append(
                    file_name
                )

    # ---------------------------------------------------------
    # Directly changed files
    # ---------------------------------------------------------

    for file_name in normalized_changes:

        if file_name in known_files:

            affected_files.add(
                file_name
            )

    # ---------------------------------------------------------
    # Find files that depend on changed files
    # ---------------------------------------------------------

    changed_set = set(
        normalized_changes
    )

    dependency_found = True

    while dependency_found:

        dependency_found = False

        for dependency in dependencies:

            source = dependency["source"]
            target = dependency["target"]

            if (
                target in changed_set
                and source not in affected_files
            ):

                affected_files.add(
                    source
                )

                changed_set.add(
                    source
                )

                dependency_found = True

    # ---------------------------------------------------------
    # Build documentation paths
    # ---------------------------------------------------------

    documentation_files = []

    for source_file in sorted(
        affected_files
    ):

        documentation_path = (
            Path("docs")
            / "api"
            / Path(source_file).with_suffix(".md").name
        )

        documentation_files.append({
            "source_file": source_file,
            "documentation_file": str(
                documentation_path
            )
        })

    return {
        "success": True,
        "changed_files": sorted(
            normalized_changes
        ),
        "affected_files": sorted(
            affected_files
        ),
        "documentation_files": documentation_files
    }