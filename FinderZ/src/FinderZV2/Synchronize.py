import os
import shutil
from FinderZV2 import FileOperands
from FinderZV2 import GatherInfo
from FinderZV2 import Logging

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

            FileOperands.copyFile(filePath, syncBackUpFolderPathMain)

            # Sync Path:
            if os.path.exists(isExistingInSyncBackUpFolderDirectory_Sync):
                os.remove(isExistingInSyncBackUpFolderDirectory_Sync)

            FileOperands.copyFile(filePath, syncBackUpFolderPathSync)

        # If the path leads to a directory:
        if os.path.isdir(filePath):
            # Here, check whether the directory already exists within the syncBackUpFolderPath:

            # Main path:
            if os.path.exists(isExistingInSyncBackUpFolderDirectory_Main):
                shutil.rmtree(isExistingInSyncBackUpFolderDirectory_Main)
            FileOperands.copyDir(filePath, syncBackUpFolderPathMain)

            # Sync path:
            if os.path.exists(isExistingInSyncBackUpFolderDirectory_Sync):
                shutil.rmtree(isExistingInSyncBackUpFolderDirectory_Sync)
            FileOperands.copyDir(filePath, syncBackUpFolderPathSync)

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
                    FileOperands.copyFile(originalpath, parentdir2)

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

                            FileOperands.copyFile(directory, os.path.join(parentdir))
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
                                    FileOperands.copyDir(dirDirectory, os.path.join(parentdir))

                        # Log list:
                        newLogList = Logging.Log(loggingBool, logList,
                                                 announcement=f"Merging missing file: {file} into {parentdir}",
                                                 logTag='C', log_non_critical=log_non_critical)
                        logList.extend(newLogList)
                        FileOperands.copyFile(directory, os.path.join(parentdir))
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

                            FileOperands.copyDir(directory, os.path.join(parentdir))
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
                                    FileOperands.copyFile(fileDirectory, os.path.join(parentdir))

                        # Add a try except block in case the function above this one already took care of the directories:
                        try:

                            newLogList = Logging.Log(loggingBool, logList,
                                                     announcement=f"Copying missing directory: {directory}, into {parentdir}",
                                                     logTag='C', log_non_critical=log_non_critical)
                            logList.extend(newLogList)

                            FileOperands.copyDir(directory, os.path.join(parentdir))
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
                        FileOperands.copyFile(maindirpath, os.path.split(dirsyncpath)[0])
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
                        FileOperands.copyFile(dirsyncpath, os.path.split(maindirpath)[0])
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
            Logging.writeLogsToFile(logList, 'synchronize')
