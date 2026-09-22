from services.project_analyzer import analyze_project

from services.documentation_impact_analyzer import (
    analyze_documentation_impact
)


repository_path = (
    "../repositories/dependency-test-project"
)


project_analysis = analyze_project(
    repository_path
)


changed_files = [
    {
        "status": "M",
        "file": "database.py"
    }
]


result = analyze_documentation_impact(
    changed_files,
    project_analysis
)


print()
print("=" * 80)
print("DOCUMENTATION IMPACT ANALYSIS")
print("=" * 80)

print()

print(result)