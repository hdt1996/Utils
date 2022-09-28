from .directory import TEST_LOC, PROJ_DIR, LOG_DIR
import os

class Development():
    def __init__(self):
        self.proj_test_dir = None
        self.proj_dir = PROJ_DIR
        self.log_dir = LOG_DIR
        self.debug = True
    def makeTestDir(self, proj_name: str = None):
        if proj_name != None:
            self.proj_test_dir = os.path.join(TEST_LOC, proj_name)
            os.makedirs(self.proj_test_dir,exist_ok = True)


        
