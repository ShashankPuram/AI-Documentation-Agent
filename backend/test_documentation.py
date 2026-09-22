from services.project_analyzer import analyze_project
from services.documentation_service import generate_project_overview


repository_path = "../repositories/dependency-test-project"


project_analysis = analyze_project(
    repository_path
)


if project_analysis["success"]:

    result = generate_project_overview(
        project_analysis
    )

    print(result)

else:

    print(project_analysis)