from services.project_analyzer import analyze_project

from services.repository_context import (
    build_repository_context
)

from services.documentation_agent import (
    generate_validated_documentation
)

from services.documentation_quality import (
    calculate_documentation_quality
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

    if not result["success"]:

        print("Generation failed:")
        print(result)
        continue

    quality = calculate_documentation_quality(
        result["documentation"],
        file_analysis
    )

    print()
    print("Validation:")
    print(result["validation"])

    print()
    print("Attempts:")
    print(result["attempts"])

    print()
    print("Quality Score:")
    print(
        f"{quality['score']}/"
        f"{quality['max_score']} "
        f"({quality['percentage']}%)"
    )

    print()
    print("Generated Documentation:")
    print(result["documentation"])
    print()
    print("Checks:")

    for check in quality["checks"]:

        status = (
            "PASS"
            if check["passed"]
            else "FAIL"
        )

        print(
            f"[{status}] "
            f"{check['check']} "
            f"({check['points']} points)"
        )