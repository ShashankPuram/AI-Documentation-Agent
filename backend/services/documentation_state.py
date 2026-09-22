import json
from pathlib import Path


STATE_FILE_NAME = ".documentation_state.json"


def get_state_file_path(repository_path: str):
    repository = Path(repository_path)

    return repository / "docs" / STATE_FILE_NAME


def save_documentation_state(
    repository_path: str,
    documented_commit: str
):
    state_file = get_state_file_path(repository_path)

    state_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    state = {
        "documented_commit": documented_commit
    }

    try:
        state_file.write_text(
            json.dumps(
                state,
                indent=4
            ),
            encoding="utf-8"
        )

        return {
            "success": True,
            "message": "Documentation state saved successfully",
            "state_file": str(state_file),
            "documented_commit": documented_commit
        }

    except OSError as error:
        return {
            "success": False,
            "message": str(error)
        }


def load_documentation_state(repository_path: str):
    state_file = get_state_file_path(repository_path)

    if not state_file.exists():
        return {
            "success": True,
            "exists": False,
            "documented_commit": None,
            "state_file": str(state_file)
        }

    try:
        state = json.loads(
            state_file.read_text(
                encoding="utf-8"
            )
        )

        return {
            "success": True,
            "exists": True,
            "documented_commit": state.get(
                "documented_commit"
            ),
            "state_file": str(state_file)
        }

    except (OSError, json.JSONDecodeError) as error:
        return {
            "success": False,
            "message": str(error)
        }