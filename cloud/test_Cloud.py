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
    # client_0 = cloud.upload_files()
    # client_1 = cloud.upload_files()
    # client_2 = cloud.upload_files()

    # client_1.upload_file("abc", 1000)
    # client_2.upload_file("aaa", 10001)
    # client_2.upload_file("bbb", 20001)

    cloud.start_cloud()
    # client_1.upload_file("abc", 1000)
    # client_2.upload_file("aaa", 10001)

    # client_1.upload_file("abc", 1000)
    # for i in range(20):
    #     cloud.upload_file().upload_file("1", 2)
    # sleep(10)
    # print("sleep")
    #
    # client_1.upload_file("abc", 1000)
    # cloud.upload_file().upload_file("1", 2)


    for i in range(20):
        files_number = random.randint(1, 3)
        random_files = [random_file() for j in range(files_number)]
        print(random_files)
        cloud.upload_files(random_files)
        # print(i)

    sleep(5)
    # print("eee")
    for i in range(2):
        files_number = random.randint(1, 3)
        random_files = [random_file() for j in range(files_number)]
        print(random_files)
        cloud.upload_files(random_files)