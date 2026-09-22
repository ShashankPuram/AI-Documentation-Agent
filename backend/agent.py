import sys

from services.project_analyzer import (
    analyze_project
)

from services.git_documentation_agent import (
    synchronize_current_documentation
)

from services.documentation_state import (
    load_documentation_state,
    save_documentation_state
)

from services.documentation_generator import (
    generate_project_documentation
)

from services.git_state_analyzer import (
    get_git_commit_state
)


def main():

    if len(sys.argv) != 2:
        print(
            "Usage: python agent.py <repository_path>"
        )
        sys.exit(1)

    repository_path = sys.argv[1]

    print("Analyzing repository...")

    project_analysis = analyze_project(
        repository_path
    )

    if not project_analysis["success"]:
        print(project_analysis["message"])
        sys.exit(1)

    state_result = load_documentation_state(
        repository_path
    )

    if not state_result["success"]:
        print(state_result["message"])
        sys.exit(1)

    if not state_result["exists"]:

        print(
            "Documentation state not found."
        )

        print(
            "Generating initial documentation..."
        )

        documentation_result = (
            generate_project_documentation(
                repository_path
            )
        )

        if not documentation_result["success"]:
            print(
                documentation_result["message"]
            )
            sys.exit(1)

        git_state_result = get_git_commit_state(
            repository_path
        )

        if not git_state_result["success"]:
            print(
                git_state_result["message"]
            )
            sys.exit(1)

        state_update_result = (
            save_documentation_state(
                repository_path,
                git_state_result["latest_commit"]
            )
        )

        if not state_update_result["success"]:
            print(
                state_update_result["message"]
            )
            sys.exit(1)

        print(
            "Initial documentation generated "
            "successfully."
        )

        sys.exit(0)

    print("Synchronizing documentation...")

    result = synchronize_current_documentation(
        repository_path,
        project_analysis
    )

    print(result)

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()