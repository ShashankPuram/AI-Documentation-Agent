import subprocess
from pathlib import Path

from services.documentation_state import (
    load_documentation_state
)

from services.git_state_analyzer import (
    get_git_commit_state
)


def validate_repository(repository_path: str):

    repository = Path(
        repository_path
    ).resolve()

    if not repository.exists():

        return {
            "success": False,
            "message": (
                f"Repository does not exist: "
                f"{repository}"
            )
        }

    if not repository.is_dir():

        return {
            "success": False,
            "message": (
                f"Repository path is not a directory: "
                f"{repository}"
            )
        }

    git_directory = repository / ".git"

    if not git_directory.exists():

        return {
            "success": False,
            "message": (
                "The selected directory is not "
                "a Git repository."
            )
        }

    return {
        "success": True,
        "repository_path": str(repository)
    }


def get_repository_status(repository_path: str):

    validation_result = validate_repository(
        repository_path
    )

    if not validation_result["success"]:
        return validation_result

    repository = validation_result[
        "repository_path"
    ]

    git_state_result = get_git_commit_state(
        repository
    )

    if not git_state_result["success"]:

        return git_state_result

    state_result = load_documentation_state(
        repository
    )

    if not state_result["success"]:

        return state_result

    latest_commit = git_state_result[
        "latest_commit"
    ]

    documented_commit = state_result[
        "documented_commit"
    ]

    if not state_result["exists"]:

        status = "Documentation not generated"

    elif documented_commit == latest_commit:

        status = "Up to date"

    else:

        status = "Changes detected"

    repository_name = Path(
        repository
    ).name

    return {
        "success": True,
        "repository": repository,
        "repository_name": repository_name,
        "latest_commit": latest_commit,
        "documented_commit": documented_commit,
        "documentation_exists": state_result[
            "exists"
        ],
        "status": status
    }


def get_remote_url(repository_path: str):

    validation_result = validate_repository(
        repository_path
    )

    if not validation_result["success"]:
        return validation_result

    repository = validation_result[
        "repository_path"
    ]

    try:

        result = subprocess.run(
            [
                "git",
                "-C",
                repository,
                "remote",
                "get-url",
                "origin"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        remote_url = result.stdout.strip()

        return {
            "success": True,
            "remote_url": remote_url
        }

    except subprocess.CalledProcessError:

        return {
            "success": True,
            "remote_url": None
        }