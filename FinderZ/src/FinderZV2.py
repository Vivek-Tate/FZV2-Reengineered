#!/usr/bin/env python3

import os
import shutil
import time
import subprocess
import hashlib
import re
import zipfile
import random


class GatherInfo:
    # For finding files with that keyword and displaying how many there are:
    def getResultsAmount(appendedList):
        valueAmount = int(len(appendedList))
        return valueAmount

    # Find the amount of files in a directory:
    def getAmountofComponentsinDir(directory, returnAmountFiles=True, returnAmountDirectories=True):
        directories, files = GatherInfo.readDir(directory)
        # Get each amount:
        count_directories = len(directories)
        count_files = len(files)
        if not returnAmountFiles and returnAmountFiles:
            return count_directories
        elif returnAmountFiles and not returnAmountDirectories:
            return count_files
        else:
            return count_directories, count_files

    # List all file names in a directory:
    def getAllFileNamesinDir(mainDir):
        try:
            filenames = os.listdir(mainDir)
            return filenames
        except FileNotFoundError:
            print(f"Directory '{mainDir}' not found.")
            return []
        except PermissionError:
            print(f"No permission to access directory '{mainDir}'.")
            return []

    # Used for display purposes:
    def expandListInfo(list):
        amountData = len(list)
        iterator = int(0)
        for i in range(amountData):
            placeHolder = str(list[iterator])
            print(placeHolder + "\n")
            iterator += 1

    # Get contents of file:
    def getFileLineContents(filePath, returnStringType=False):
        try:
            with open(filePath, 'r') as file:
                if not returnStringType:
                    lines = file.readlines()
                else:
                    lines = file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError("ERR: The file could not be found.")
        except PermissionError:
            raise PermissionError("ERR: Permission denied to open the file.")
        except Exception as e:
            raise Exception(f"ERR: An error occured while opening the file: {str(e)}")
        return lines

    # Get tile line amount
    ##Modified the method to not accept a blank line as a count
    def getFileLineAmount(file_path):
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines()]
                amount_of_lines = sum(1 for line in lines if line)
                return amount_of_lines
        except FileNotFoundError:
            print("File not found", file_path)
            return -1

    # New in V2:
    # New function in V2:
    def isEmptyDir(directory):
        directories, files = GatherInfo.readDir(directory)
        return len(directories) == 0 and len(files) == 0

    # New in V2:
    def computeHash(path):
        try:
            with open(path, 'rb') as file:
                h = hashlib.sha1()
                for chunk in iter(lambda: file.read(1024), b''):
                    h.update(chunk)
                return h.hexdigest() if os.path.getsize(path) > 0 else False
        except:
            return False

    # New in V2: Comparing two lists for at least one common element:
    def isOneInCommon(list1, list2):
        return any(x == y for x in list1 for y in list2)

    def readDir(directory, return_files=True, return_directories=True):
        all_files = GatherInfo.getAllFileNamesinDir(directory)
        directories = [file for file in all_files if os.path.isdir(os.path.join(directory, file))]
        files = [file for file in all_files if not os.path.isdir(os.path.join(directory, file))]

        return (directories, []) if not return_files else (
            [] if not return_directories else (directories, [])) if not return_directories else (
            [], files) if not return_files else (directories, files)

    def isRegexAndStringMatching(pattern, string, exactMatch=False):
        matched = False
        # Regex goes in here:
        regexp = re.compile(r'%s' % pattern)
        # Check if exactMatch is set to True:
        if exactMatch == True:
            # If exactMatch is True, check if the string exactly matches the pattern.
            if regexp.fullmatch(string):
                matched = True
        else:
            # If exactMatch is not set to True, search if the string contains the pattern.
            if regexp.search(string):
                matched = True
        return matched

    # Get total amount of lines recusrively in a directory, and optionally even files.
    def getTotalInfo(path, return_file_amount=False, extension_filters=[], recursive=False):
        total_amount = file_amount = 0

        def process_file(file_path):
            nonlocal total_amount, file_amount
            try:
                total_amount += GatherInfo.getFileLineAmount(file_path)
                file_amount += 1
            except UnicodeDecodeError:
                pass

        def matches_extension(file):
            return any(file.endswith(extension) for extension in extension_filters)

        for folder, _, files in os.walk(path) if recursive else [
            (path, None, GatherInfo.readDir(path))]:
            for file in files:
                if not extension_filters or matches_extension(file):
                    process_file(os.path.join(folder, file))

        return (total_amount, file_amount) if return_file_amount else total_amount

    # New in 2.0.4
    def compareFiles(file1, file2, comparison_output_file=''):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            differences = [f"\nLine {i + 1}:\nFile1: {line1} File2: {line2}\n" for i, (line1, line2) in
                           enumerate(zip(f1, f2)) if line1 != line2]

        if comparison_output_file:
            with open(comparison_output_file, 'w') as f:
                f.writelines(differences)

        return differences

    # New functions (GatherInfo):
    def wordCount(string):
        return len(string.split())

    def charCount(string):
        return len(string)

    def byteCount(filePath):
        return os.path.getsize(filePath)

    def getFileStats(filePath):
        try:
            f = open(filePath)
            stringed_contents = f.read()
        except:
            raise Exception("ERR: The file could not be opened/decoded.")

        stats = {'Word Count': 0, 'Char Count': 0, 'Byte Count': 0, 'Line Count': 0}

        # word count:
        stats["Word Count"] = (GatherInfo.wordCount(stringed_contents))

        # char count:
        stats["Char Count"] = (GatherInfo.charCount(stringed_contents))

        # byte count:
        stats["Byte Count"] = (GatherInfo.byteCount(filePath))

        # line count:
        stats["Line Count"] = (GatherInfo.getFileLineAmount(filePath))

        return stats

    # New in V2.1.2: (These functions below are all new in V 2.1.2)
    def isHiddenFile(file_path):
        file_name = os.path.basename(file_path)
        if file_name.startswith('.'):
            return True
        else:
            return False

    def getAllHiddenFilesInDir(directory):
        hiddenFiles = []
        files = GatherInfo.readDir(directory, returnDirectories=False)
        for file in files:
            filePath = os.path.join(directory, file)
            if GatherInfo.isHiddenFile(filePath):
                hiddenFiles.append(filePath)
        return hiddenFiles

    # Function that returns the amount of each file extension within a directory (either recursively or not):
    def getAmountOfEachFileTypeInDir(directory, recursive=False):
        counter = 0
        # The two main lists that will be concatenated and put into a dictionary:
        extensions = []
        amounts = []
        for root, dirs, files in os.walk(directory):
            if recursive == False and counter != 0:
                break
            # First, get the total amount of extensions:
            for file in files:
                extension = os.path.splitext(file)[1]
                if extension not in extensions:
                    # Append the extension to the list:
                    extensions.append(extension)
            counter += 1
        # Second, get the amount of each extension once the extensions list is complete:
        for i in range(len(extensions)):
            extension_amount_counter = 0
            counter = 0
            for root, dirs, files in os.walk(directory):
                if recursive == False and counter != 0:
                    break
                # First, get the total amount of extensions:
                for file in files:
                    extension = os.path.splitext(file)[1]
                    if extension == extensions[i]:
                        extension_amount_counter += 1

                counter += 1
            # Append the amount to the amounts list:
            amounts.append(extension_amount_counter)
        # Here, create the dictionary:
        extensions = [x for _, x in sorted(zip(amounts, extensions), reverse=True)]
        amounts = sorted(amounts, reverse=True)
        # Create the dictionary:
        extensions_dict = {}
        for i in range(len(extensions)):
            extensions_dict[extensions[i]] = amounts[i]
        return extensions_dict


class FileUtils:
    @staticmethod
    def get_matching_files(fileName, files, regex=False, exactSearch=False):
        matching_files = []
        for file in files:
            if regex:
                if GatherInfo.isRegexAndStringMatching(fileName, file, exactMatch=exactSearch):
                    matching_files.append(file)
            else:
                if (exactSearch and fileName == file) or (not exactSearch and fileName in file):
                    matching_files.append(file)
        return matching_files

    @staticmethod
    def get_files_with_extension(files, extensionFilters):
        if not extensionFilters:
            return files
        return [file for file in files if any(file.endswith(ext) for ext in extensionFilters)]

    @staticmethod
    def process_files_in_dir(path, recursive, process_func):
        for root, _, files in os.walk(path):
            process_func(root, files)
            if not recursive:
                break


class fileOperands:
    @staticmethod
    def findFiles(fileName, path, exactSearch=False, recursive=False, regex=False):
        results = []

        def process_func(root, files):
            matching_files = FileUtils.get_matching_files(fileName, files, regex, exactSearch)
            for file in matching_files:
                results.append(os.path.join(root, file))

        FileUtils.process_files_in_dir(path, recursive, process_func)
        return results

    @staticmethod
    def scanFilesForContent(contentKeyWord, path, extensionFilters=[], recursive=False, regex=False):
        results = []

        def process_func(root, files):
            filtered_files = FileUtils.get_files_with_extension(files, extensionFilters)
            for file in filtered_files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if (regex and GatherInfo.isRegexAndStringMatching(contentKeyWord, line)) or (
                                    contentKeyWord in line):
                                results.append(file_path)
                                break
                except:
                    pass

        FileUtils.process_files_in_dir(path, recursive, process_func)
        return results

    @staticmethod
    def removeFiles(fileName, path, exactSearch=False, extensionFilters=[], recursive=False, regex=False):
        results = []

        def process_func(root, files):
            filtered_files = FileUtils.get_files_with_extension(files, extensionFilters)
            matching_files = FileUtils.get_matching_files(fileName, filtered_files, regex, exactSearch)
            for file in matching_files:
                file_path = os.path.join(root, file)
                results.append(file_path)
                print(f"\n File Found at:\n{file_path}")
                if int(input("\nYou are about to delete this file. Continue? ((1) Yes / (2) No): ")) == 1:
                    os.remove(file_path)
                    print("\nRemoved 1 File")

        FileUtils.process_files_in_dir(path, recursive, process_func)
        if results:
            print(f"\nAll selected files with keyword '{fileName}' successfully removed.")
        else:
            print(f"\nNo files removed or found with the keyword '{fileName}'")

    @staticmethod
    def createFiles(createAmount, keyWord, extensionType, path, firstFileStartsAtOne=False):
        originalDir = os.getcwd()
        os.chdir(path)
        for i in range(createAmount):
            numExtension = str(i + 1) if firstFileStartsAtOne or i > 0 else ''
            file_name = f"{keyWord}{numExtension}{extensionType}"
            with open(file_name, 'w'):
                pass
        os.chdir(originalDir)

    @staticmethod
    def findAndReplaceInFiles(keyWord, replacementKeyword, path, recursive=True):
        def process_func(root, files):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                    new_lines = [line.replace(keyWord, replacementKeyword) for line in lines]
                    if lines != new_lines:
                        with open(file_path, 'w') as f:
                            f.writelines(new_lines)
                except:
                    pass

        FileUtils.process_files_in_dir(path, recursive, process_func)

    @staticmethod
    def mergeClassFolders(parentClassPath, mergeDestination, removeOriginal=False):
        directories, _ = GatherInfo.readDir(parentClassPath)
        for directory in directories:
            directory_path = os.path.join(parentClassPath, directory)
            _, files = GatherInfo.readDir(directory_path)
            for file in files:
                source_path = os.path.join(directory_path, file)
                if removeOriginal:
                    shutil.move(source_path, mergeDestination)
                else:
                    shutil.copy(source_path, mergeDestination)

    @staticmethod
    def moveFile(originalFileDir, newFileDir):
        shutil.move(originalFileDir, newFileDir)

    @staticmethod
    def copyFile(originalFileDir, newFileDir):
        shutil.copy(originalFileDir, newFileDir)

    @staticmethod
    def moveDir(originalDir, newDir):
        shutil.move(originalDir, newDir)

    @staticmethod
    def copyDir(originalDir, newDir):
        shutil.copytree(originalDir, os.path.join(newDir, os.path.basename(originalDir)))

    @staticmethod
    def renameFile(newName, filePath):
        os.rename(filePath, os.path.join(os.path.dirname(filePath), newName))

    @staticmethod
    def renameDirectory(newName, directoryPath):
        os.rename(directoryPath, os.path.join(os.path.dirname(directoryPath), newName))

    @staticmethod
    def createFile(fileName, path):
        with open(os.path.join(path, fileName), 'w'):
            pass

    @staticmethod
    def removeFile(filePath):
        os.remove(filePath)

    @staticmethod
    def removeAllFilesInDir(directory, removeDirectories=False):
        directories, files = GatherInfo.readDir(directory)
        for file in files:
            os.remove(os.path.join(directory, file))
        if removeDirectories:
            for directory in directories:
                shutil.rmtree(os.path.join(directory, directory))

    @staticmethod
    def xor_encrypt_file(file_path, key, removeOriginal=False):
        hashed_key = hashlib.sha256(str(key).encode()).digest()[0]
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = bytearray(b ^ hashed_key for b in data)
        enc_file_path = file_path + '.enc'
        with open(enc_file_path, 'wb') as f:
            f.write(encrypted_data)
        if removeOriginal:
            os.remove(file_path)

    @staticmethod
    def xor_decrypt_file(enc_file_path, key, removeEncrypted=False):
        hashed_key = hashlib.sha256(str(key).encode()).digest()[0]
        with open(enc_file_path, 'rb') as f:
            data = f.read()
        decrypted_data = bytearray(b ^ hashed_key for b in data)
        file_path = enc_file_path.replace('.enc', '')
        with open(file_path, 'wb') as f:
            f.write(decrypted_data)
        if removeEncrypted:
            os.remove(enc_file_path)

    @staticmethod
    def xor_encrypt_files(directory, key, removeOriginal=False, recursive=False):
        def process_func(root, files):
            for file in files:
                file_path = os.path.join(root, file)
                fileOperands.xor_encrypt_file(file_path, key, removeOriginal)

        FileUtils.process_files_in_dir(directory, recursive, process_func)

    @staticmethod
    def xor_decrypt_files(directory, key, removeEncrypted=False, recursive=False):
        def process_func(root, files):
            for file in files:
                if file.endswith('.enc'):
                    file_path = os.path.join(root, file)
                    fileOperands.xor_decrypt_file(file_path, key, removeEncrypted)

        FileUtils.process_files_in_dir(directory, recursive, process_func)

    @staticmethod
    def removeEncFiles(directory, recursive=False):
        def process_func(root, files):
            for file in files:
                if file.endswith('.enc'):
                    os.remove(os.path.join(root, file))

        FileUtils.process_files_in_dir(directory, recursive, process_func)

    @staticmethod
    def calculateFileSize(filePath):
        return os.path.getsize(filePath)

    @staticmethod
    def calculateDirectorySize(directory):
        total_size = 0
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    @staticmethod
    def backupFiles(files, backupDir):
        if not os.path.exists(backupDir):
            os.makedirs(backupDir)
        for file in files:
            shutil.copy(file, backupDir)

    @staticmethod
    def restoreFiles(backupDir, restoreDir):
        if not os.path.exists(backupDir):
            raise Exception(f"Backup directory {backupDir} does not exist")
        if not os.path.exists(restoreDir):
            os.makedirs(restoreDir)
        for file in os.listdir(backupDir):
            shutil.copy(os.path.join(backupDir, file), restoreDir)

    @staticmethod
    def compressFiles(files, zipName):
        with zipfile.ZipFile(zipName, 'w') as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))

    @staticmethod
    def decompressFiles(zipFilePath, extractDir):
        with zipfile.ZipFile(zipFilePath, 'r') as zipf:
            zipf.extractall(extractDir)


# The main logging class (Used in Synchronize and Backup classes)
def writeLogsToFile(creationPath, fileLines, mode):
    currentTime = time.strftime("%Y-%m-%d_%H-%M-%S")
    logFileName = f"LogRun({mode})__{currentTime}.txt"
    filePath = os.path.join(creationPath, logFileName)

    with open(filePath, 'a') as f:
        f.writelines(fileLines)


class Logging:
    @staticmethod
    def Log(loggingBool, logList, announcement='', dir1='', dir2='', dir1Action='', dir2Action='', logTag='NC',
            log_non_critical=True):
        if not loggingBool:
            return logList

        currentTime = time.ctime()
        newLogList = logList.copy()

        def printAnnouncement(announcement, currentTime):
            if announcement:
                log = f"\n\n[{logTag}] CURRENT/MAIN ACTIVITY:\n{currentTime}: {announcement}\n"
                print(log)
                newLogList.append(log)

        def logDirectories(dir1, dir2, dir1Action, dir2Action, currentTime):
            if dir1 and not dir2:
                log = f"\n\t{currentTime}: SUBPROCESS: {dir1Action} {dir1}"
            elif not dir1 and dir2:
                log = f"\n\t{currentTime}: SUBPROCESS: {dir2Action} {dir2}"
            elif dir1 and dir2:
                log = f"\n\t{currentTime}: SUBPROCESS: {dir1Action} {dir1} {dir2Action} {dir2}"
            else:
                log = ""

            if log:
                print(log)
                newLogList.append(log)

        if log_non_critical or logTag != 'NC':
            printAnnouncement(announcement, currentTime)
            logDirectories(dir1, dir2, dir1Action, dir2Action, currentTime)

        return newLogList


# Main Synchronize class:
class Synchronize:
    def backUpToSyncFolder(filePath, syncBackUpFolderName, maindir, syncdir):

        # This function returns a path, with an ending including the syncBackUpFolderName:
        def getSyncBackUpFolderPath(maindir, syncdir, syncBackUpFolderName):

            # Join the two paths:
            syncBackUpFolderPathMain = os.path.join(maindir, f"{syncBackUpFolderName}")

            syncBackUpFolderPathSync = os.path.join(syncdir, f"{syncBackUpFolderName}")
            return syncBackUpFolderPathMain, syncBackUpFolderPathSync

        # Check whether or not the filePath is in the syncBackUpFolder. If it is, dont execute it:
        if syncBackUpFolderName in filePath:
            return False
        # Step 1: retreive the syncBackUpFolderPath
        syncBackUpFolderPathMain, syncBackUpFolderPathSync = getSyncBackUpFolderPath(maindir, syncdir,
                                                                                     syncBackUpFolderName)

        # Once we have the syncBackUpFolderPath, we can then, copy the file or directory within the parametric filePath variable, and move it to the syncBackUpFolderPath.
        singleComponent = os.path.split(filePath)[1]

        isExistingInSyncBackUpFolderDirectory_Main = os.path.join(syncBackUpFolderPathMain, singleComponent)
        isExistingInSyncBackUpFolderDirectory_Sync = os.path.join(syncBackUpFolderPathSync, singleComponent)

        # If the path leads to a file:
        if os.path.isfile(filePath):
            # Here, check whether or not the file already exists within the syncBackUpFolderPath:

            # Main Path:
            if os.path.exists(isExistingInSyncBackUpFolderDirectory_Main):
                os.remove(isExistingInSyncBackUpFolderDirectory_Main)

            fileOperands.copyFile(filePath, syncBackUpFolderPathMain)

            # Sync Path:
            if os.path.exists(isExistingInSyncBackUpFolderDirectory_Sync):
                os.remove(isExistingInSyncBackUpFolderDirectory_Sync)

            fileOperands.copyFile(filePath, syncBackUpFolderPathSync)

        # If the path leads to a directory:
        if os.path.isdir(filePath):
            # Here, check whether the directory already exists within the syncBackUpFolderPath:

            # Main path:
            if os.path.exists(isExistingInSyncBackUpFolderDirectory_Main):
                shutil.rmtree(isExistingInSyncBackUpFolderDirectory_Main)
            fileOperands.copyDir(filePath, syncBackUpFolderPathMain)

            # Sync path:
            if os.path.exists(isExistingInSyncBackUpFolderDirectory_Sync):
                shutil.rmtree(isExistingInSyncBackUpFolderDirectory_Sync)
            fileOperands.copyDir(filePath, syncBackUpFolderPathSync)

    # IMPORTANT: Important files flag is used to never delete certain files that start with a specific character (
    # default = _ ). The importantFilesFlag is important as it may prevent deletion of files/dirs!
    def synchronizeComponents(dir1, dir2, syncBackUpFolderName, syncBackUpFolderExists, importantFilesFlag, loggingBool,
                              maindir, syncdir, log_non_critical=True):

        logList = []

        # Checks whether or not the directory or file is important by checking the first character of the string:
        def isImportantFile(directory, importantFilesFlag):

            directory = os.path.basename(os.path.normpath(directory))
            # Get first character and check if it equals importFilesFlag:
            if directory[0] == importantFilesFlag:
                return True
            else:
                return False

        # The two very important functions: merge
        def mergeDirectories(parentdir, parentdir2, parentdirs, parent2dirs):
            # For parentdir:
            parentdirHashes = []

            # For parentdir2:
            parentdir2Hashes = []

            # First, iterate through parentdir files:
            if len(parentdirs) != 0:
                for directory in parentdirs:
                    fullpath = os.path.join(parentdir, directory)
                    for folder, dirs, files in os.walk(fullpath):
                        os.chdir(folder)
                        if len(files) != 0:
                            for file in files:
                                Hash = GatherInfo.computeHash(file)
                                if Hash == False:
                                    pass
                                else:
                                    parentdirHashes.append(Hash)

            # Second, iterate through parentdir2 files:
            if len(parent2dirs) != 0:
                for directory in parent2dirs:
                    fullpath = os.path.join(parentdir2, directory)
                    for folder, dirs, files in os.walk(fullpath):
                        os.chdir(folder)
                        if len(files) != 0:
                            for file in files:
                                Hash = GatherInfo.computeHash(file)
                                if Hash == False:
                                    pass
                                else:
                                    parentdir2Hashes.append(Hash)
            matchBoolean = GatherInfo.isOneInCommon(parentdirHashes, parentdir2Hashes)

            return matchBoolean

        # The main merge function: Merges the important files and directories together in order to avoid loss of files. Worst case scenario, the deleted files will end up in the syncBackups folder:
        def mergeFiles(parentdir, parentdir2, parentfiles, parent2files):
            # For parentdir:
            parentdirHashes = []

            # For parentdir2:
            parentdir2Hashes = []

            # First, iterate through parentdir files:
            if len(parentfiles) != 0:
                for file in parentfiles:
                    fullpath = os.path.join(parentdir, file)
                    Hash = GatherInfo.computeHash(fullpath)
                    if Hash == False:
                        pass
                    else:
                        parentdirHashes.append(Hash)

            # Second, iterate through parentdir2 files:
            if len(parent2files) != 0:
                for file in parent2files:
                    fullpath = os.path.join(parentdir2, file)
                    Hash = GatherInfo.computeHash(fullpath)  # Problem lies here:
                    if Hash == False:
                        pass
                    else:
                        parentdir2Hashes.append(Hash)

            # Now, for the comparison:
            matchBoolean = GatherInfo.isOneInCommon(parentdirHashes, parentdir2Hashes)

            return matchBoolean

        # Take in both the parentfiles lists to get the files in each directory. For each of those, create a list with the computed hashes. IF any of those hashes matches any other hash from the other files listed... else...
        # We can return a boolean. True = mathing. False = not matching. Based on this boolean, we can then execute either deleting or merging.

        # Main class that takes in dir1, dir2, separates the files and dirs, makes the comparisons, and adds/removes the files, or even renames directories.
        def main(parentdir, parentdir2, syncBackUpFolderName, syncBackUpFolderExists, importantFilesFlag, loggingBool,
                 maindir, syncdir, log_non_critical=log_non_critical):

            logList = []
            # Get the source components of the parentdir and parentdir2:
            parentdirs, parentfiles = GatherInfo.readDir(parentdir)
            parent2dirs, parent2files = GatherInfo.readDir(parentdir2)

            # First, do the basic operations:

            # To add files:
            for directory in parentdirs:
                if directory not in parent2dirs:
                    newLogList = Logging.Log(loggingBool, logList,
                                             announcement=f"Adding directories that exist in mainpath but not in syncpath (missing/extra).",
                                             dir1=f"'{directory}'", dir2=parentdir2, dir1Action='Found directory',
                                             dir2Action=f'in {parentdir}, but not in', logTag="C",
                                             log_non_critical=log_non_critical)
                    logList.extend(newLogList)
                    # If the directory is not in the folder to sync to, then it adds it:
                    path = os.path.join(parentdir2, directory)
                    os.mkdir(path)
            for file in parentfiles:
                # If the file is not in the folder to sync to, then it adds it
                if file not in parent2files:
                    originalpath = os.path.join(parentdir, file)

                    newLogList = Logging.Log(loggingBool, logList,
                                             announcement=f"Adding files that exist in mainpath but not in syncpath (missing/extra).",
                                             dir1=f"'{file}'", dir2=parentdir2, dir1Action='Found file',
                                             dir2Action=f'in {parentdir}, but not in', logTag='C',
                                             log_non_critical=log_non_critical)
                    logList.extend(newLogList)
                    fileOperands.copyFile(originalpath, parentdir2)

            # Second, do the hard operations (Merging, replacing with newer versions, important files/dirs)

            # Pop out the syncBackUps folder name as to not remove any files or folders from there, if the syncBackUpsFolderExists, of course:
            if syncBackUpFolderExists:
                if syncBackUpFolderName in parentdirs:
                    parentdirs.pop(parentdirs.index(syncBackUpFolderName))
                if syncBackUpFolderName in parent2dirs:
                    parent2dirs.pop(parent2dirs.index(syncBackUpFolderName))

            # To deal with removing files:
            for file in parent2files:
                if file not in parentfiles:

                    # Log it:
                    newLogList = Logging.Log(loggingBool, logList, announcement=f"Removing additional files:",
                                             dir1=os.path.join(parentdir2, file),
                                             dir2=f'Removing file from {parentdir}', dir1Action='File found at ',
                                             dir2Action=f'but not found in {parentdir}', logTag='C',
                                             log_non_critical=log_non_critical)
                    logList.extend(newLogList)
                    isMatching = mergeFiles(parentdir, parentdir2, parentfiles, parent2files)

                    directory = os.path.join(parentdir2, file)

                    if isMatching == True or len(parentfiles) < 1:

                        newLogList = Logging.Log(loggingBool, logList,
                                                 announcement="Skipping file and directory merging as some files/dirs are matching.",
                                                 logTag='C', log_non_critical=log_non_critical)
                        logList.extend(newLogList)
                        # Check if the files are important files. If they are, do not remove them, but rather copy them to the parent directory:
                        if isImportantFile(directory, importantFilesFlag) == True:
                            # Log it:
                            newLogList = Logging.Log(loggingBool, logList,
                                                     announcement=f"'{directory}' is an important file, as the first character matches the importantFilesFlag. Restoring...",
                                                     logTag='C', log_non_critical=log_non_critical)
                            logList.extend(newLogList)

                            fileOperands.copyFile(directory, os.path.join(parentdir))
                        else:

                            # If the directory is not in the main directory but is in the sync directory, remove the directory from the sync directory:
                            checkDir = os.path.split(directory)[0]
                            if os.path.basename(os.path.normpath(checkDir)) == syncBackUpFolderName:
                                pass
                            else:
                                # Check if the user wants a backup folder or not:
                                if syncBackUpFolderExists:
                                    Synchronize.backUpToSyncFolder(directory, syncBackUpFolderName, maindir, syncdir)

                                # Log it:
                                newLogList = Logging.Log(loggingBool, logList,
                                                         announcement=f"Removing {file} from {parentdir2}, as it doesn't exist in {parentdir}",
                                                         logTag='C', log_non_critical=log_non_critical)
                                logList.extend(newLogList)
                                os.remove(directory)
                    elif isMatching == False:
                        # Log it:

                        # Merge the directories as well:
                        for directory in parent2dirs:
                            if directory not in parentdirs:
                                # Log it:
                                newLogList = Logging.Log(loggingBool, logList,
                                                         announcement="Merging files and dirs, as no files/dirs are matching.",
                                                         dir1=directory, dir2=f"'{parentdir}'. Merging directories...",
                                                         dir1Action="Directory '",
                                                         dir2Action=f"' exists in {parentdir2}, but not in", logTag='C',
                                                         log_non_critical=log_non_critical)
                                logList.extend(newLogList)
                                dirDirectory = os.path.join(parentdir2, directory)

                                dirDirectoryParent = os.path.join(parentdir, directory)

                                # Copy the files and the directories:
                                if not os.path.exists(dirDirectoryParent):
                                    fileOperands.copyDir(dirDirectory, os.path.join(parentdir))

                        # Log list:
                        newLogList = Logging.Log(loggingBool, logList,
                                                 announcement=f"Merging missing file: {file} into {parentdir}",
                                                 logTag='C', log_non_critical=log_non_critical)
                        logList.extend(newLogList)
                        fileOperands.copyFile(directory, os.path.join(parentdir))
            # To deal with directories: (remove from folder to sync to:)
            for directory in parent2dirs:
                if directory not in parentdirs:

                    # If the directory is not in the main directory but is in the sync directory, remove the directory from the sync directory:

                    isMatching = mergeDirectories(parentdir, parentdir2, parentdirs, parent2dirs)

                    directory = os.path.join(parentdir2, directory)

                    if isMatching == True or len(parentdirs) < 1:
                        # Log it: CONTINUE HERE
                        newLogList = Logging.Log(loggingBool, logList,
                                                 announcement="Skipping file and directory merging as some files/dirs are matching.",
                                                 log_non_critical=log_non_critical)
                        logList.extend(newLogList)

                        # Check if it is important directory:
                        if isImportantFile(directory, importantFilesFlag):
                            # Log it:
                            newLogList = Logging.Log(loggingBool, logList,
                                                     announcement=f"'{directory}' is an important directory, as the first character matches the importantFilesFlag. Restoring...",
                                                     logTag='C', log_non_critical=log_non_critical)
                            logList.extend(newLogList)

                            fileOperands.copyDir(directory, os.path.join(parentdir))
                        else:
                            # Here check if the directory name before the directory is the synBackUpFolderName. That way, the remove doesnt deal with the synBackUpsFolder:
                            checkDir = os.path.split(directory)[0]
                            if os.path.basename(os.path.normpath(checkDir)) == syncBackUpFolderName:
                                pass
                            else:
                                # Backup:
                                if syncBackUpFolderExists:
                                    Synchronize.backUpToSyncFolder(directory, syncBackUpFolderName, maindir, syncdir)

                                # Log it:
                                newLogList = Logging.Log(loggingBool, logList,
                                                         announcement=f"Removing {directory} and all of its contents, as it is directory {parentdir2}, but not in {parentdir}",
                                                         logTag='C', log_non_critical=log_non_critical)
                                logList.extend(newLogList)

                                shutil.rmtree(directory)
                    else:

                        for file in parent2files:
                            if file not in parentfiles:
                                fileDirectory = os.path.join(parentdir2, file)
                                parentFileDirectory = os.path.join(parentdir, file)

                                # Log it:
                                newLogList = Logging.Log(loggingBool, logList,
                                                         announcement="Merging files and dirs, as no files/dirs are matching.",
                                                         dir1=file, dir2=f"'{parentdir}'. Merging Files...",
                                                         dir1Action="File '",
                                                         dir2Action=f"' exists in {parentdir2}, but not in", logTag='C',
                                                         log_non_critical=log_non_critical)
                                logList.extend(newLogList)

                                # Copy the files and the directories:
                                if not os.path.exists(parentFileDirectory):
                                    fileOperands.copyFile(fileDirectory, os.path.join(parentdir))

                        # Add a try except block in case the function above this one already took care of the directories:
                        try:

                            newLogList = Logging.Log(loggingBool, logList,
                                                     announcement=f"Copying missing directory: {directory}, into {parentdir}",
                                                     logTag='C', log_non_critical=log_non_critical)
                            logList.extend(newLogList)

                            fileOperands.copyDir(directory, os.path.join(parentdir))
                        except FileExistsError:
                            pass

            # Here, create a for loop similar to those above that actually update the contents of a file by checking the time last modified, removing the old file, and copying the new one.
            for file in parentfiles:
                maindirpath = os.path.join(parentdir, file)
                dirsyncpath = os.path.join(parentdir2, file)

                mainfiletime = os.path.getmtime(maindirpath)

                dirsyncfiletime = os.path.getmtime(dirsyncpath)
                # Compute hashes (hot fix 2.0.4)
                if (GatherInfo.computeHash(maindirpath) != GatherInfo.computeHash(dirsyncpath)):
                    if (mainfiletime > dirsyncfiletime):
                        # Remove and copy the file:
                        os.remove(dirsyncpath)
                        fileOperands.copyFile(maindirpath, os.path.split(dirsyncpath)[0])
                        newLogList = Logging.Log(loggingBool, logList, announcement=f"Updating file contents:",
                                                 dir1=maindirpath, dir2="Updating file.", dir1Action='File at path',
                                                 dir2Action=f'was modified before file {dirsyncpath}.', logTag='C',
                                                 log_non_critical=log_non_critical)
                        logList.extend(newLogList)
                    elif mainfiletime < dirsyncfiletime:
                        os.remove(maindirpath)
                        newLogList = Logging.Log(loggingBool, logList, announcement=f"Updating file contents:",
                                                 dir1=dirsyncpath, dir2="Updating file.", dir1Action='File at path',
                                                 dir2Action=f'was modified before file {maindirpath}.', logTag='C',
                                                 log_non_critical=log_non_critical)
                        logList.extend(newLogList)
                        fileOperands.copyFile(dirsyncpath, os.path.split(maindirpath)[0])
            return logList

        # Execute the main function:
        newLogList = main(dir1, dir2, syncBackUpFolderName, syncBackUpFolderExists, importantFilesFlag, loggingBool,
                          maindir, syncdir)
        logList.extend(newLogList)

        return logList

    # Organize the path slashes, as os.path.join would not always work properly:
    def organizePathSlashes(path):
        if not path:
            return "/"
        if path[-1] not in ("/", "\\"):
            path += "/"
        return path

    # Function to move removed files and folders into in case of accidental deletions:
    def createSyncBackupFolder(dir1, dir2, syncBackUpFolderName):
        os.chdir(dir1)
        if not os.path.exists(syncBackUpFolderName):
            os.mkdir(syncBackUpFolderName)

        os.chdir(dir2)
        if not os.path.exists(syncBackUpFolderName):
            os.mkdir(syncBackUpFolderName)

    # For synchronizing files and dirs (The main function:)
    def synchronize(dir1, dir2, importantFilesFlag='_', syncBackUpFolderExists=True, loggingBool=False,
                    logCreationPath='', log_non_critical=True):

        # The main logList:
        logList = []

        # Log it:
        # Check if the user actually wants to create a syncBackUpFolder (It is recommended in order to reduce the chances of accidental file loss!)
        newLogList = Logging.Log(loggingBool, logList,
                                 announcement=f"Running in mode SYNCHRONIZATION: importantFilesFlag = '{importantFilesFlag}', syncBackUpFolderExists = {syncBackUpFolderExists}",
                                 logTag='C', log_non_critical=log_non_critical)
        # Append to the logList
        logList.extend(newLogList)
        # Initialize the backup directory:
        syncBackUpFolderName = f"{importantFilesFlag}syncBackups"
        if syncBackUpFolderExists:
            # Create the backup Folder:
            Synchronize.createSyncBackupFolder(dir1, dir2, syncBackUpFolderName)

        # Organize the directory slash marks (to avoid errors)
        dir1 = Synchronize.organizePathSlashes(dir1)
        dir2 = Synchronize.organizePathSlashes(dir2)

        maindir = dir1
        syncdir = dir2
        # Get the time of when the folders were last modified:
        # dir1ti_m = os.path.getmtime(dir1)
        # dir2ti_m = os.path.getmtime(dir2)
        dir1ti_m = []
        dir2ti_m = []

        # Check the times in the dir1:
        for folder, dirs, files in os.walk(dir1):
            # Here, get everything that is after the dir1 in order to get the other directories:

            time = os.path.getmtime(folder)

            # Append the values:
            dir1ti_m.append(time)

            # Get the time modified for the files as well:
            if len(files) != 0:
                for i in range(len(files)):
                    filePath = os.path.join(folder, files[i])

                    fileTimeModified = os.path.getmtime(filePath)

                    dir1ti_m.append(fileTimeModified)
        # Now, do the same thing, but check for dir2 for which was last modified:
        for folder, dirs, files in os.walk(dir2):

            # Here, get everything that is after the dir1 in order to get the other directories:

            timedir = os.path.getmtime(folder)

            # Append the values:
            dir2ti_m.append(timedir)

            if len(files) != 0:
                for i in range(len(files)):
                    filePath = os.path.join(folder, files[i])

                    fileTimeModified = os.path.getmtime(filePath)

                    dir2ti_m.append(fileTimeModified)

        dir1time = max(dir1ti_m)
        dir2time = max(dir2ti_m)

        # Log it:
        newLogList = Logging.Log(loggingBool, logList,
                                 announcement=f"Recursively got the time last modified for each directory: {dir1time} for {dir1} and {dir2time} for {dir2}",
                                 log_non_critical=log_non_critical)
        # Append to the logList
        logList.extend(newLogList)

        # The greater (bigger) time indicates the folder that was edited most recently:
        if float(dir1time) > float(dir2time):
            # IMPORTANT: Here, place if statement, deciding which folder was edited last (In other words,
            # decide which one should follow the other based on the time they were edited. The one that gets edited
            # the most recent gets the priority) When doing the above, invert the dir1 with dir2 (Because you are
            # doing pretty much the opposite!)
            for folder, dirs, files in os.walk(dir1):
                # Here, get everything that is after the dir1 in order to get the other directories:

                childdir = (folder.split(dir1, 1)[1])

                syncpath = os.path.join(dir2, childdir)

                newLogList = Logging.Log(loggingBool, logList,
                                         announcement=f"Iterating through main loop with {dir1} as the main directory, as {dir2} has an older modification time.",
                                         dir1=folder, dir2=syncpath, dir1Action='Entering child directory',
                                         dir2Action="to compare files and dirs with ",
                                         log_non_critical=log_non_critical)
                # Append to the logList
                logList.extend(newLogList)

                # Set the newLogList equal to the log that the function returns:
                newLogList = Synchronize.synchronizeComponents(folder, syncpath, syncBackUpFolderName,
                                                               syncBackUpFolderExists, importantFilesFlag, loggingBool,
                                                               maindir, syncdir, log_non_critical=log_non_critical)
                logList.extend(newLogList)

        elif float(dir1time) < float(dir2time):
            for folder, dirs, files in os.walk(dir2):
                # Here, get everything that is after the dir1 in order to get the other directories:
                childdir = (folder.split(dir2, 1)[1])
                syncpath = os.path.join(dir1, childdir)

                newLogList = Logging.Log(loggingBool, logList,
                                         announcement=f"Iterating through main loop with {dir2} as the main directory, as {dir1} has an older modification time.",
                                         dir1=folder, dir2=syncpath, dir1Action='Entering child directory',
                                         dir2Action="to compare files and dirs with ",
                                         log_non_critical=log_non_critical)
                # Append to the logList
                logList.extend(newLogList)

                # Set the newLogList equal to the log that the function returns:
                newLogList = Synchronize.synchronizeComponents(folder, syncpath, syncBackUpFolderName,
                                                               syncBackUpFolderExists, importantFilesFlag, loggingBool,
                                                               maindir, syncdir, log_non_critical=log_non_critical)

                logList.extend(newLogList)
        # At the very end, check if loggingBool is True. If it is, write the lines of the list logList to the specific directory of where the Log should be created:
        if loggingBool:
            # Write logs to file:
            writeLogsToFile(logList, 'synchronize')


# Class Backup: Unlike synchronization, this backs up to a 'child' directory, meaning that the 'child' directory plays no role on the parent one.
class Backup:
    # Capture the newLogList from the mainIteration function:
    def main(parentmaindir, childbackupdir, loggingBool, log_non_critical=True):

        # Define the main loglist to append to:
        logList = []

        # Get the source components of the parentdir and childsyncdir (in order to compare them later:)

        maindirs, mainfiles = GatherInfo.readDir(parentmaindir)
        syncdirs, syncfiles = GatherInfo.readDir(childbackupdir)

        # Log it:
        newLogList = Logging.Log(loggingBool, logList,
                                 announcement="Reading directories and files in the listed directories:",
                                 dir1=parentmaindir, dir2=childbackupdir, dir2Action=',',
                                 log_non_critical=log_non_critical)
        # Append to the logList
        logList.extend(newLogList)

        # To add files:
        for directory in maindirs:
            if directory not in syncdirs:
                # If the directory is not in the folder to sync to, then it adds it:

                # Log it:
                newLogList = Logging.Log(loggingBool, logList,
                                         announcement="Adding missing directories in the backup folder(s): ",
                                         dir1=parentmaindir, dir2=childbackupdir, dir1Action=f"directory '{directory}' found in",
                                         dir2Action='but not found in', logTag='C', log_non_critical=log_non_critical)
                # Append to the logList
                logList.extend(newLogList)

                path = os.path.join(childbackupdir, directory)
                os.mkdir(path)
        for file in mainfiles:
            # If the file is not in the folder to sync to, then it adds it:
            if file not in syncfiles:
                filepath = os.path.join(parentmaindir, file)

                newLogList = Logging.Log(loggingBool, logList,
                                         announcement="Adding missing files in the backup folder(s): ",
                                         dir1=parentmaindir, dir2=childbackupdir, dir1Action=f"File '{file}' found in",
                                         dir2Action='but not found in', logTag='C', log_non_critical=log_non_critical)
                # Append to the logList
                logList.extend(newLogList)

                fileOperands.copyFile(filepath, childbackupdir)

        # To remove files (remove from folder to sync to:)
        for directory in syncdirs:
            if directory not in maindirs:
                # Log it:
                newLogList = Logging.Log(loggingBool, logList,
                                         announcement="Removing extra directories in the backup folder: ",
                                         dir1=parentmaindir, dir2=childbackupdir,
                                         dir1Action=f"File '{file}' not found in",
                                         dir2Action='but found in backup folder. Removing from backup Folder:',
                                         logTag='C', log_non_critical=log_non_critical)
                # Append to the logList
                logList.extend(newLogList)
                # If the directory is in the backup directory but not in the main directory, remove the directory from the backup (sync) directory:
                directory = os.path.join(childbackupdir, directory)

                shutil.rmtree(directory)

        # Remove the file from the
        for file in syncfiles:
            if file not in mainfiles:
                # Log it:
                newLogList = Logging.Log(loggingBool, logList,
                                         announcement="Removing any extra files in the backup folder: ",
                                         dir1=parentmaindir, dir2=childbackupdir,
                                         dir1Action=f"File '{file}'not found in",
                                         dir2Action='but found in backup folder. Adding removing from backup Folder:',
                                         logTag='C', log_non_critical=log_non_critical)
                logList.extend(newLogList)

                # If the backup directory has the file but the main one doesn't, remove it from the backup directory:
                os.remove(os.path.join(childbackupdir, file))

        # Use this to update file content:
        for file in mainfiles:
            maindirpath = os.path.join(parentmaindir, file)
            dirsyncpath = os.path.join(childbackupdir, file)

            mainfiletime = os.path.getmtime(maindirpath)

            dirsyncfiletime = os.path.getmtime(dirsyncpath)

            # If the file needs to be updated, remove the old one and copy the new one to the backup folder:
            if (GatherInfo.computeHash(maindirpath) != GatherInfo.computeHash(dirsyncpath)):
                if mainfiletime > dirsyncfiletime:
                    # Remove and copy the file:
                    os.remove(dirsyncpath)
                    fileOperands.copyFile(maindirpath, os.path.split(dirsyncpath)[0])

                    newLogList = Logging.Log(loggingBool, logList, announcement=f"Updating content of file '{file}'",
                                             dir1=dirsyncpath, dir2=maindirpath,
                                             dir1Action="Updating file content at '",
                                             dir2Action=f"' as file '{file}' in backup folder is older than",
                                             logTag='C', log_non_critical=log_non_critical)
                    logList.extend(newLogList)

        # At the end of the main() function, return the logList
        return logList

    def mainIteration(maindir, backupdir, loggingBool, log_non_critical=True):

        logList = []
        for folder, dirs, files in os.walk(maindir):

            childdir = (folder.split(maindir, 1)[1])
            # Replace the first slash:
            try:
                if childdir[0] == "/" or childdir[0] == "\\":
                    childdir = childdir[1:]
            except:
                pass
            backupdir = Synchronize.organizePathSlashes(backupdir)
            # Here, the very start is blank because the childdir is blank (Perhaps, just leave it as is? It does not really matter)
            backUpFullPath = os.path.join(backupdir, childdir)
            # Log it:
            newLogList = Logging.Log(loggingBool, logList,
                                     announcement="Entering main loop under mainIteration function", dir1=childdir,
                                     dir2=backUpFullPath, dir1Action="Merged child path string '",
                                     dir2Action="' into sync path:", log_non_critical=log_non_critical)
            logList.extend(newLogList)

            # Transfer the newLogList to the main() function:

            logListMain = Backup.main(folder, backUpFullPath, loggingBool, log_non_critical=log_non_critical)

            logList.extend(logListMain)

        # Return the logList, which is the file lines to write:
        return logList

    def backup(maindir, backupdirs, logging_enabled=False, log_path='', log_non_critical=True):
        # Initialize the main logList:
        logList = []

        newLogList = Logging.Log(logging_enabled, logList, announcement="Running in BACKUP mode:", logTag='C',
                                 log_non_critical=log_non_critical)

        logList.extend(newLogList)

        if isinstance(backupdirs, list) != True:
            raise Exception("ERR: 'backupdirs' must be of type 'list'")

        try:
            # For every directory within the backup directories, backup:
            for directory in backupdirs:
                if len(backupdirs) > 1:
                    newLog = Logging.Log(logging_enabled, logList,
                                         announcement=f"Multiple Directories were given. Now, backing up to directory: {directory}",
                                         log_non_critical=log_non_critical)
                    logList.extend(newLog)
                newLogList = Backup.mainIteration(maindir, directory, logging_enabled, log_non_critical=log_non_critical)
                logList.extend(newLogList)
            # Write the logs:

            if logging_enabled == True:
                writeLogsToFile(logList, 'backup')

            print("Backup completed successfully.")

        except Exception as e:
            print(f"Backup failed: {str(e)}")

    def backgroundBackup(maindir, backupdirs, loggingBool=False, logCreationPath='', refreshInterval=8,
                         log_non_critical=True):

        # Now, implement logging in the synchronization algorithm.
        modeAnnounced = False
        while True:
            logList = []
            if modeAnnounced == False:
                newLogList = Logging.Log(loggingBool, logList, announcement="Running in BACKGROUNDBACKUP mode:",
                                         logTag='C', log_non_critical=log_non_critical)
                logList.extend(newLogList)
                modeAnnounced = True

            for directory in backupdirs:

                if len(backupdirs) > 1:
                    newLog = Logging.Log(loggingBool, logList,
                                         announcement=f"Multiple Directories were given. Now, backing up to directory: {directory}",
                                         log_non_critical=log_non_critical)
                    logList.extend(newLog)
                newLogList = Backup.mainIteration(maindir, directory, loggingBool, log_non_critical=log_non_critical)
                logList.extend(newLogList)
            # Write the logs to a file:
            if loggingBool == True:
                writeLogsToFile(logList, 'backgroundBackup')
            time.sleep(refreshInterval)


# Call a bash/shell script:
class callBash:
    def runFile(path, editPermissions=False):
        # If edit permissions is set to true, edit the permission (to avoid permission errors)
        if editPermissions == True:
            os.system("chmod +x " + path)
        subprocess.run([path], shell=True)
