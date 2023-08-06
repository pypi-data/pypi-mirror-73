import os
import re
import sys

from git import Repo, exc

from git_tagup import util


def main():

    # Connect to Git repository in current directory, if available
    try:
        repo = Repo(os.path.abspath(os.getcwd()))

    except exc.InvalidGitRepositoryError:
        print("Error: No Git repository found in current directory. Please browse into a Git repository and try again.")
        sys.exit()

    # Create map between commits and their tags
    tagmap = {}
    for t in repo.tags:
        tagmap.setdefault(repo.commit(t).hexsha, []).append(t)

    # Found-a-version flag
    found_version = False

    # Iterate commits on checked-out branch
    for commit in reversed(list(repo.iter_commits(repo.active_branch))):

	# Look for version number (format xxx.yyy.zzz) in the commit message
        version = re.search(r'(?:(\d+\.(?:\d+\.)*\d+))', commit.message)

        if version:
            version = version.group()

        # If version is found in commit message, and version is not already tagged, and commit has no tags
        if ( version and 'v'+version not in [t.name for t in repo.tags] and commit.hexsha not in tagmap ):

            found_version = True

            # User interation loop
            while 1:

                # Prompt user to create the tag for this version, skip, or quit
                confirm = input("Create the tag 'v" + version + "' for commit message '" + util.remove_prefix(commit.message[0:-1], util.gitpython_commit_prefixes) + "'? (y/n/q): ")

                # If 'y' input, try to create the new tag
                if ( confirm == 'y' ):

                    try:
                        repo.create_tag('v' + version, ref=commit.hexsha, message="Version " + version)

                    except exc.GitCommandError:
                        print("Duplicate version '" + version + "' found in commit " + commit.hexsha + ". Skipping.")

                    finally:
                        break

                # If 'n' input, skip this commit and move on
                elif ( confirm == 'n'):
                    break

                # If 'q' input, quit the program
                elif ( confirm == 'q'):
                    print("Exiting the program...")
                    sys.exit()

		# Else, reprompt the user
                else:
                    print("Error: Invalid entry, please try again.")

    # If no versions found, print message to that effect
    if not found_version:
        print("No version numbers of form 'xxx.yyy.zzz' found in active branch commit messages.")


if __name__ == "__main__":
    main()
