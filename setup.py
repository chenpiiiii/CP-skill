"""影律通安装配置"""

from setuptools import setup, find_packages

setup(
    name="cinemalaw-ai",
    version="1.0.0",
    description="影律通 - 影视行业合同与版权合规智能审查系统",
    author="Cinemalaw AI Team",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.115.0",
        "pydantic>=2.9.0",
        "pydantic-settings>=2.5.0",
        "httpx>=0.27.0",
        "pymilvus>=2.4.0",
        "elasticsearch>=8.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0",
            "pytest-cov>=5.0",
            "black>=24.0",
            "mypy>=1.11",
        ],
    },
    entry_points={
        "console_scripts": [
            "cinemalaw=api.main:app",
        ],
    },
)
