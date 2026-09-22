from services.git_documentation_sync import (
    analyze_git_documentation_impact
)
from services.incremental_documentation import (
    regenerate_affected_documentation
)
from services.repository_context import (
    build_repository_context
)
from services.documentation_state import (
    load_documentation_state,
    save_documentation_state
)
from services.git_state_analyzer import (
    get_git_commit_state
)


def synchronize_current_documentation(
    repository_path: str,
    project_analysis
):
    """
    Synchronize documentation using the commit for which
    documentation was last generated.
    """

    repository_context = build_repository_context(
        project_analysis
    )

    if not repository_context["success"]:
        return repository_context

    state_result = load_documentation_state(
        repository_path
    )

    if not state_result["success"]:
        return state_result

    # Documentation has never been generated for this repository.
    if not state_result["exists"]:
        return {
            "success": False,
            "message": (
                "Documentation state not found. "
                "Generate the initial documentation first."
            ),
            "requires_initial_generation": True
        }

    documented_commit = state_result["documented_commit"]

    git_state_result = get_git_commit_state(
        repository_path
    )

    if not git_state_result["success"]:
        return git_state_result

    latest_commit = git_state_result["latest_commit"]

    # Nothing changed since the last documentation generation.
    if documented_commit == latest_commit:
        return {
            "success": True,
            "message": "Documentation is already up to date.",
            "repository": repository_path,
            "documented_commit": documented_commit,
            "latest_commit": latest_commit,
            "changed_files": [],
            "affected_files": [],
            "documentation_files": [],
            "regeneration": {
                "success": True,
                "message": "No documentation regeneration required.",
                "regenerated_files": [],
                "skipped_files": []
            }
        }

    impact_result = analyze_git_documentation_impact(
        repository_path,
        documented_commit,
        latest_commit,
        project_analysis
    )

    if not impact_result["success"]:
        return impact_result

    affected_files = impact_result["affected_files"]

    regeneration_result = regenerate_affected_documentation(
        repository_path,
        affected_files,
        project_analysis,
        repository_context
    )

    if not regeneration_result["success"]:
        return regeneration_result

    # Update the documentation state only after
    # successful regeneration.
    state_update_result = save_documentation_state(
        repository_path,
        latest_commit
    )

    if not state_update_result["success"]:
        return state_update_result

    return {
        "success": True,
        "message": "Documentation synchronized successfully",
        "repository": repository_path,
        "previous_documented_commit": documented_commit,
        "latest_commit": latest_commit,
        "changed_files": impact_result["changed_files"],
        "affected_files": impact_result["affected_files"],
        "documentation_files": impact_result["documentation_files"],
        "regeneration": regeneration_result,
        "state": state_update_result
    }


def synchronize_documentation(
    repository_path: str,
    old_commit: str,
    new_commit: str,
    project_analysis
):
    """
    Manual synchronization workflow.

    Kept for compatibility with the existing endpoint.
    """

    repository_context = build_repository_context(
        project_analysis
    )

    if not repository_context["success"]:
        return repository_context

    impact_result = analyze_git_documentation_impact(
        repository_path,
        old_commit,
        new_commit,
        project_analysis
    )

    if not impact_result["success"]:
        return impact_result

    affected_files = impact_result["affected_files"]

    regeneration_result = regenerate_affected_documentation(
        repository_path,
        affected_files,
        project_analysis,
        repository_context
    )

    if not regeneration_result["success"]:
        return regeneration_result

    return {
        "success": True,
        "message": "Documentation synchronized successfully",
        "old_commit": old_commit,
        "new_commit": new_commit,
        "changed_files": impact_result["changed_files"],
        "affected_files": impact_result["affected_files"],
        "documentation_files": impact_result["documentation_files"],
        "regeneration": regeneration_result
    }