from services.repository_analyzer import analyze_repository


repository_path = "../repositories/ast-test-project"


result = analyze_repository(repository_path)

print(result)