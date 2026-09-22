from pathlib import Path

from services.project_analyzer import analyze_project

from services.uml_generator import (
    generate_class_diagram
)


repository_path = (
    "../repositories/dependency-test-project"
)


project_analysis = analyze_project(
    repository_path
)


output_path = (
    Path(repository_path)
    / "class_diagram.png"
)


result = generate_class_diagram(
    project_analysis,
    output_path
)


print()
print("=" * 80)
print("UML CLASS DIAGRAM")
print("=" * 80)

print()

print(result)