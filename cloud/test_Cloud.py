from unittest import TestCase
from cloud.Cloud import Cloud

from cloud.Client import Client
from time import sleep
import threading

if __name__ == '__main__':
    cloud = Cloud()
    client_0 = cloud.add_client()
    client_1 = cloud.add_client()
    client_2 = cloud.add_client()

    # client_1.upload_file("abc", 1000)
    # client_2.upload_file("aaa", 10001)
    # client_2.upload_file("bbb", 20001)

    cloud.start_cloud()
    # client_1.upload_file("abc", 1000)
    # client_2.upload_file("aaa", 10001)

    client_1.upload_file("abc", 1000)
    for i in range(20):
        cloud.add_client().upload_file("1",2)
    sleep(10)
    print("sleep")
    client_1.upload_file("abc", 1000)
    cloud.add_client().upload_file("1", 2)