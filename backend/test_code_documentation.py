from services.project_analyzer import analyze_project
from services.documentation_service import generate_code_documentation


repository_path = "../repositories/dependency-test-project"


project_analysis = analyze_project(
    repository_path
)


if project_analysis["success"]:

    for file_analysis in project_analysis["code"]["python_files"]:

        print("\n")
        print("=" * 80)
        print(file_analysis["file"])
        print("=" * 80)

        result = generate_code_documentation(
            file_analysis
        )

        print(result)

else:

    print(project_analysis)