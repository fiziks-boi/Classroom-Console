from setuptools import setup, find_packages

setup(
    name="classroom_console",
    version="1.0.0",
    description="AI CLI with dynamic personas and OpenAI integration",
    author="Kade Ogden",
    install_requires=[
        "openai",
        "prompt_toolkit",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ai-cli=class_console_with_personas:main",  # Replace `ai_script` with your script's filename (without .py)
        ]
    },
)
