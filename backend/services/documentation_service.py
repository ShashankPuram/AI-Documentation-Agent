import json
import re

from services.llm_service import generate_text
from services.repository_context import get_file_context


def generate_project_overview(project_analysis):
    """
    Generate a source-grounded project overview.
    """

    context = {
        "repository": project_analysis["repository"],
        "structure": project_analysis["structure"],
        "python_files": project_analysis["code"]["python_files"],
        "dependencies": project_analysis["dependencies"]
    }

    prompt = f"""
You are a technical documentation generator.

Generate a concise project overview using ONLY the repository
analysis provided below.

Do not invent technologies, features, databases, APIs, users,
deployment systems, or behavior that cannot be supported by
the provided information.

Repository analysis:

{json.dumps(context, indent=2)}

Include:

# Project Overview

A short description of what the repository contains.

## Project Structure

Describe the available files and directories.

## Components

Describe the Python files and the classes/functions they contain.

## Dependencies

Describe the detected relationships between project files.

Return ONLY Markdown documentation.
"""

    result = generate_text(prompt)

    if not result["success"]:
        return result

    cleaned = clean_generated_documentation(
        result["response"],
        None
    )

    return {
        "success": True,
        "response": cleaned
    }


def prepare_documentation_context(file_analysis):
    """
    Prepare safe AST information for the LLM.
    """

    safe_analysis = {
        "file": file_analysis["file"],
        "classes": [],
        "standalone_functions": [],
        "imports": file_analysis["imports"]
    }

    for class_info in file_analysis["classes"]:

        class_context = {
            "name": class_info["name"],
            "docstring": class_info["docstring"],
            "methods": []
        }

        for method in class_info["methods"]:

            parameters = [
                parameter
                for parameter in method["parameters"]
                if parameter != "self"
            ]

            class_context["methods"].append({
                "name": method["name"],
                "parameters": parameters,
                "docstring": method["docstring"],
                "returns": method["returns"],
                "calls": method["calls"]
            })

        safe_analysis["classes"].append(
            class_context
        )

    for function in file_analysis["standalone_functions"]:

        safe_analysis["standalone_functions"].append({
            "name": function["name"],
            "parameters": function["parameters"],
            "docstring": function["docstring"],
            "returns": function["returns"],
            "calls": function["calls"]
        })

    return safe_analysis


def generate_code_documentation(
    file_analysis,
    repository_context=None
):
    """
    Generate source-grounded documentation for one Python file.
    """

    safe_file_analysis = prepare_documentation_context(
        file_analysis
    )

    source_code = file_analysis["source_code"]

    code_context = json.dumps(
        safe_file_analysis,
        indent=2
    )

    related_context = ""

    if repository_context:

        file_name = file_analysis["file"]

        context_result = get_file_context(
            repository_context,
            file_name
        )

        if context_result["success"]:

            related_context = json.dumps(
                context_result["context"],
                indent=2
            )

    prompt = f"""
You are an automated technical documentation generator.

Generate documentation for ONE Python source file.

The source code is the primary source of truth.

========================================
SOURCE CODE
========================================

{source_code}

========================================
AST ANALYSIS
========================================

{code_context}

========================================
RELATED REPOSITORY CONTEXT
========================================

{related_context}

========================================
STRICT RULES
========================================

1. Document ONLY classes actually defined in this file.

2. Document ONLY standalone functions actually defined in
   this file.

3. Document ONLY methods actually defined inside those classes.

4. Never invent classes.

5. Never invent functions.

6. Never invent methods.

7. Never invent parameters.

8. Never document "self" as a parameter.

9. Never invent parameter types.

10. Never invent return values.

11. Preserve the EXACT return expression from the AST analysis.

12. For every function or method with a return expression,
    include the exact expression in the Returns section
    using inline Markdown code formatting.

    Example:

    **Returns:**

    `str(user)`

13. Only describe behavior supported by the source code.

14. Imported classes and functions are NOT definitions in this file.

15. If the file has no classes, DO NOT create a Classes section.

16. If the file has no standalone functions, DO NOT create a
    Functions section.

17. Imports may be documented if imports exist.

18. Do not add information about technologies or systems that
    are not present in the source.

19. Return ONLY the final Markdown documentation.

20. Do NOT include analysis or explanations.

21. Do NOT include source code.

22. Do NOT include AST analysis.

23. Do NOT include validation errors.

24. Do NOT include a justification.

25. Do NOT write "Here is the documentation."

26. Do NOT write "CORRECTED DOCUMENTATION."

========================================
FORMAT
========================================

Start with:

# File: <filename>

For actual classes:

## Classes

### ClassName

**Purpose:**

#### Methods

##### method_name

**Parameters:**

**Returns:**

`<EXACT RETURN EXPRESSION>`

**Behavior:**

For actual standalone functions:

## Functions

### function_name

**Purpose:**

**Parameters:**

**Returns:**

`<EXACT RETURN EXPRESSION>`

**Behavior:**

If imports exist:

## Imports

List the actual imports.

Return ONLY Markdown.
"""

    result = generate_text(prompt)

    if not result["success"]:
        return result

    cleaned_documentation = (
        clean_generated_documentation(
            result["response"],
            file_analysis
        )
    )

    return {
        "success": True,
        "response": cleaned_documentation
    }


def regenerate_documentation(
    file_analysis,
    repository_context,
    previous_documentation,
    validation_errors
):
    """
    Regenerate documentation using validator feedback.
    """

    safe_file_analysis = prepare_documentation_context(
        file_analysis
    )

    source_code = file_analysis["source_code"]

    code_context = json.dumps(
        safe_file_analysis,
        indent=2
    )

    related_context = ""

    if repository_context:

        file_name = file_analysis["file"]

        context_result = get_file_context(
            repository_context,
            file_name
        )

        if context_result["success"]:

            related_context = json.dumps(
                context_result["context"],
                indent=2
            )

    errors = "\n".join(
        f"- {error}"
        for error in validation_errors
    )

    prompt = f"""
You are correcting automatically generated technical
documentation.

The previous documentation failed validation.

Generate ONLY the corrected final Markdown documentation.

========================================
SOURCE CODE
========================================

{source_code}

========================================
AST ANALYSIS
========================================

{code_context}

========================================
VALIDATION ERRORS
========================================

{errors}

========================================
PREVIOUS DOCUMENTATION
========================================

{previous_documentation}

========================================
RELATED REPOSITORY CONTEXT
========================================

{related_context}

========================================
STRICT RULES
========================================

1. Fix every validation error.

2. Document ONLY definitions present in the source.

3. Never invent classes.

4. Never invent functions.

5. Never invent methods.

6. Never invent parameters.

7. Never document self as a parameter.

8. Never invent parameter types.

9. Preserve the EXACT return expression from the AST.

10. Every expected return expression MUST appear literally
    in the documentation.

11. Put each return expression inside Markdown inline code.

    Example:

    **Returns:**

    `str(user)`

12. Never invent behavior.

13. Do not create a Classes section when there are no classes.

14. Do not create a Functions section when there are no
    standalone functions.

15. Imported classes are not classes defined in this file.

16. Return ONLY Markdown documentation.

17. Do not include source code.

18. Do not include AST analysis.

19. Do not include validation errors.

20. Do not include correction explanations.

21. Do not include a justification.

22. Do not write "Here is the documentation."

23. Do not write "CORRECTED DOCUMENTATION."

24. Do not duplicate Markdown labels such as:

    **Returns:** **Returns:**

Start with:

# File: <filename>

Return ONLY the final documentation.
"""

    result = generate_text(prompt)

    if not result["success"]:
        return result

    cleaned_documentation = (
        clean_generated_documentation(
            result["response"],
            file_analysis
        )
    )

    return {
        "success": True,
        "response": cleaned_documentation
    }


def clean_generated_documentation(
    documentation,
    file_analysis
):
    """
    Deterministically clean common LLM meta-output and
    enforce basic structural consistency with the AST.
    """

    if not documentation:
        return documentation

    documentation = documentation.strip()

    # Remove common meta prefixes.
    documentation = re.sub(
        r"(?is)^here\s+is\s+the\s+documentation\s*:?\s*",
        "",
        documentation
    )

    documentation = re.sub(
        r"(?is)^corrected\s+documentation\s*:?\s*",
        "",
        documentation
    )

    # Remove wrapper headings.
    marker_patterns = [
        r"(?is)^=+\s*CORRECTED DOCUMENTATION\s*=+\s*",
        r"(?is)^=+\s*FINAL DOCUMENTATION\s*=+\s*"
    ]

    for pattern in marker_patterns:

        documentation = re.sub(
            pattern,
            "",
            documentation
        )

    # Remove large prompt/debug sections.
    unwanted_headings = [
        "SOURCE CODE",
        "AST ANALYSIS",
        "VALIDATION ERRORS",
        "JUSTIFICATION",
        "CORRECTION",
        "CORRECTIONS",
        "REASONING"
    ]

    for heading in unwanted_headings:

        pattern = (
            rf"(?is)"
            rf"(?:^|\n)"
            rf"=+\s*{re.escape(heading)}\s*=+"
            rf".*"
        )

        match = re.search(
            pattern,
            documentation
        )

        if match:

            documentation = (
                documentation[:match.start()]
                .rstrip()
            )

    # Remove duplicate labels.
    documentation = re.sub(
        r"(?im)"
        r"(\*\*(?:Returns|Parameters|Purpose|Behavior):\*\*)"
        r"\s*\n\s*"
        r"\1",
        r"\1",
        documentation
    )

    # Normalize File heading.
    documentation = re.sub(
        r"(?im)^#\s*File:\s*",
        "# File: ",
        documentation
    )

    # Fix bold File heading.
    documentation = re.sub(
        r"(?im)^\*\*File:\s*([^*]+)\*\*\s*$",
        r"# File: \1",
        documentation
    )

    # Remove Classes section if no classes exist.
    if file_analysis is not None:

        if not file_analysis["classes"]:

            documentation = re.sub(
                r"(?is)"
                r"^##\s+Classes\s*$"
                r".*?"
                r"(?=^##\s+|\Z)",
                "",
                documentation
            )

        # Remove Functions section if no standalone functions.
        if not file_analysis["standalone_functions"]:

            documentation = re.sub(
                r"(?is)"
                r"^##\s+Functions\s*$"
                r".*?"
                r"(?=^##\s+|\Z)",
                "",
                documentation
            )

    # Remove excessive blank lines.
    documentation = re.sub(
        r"\n{3,}",
        "\n\n",
        documentation
    )

    return documentation.strip()