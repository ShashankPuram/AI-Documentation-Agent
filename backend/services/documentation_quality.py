import re


def calculate_documentation_quality(
    documentation,
    file_analysis
):
    """
    Calculate a deterministic documentation quality score.

    Only applicable source-code components are evaluated.
    """

    checks = []

    actual_classes = {
        class_info["name"]
        for class_info in file_analysis["classes"]
    }

    actual_functions = {
        function["name"]
        for function in file_analysis[
            "standalone_functions"
        ]
    }

    methods_expected = []

    for class_info in file_analysis["classes"]:

        for method in class_info["methods"]:

            methods_expected.append(
                (
                    class_info["name"],
                    method["name"]
                )
            )

    expected_parameters = set()

    for class_info in file_analysis["classes"]:

        for method in class_info["methods"]:

            for parameter in method["parameters"]:

                if parameter != "self":
                    expected_parameters.add(
                        parameter
                    )

    for function in file_analysis[
        "standalone_functions"
    ]:

        for parameter in function["parameters"]:
            expected_parameters.add(parameter)

    expected_returns = []

    for class_info in file_analysis["classes"]:

        for method in class_info["methods"]:
            expected_returns.extend(
                method["returns"]
            )

    for function in file_analysis[
        "standalone_functions"
    ]:

        expected_returns.extend(
            function["returns"]
        )

    # ---------------------------------------------------------
    # File heading
    # ---------------------------------------------------------

    applicable_checks = [
        ("File heading", 10)
    ]

    file_heading_found = bool(
        re.search(
            rf"(?im)^#\s*File:\s*"
            rf"{re.escape(file_analysis['file'])}\s*$",
            documentation
        )
    )

    checks.append({
        "check": "File heading",
        "points": 10 if file_heading_found else 0,
        "passed": file_heading_found
    })

    # ---------------------------------------------------------
    # Classes
    # ---------------------------------------------------------

    if actual_classes:

        applicable_checks.append(
            ("Classes", 20)
        )

        documented_classes = set(
            re.findall(
                r"(?m)^###\s+`?"
                r"([A-Za-z_][A-Za-z0-9_]*)"
                r"`?\s*$",
                _get_section(
                    documentation,
                    "Classes"
                )
            )
        )

        classes_correct = (
            actual_classes == documented_classes
        )

        checks.append({
            "check": "Classes",
            "points": (
                20
                if classes_correct
                else 0
            ),
            "passed": classes_correct
        })

    # ---------------------------------------------------------
    # Standalone functions
    # ---------------------------------------------------------

    if actual_functions:

        applicable_checks.append(
            ("Standalone functions", 20)
        )

        documented_functions = set(
            re.findall(
                r"(?m)^###\s+`?"
                r"([A-Za-z_][A-Za-z0-9_]*)"
                r"`?\s*$",
                _get_section(
                    documentation,
                    "Functions"
                )
            )
        )

        functions_correct = (
            actual_functions == documented_functions
        )

        checks.append({
            "check": "Standalone functions",
            "points": (
                20
                if functions_correct
                else 0
            ),
            "passed": functions_correct
        })

    # ---------------------------------------------------------
    # Methods
    # ---------------------------------------------------------

    if methods_expected:

        applicable_checks.append(
            ("Methods", 15)
        )

        methods_found = []

        classes_section = _get_section(
            documentation,
            "Classes"
        )

        for class_info in file_analysis["classes"]:

            class_name = class_info["name"]

            class_pattern = (
                rf"(?ms)^###\s+`?"
                rf"{re.escape(class_name)}"
                rf"`?\s*$"
                rf"(.*?)(?=^###\s+|\Z)"
            )

            class_match = re.search(
                class_pattern,
                classes_section
            )

            if not class_match:
                continue

            class_content = class_match.group(1)

            method_names = re.findall(
                r"(?m)^#####\s+`?"
                r"([A-Za-z_][A-Za-z0-9_]*)"
                r"`?\s*$",
                class_content
            )

            for method_name in method_names:

                methods_found.append(
                    (
                        class_name,
                        method_name
                    )
                )

        methods_correct = (
            set(methods_expected)
            == set(methods_found)
        )

        checks.append({
            "check": "Methods",
            "points": (
                15
                if methods_correct
                else 0
            ),
            "passed": methods_correct
        })

    # ---------------------------------------------------------
    # Parameters
    # ---------------------------------------------------------

    if expected_parameters:

        applicable_checks.append(
            ("Parameters", 10)
        )

        parameters_correct = True
        missing_parameters = []

        for parameter in expected_parameters:

            parameter_pattern = (
                rf"(?<![A-Za-z0-9_])"
                rf"(?:`{re.escape(parameter)}`"
                rf"|"
                rf"\*\*{re.escape(parameter)}\*\*"
                rf"|"
                rf"{re.escape(parameter)})"
                rf"(?![A-Za-z0-9_])"
            )

            if not re.search(
                parameter_pattern,
                documentation
            ):
                parameters_correct = False

                missing_parameters.append(
                    parameter
                )

        # self must never be documented as a parameter.
        parameter_sections = re.findall(
            r"\*\*Parameters:\*\*"
            r"(.*?)(?=\n\*\*Returns:\*\*|\n##|\Z)",
            documentation,
            re.IGNORECASE | re.DOTALL
        )

        for section in parameter_sections:

            if re.search(
                r"(?im)"
                r"(?:^|\n)"
                r"[\s*\-`]*self[\s*`]*"
                r"(?::|$)",
                section
            ):
                parameters_correct = False

        checks.append({
            "check": "Parameters",
            "points": (
                10
                if parameters_correct
                else 0
            ),
            "passed": parameters_correct,
            "missing": missing_parameters
        })

    # ---------------------------------------------------------
    # Return expressions
    # ---------------------------------------------------------

    if expected_returns:

        applicable_checks.append(
            ("Return expressions", 10)
        )

        returns_correct = all(
            return_expression in documentation
            for return_expression
            in expected_returns
        )

        checks.append({
            "check": "Return expressions",
            "points": (
                10
                if returns_correct
                else 0
            ),
            "passed": returns_correct
        })

    # ---------------------------------------------------------
    # Meta-output
    # ---------------------------------------------------------

    applicable_checks.append(
        ("No obvious meta-output", 10)
    )

    forbidden_phrases = [
        "SOURCE CODE",
        "AST ANALYSIS",
        "VALIDATION ERRORS",
        "JUSTIFICATION",
        "CORRECTED DOCUMENTATION",
        "REASONING",
        "CORRECTIONS"
    ]

    has_meta_output = any(
        re.search(
            rf"(?im)^\s*{re.escape(phrase)}\s*$",
            documentation
        )
        for phrase in forbidden_phrases
    )

    has_introductory_text = bool(
        re.search(
            r"(?im)"
            r"^(based on|here is|here's|"
            r"the following is|"
            r"below is).*"
            r"(documentation|source code|rules)",
            documentation
        )
    )

    meta_output_found = (
        has_meta_output
        or has_introductory_text
    )

    checks.append({
        "check": "No obvious meta-output",
        "points": (
            0
            if meta_output_found
            else 10
        ),
        "passed": not meta_output_found
    })

    # ---------------------------------------------------------
    # Calculate score
    # ---------------------------------------------------------

    total_possible = sum(
        points
        for _, points in applicable_checks
    )

    total_score = sum(
        check["points"]
        for check in checks
    )

    if total_possible == 0:
        percentage = 0
    else:
        percentage = round(
            (
                total_score
                / total_possible
            ) * 100,
            2
        )

    return {
        "score": total_score,
        "max_score": total_possible,
        "percentage": percentage,
        "checks": checks
    }


def _get_section(
    documentation,
    section_name
):
    """
    Extract a Markdown H2 section.
    """

    pattern = (
        rf"(?ms)^##\s+"
        rf"{re.escape(section_name)}\s*$"
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