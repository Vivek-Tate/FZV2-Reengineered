import os
import shutil
import time
from .GatherInfo import GatherInfo
from .Logging import Logging
from .FileOperands import FileOperands
from .Synchronize import Synchronize

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

                FileOperands.copyFile(filepath, childbackupdir)

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
                    FileOperands.copyFile(maindirpath, os.path.split(dirsyncpath)[0])

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
                Logging.writeLogsToFile(logList, 'backup')

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
                Logging.writeLogsToFile(logList, 'backgroundBackup')
            time.sleep(refreshInterval)