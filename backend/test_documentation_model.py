from services.project_analyzer import analyze_project

from services.documentation_model import (
    build_documentation_model
)


repository_path = (
    "../repositories/dependency-test-project"
)


project_analysis = analyze_project(
    repository_path
)


for file_analysis in (
    project_analysis["code"]["python_files"]
):

    model = build_documentation_model(
        file_analysis
    )

    print()
    print("=" * 80)
    print(model.file)
    print("=" * 80)

    print()

    print("Classes:")

    for class_info in model.classes:

        print(
            f"  Class: {class_info.name}"
        )

        for method in class_info.methods:

            parameters = [
                parameter.name
                for parameter
                in method.parameters
            ]

            print(
                f"    Method: "
                f"{method.name}"
            )

            print(
                f"      Parameters: "
                f"{parameters}"
            )

            print(
                f"      Returns: "
                f"{method.returns}"
            )

            print(
                f"      Calls: "
                f"{method.calls}"
            )

    print()

    print("Functions:")

    for function in model.functions:

        parameters = [
            parameter.name
            for parameter
            in function.parameters
        ]

        print(
            f"  Function: "
            f"{function.name}"
        )

        print(
            f"    Parameters: "
            f"{parameters}"
        )

        print(
            f"    Returns: "
            f"{function.returns}"
        )

        print(
            f"    Calls: "
            f"{function.calls}"
        )

    print()

    print(
        f"Imports: {model.imports}"
    )