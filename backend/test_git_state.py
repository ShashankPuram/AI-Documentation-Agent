from services.git_state_analyzer import get_git_commit_state


repository_path = "../repositories/dependency-test-project"

result = get_git_commit_state(repository_path)

print(result)