from pathlib import Path

from services.project_analyzer import analyze_project

from services.component_dependency_analyzer import (
    analyze_component_dependencies
)

from services.architecture_diagram_generator import (
    generate_component_architecture_graph
)


repository_path = (
    "../repositories/dependency-test-project"
)


project_analysis = analyze_project(
    repository_path
)


component_analysis = (
    analyze_component_dependencies(
        project_analysis
    )
)


output_path = (
    Path(repository_path)
    / "architecture_graph.png"
)


result = generate_component_architecture_graph(
    component_analysis["dependencies"],
    output_path
)


print()
print("=" * 80)
print("ARCHITECTURE DIAGRAM")
print("=" * 80)

print()

print(result)