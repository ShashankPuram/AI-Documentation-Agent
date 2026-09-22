from services.documentation_state import (
    save_documentation_state,
    load_documentation_state
)


repository_path = "../repositories/dependency-test-project"

commit = "b70cf5c1329512ebe89ab5b63b2bbc6925d9f535"


save_result = save_documentation_state(
    repository_path,
    commit
)

print("SAVE RESULT:")
print(save_result)

load_result = load_documentation_state(
    repository_path
)

print()
print("LOAD RESULT:")
print(load_result)