from services.documentation_service import (
    generate_code_documentation,
    regenerate_documentation
)

from services.documentation_validator import (
    validate_documentation
)

from services.documentation_quality import (
    calculate_documentation_quality
)


MAX_RETRIES = 3
QUALITY_THRESHOLD = 95


def generate_validated_documentation(
    file_analysis,
    repository_context=None
):
    generation_result = generate_code_documentation(
        file_analysis,
        repository_context
    )

    if not generation_result["success"]:
        return generation_result

    documentation = generation_result["response"]

    documentation = enforce_return_expressions(
        documentation,
        file_analysis
    )

    validation_result = validate_documentation(
        documentation,
        file_analysis
    )

    quality_result = calculate_documentation_quality(
        documentation,
        file_analysis
    )

    if (
        validation_result["valid"]
        and quality_result["percentage"] >= QUALITY_THRESHOLD
    ):
        return {
            "success": True,
            "documentation": documentation,
            "validation": validation_result,
            "quality": quality_result,
            "attempts": 1
        }

    previous_documentation = documentation

    for retry_number in range(1, MAX_RETRIES + 1):

        feedback = []

        for error in validation_result["errors"]:
            feedback.append(
                f"Validation error: {error}"
            )

        for check in quality_result["checks"]:
            if not check["passed"]:
                feedback.append(
                    "Quality check failed: "
                    f"{check['check']}"
                )

        if not feedback:
            feedback.append(
                "Documentation quality is below "
                f"the required threshold of "
                f"{QUALITY_THRESHOLD}%."
            )

        regeneration_result = regenerate_documentation(
            file_analysis,
            repository_context,
            previous_documentation,
            feedback
        )

        if not regeneration_result["success"]:
            return regeneration_result

        documentation = regeneration_result["response"]

        documentation = enforce_return_expressions(
            documentation,
            file_analysis
        )

        validation_result = validate_documentation(
            documentation,
            file_analysis
        )

        quality_result = calculate_documentation_quality(
            documentation,
            file_analysis
        )

        if (
            validation_result["valid"]
            and quality_result["percentage"] >= QUALITY_THRESHOLD
        ):
            return {
                "success": True,
                "documentation": documentation,
                "validation": validation_result,
                "quality": quality_result,
                "attempts": retry_number + 1
            }

        previous_documentation = documentation

    return {
        "success": False,
        "message": (
            "Documentation failed validation or quality "
            "requirements after 4 attempts."
        ),
        "documentation": documentation,
        "validation": validation_result,
        "quality": quality_result,
        "attempts": MAX_RETRIES + 1
    }


def enforce_return_expressions(
    documentation,
    file_analysis
):
    """
    Ensure every return expression detected directly
    from the source code appears literally in the
    generated documentation.

    This prevents the LLM from replacing an actual
    source expression with an equivalent rewritten
    expression.
    """

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

        if not return_expression:
            continue

        if return_expression in documentation:
            continue

        documentation = _append_missing_return_expression(
            documentation,
            return_expression
        )

    return documentation


def _append_missing_return_expression(
    documentation,
    return_expression
):
    """
    Add the exact source return expression to the
    documentation when the LLM omitted or rewrote it.
    """

    exact_return = f"`{return_expression}`"

    lines = documentation.splitlines()

    returns_heading_index = None

    for index, line in enumerate(lines):
        if line.strip().lower() == "**returns:**":
            returns_heading_index = index
            break

    if returns_heading_index is not None:

        insertion_index = returns_heading_index + 1

        lines.insert(
            insertion_index,
            f"Source return expression: {exact_return}"
        )

        return "\n".join(lines)

    return (
        documentation.rstrip()
        + "\n\n"
        + "**Returns:**\n\n"
        + f"Source return expression: {exact_return}\n"
    )