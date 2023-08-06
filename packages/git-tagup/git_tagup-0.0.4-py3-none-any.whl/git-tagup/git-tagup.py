import os
import sys
import re

from git import Repo, exc

gitpython_commit_prefixes = ['commit (initial): ', 'commit: ']

def main():

    try:
        repo = Repo(os.path.abspath(os.getcwd()))

    except exc.InvalidGitRepositoryError:
        print("Error: No Git repository found in current directory. Please browse into a Git repository and try again.")
        sys.exit()

    tagmap = {}
    for t in repo.tags:
        tagmap.setdefault(repo.commit(t).hexsha, []).append(t)

    for commit in reversed(list(repo.iter_commits(repo.active_branch))):

        version = re.search(r'(?:(\d+\.(?:\d+\.)*\d+))', commit.message)

        if ( version ):
            version = version.group()

        if ( version and 'v'+version not in [t.tag.tag for t in repo.tags] and commit.hexsha not in tagmap ):

            while 1:

                confirm = input("Create the tag 'v" + version + "' for commit message '" + remove_prefix(commit.message[0:-1], gitpython_commit_prefixes) + "'? (y/n/q): ")

                if ( confirm == 'y' ):

                    try:
                        repo.create_tag('v' + version, ref=commit.hexsha, message="Version " + version)

                    except exc.GitCommandError:
                        print("Duplicate version '" + version + "' found in commit " + commit.hexsha + ". Skipping.")

                    finally:
                        break

                elif ( confirm == 'n'):
                    break

                elif ( confirm == 'q'):
                    sys.exit()

                else:
                    print("Error: Invalid entry, please try again.")


def remove_prefix(text, prefix_list):

    for prefix in prefix_list:

        if text.startswith(prefix):
            text = text[len(prefix):]

    return text

if __name__ == "__main__":
    main()
