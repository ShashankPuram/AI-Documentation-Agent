import os
import subprocess
from pathlib import Path


REPOSITORY_DIR = Path(__file__).resolve().parent.parent.parent / "repositories"


def clone_repository(repository_url: str, repository_name: str):
    repository_path = REPOSITORY_DIR / repository_name

    if repository_path.exists():
        return {
            "success": False,
            "message": "Repository already exists",
            "path": str(repository_path)
        }

    os.makedirs(REPOSITORY_DIR, exist_ok=True)

    try:
        subprocess.run(
            ["git", "clone", repository_url, str(repository_path)],
            check=True,
            capture_output=True,
            text=True
        )

        return {
            "success": True,
            "message": "Repository cloned successfully",
            "path": str(repository_path)
        }

    except subprocess.CalledProcessError as error:
        return {
            "success": False,
            "message": error.stderr
        }