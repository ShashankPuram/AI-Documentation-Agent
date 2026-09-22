import json


# Keep the global repository context small enough for cloud LLM APIs.
MAX_CONTEXT_CHARS = 12000


def build_repository_context(project_analysis):
    """
    Build a structured context representation of the repository.
    """

    if not project_analysis.get("success"):

        return {
            "success": False,
            "message": "Invalid project analysis"
        }

    repository_name = project_analysis[
        "repository"
    ]

    structure = project_analysis[
        "structure"
    ]

    python_files = project_analysis[
        "code"
    ][
        "python_files"
    ]

    dependencies = project_analysis[
        "dependencies"
    ]

    context = {

        "repository": repository_name,

        "structure": {
            "files": structure["files"],
            "directories": structure["directories"],
            "file_count": structure["file_count"],
            "directory_count": structure[
                "directory_count"
            ]
        },

        "files": [],

        "dependencies": dependencies
    }

    for file_analysis in python_files:

        file_context = {

            "file": file_analysis["file"],

            "classes": [],

            "standalone_functions": [],

            "imports": file_analysis[
                "imports"
            ]
        }

        for class_info in file_analysis[
            "classes"
        ]:

            class_context = {

                "name": class_info[
                    "name"
                ],

                "docstring": class_info[
                    "docstring"
                ],

                "methods": []
            }

            for method in class_info[
                "methods"
            ]:

                parameters = [
                    parameter
                    for parameter in method[
                        "parameters"
                    ]
                    if parameter != "self"
                ]

                class_context[
                    "methods"
                ].append({

                    "name": method[
                        "name"
                    ],

                    "parameters": parameters,

                    "docstring": method[
                        "docstring"
                    ],

                    "returns": method[
                        "returns"
                    ],

                    "calls": method[
                        "calls"
                    ]
                })

            file_context[
                "classes"
            ].append(
                class_context
            )

        for function in file_analysis[
            "standalone_functions"
        ]:

            file_context[
                "standalone_functions"
            ].append({

                "name": function[
                    "name"
                ],

                "parameters": function[
                    "parameters"
                ],

                "docstring": function[
                    "docstring"
                ],

                "returns": function[
                    "returns"
                ],

                "calls": function[
                    "calls"
                ]
            })

        context[
            "files"
        ].append(
            file_context
        )

    return {
        "success": True,
        "context": context
    }


def get_file_context(
    repository_context,
    file_name
):

    if not repository_context.get(
        "success"
    ):

        return {
            "success": False,
            "message": "Invalid repository context"
        }

    context = repository_context[
        "context"
    ]

    for file_context in context[
        "files"
    ]:

        if file_context[
            "file"
        ] == file_name:

            related_dependencies = []

            for dependency in context[
                "dependencies"
            ]:

                if dependency[
                    "source"
                ] == file_name:

                    related_dependencies.append(
                        dependency
                    )

                elif dependency[
                    "target"
                ] == file_name:

                    related_dependencies.append(
                        dependency
                    )

            return {

                "success": True,

                "file": file_name,

                "context": {

                    "file": file_context,

                    "related_dependencies":
                        related_dependencies
                }
            }

    return {
        "success": False,
        "message": f"File not found: {file_name}"
    }


def context_to_text(context):

    if not context.get(
        "success"
    ):

        return ""

    context_text = json.dumps(
        context["context"],
        indent=2
    )

    # Prevent very large repository-wide context
    # from exceeding cloud LLM request limits.
    if len(context_text) > MAX_CONTEXT_CHARS:

        context_text = (
            context_text[
                :MAX_CONTEXT_CHARS
            ]
            + "\n\n"
            + "[Repository context truncated "
            "to fit the LLM request limit.]"
        )

    return context_text