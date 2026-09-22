import subprocess
from pathlib import Path


def get_git_commit_state(repository_path: str):
    repository = Path(repository_path)

    if not repository.exists():
        return {
            "success": False,
            "message": f"Repository does not exist: {repository_path}"
        }

    try:
        # Get the latest commit
        latest_result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "rev-parse",
                "HEAD"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        latest_commit = latest_result.stdout.strip()

        # Get the commit immediately before HEAD
        previous_result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "rev-parse",
                "HEAD~1"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        previous_commit = previous_result.stdout.strip()

        return {
            "success": True,
            "repository": str(repository),
            "previous_commit": previous_commit,
            "latest_commit": latest_commit
        }

    except subprocess.CalledProcessError as error:
        return {
            "success": False,
            "message": error.stderr.strip()
        }