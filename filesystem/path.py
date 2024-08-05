import os


def copy(src, dest):
    try:
        with open(src, "rb") as srcf, open(dest, "wb") as destf:
            destf.write(srcf.read())
        return {
            "success": True,
            "msg": f"\n-file\tsrc: {src}\tdest: {dest}\n"
        }
    except Exception as e:
        return {
            "success": False,
            "msg": f"\n-file-error\t{e}\n"
        }


def remove(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            return {
                "success": True,
                "msg": f"\n-file-deleted\t{path}\n"
            }
        else:
            raise Exception("path is not a file")
    except Exception as e:
        return {
            "success": False,
            "msg": f"\n-file-error\t{e}\n"
        }
