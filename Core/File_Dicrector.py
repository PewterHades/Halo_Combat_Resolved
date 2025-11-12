from os.path import abspath, join, dirname
import sys



def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else: 
        return dirname(dirname(abspath(__file__)))

base_path = get_base_path()

def create_diretory(file_name):
    directory = join(base_path, *file_name)
    return directory