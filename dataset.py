import os

def readFile(file_name):
    with open(file_name) as f:
        return f.read()

def readFilesInDirectory(dir_name):
    rv=dict()
    for file_name in os.listdir(dir_name):
        if not os.path.isdir(os.path.join(dir_name,file_name)):
            try:
                rv[file_name]=readFile(os.path.join(dir_name,file_name))
            except:
                pass
    return rv

def readDataSet(root_dir_name):
    rv=dict()
    for sub_dir_name in os.listdir(root_dir_name):
        dir_name=os.path.join(root_dir_name,sub_dir_name)
        if  os.path.isdir(dir_name):
            rv[sub_dir_name]=readFilesInDirectory(dir_name)
    return rv


def test():
    pass

if __name__=='__main__':
    test()
