from setuptools import setup, find_packages

setup(
    name="mcp-copper",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "pydantic>=1.8.0,<2.0.0",
        "httpx>=0.23.0,<0.24.0",
        "python-dotenv>=0.19.0,<0.20.0",
        "tenacity>=8.0.1,<9.0.0",
        "typing-extensions>=4.0.0,<5.0.0",
        "aiohttp>=3.8.0,<4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0,<8.0.0",
            "pytest-cov>=2.12.0,<3.0.0",
            "black>=22.0.0,<23.0.0",
            "mypy>=0.910,<1.0.0",
            "isort>=5.9.0,<6.0.0",
            "flake8>=3.9.0,<4.0.0",
            "pytest-asyncio>=0.18.0,<0.19.0",
        ]
    },
    python_requires=">=3.8",
) 