import os
from shutil import rmtree


class folder_management():
    def __init__(self, path):
        self.path=path

    def folder(self):
        try:
            os.makedirs(self.path)
        except:
            rmtree(self.path)
            os.makedirs(self.path)