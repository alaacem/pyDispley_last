import os

def print_directory_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        if "myenv" in dirs:
            dirs.remove("myenv")
        if "setting" in dirs:
            dirs.remove("setting")
        if ".git" in dirs:
            dirs.remove(".git")
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(sub_indent, f))

project_root = os.path.dirname(os.path.realpath(__file__))
print_directory_tree(project_root)