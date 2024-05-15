import os
from FinderZV2 import GatherInfo
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