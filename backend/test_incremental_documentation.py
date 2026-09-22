from services.project_analyzer import analyze_project

from services.repository_context import (
    build_repository_context
)

from services.incremental_documentation import (
    regenerate_affected_documentation
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


affected_files = [
    "utils.py"
]


result = regenerate_affected_documentation(
    repository_path,
    affected_files,
    project_analysis,
    repository_context
)


print()
print("=" * 80)
print("INCREMENTAL DOCUMENTATION REGENERATION")
print("=" * 80)

print()

print(result)