import codecs
import os
from setuptools import setup

setup(
    name="import-git-files",
    author="Michael T. Neylon",
    url="https://github.com/michaeltneylon/import-git-files",
    description="Import files from git repositories to local destinations.",
    long_description_content_type="text/markdown",
    long_description=codecs.open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"),
        "rb",
        "utf-8",
    ).read(),
    license="Apache License 2.0",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    py_modules=["import_git_files"],
    install_requires=[
        "GitPython>=3.1.3",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "import-git-files=import_git_files:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Localization",
        "Topic :: Software Development :: Version Control",
        "Topic :: Software Development :: Version Control :: Git",
    ],
)
