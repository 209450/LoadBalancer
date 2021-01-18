import random
from unittest import TestCase
from cloud.Cloud import Cloud

from cloud.Client import Client
from time import sleep
import threading

from cloud.File import File

names = "abcdef"


def random_file():
    name = names[random.randint(0, len(names) - 1)]
    size = random.randint(0, 10000)
    return File(name, size)


if __name__ == '__main__':
    cloud = Cloud()
    cloud.start()

    for i in range(2):
        files_number = random.randint(1, 3)
        random_files = [random_file() for j in range(files_number)]
        print(random_files)
        cloud.upload_files(random_files)
        # print(i)
    #
    # cloud.upload_files([File('a', 3000), File('a', 4000)])
    # cloud.upload_files([File('a', 1000), File('b', 1000), File('c', 1000), File('d', 1000), File('a', 1000), File('a', 1000)])

    # sleep(5)
    # # print("eee")
    # for i in range(2):
    #     files_number = random.randint(1, 3)
    #     random_files = [random_file() for j in range(files_number)]
    #     print(random_files)
    #     cloud.upload_files(random_files)

