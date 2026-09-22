from services.project_analyzer import analyze_project
from services.git_documentation_sync import (
    analyze_current_git_documentation_impact
)


repository_path = "../repositories/dependency-test-project"

project_analysis = analyze_project(
    repository_path
)

if not project_analysis["success"]:
    print(project_analysis)
    raise SystemExit(1)

result = analyze_current_git_documentation_impact(
    repository_path,
    project_analysis
)

print(result)