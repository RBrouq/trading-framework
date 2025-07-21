import os


def tree(path=".", prefix="", max_depth=2, depth=0):
    if depth > max_depth:
        return
    print(f"{prefix}{os.path.basename(path) or path}/")
    entries = sorted(os.listdir(path))
    for e in entries:
        if e == "__pycache__":
            continue
        full = os.path.join(path, e)
        if os.path.isdir(full):
            tree(full, prefix + "    ", max_depth, depth + 1)
        else:
            print(f"{prefix}    {e}")


if __name__ == "__main__":
    tree()
