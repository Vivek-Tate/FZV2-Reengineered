import os
import hashlib
import re


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