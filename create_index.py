#!/usr/bin/python3
import os
import glob

exclude_dirs = ['.git']
# glob patterns of paths you want to exclude
exclude_path = ['.git*', '*.DS_Store*']

all_dirs = {}  # Key is path, value is list of directories
all_files = {}  # Key is path, value is list of directories

# Iterate over all directories and sub-directories
for path, dirs, files in os.walk("."):
    # path begins with ./
    if set(path[2:].split("/")).intersection(exclude_dirs):
        continue
    all_dirs[path] = dirs
    all_files[path] = files


def create_html(header, list_of_paths):
    li_elements = ""
    for path in list_of_paths:
        li_elements += f'<li><a href="{path}">{path}</li>\n'

    html = f"""
    <body>
    <html>
    <h2>{header}</h2>
    <p>
    {li_elements}
    </p>
    </body>
    </html>
    """

    return html

cwd = os.getcwd()
for _path in all_dirs.keys():
    _dirs = all_dirs[_path]
    _files = all_files[_path]

    list_of_paths = []

    path = _path.replace('.', '')

    for link in [*_dirs, *_files]:
        link_is_included = True
        for p in exclude_path:
            if glob.fnmatch.fnmatch(link, p):
                link_is_included = False
                continue
        if link_is_included:
            list_of_paths.append(link)
    html = create_html(path, list_of_paths)
    index_path = cwd + path + "/index.html"
    with open(index_path, "w") as index:
        index.write(html)
    print("Written ", index_path)
