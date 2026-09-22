from services.project_analyzer import analyze_project

from services.repository_context import (
    build_repository_context
)

from services.documentation_agent import (
    generate_validated_documentation
)


repository_path = (
    "../repositories/dependency-test-project"
)


project_analysis = analyze_project(
    repository_path
)


repository_context = build_repository_context(
    project_analysis
)


for file_analysis in (
    project_analysis["code"]["python_files"]
):

    print()
    print("=" * 80)
    print(file_analysis["file"])
    print("=" * 80)

    result = generate_validated_documentation(
        file_analysis,
        repository_context
    )

    print()

    print("RESULT:")
    print(result)