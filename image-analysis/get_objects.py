import os
import os.path
import subprocess
from PIL import Image
import glob
import tarfile
from shutil import copyfile
import shutil
from pathlib import Path
from zipfile import ZipFile
import tarfile

# please enter whole path of your darknet-directory:
darknet = 'C:\\Users\\hinri\\vcpkg_darknet\\darknet'

img_dir = 'sbbget\\sbbget_downloads\\extracted_images'
image_list = []
logFileName = 'ppn_log.txt'
version = 'yolo9000'


def get_filenames(d):
    g = open("C:/Users/hinri/vcpkg_darknet/darknet/images_files.txt", "w")
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            full_path2 = os.path.abspath(full_path)
            print(full_path2)
            g.write(full_path2 + "\n")


def get_objects():
    wdir = darknet
    command = 'darknet detector test cfg/combine9k.data cfg/yolo9000.cfg yolo9000.weights < ' \
              'images_files.txt -dont_show -out result.json'
    # other parameters and version, for dev or trying
    # command = 'darknet detector test cfg/combine9k.data cfg/yolo9000.cfg yolo9000.weights
    # < images_files.txt -dont_show -predictions'
    # yolov4
    # command = 'darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights
    # < images_files.txt -dont_show -out result.json'
    subprocess.call(command, shell=True, cwd=wdir)
    os.remove(darknet + '\\images_files.txt')


def save_results(ppn):
    src = darknet + '\\result.json'
    dst = r'image-analysis/results/' + version + '/' + ppn + '_objects.json'
    print('dst = ' + dst)
    copyfile(src, dst)
    os.remove(src)


def extract_files(directory_tars):
    my_tar = tarfile.open(directory_tars)
    my_tar.extractall(path='opened_tars')


def remove_jpg(ppn):
    d = 'opened_tars/sbbget_downloads/extracted_images/' + ppn
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            os.remove(full_path)
    os.rmdir(d)


with open(logFileName, 'r') as log_file:
    log_entries = log_file.readlines()
    print(log_entries)


for subdir, dirs, files in os.walk(img_dir):
    print(subdir)
    for file in files:
        file_name = os.path.join(subdir, file)
        if file_name.endswith('tar'):
            current_ppn = Path(os.path.join(subdir, file)).stem
            if current_ppn not in log_entries:
                extract_files(file_name)
                directory = 'opened_tars/sbbget_downloads/extracted_images/' + current_ppn
                get_filenames(directory)
                get_objects()
                save_results(current_ppn)
                remove_jpg(current_ppn)
                with open(logFileName, 'a') as log_file:
                    log_file.write(current_ppn + "\n")
