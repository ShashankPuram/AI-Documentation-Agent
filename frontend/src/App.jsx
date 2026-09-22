import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [repositoryPath, setRepositoryPath] = useState("");
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const checkChanges = async (repository) => {
    try {
      const response = await fetch(
        `${API_URL}/repositories/status`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            repository_path: repository.path,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message ||
            "Failed to check repository."
        );
      }

      setRepositories((current) =>
        current.map((item) =>
          item.path === repository.path
            ? {
                ...item,
                status: data.status,
                latestCommit:
                  data.latest_commit,
                documentedCommit:
                  data.documented_commit,
                documentationExists:
                  data.documentation_exists,
              }
            : item
        )
      );

    } catch (error) {
      setError(
        error.message ||
          "Unable to check repository."
      );
    }
  };
  const addRepository = async () => {
    const path = repositoryPath.trim();

    if (!path) {
      setError("Please enter a repository path.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/repositories/status`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            repository_path: path,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message ||
            "Failed to load repository."
        );
      }

      const repository = {
        id: data.repository,
        path: data.repository,
        name: data.repository_name,
        status: data.status,
        latestCommit: data.latest_commit,
        documentedCommit:
          data.documented_commit,
        documentationExists:
          data.documentation_exists,
      };

      setRepositories((current) => {
        const alreadyExists = current.some(
          (item) =>
            item.path === repository.path
        );

        if (alreadyExists) {
          return current.map((item) =>
            item.path === repository.path
              ? repository
              : item
          );
        }

        return [
          ...current,
          repository,
        ];
      });

      setRepositoryPath("");

    } catch (error) {
      setError(
        error.message ||
          "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const getStatusClass = (status) => {
    if (status === "Up to date") {
      return "status-up-to-date";
    }

    if (status === "Changes detected") {
      return "status-changes";
    }

    return "status-not-generated";
  };

  return (
    <div className="app">

      {/* Header */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            AI
          </div>

          <div>
            <h1>
              AI Documentation Agent
            </h1>

            <p>
              Automated technical documentation
            </p>
          </div>

        </div>

        <div className="ollama-status">

          <span className="status-dot"></span>

          Ollama Connected

        </div>

      </header>


      {/* Main */}

      <main className="main">

        {/* Add Repository */}

        <section className="add-repository">

          <div className="section-heading">

            <div>

              <h2>
                Add Repository
              </h2>

              <p>
                Add a new local Git repository
                to generate and maintain
                documentation.
              </p>

            </div>

          </div>


          <div className="repository-input">

            <input
              type="text"
              placeholder="D:\Projects\MyProject"
              value={repositoryPath}
              onChange={(event) =>
                setRepositoryPath(
                  event.target.value
                )
              }
              onKeyDown={(event) => {

                if (
                  event.key === "Enter" &&
                  !loading
                ) {
                  addRepository();
                }

              }}
              disabled={loading}
            />

            <button
              onClick={addRepository}
              disabled={loading}
            >
              {loading
                ? "Loading..."
                : "+ Add Repository"}
            </button>

          </div>


          <p className="input-hint">
            Enter the path of a local Git
            repository.
          </p>


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}

        </section>


        {/* Repository List */}

        <section className="repositories">

          <div className="section-heading">

            <div>

              <h2>
                My Repositories
              </h2>

              <p>
                Manage your documentation
                projects.
              </p>

            </div>

            <span className="repository-count">
              {repositories.length}{" "}
              {repositories.length === 1
                ? "repository"
                : "repositories"}
            </span>

          </div>


          {repositories.length === 0 ? (

            <div className="empty-state">

              <div className="empty-icon">
                📁
              </div>

              <h3>
                No repositories added
              </h3>

              <p>
                Add a local Git repository
                above to get started.
              </p>

            </div>

          ) : (

            <div className="repository-grid">

              {repositories.map(
                (repository) => (

                  <div
                    className="repository-card"
                    key={repository.id}
                  >

                    <div className="repository-card-header">

                      <div className="folder-icon">
                        📁
                      </div>

                      <div className="repository-info">

                        <h3>
                          {repository.name}
                        </h3>

                        <p>
                          {repository.path}
                        </p>

                      </div>

                    </div>


                    <div className="repository-status">

                      <span className="status-label">
                        Status
                      </span>

                      <span
                        className={getStatusClass(
                          repository.status
                        )}
                      >
                        {repository.status}
                      </span>

                    </div>


                    <div className="repository-commit">

                      <span>
                        Current commit
                      </span>

                      <strong>
                        {repository.latestCommit
                          ? repository.latestCommit.substring(
                              0,
                              8
                            )
                          : "—"}
                      </strong>

                    </div>


                    <div className="repository-commit">

                      <span>
                        Documented commit
                      </span>

                      <strong>
                        {repository.documentedCommit
                          ? repository.documentedCommit.substring(
                              0,
                              8
                            )
                          : "Not generated"}
                      </strong>

                    </div>


                    <div className="repository-actions">

                      <button
                        onClick={() =>
                          checkChanges(repository)
                        }
                      >
                        Check Changes
                      </button>
                      <button className="secondary-button">
                        Open Docs
                      </button>

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </section>

      </main>

    </div>
  );
}

export default App;