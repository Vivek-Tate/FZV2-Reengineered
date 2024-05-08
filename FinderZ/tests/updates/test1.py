from FinderZV2 import GatherInfo
from FinderZV2 import fileOperands
from FinderZV2 import Synchronize
from FinderZV2 import Backup
from FinderZV2 import callBash

files = GatherInfo.getAllFileNamesinDir('/Users/vivek/Developer/Python-Programming-Workspace/COM6523-Software-Reengineering/Assignment-2023-24-FinderZ') #Replace /path/to/dir with a path to a directory.
print(files)