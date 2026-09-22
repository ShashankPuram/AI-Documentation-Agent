import subprocess
from pathlib import Path


GENERATED_PATHS = (
    "docs/",
)

GENERATED_FILES = {
    "docs/.documentation_state.json",
}


def is_generated_documentation_file(file_name: str):
    normalized_file = file_name.replace("\\", "/")

    if normalized_file in GENERATED_FILES:
        return True

    for generated_path in GENERATED_PATHS:
        if normalized_file.startswith(generated_path):
            return True

    return False


def get_changed_files(repository_path: str, old_commit: str, new_commit: str):
    repository = Path(repository_path)

    if not repository.exists():
        return {
            "success": False,
            "message": f"Repository does not exist: {repository_path}"
        }

    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "diff",
                "--name-status",
                old_commit,
                new_commit
            ],
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as error:
        return {
            "success": False,
            "message": error.stderr.strip()
        }

    changed_files = []
    generated_files = []

    for line in result.stdout.splitlines():

        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")

        status = parts[0]

        if status in {"A", "M", "D"}:

            if len(parts) < 2:
                continue

            file_name = parts[1]

            change = {
                "status": status,
                "file": file_name
            }

            if is_generated_documentation_file(file_name):
                generated_files.append(change)
            else:
                changed_files.append(change)

        elif status.startswith("R"):

            if len(parts) < 3:
                continue

            old_file = parts[1]
            new_file = parts[2]

            change = {
                "status": "R",
                "old_file": old_file,
                "file": new_file
            }

            if (
                is_generated_documentation_file(old_file)
                or is_generated_documentation_file(new_file)
            ):
                generated_files.append(change)
            else:
                changed_files.append(change)

        elif status.startswith("C"):

            if len(parts) < 3:
                continue

            old_file = parts[1]
            new_file = parts[2]

            change = {
                "status": "C",
                "old_file": old_file,
                "file": new_file
            }

            if (
                is_generated_documentation_file(old_file)
                or is_generated_documentation_file(new_file)
            ):
                generated_files.append(change)
            else:
                changed_files.append(change)

    return {
        "success": True,
        "old_commit": old_commit,
        "new_commit": new_commit,
        "changed_files": changed_files,
        "generated_files": generated_files
    }