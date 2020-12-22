from unittest import TestCase
from Cloud import Cloud
from Client import Client
from File import File


class TestCloud(TestCase):
    def setUp(self):
        self.cloud = Cloud()

    def test(self):
        self.assertTrue(True)
