import os
import zipfile
import time
import datetime
from alive_progress import alive_bar
from colorama import Fore

counter = 0
# Path of the folder to be backed up
source_path = './Exampledir/'

# Delay until Backup is created (Seconds)
delay = 10 # 10 seconds Standard
# 1 Hour = 3600

# Path where the backup should be saved
backup_path = './Backups/'

# How old a backup should be so that it gets deleted.
maxold = 30
# Seconds
def wait_and_count(seconds):
    d = seconds*1000
    with alive_bar(d) as bar:
        for i in range(d, 0, -1):
            bar()
            time.sleep(0.001)
    print("\n")
    
def delete_old_file(filename):
  # Get the current time
  now = datetime.datetime.now()
  
  # Get the modification time of the file
  mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
  
  # Calculate the difference between the current time and the modification time
  time_diff = now - mod_time
  
  # If the difference is greater than 7 days (in seconds), delete the file
  if time_diff.total_seconds() > maxold:
    os.remove(filename)
    print(f"{Fore.RED}Deleted file: {Fore.BLUE + filename}")
  else:
    print(f"{Fore.GREEN}File is not old enough to be deleted: {Fore.BLUE + filename}")

while True:
    try:
        if(os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')

        

        # Update the Counter
        counter += 1
        print(f"{Fore.WHITE}At: {Fore.LIGHTBLUE_EX}" + str(counter))
        # Name for the backup file
        backup_filename = f'backup-{str(counter) + "-" + time.strftime("%Y_%m_%d-%H_%M_%S")}.zip'
        print(f"{Fore.WHITE}Filename: {Fore.LIGHTBLUE_EX}" + backup_filename)

        # Create a backup of the folder as a zip file with maximum compression
        zipf = zipfile.ZipFile(backup_path + backup_filename, 'w', zipfile.ZIP_DEFLATED)
        
        # Count the number of files in the folder
        num_files = 0
        print(f"{Fore.WHITE} Checking Number of Files")
        for root, dirs, files in os.walk(source_path):
            num_files += len(files)
        
        # Add the files to the zip and display the progress bar
        i = 0
        with alive_bar(num_files) as bar:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    print(Fore.CYAN + root + "/" + Fore.BLUE + file)
                    zipf.write(os.path.join(root.replace("\\", "/").replace("//", "/"), file))
                    i += 1
                    bar()
            zipf.close()
        print(f"{Fore.WHITE}Finished: {Fore.LIGHTBLUE_EX}" + str(counter))
        print(f"{Fore.WHITE}Running old check...")
        num_files = 0
        for root, dirs, files in os.walk(backup_path):
            num_files += len(files)
        
        for filename in os.listdir(backup_path):
            f = os.path.join(backup_path, filename)
            # checking if it is a file
            if os.path.isfile(f):
                delete_old_file(f)

        # Wait a delay before creating the next backup
        print(Fore.WHITE)
        wait_and_count(delay)
    except Exception as e:
        
        print(Fore.LIGHTRED_EX + "[ERROR] " + str(e))
        input("Press <enter> to exit.")
        print(Fore.RESET)
        exit(1)
        break
        