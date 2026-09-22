from services.project_analyzer import analyze_project
from services.diagram_generator import generate_dependency_graph


repository_path = "../repositories/dependency-test-project"

result = analyze_project(repository_path)

if result["success"]:

    output_path = "../repositories/dependency-test-project/dependency_graph.png"

    diagram_result = generate_dependency_graph(
        result["dependencies"],
        output_path
    )

    print(diagram_result)

else:

    print(result)