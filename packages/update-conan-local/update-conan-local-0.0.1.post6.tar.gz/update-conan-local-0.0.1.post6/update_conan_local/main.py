import os
import sys
import json
from collections import OrderedDict

# Updates header and binary files to local conan cache

def getjson(fn):
    try:
        with open(fn) as f:
            return json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError as ex:
        print("<<== "+fn+" not found. " + ex.strerror)
    except json.decoder.JSONDecodeError as ex:
        print("<<== json error in "+fn)

def find(path, name):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def find_cache(sourcePath = None):
    result = ''

    print(sourcePath)
    
    current_path = os.getcwd()
    if (sourcePath != None and os.path.isdir(sourcePath)):
        current_path = sourcePath

    conanfile_path = current_path

    parent_path = os.path.join(current_path, '..')
    conanfile_py = 'conanfile.py'
    if os.path.isfile(os.path.join(current_path, conanfile_py)):
        conanfile_path = current_path
    if os.path.isfile(os.path.join(parent_path, conanfile_py)):
        conanfile_path = parent_path

    build_path = os.path.join(conanfile_path, 'build')

    if os.path.isdir(build_path) == False:
        print(f'{build_path} is not found.')
        return result




    graph_info = getjson(os.path.join(build_path, 'graph_info.json'))
    root_name = graph_info['root']['name']
    root_version = graph_info['root']['version']
    name_version = f'{root_name}/{root_version}'


    conan_search_file = os.path.join(build_path, 'conan_search.txt')
    os.system(f'conan search {name_version} > {conan_search_file}')

    if os.path.isfile(conan_search_file) == False:
        print(f'{conan_search_file} is not found.')
        return result

    f = open(conan_search_file, "r")
    conan_search = f.readlines()
    f.close()

    package_name = ''
    for line in conan_search: 
        print(line)
        if line.startswith(name_version):
            package_name = line.strip('\n')

    if (len(package_name) == 0):
        print(f'{name_version} package not found')
        return result

    user_channel_split = package_name.split('@')[1].split('/')
    user, channel = user_channel_split


    user_profile = os.getenv('USERPROFILE')
    if (user_profile == None):
        user_profile = '~'


    conan_main = os.path.join(user_profile, '.conan', 'data', root_name, root_version, user, channel)

    if (os.path.isdir(conan_main) == False):
        print(f'{conan_main} is not found.')

    conan_main_package = os.path.join(conan_main, 'package')
    print(conan_main_package)


    conan_link_file = find(conan_main_package, '.conan_link')
    if (conan_link_file == None):
        print('conan_link is not found.')
        return result

    f = open(conan_link_file, "r")
    conan_link = f.read().strip('\n')
    f.close()

    result = conan_link
    return result


if __name__ == "__main__":

    current_path = os.path.dirname(os.path.realpath(__file__))
    
    if (len(sys.argv) >= 2):
        current_path = sys.argv[1]
    
    print(current_path)

    conan_link = find_cache(current_path)
    print(conan_link)
    
    conan_link_bin = os.path.join(conan_link, 'bin')
    conan_link_lib = os.path.join(conan_link, 'lib')













