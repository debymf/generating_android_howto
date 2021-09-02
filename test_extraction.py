import os

with open("test.txt") as f:
    downloaded = [line.rstrip() for line in f]


filenames_list = list()
with open("used_warc.paths") as f:
    files = [line.rstrip() for line in f]


out = list()

not_saved = list()
saved_files = dict()
for i, f in enumerate(files):
    head, filename = os.path.split(f)
    filenames_list.append(filename)

    found = 0
    for d in downloaded:
        if filename in d:
            found = 1
            break

    if found == 0:
        print(filename)
        not_saved.append(f)

