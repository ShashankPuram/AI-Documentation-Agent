from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from services.repository_service import (
    clone_repository
)

from services.project_analyzer import (
    analyze_project
)

from services.documentation_generator import (
    generate_project_documentation
)

from services.git_documentation_agent import (
    synchronize_documentation
)


app = FastAPI(
    title="AI Documentation Agent",
    description=(
        "AI Agent for Automated Technical "
        "Documentation Generation"
    ),
    version="1.0.0"
)


app.mount(
    "/diagrams",
    StaticFiles(
        directory="../repositories"
    ),
    name="diagrams"
)


# ============================================================
# Request Models
# ============================================================


class RepositoryRequest(BaseModel):

    repository_url: str
    repository_name: str


class ProjectAnalysisRequest(BaseModel):

    repository_path: str


class DocumentationRequest(BaseModel):

    repository_path: str


class DocumentationSyncRequest(BaseModel):

    repository_path: str
    old_commit: str
    new_commit: str


# ============================================================
# Root
# ============================================================


@app.get("/")
def root():

    return {
        "message": (
            "AI Documentation Agent is running"
        )
    }


# ============================================================
# Repository Clone
# ============================================================


@app.post(
    "/repositories/clone"
)
def clone_repository_endpoint(
    request: RepositoryRequest
):

    result = clone_repository(
        request.repository_url,
        request.repository_name
    )

    return result


# ============================================================
# Repository Analysis
# ============================================================


@app.post(
    "/repositories/analyze"
)
def analyze_repository_endpoint(
    request: ProjectAnalysisRequest
):

    result = analyze_project(
        request.repository_path
    )

    return result


# ============================================================
# Complete Documentation Generation
# ============================================================


@app.post(
    "/repositories/document"
)
def generate_documentation_endpoint(
    request: DocumentationRequest
):

    result = generate_project_documentation(
        request.repository_path
    )

    return result


# ============================================================
# Git Documentation Synchronization
# ============================================================


@app.post(
    "/repositories/synchronize"
)
def synchronize_documentation_endpoint(
    request: DocumentationSyncRequest
):

    project_analysis = analyze_project(
        request.repository_path
    )

    if not project_analysis["success"]:

        return project_analysis

    result = synchronize_documentation(
        request.repository_path,
        request.old_commit,
        request.new_commit,
        project_analysis
    )

    return result