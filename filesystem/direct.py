import os

from filesystem import path


def copy(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    for content in contents(src):
        if os.path.isfile(content):
            path.copy(content, os.path.join(dest, os.path.basename(content)))
        elif os.path.isdir(content):
            copy(content, os.path.join(dest, os.path.basename(content)))
    print(f"-directory\tsrc: {src}\tdest: {dest}")


def remove(direct):
    for content in contents(direct):
        if os.path.isfile(content):
            path.remove(content)
        elif os.path.isdir(content):
            remove(content)
    os.rmdir(direct)
    print(f"-directory-deleted\t{direct}")


def contents(direct):
    return [os.path.join(direct, content) for content in os.listdir(direct)]


def fulltree(direct, avoid=[]):
    subdirs = contents(direct)
    for subdir in subdirs:
        if os.path.isdir(subdir) and not os.path.basename(subdir) in avoid:
            subdirs.remove(subdir)
            subdirs.extend(fulltree(subdir))
    return subdirs
