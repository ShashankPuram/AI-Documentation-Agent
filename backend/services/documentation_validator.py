import re


def validate_documentation(
    documentation,
    file_analysis
):
    """
    Validate generated documentation against deterministic
    AST facts and reject obvious LLM meta-output.
    """

    errors = []

    actual_classes = {
        class_info["name"]
        for class_info in file_analysis["classes"]
    }

    actual_functions = {
        function["name"]
        for function in file_analysis["standalone_functions"]
    }

    # ---------------------------------------------------------
    # Meta-output validation
    # ---------------------------------------------------------

    forbidden_meta_sections = [
        "SOURCE CODE",
        "AST ANALYSIS",
        "VALIDATION ERRORS",
        "JUSTIFICATION",
        "CORRECTED DOCUMENTATION",
        "CORRECTIONS",
        "REASONING"
    ]

    for phrase in forbidden_meta_sections:

        if re.search(
            rf"(?im)^\s*{re.escape(phrase)}\s*$",
            documentation
        ):
            errors.append(
                f"Unwanted meta-output detected: {phrase}"
            )

    if re.search(
        r"(?i)here\s+is\s+the\s+documentation",
        documentation
    ):
        errors.append(
            "Unwanted introductory text detected."
        )

    # ---------------------------------------------------------
    # File heading
    # ---------------------------------------------------------

    expected_file = file_analysis["file"]

    if not re.search(
        rf"(?im)^#\s*File:\s*{re.escape(expected_file)}\s*$",
        documentation
    ):
        errors.append(
            f"Expected file heading not found: {expected_file}"
        )

    # ---------------------------------------------------------
    # Classes
    # ---------------------------------------------------------

    class_section = _get_section(
        documentation,
        "Classes"
    )

    class_headings = re.findall(
        r"(?m)^###\s+`?([A-Za-z_][A-Za-z0-9_]*)`?\s*$",
        class_section
    )

    for class_name in class_headings:

        if class_name not in actual_classes:
            errors.append(
                f"Invented class detected: {class_name}"
            )

    if not actual_classes:

        if re.search(
            r"(?im)^##\s+Classes\s*$",
            documentation
        ):
            errors.append(
                "Classes section exists but the source "
                "contains no class definitions."
            )

    # ---------------------------------------------------------
    # Standalone functions
    # ---------------------------------------------------------

    function_section = _get_section(
        documentation,
        "Functions"
    )

    function_headings = re.findall(
        r"(?m)^###\s+`?([A-Za-z_][A-Za-z0-9_]*)`?\s*$",
        function_section
    )

    for function_name in function_headings:

        if function_name not in actual_functions:
            errors.append(
                f"Invented function detected: {function_name}"
            )

    if not actual_functions:

        if re.search(
            r"(?im)^##\s+Functions\s*$",
            documentation
        ):
            errors.append(
                "Functions section exists but the source "
                "contains no standalone functions."
            )

    # ---------------------------------------------------------
    # Parameters
    # ---------------------------------------------------------

    valid_parameters = set()

    for class_info in file_analysis["classes"]:

        for method in class_info["methods"]:

            for parameter in method["parameters"]:

                if parameter != "self":
                    valid_parameters.add(parameter)

    for function in file_analysis["standalone_functions"]:

        for parameter in function["parameters"]:
            valid_parameters.add(parameter)

    for parameter in valid_parameters:

        pattern = (
            rf"`?{re.escape(parameter)}`?"
            rf"\s*(?::|\()\s*"
            rf"(int|str|float|bool|list|dict|"
            rf"tuple|set|object|Any)"
        )

        if re.search(
            pattern,
            documentation,
            re.IGNORECASE
        ):
            errors.append(
                f"Invented parameter type detected: "
                f"{parameter}"
            )

    # ---------------------------------------------------------
    # self parameter
    # ---------------------------------------------------------

    parameter_sections = re.findall(
        r"\*\*Parameters:\*\*"
        r"(.*?)(?=\n\*\*Returns:\*\*|\n##|\Z)",
        documentation,
        re.IGNORECASE | re.DOTALL
    )

    for section in parameter_sections:

        if re.search(
            r"(?m)(?:^|\n)[\s*\-`]*self[\s*`]*(?:$|\n)",
            section
        ):
            errors.append(
                "Invalid parameter detected: self"
            )

    # ---------------------------------------------------------
    # Return expressions
    # ---------------------------------------------------------

    actual_returns = []

    for class_info in file_analysis["classes"]:

        for method in class_info["methods"]:
            actual_returns.extend(
                method["returns"]
            )

    for function in file_analysis["standalone_functions"]:

        actual_returns.extend(
            function["returns"]
        )

    for return_expression in actual_returns:

        if return_expression not in documentation:
            errors.append(
                f"Expected return expression not found: "
                f"{return_expression}"
            )

    # ---------------------------------------------------------
    # Methods
    # ---------------------------------------------------------

    for class_info in file_analysis["classes"]:

        class_name = class_info["name"]

        class_pattern = (
            rf"(?ms)^###\s+`?{re.escape(class_name)}`?\s*$"
            rf"(.*?)(?=^###\s+|\Z)"
        )

        class_match = re.search(
            class_pattern,
            class_section
        )

        if not class_match:
            continue

        class_content = class_match.group(1)

        for method in class_info["methods"]:

            method_name = method["name"]

            method_pattern = (
                rf"(?m)^#####\s+`?"
                rf"{re.escape(method_name)}"
                rf"`?\s*$"
            )

            if not re.search(
                method_pattern,
                class_content
            ):
                errors.append(
                    f"Expected method not documented: "
                    f"{class_name}.{method_name}"
                )

    # ---------------------------------------------------------
    # Duplicate labels
    # ---------------------------------------------------------

    duplicate_labels = re.findall(
        r"(?im)"
        r"(\*\*(?:Returns|Parameters|Purpose|Behavior):\*\*)"
        r"\s*\n\s*\1",
        documentation
    )

    for label in duplicate_labels:

        errors.append(
            f"Duplicate documentation label detected: "
            f"{label}"
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def _get_section(
    documentation,
    section_name
):
    """
    Extract a Markdown H2 section.
    """

    pattern = (
        rf"(?ms)^##\s+{re.escape(section_name)}\s*$"
        rf"(.*?)(?=^##\s+|\Z)"
    )

    match = re.search(
        pattern,
        documentation,
        re.IGNORECASE
    )

    if not match:
        return ""

    return match.group(1)