from services.git_change_analyzer import (
    get_changed_files
)

from services.documentation_impact_analyzer import (
    analyze_documentation_impact
)


def analyze_git_documentation_impact(
    repository_path: str,
    old_commit: str,
    new_commit: str,
    project_analysis
):
    """
    Determine which documentation is affected by changes
    between two Git commits.
    """

    # ---------------------------------------------------------
    # Detect changed files
    # ---------------------------------------------------------

    git_result = get_changed_files(
        repository_path,
        old_commit,
        new_commit
    )

    if not git_result["success"]:
        return git_result

    changed_files = (
        git_result["changed_files"]
    )

    # ---------------------------------------------------------
    # Determine documentation impact
    # ---------------------------------------------------------

    impact_result = (
        analyze_documentation_impact(
            changed_files,
            project_analysis
        )
    )

    if not impact_result["success"]:
        return impact_result

    # ---------------------------------------------------------
    # Return combined result
    # ---------------------------------------------------------

    return {
        "success": True,
        "repository": repository_path,
        "old_commit": old_commit,
        "new_commit": new_commit,
        "changed_files": changed_files,
        "affected_files": (
            impact_result["affected_files"]
        ),
        "documentation_files": (
            impact_result["documentation_files"]
        )
    }