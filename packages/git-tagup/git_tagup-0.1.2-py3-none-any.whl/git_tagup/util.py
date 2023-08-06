# Strip these prefixes from GitPython commit messages
gitpython_commit_prefixes = ['commit (initial): ', 'commit: ']

def remove_prefix(text, prefix_list):
    """Remove a list of prefixes from a string."""

    for prefix in prefix_list:

        if text.startswith(prefix):
            text = text[len(prefix):]

    return text
