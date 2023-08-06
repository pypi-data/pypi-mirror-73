# git-tagup
---

Find and tag Git commits based on version numbers in commit messages.

## Quickstart
---

1) Install `git-tagup`:

```shell
$ pip install git-tagup
```

2) Browse to the Git repository you want to add tags to - this is usually your project root directory containing the `.git` directory:

```shell
$ cd path/to/project/root
```

3) Run the program:

```shell
$ git-tagup
```

## Example
---

```shell
$ cd path/to/project/root
$ git-tagup
Create the tag 'v0.1.1' for commit message 'Bump version to 0.1.1'? (y/n/q): n
Create the tag 'v0.1.2' for commit message 'Bump version to 0.1.2'? (y/n/q): y
Create the tag 'v0.1.3' for commit message 'Bump version to 0.1.3'? (y/n/q): q
```

## Installation
---

```shell
$ pip install git-tagup
```

## Learn More
---

Learn more about this project on the [git-tagup project page](https://initialcommit.com/projects/git-tagup).

## Authors
---

* **Jacob Stopak** - on behalf of [Initial Commit](https://initialcommit.com)
