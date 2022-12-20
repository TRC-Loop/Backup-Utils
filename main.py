import os
import logging
import zipfile
import time
import datetime
from alive_progress import alive_bar
from colorama import Fore

logging.info("Starting")
counter = 0

# System Command before start
logging.info("Setting up custom config")
PCommand = ""
delayP = 2

# System Command after stop
SCommand = ""

# Path of the folder to be backed up
source_path = 'C:\\Users\\Arne\\Desktop\\'

# Delay until Backup is created (Seconds)
delay = 10 # 10 seconds Standard
# 1 Hour = 3600

# Path where the backup should be saved
backup_path = './Backups/'

# How old a backup should be so that it gets deleted.
maxold = 3600
# Seconds
logging.info("Defining Functions")
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
    logging.info("Deleted file %s" % filename)
    print(f"{Fore.RED}Deleted file: {Fore.BLUE + filename}")
  else:
    logging.info("Skipped file %s" % filename)
    print(f"{Fore.GREEN}File is not old enough to be deleted: {Fore.BLUE + filename}")

while True:
    try:
        logging.info("Clearing Console")
        if(os.name == 'posix'):
            logging.info("Clearing Console: Posix")
            os.system('clear')
        else:
            logging.info("Clearing Console: Win")
            os.system('cls')

        

        # Update the Counter
        logging.info("Running PCommand")
        os.system(PCommand)
        logging.info("Wating PDelay")
        time.sleep(delayP)
        
        
        counter += 1
        logging.info("Current: " + str(counter))
        print(f"{Fore.WHITE}At: {Fore.LIGHTBLUE_EX}" + str(counter))
        # Name for the backup file
        logging.info("Creating backup file: ")
        backup_filename = f'backup-{str(counter) + "-" + time.strftime("%Y_%m_%d-%H_%M_%S")}.zip'
        logging.info(backup_filename)
        print(f"{Fore.WHITE}Filename: {Fore.LIGHTBLUE_EX}" + backup_filename)

        # Create a backup of the folder as a zip file with maximum compression
        logging.info("Creating backup")
        zipf = zipfile.ZipFile(backup_path + backup_filename, 'w', zipfile.ZIP_DEFLATED)
        
        # Count the number of files in the folder
        num_files = 0
        logging.info("Checking Number of files in source directory")
        print(f"{Fore.WHITE} Checking Number of Files")
        for root, dirs, files in os.walk(source_path):
            num_files += len(files)
        
        # Add the files to the zip and display the progress bar
        i = 0
        logging.info("Zipping all files")
        with alive_bar(num_files) as bar:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    logging.info(root + file)
                    print(Fore.CYAN + root.replace("\\", "/").replace("//", "/") + "/" + Fore.BLUE + file)
                    zipf.write(os.path.join(root.replace("\\", "/").replace("//", "/"), file))
                    i += 1
                    bar()
            logging.info("Closing backup File")
            zipf.close()
        logging.info("Running Suffix Command")
        os.system(SCommand)
        print(f"{Fore.WHITE}Finished: {Fore.LIGHTBLUE_EX}" + str(counter))
        print(f"{Fore.WHITE}Running old check...")
        logging.info("Running old check")
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
        logging.info("Waiting for next run")
        wait_and_count(delay)
    except Exception as e:
        logging.exception(e)
        print(Fore.LIGHTRED_EX + "[ERROR] " + str(e))
        input("Press <enter> to exit.")
        print(Fore.RESET)
        exit(1)
        break
        