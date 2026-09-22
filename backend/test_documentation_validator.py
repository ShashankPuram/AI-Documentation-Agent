from services.project_analyzer import analyze_project
from services.documentation_service import (
    generate_code_documentation
)
from services.documentation_validator import (
    validate_documentation
)
from services.repository_context import (
    build_repository_context
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

    documentation_result = (
        generate_code_documentation(
            file_analysis,
            repository_context
        )
    )

    if not documentation_result["success"]:

        print(
            documentation_result
        )

        continue

    documentation = (
        documentation_result["response"]
    )

    validation_result = validate_documentation(
        documentation,
        file_analysis
    )

    print()
    print("DOCUMENTATION:")
    print(documentation)

    print()
    print("VALIDATION:")
    print(validation_result)