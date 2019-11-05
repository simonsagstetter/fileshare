import sys

from libary.models import Folder

def get_folder_size(instances):
    real_size = sys.getsizeof(instances)
    return real_size
