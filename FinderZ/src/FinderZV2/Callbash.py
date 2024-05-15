import os
import subprocess

#Call a bash/shell script:
class Callbash:
	def runFile(file_path, change_file_permission = False):
		#If edit permissions is set to true, edit the permission (to avoid permission errors)
		if not os.path.exists(file_path):
			print(f"File does not exist: {file_path}")
			return
		if change_file_permission:
			os.chmod(file_path, 0o755)
		subprocess.run([file_path], shell = True)