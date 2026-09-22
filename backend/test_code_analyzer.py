from services.code_analyzer import analyze_python_file


file_path = "../repositories/ast-test-project/main.py"


result = analyze_python_file(file_path)

print(result)