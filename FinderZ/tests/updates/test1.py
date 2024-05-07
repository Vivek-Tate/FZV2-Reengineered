from FinderZV2 import GatherInfo
from FinderZV2 import fileOperands
from FinderZV2 import Synchronize
from FinderZV2 import Backup
from FinderZV2 import callBash

# amountFiles = GatherInfo.getAmountofComponentsinDir('D:\Sem2\SR-Test\Testing-FinderZ')
# print("Amount of files in dir: ",amountFiles)
#
# files = GatherInfo.getAllFileNamesinDir('D:\Sem2\SR-Test\Testing-FinderZ') #Replace /path/to/dir with a path to a directory.
# print("All file names in dir: ", files)

# #Just returns the list - useless function
# GatherInfo.expandListInfo(files)

#Returns the lines of a file in form of a list
# fileLines = GatherInfo.getFileLineContents('D:\Sem2\SR-Test\Testing-FinderZ/tp.txt')
# print(fileLines)

#Gets the number of lines in a file, will even return a blank line as a count
# lineAmount = GatherInfo.getFileLineAmount('D:\Sem2\SR-Test\Testing-FinderZ/tp.txt') #Replace /path/to/file with a path to a file.
# print(lineAmount)

#Run a bash script
# callBash.runFile("D:\Sem2\SR-Test\Testing-FinderZ/helloworld.bat")

# main_dir = r"D:\Sem2\SR-Test\Testing-FinderZ\New-test-dir"
# backup_dir = [r"D:\Sem2\SR-Test\Testing-FinderZ\backup_dir"]
# Backup.backup(main_dir, backup_dir)

# Backup.backup(r"D:\Sem2\SR-Test\Testing-FinderZ\New-test-dir", [r"D:\Sem2\SR-Test\Testing-FinderZ\backup_dir"])


