import time
import os

class Logging:
    # The main logging class (Used in Synchronize and Backup classes)
    def writeLogsToFile(creationPath, fileLines, mode):
        currentTime = time.strftime("%Y-%m-%d_%H-%M-%S")
        logFileName = f"LogRun({mode})__{currentTime}.txt"
        filePath = os.path.join(creationPath, logFileName)

        with open(filePath, 'a') as f:
            f.writelines(fileLines)

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