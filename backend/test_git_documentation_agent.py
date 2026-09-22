from services.project_analyzer import analyze_project

from services.git_documentation_agent import (
    synchronize_documentation
)


repository_path = (
    "../repositories/dependency-test-project"
)

old_commit = "5a413ec"
new_commit = "b70cf5c"


project_analysis = analyze_project(
    repository_path
)


result = synchronize_documentation(
    repository_path,
    old_commit,
    new_commit,
    project_analysis
)


print()
print("=" * 80)
print("GIT DOCUMENTATION SYNCHRONIZATION")
print("=" * 80)

print()

print(result)