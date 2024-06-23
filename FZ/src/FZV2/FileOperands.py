import os
import shutil
import hashlib
import zipfile
from FZV2 import GatherInfo


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


class FileOperands:
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
                FileOperands.xor_encrypt_file(file_path, key, removeOriginal)

        FileUtils.process_files_in_dir(directory, recursive, process_func)

    @staticmethod
    def xor_decrypt_files(directory, key, removeEncrypted=False, recursive=False):
        def process_func(root, files):
            for file in files:
                if file.endswith('.enc'):
                    file_path = os.path.join(root, file)
                    FileOperands.xor_decrypt_file(file_path, key, removeEncrypted)

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
