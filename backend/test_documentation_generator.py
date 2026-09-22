from services.documentation_generator import (
    generate_project_documentation
)


repository_path = (
    "../repositories/dependency-test-project"
)


result = generate_project_documentation(
    repository_path
)


print(result)