from FinderZV2 import GatherInfo
from FinderZV2 import fileOperands
from FinderZV2 import Synchronize
from FinderZV2 import Backup
from FinderZV2 import callBash

files = GatherInfo.getAllFileNamesinDir('D:\Sem2\SR-Test\Testing-FinderZ') #Replace /path/to/dir with a path to a directory. 
print(files)