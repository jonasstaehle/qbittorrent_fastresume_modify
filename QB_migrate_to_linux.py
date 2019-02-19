# Written 2/17/2019
# This is my first program fresh out of a 1 week course. So, it is probably a little crude.
# This was written for Python 3.7.
# Bencode module can be installed with "pip install bencode.py" found here: https://pypi.org/project/bencode.py/
# Please do not try and use this without at least a basic understanding of Python.
# BACK UP YOUR FILES BEFORE PROCEEDING!!! THIS WILL OVERWRITE THEM!!!
# CORRUPTION MAY HAPPEN!!! USE AT YOUR OWN RISK!!!
# I would recommend COPYING the "BT_backup" directory to your desktop and running this script on the backup to ensure the originals are untouched.
# The intent of this is to be able to modify the file locations in the fastresume files to make migrating QBittorrent to Linux easier than manually changing the save path on hundreds of torrents.
# You will need to modify the value for "tor_dir" and "linux_dir_start" to suite your needs.
# In my testing, all of my fastresume files (almost 500) the save_path and qBt-savepath had identical values. I don't know if this is true 100% of the time.
# If for some reason they don't match, this will make them match as it is currently written. I do not know if that will cause a problem
# Example: this will convert the values of "save_path" and "qBt-savepath" from c:\torrent\downloads\faketorrentsite\music to /data/torrent/downloads/faketorrentsite/music
# Due to limitations in the bencode.py module, I had to re-write the entire fastresume file instead of just modifying the value in "save_path" and "qBt-savepath"
import os
import bencode
import re

# MODIFY these 2 values to suite your needs
# Directory where your QBittorrent fastresume files are
tor_dir = "C:\\Users\\joem\\Desktop\\BT_backup\\"
# Start of linux file structure for torrents
linux_dir_start = "/data/"

# for each file in the directory that has the extension ".fastresume"
for file in os.listdir(tor_dir):
    if file.endswith(".fastresume"):
# set variable for each file name
        file_path_name = os.path.join(tor_dir, file)
# set variable for the contents of each fastresume file
        torrent = bencode.bread(file_path_name)
# set the variable for the original "save_path" value
        save_path_orig = (torrent['save_path'])
# Replace {x}:\ with linux_dir_start (ie "c:\" converts to "/data/"). triple esc backslash. Period = any drive letter. Carrot "^" indicates beginning of string.
        save_path1 = re.sub("^.:\\\\",linux_dir_start,save_path_orig)
# replace rest of the backslashes with forward slashes
        save_path2 = re.sub("\\\\", "/", save_path1)
# Replace value of dictionary item "save_path" with the linux equivalent
        torrent['save_path']=save_path2
# Replace value of dictionary item "qBt-savePath" with the linux equivalent
        torrent['qBt-savePath']=save_path2
# Write the modified dictionary back to the fastresume file
        bencode.bwrite(torrent, file_path_name)
# print the new torrent path
        print(torrent['save_path'])