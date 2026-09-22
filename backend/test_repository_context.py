from services.project_analyzer import analyze_project
from services.repository_context import (
    build_repository_context,
    get_file_context,
    context_to_text
)


repository_path = (
    "../repositories/dependency-test-project"
)


# --------------------------------
# Analyze repository
# --------------------------------

project_analysis = analyze_project(
    repository_path
)


if not project_analysis["success"]:

    print(project_analysis)

    raise SystemExit


# --------------------------------
# Build repository context
# --------------------------------

repository_context = build_repository_context(
    project_analysis
)


print("\n")
print("=" * 80)
print("REPOSITORY CONTEXT")
print("=" * 80)

print(repository_context)


# --------------------------------
# Retrieve context for main.py
# --------------------------------

main_context = get_file_context(
    repository_context,
    "main.py"
)


print("\n")
print("=" * 80)
print("MAIN.PY CONTEXT")
print("=" * 80)

print(main_context)


# --------------------------------
# Convert context to LLM text
# --------------------------------

context_text = context_to_text(
    repository_context
)


print("\n")
print("=" * 80)
print("LLM CONTEXT")
print("=" * 80)

print(context_text)