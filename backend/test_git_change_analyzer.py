from services.git_change_analyzer import (
    get_changed_files
)


repository_path = (
    "../repositories/dependency-test-project"
)

old_commit = "b70cf5c1329512ebe89ab5b63b2bbc6925d9f535"
new_commit = "2ac9613470638b6c8cee323150972bdf706e9ba9"

result = get_changed_files(
    repository_path,
    old_commit,
    new_commit
)


print()
print("=" * 80)
print("GIT CHANGE ANALYSIS")
print("=" * 80)

print()

print(result)