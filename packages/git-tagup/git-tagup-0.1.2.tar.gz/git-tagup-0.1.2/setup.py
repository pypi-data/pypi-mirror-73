import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git-tagup",
    version="0.1.2",
    author="Jacob Stopak",
    author_email="jacob@initialcommit.io",
    description="Find and tag Git commits based on version numbers in commit messages.",
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
    keywords='git tag git-tagup tagup tag-up version autotag auto-tag commit message',
    project_urls={
        'Homepage': 'https://initialcommit.com/projects/git-tagup',
    },
    entry_points={
        'console_scripts': [
            'git-tagup=git_tagup.__main__:main',
            'gtu=git_tagup.__main__:main',
        ],
    },
)
