import os


def walk_level(path: str, depth: int):
    """
    It works just like os.walk, but you can pass it a level parameter
    that indicates how deep the recursion will go.
    If depth is -1 (or less than 0), the full depth is walked.
    """
    # if depth is negative, just walk
    if depth < 0:
        for root, dirs, files in os.walk(path):
            yield root, dirs, files

    # path.count works because is a file has a "/" it will show up in the list
    # as a ":"
    path = path.rstrip(os.path.sep)
    num_sep = path.count(os.path.sep)
    for root, dirs, files in os.walk(path):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + depth <= num_sep_this:
            del dirs[:]
