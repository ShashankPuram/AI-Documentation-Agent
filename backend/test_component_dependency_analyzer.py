from services.project_analyzer import analyze_project

from services.component_dependency_analyzer import (
    analyze_component_dependencies
)


repository_path = (
    "../repositories/dependency-test-project"
)


project_analysis = analyze_project(
    repository_path
)


result = analyze_component_dependencies(
    project_analysis
)


print()
print("=" * 80)
print("COMPONENT INDEX")
print("=" * 80)

for name, component in (
    result["components"].items()
):

    print(
        f"{name} "
        f"({component['type']}) "
        f"-> {component['file']}"
    )


print()
print("=" * 80)
print("COMPONENT DEPENDENCIES")
print("=" * 80)

for dependency in result["dependencies"]:

    print(
        f"{dependency['source']} "
        f"--{dependency['relationship']}--> "
        f"{dependency['target']}"
    )