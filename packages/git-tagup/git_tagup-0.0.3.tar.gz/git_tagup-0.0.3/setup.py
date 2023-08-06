import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git_tagup",
    version="0.0.3",
    author="Jacob Stopak",
    author_email="jacob@initialcommit.io",
    description="A command-line tool for finding and tagging relevant Git commits based on existing commit messages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://initialcommit.com/projects/git-tagup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'gitpython'
    ],
)
