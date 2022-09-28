import os

ROOT = 'C:\\Users\\hduon\\Documents\\'
TEST_LOC = os.path.join(ROOT, 'Tests')
PROJ_DIR = os.path.join(ROOT, 'Enzyme\\configurator')
LOG_DIR = os.path.join(ROOT, 'Logs')


for dir in [TEST_LOC, PROJ_DIR, LOG_DIR]:
    os.makedirs(name = dir, exist_ok=True)