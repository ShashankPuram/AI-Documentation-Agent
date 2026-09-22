from dataclasses import dataclass, field
from typing import List


@dataclass
class ParameterInfo:
    name: str


@dataclass
class MethodInfo:
    name: str
    parameters: List[ParameterInfo] = field(
        default_factory=list
    )
    returns: List[str] = field(
        default_factory=list
    )
    calls: List[str] = field(
        default_factory=list
    )
    docstring: str = ""


@dataclass
class ClassInfo:
    name: str
    docstring: str = ""
    methods: List[MethodInfo] = field(
        default_factory=list
    )


@dataclass
class FunctionInfo:
    name: str
    parameters: List[ParameterInfo] = field(
        default_factory=list
    )
    returns: List[str] = field(
        default_factory=list
    )
    calls: List[str] = field(
        default_factory=list
    )
    docstring: str = ""


@dataclass
class FileDocumentationModel:
    file: str
    classes: List[ClassInfo] = field(
        default_factory=list
    )
    functions: List[FunctionInfo] = field(
        default_factory=list
    )
    imports: List[str] = field(
        default_factory=list
    )


def build_documentation_model(
    file_analysis
):
    """
    Convert AST analysis into a structured documentation
    model.

    This model contains only deterministic information
    extracted from source code.
    """

    classes = []

    for class_analysis in file_analysis["classes"]:

        methods = []

        for method_analysis in class_analysis[
            "methods"
        ]:

            parameters = [
                ParameterInfo(
                    name=parameter
                )
                for parameter
                in method_analysis["parameters"]
                if parameter != "self"
            ]

            methods.append(
                MethodInfo(
                    name=method_analysis["name"],
                    parameters=parameters,
                    returns=method_analysis["returns"],
                    calls=method_analysis["calls"],
                    docstring=method_analysis["docstring"]
                )
            )

        classes.append(
            ClassInfo(
                name=class_analysis["name"],
                docstring=class_analysis["docstring"],
                methods=methods
            )
        )

    functions = []

    for function_analysis in file_analysis[
        "standalone_functions"
    ]:

        parameters = [
            ParameterInfo(
                name=parameter
            )
            for parameter
            in function_analysis["parameters"]
        ]

        functions.append(
            FunctionInfo(
                name=function_analysis["name"],
                parameters=parameters,
                returns=function_analysis["returns"],
                calls=function_analysis["calls"],
                docstring=function_analysis["docstring"]
            )
        )

    return FileDocumentationModel(
        file=file_analysis["file"],
        classes=classes,
        functions=functions,
        imports=file_analysis["imports"]
    )