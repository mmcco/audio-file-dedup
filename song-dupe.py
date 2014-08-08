# A simple script to remove iTunes' irritating duplicated files.

import os, hashlib
from collections import defaultdict


music_dir = raw_input("enter root directory under which all music is stored: ")

song_paths = set()

for (dirpath, _, filenames) in os.walk(music_dir):
    for filename in filenames:
        if any([filename.strip().endswith(suffix) for suffix in [".mp3", ".flac", ".wav", ".aac"]]):
            song_paths.add(dirpath + '/' + filename)

print len(song_paths), "song paths gathered"


proc_count = 0
checksums = defaultdict(list)

for song_path in song_paths:

    if proc_count % 1000 == 0:
        print proc_count / 1000, "thousand files hashed"
    proc_count += 1

    with open(song_path, "r") as song_file:
        md5 = hashlib.new("md5")
        md5.update(song_file.read())
        checksums[md5.digest()].append(song_path)


for dupe_paths in checksums.values():

    if len(dupe_paths) > 1:
        dupe_paths.sort()
        for dupe_path in dupe_paths[1:]:
            if dupe_path.strip().split()[-1].isdigit() and dupe_path.startswith(dupe_paths[0]):
                print "will delete", dupe_path


with open("dupefiles.txt", "w") as outfile:
    lines = []
    for dupe_paths in checksums.values():
        if len(dupe_paths) > 1:
            lines.append('\n'.join(dupe_paths) + '\n\n')
    outfile.writelines(lines)
