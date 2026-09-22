from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.repository_service import (
    clone_repository
)

from services.repository_manager import (
    get_repository_status
)

from services.project_analyzer import (
    analyze_project
)

from services.documentation_generator import (
    generate_project_documentation
)

from services.git_documentation_agent import (
    synchronize_documentation,
    synchronize_current_documentation
)

from services.documentation_state import (
    save_documentation_state
)

from services.git_state_analyzer import (
    get_git_commit_state
)


app = FastAPI(
    title="AI Documentation Agent",
    description=(
        "AI Agent for Automated Technical "
        "Documentation Generation"
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Static Diagrams
# ============================================================

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


class CurrentDocumentationSyncRequest(BaseModel):

    repository_path: str


class RepositoryStatusRequest(BaseModel):

    repository_path: str


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
# Repository Status
# ============================================================


@app.post(
    "/repositories/status"
)
def repository_status_endpoint(
    request: RepositoryStatusRequest
):

    result = get_repository_status(
        request.repository_path
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

    if not result["success"]:

        return result

    git_state_result = get_git_commit_state(
        request.repository_path
    )

    if not git_state_result["success"]:

        return git_state_result

    state_result = save_documentation_state(
        request.repository_path,
        git_state_result["latest_commit"]
    )

    if not state_result["success"]:

        return state_result

    result["documentation_state"] = (
        state_result
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


# ============================================================
# Automatic Current Git Synchronization
# ============================================================


@app.post(
    "/repositories/synchronize-current"
)
def synchronize_current_documentation_endpoint(
    request: CurrentDocumentationSyncRequest
):

    project_analysis = analyze_project(
        request.repository_path
    )

    if not project_analysis["success"]:

        return project_analysis

    result = synchronize_current_documentation(
        request.repository_path,
        project_analysis
    )

    return result