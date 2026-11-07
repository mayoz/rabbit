"""Print every git repository named <name> directly under <folder> or one level deeper."""
import os
import sys


def find(folder, name):
    folder = os.path.expanduser(folder)
    hits = []
    for parent in [folder] + sorted(os.path.join(folder, d) for d in os.listdir(folder)
                                    if os.path.isdir(os.path.join(folder, d))):
        path = os.path.join(parent, name)
        if os.path.isdir(path) and os.path.exists(os.path.join(path, ".git")):
            hits.append(path)
    return sorted(set(hits))


def main(argv):
    if len(argv) != 3:
        print("usage: find_repo.py <repositories-folder> <name>", file=sys.stderr)
        return 2
    try:
        hits = find(argv[1], argv[2])
    except OSError:
        hits = []
    for h in hits:
        print(h)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
