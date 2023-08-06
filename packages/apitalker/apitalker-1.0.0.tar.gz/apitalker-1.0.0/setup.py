from setuptools import setup, find_packages

with open("./README.md", mode="r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="apitalker",
    version="v1.0.0",
    packages=find_packages(),
    install_requires=["requests", "pandas"],
    author="Radek 'bednaJedna' Bednarik",
    author_email="bednarik.radek@gmail.com",
    description="Python wrapper for using Apitalks API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="api Apitalks wrapper python3 data library utility",
    url="https://github.com/bednaJedna/att",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
)
