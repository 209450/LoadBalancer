import random
from unittest import TestCase
from cloud.Cloud import Cloud

from cloud.Client import Client
from time import sleep
import threading

from cloud.File import File

names = "abcdef"


def random_files(min_files, max_files, min_size, max_size):
    files_number = random.randint(min_files, max_files)

    files = []
    for i in range(files_number):
        name = names[random.randint(0, len(names) - 1)]
        size = random.randint(min_size, max_size)
        files.append(File(name, size))

    return files


if __name__ == '__main__':
    cloud = Cloud()
    cloud.start()

    # # 25 random
    # for i in range(25):
    #     files = random_files(1, 3, 1000, 10000)
    #     print(files)
    #     cloud.upload_files(files)
    #     # print(i)

    # # 50 small, 1 big
    # for i in range(1):
    #     files = random_files(50, 50, 1000, 10000)
    #     print(files)
    #     cloud.upload_files(files)
    #     # print(i)
    #
    # for i in range(1):
    #     files = random_files(1, 1, 100000, 100000)
    #     print(files)
    #     cloud.upload_files(files)
    #     # print(i)

    # # 25 small, 25 big
    # for i in range(25):
    #     files = random_files(10, 10, 1000, 5000)
    #     print(files)
    #     cloud.upload_files(files)
    #     # print(i)
    #
    # # 25 random
    # for i in range(25):
    #     files = random_files(10, 10, 10000, 20000)
    #     print(files)
    #     cloud.upload_files(files)
    #     # print(i)