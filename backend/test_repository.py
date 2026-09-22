from services.repository_service import clone_repository


repository_url = "https://github.com/octocat/Hello-World.git"
repository_name = "hello-world"


result = clone_repository(repository_url, repository_name)

print(result)