import git
import typing


def git_unstaged_and_untracked_file_list(proj_dir: str) -> typing.List[str]:
    """
    :proj_dir: 项目路径， git根路劲
    :return: List
    """
    repo = git.Repo(proj_dir)
    file_set = set()
    for diff in repo.index.diff(None):
        file_set.add(diff.a_path)
        file_set.add(diff.b_path)
    file_list = list(file_set)
    file_list = file_list + repo.untracked_files
    return file_list


def git_current_branch(proj_dir: str) -> str:
    repo = git.Repo(proj_dir)
    return repo.active_branch
