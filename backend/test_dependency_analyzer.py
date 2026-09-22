from services.dependency_analyzer import analyze_dependencies


repository_path = "../repositories/dependency-test-project"


result = analyze_dependencies(repository_path)

print(result)