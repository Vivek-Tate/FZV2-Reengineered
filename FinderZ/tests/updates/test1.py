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


#files = GatherInfo.getAllFileNamesinDir('/Users/vivek/Developer/Python-Programming-Workspace/COM6523-Software-Reengineering/Assignment-2023-24-FinderZ') #Replace /path/to/dir with a path to a directory.
#print(files)

files = GatherInfo.isEmptyDir('C:/Users/kavik/PycharmProjects/grp-project/group-project-pgt04/FinderZ/tests/Testing-FinderZ')
print(files)

actual_output = GatherInfo.computeHash('C:/Users/kavik/PycharmProjects/grp-project/group-project-pgt04/FinderZ/tests/Testing-FinderZ/Now.txt')
print(actual_output)

list1 = 'tp.txt'
list2 = 'Now.txt'
actual_output = GatherInfo.isOneInCommon(list1, list2)
print(actual_output)

directories, files = GatherInfo.readDir('C:/Users/kavik/PycharmProjects/grp-project/group-project-pgt04/FinderZ/tests/Testing-FinderZ')
print(files, directories)

actual_file = GatherInfo.getTotalInfo('C:/Users/kavik/PycharmProjects/grp-project/group-project-pgt04/FinderZ/tests/Testing-FinderZ/Now.txt', 'int', recursive=True)
print(actual_file)

file1 = 'C:/Users/kavik/PycharmProjects/grp-project/group-project-pgt04/FinderZ/tests/Testing-FinderZ/Now.txt'
file2 = 'C:/Users/kavik/PycharmProjects/grp-project/group-project-pgt04/FinderZ/tests/Testing-FinderZ/tp.txt'
difference = GatherInfo.compareFiles(file1, file2)
print(difference)