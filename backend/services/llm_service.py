import os
import requests


# ============================================================
# LLM Configuration
# ============================================================

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.1:8b"
)

LLM_API_URL = os.getenv(
    "LLM_API_URL",
    ""
)

LLM_API_KEY = os.getenv(
    "LLM_API_KEY",
    ""
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    ""
)


# ============================================================
# Ollama
# ============================================================


def generate_with_ollama(prompt: str):

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]


# ============================================================
# OpenAI-Compatible API
# ============================================================


def generate_with_api(prompt: str):

    if not LLM_API_URL:
        raise ValueError(
            "LLM_API_URL is not configured."
        )

    if not LLM_API_KEY:
        raise ValueError(
            "LLM_API_KEY is not configured."
        )

    if not LLM_MODEL:
        raise ValueError(
            "LLM_MODEL is not configured."
        )

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": (
            f"Bearer {LLM_API_KEY}"
        ),
        "Content-Type": "application/json"
    }

    response = requests.post(
        LLM_API_URL,
        json=payload,
        headers=headers,
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


# ============================================================
# Main LLM Function
# ============================================================


def generate_text(prompt: str):

    try:

        if LLM_PROVIDER.lower() == "ollama":

            response = generate_with_ollama(
                prompt
            )

        elif LLM_PROVIDER.lower() == "api":

            response = generate_with_api(
                prompt
            )

        else:

            return {
                "success": False,
                "message": (
                    f"Unsupported LLM provider: "
                    f"{LLM_PROVIDER}"
                )
            }

        return {
            "success": True,
            "response": response
        }

    except (
        requests.RequestException,
        KeyError,
        ValueError
    ) as error:

        return {
            "success": False,
            "message": str(error)
        }