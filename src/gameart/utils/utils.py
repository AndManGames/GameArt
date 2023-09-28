import subprocess


def get_git_root_path() -> str:
    """
    Gets the root path of the current git repository

    Returns:
        str: string with the root path of the current git repository
    """
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
