from services.project_analyzer import analyze_project


repository_path = "../repositories/dependency-test-project"


result = analyze_project(repository_path)

print(result)