import sys

from services.project_analyzer import analyze_project
from services.git_documentation_agent import (
    synchronize_current_documentation
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