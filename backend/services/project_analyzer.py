from pathlib import Path

from services.repository_analyzer import analyze_repository
from services.dependency_analyzer import analyze_dependencies
from services.diagram_generator import generate_dependency_graph


def analyze_project(repository_path: str):

    repository_analysis = analyze_repository(repository_path)

    if not repository_analysis["success"]:
        return repository_analysis

    dependency_analysis = analyze_dependencies(repository_path)

    if not dependency_analysis["success"]:
        return dependency_analysis

    repository = repository_analysis["repository"]

    diagram_path = (
        Path(repository_path) / "dependency_graph.png"
    )

    diagram_result = generate_dependency_graph(
        dependency_analysis["dependencies"],
        diagram_path
    )

    return {
        "success": True,
        "repository": repository,

        "structure": {
            "files": repository_analysis["files"],
            "directories": repository_analysis["directories"],
            "file_count": repository_analysis["file_count"],
            "directory_count": repository_analysis["directory_count"]
        },

        "code": {
            "python_files": repository_analysis["python_files"]
        },

        "dependencies": dependency_analysis["dependencies"],

        "diagram": diagram_result
    }