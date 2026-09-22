from services.project_analyzer import analyze_project

from services.git_documentation_sync import (
    analyze_git_documentation_impact
)


repository_path = (
    "../repositories/dependency-test-project"
)

old_commit = "5a413ec"
new_commit = "b70cf5c"


project_analysis = analyze_project(
    repository_path
)


result = analyze_git_documentation_impact(
    repository_path,
    old_commit,
    new_commit,
    project_analysis
)


print()
print("=" * 80)
print("GIT DOCUMENTATION IMPACT")
print("=" * 80)

print()

print(result)