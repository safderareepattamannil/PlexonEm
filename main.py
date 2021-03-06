import os
import sys
from mutagen.easymp4 import MP4
import shutil
from progress.bar import Bar
from datetime import datetime
import time


# GLOBAL VARIALBLES
# PATH = "C:\\Users\\bb\Documents\\projects\\MetaCleanse\\movie_env\\"
PATH = os.getcwd()+"\\movie_env\\"
PLEX_PATH = "D:\\Media\\Movies"
# PATH = "C:\\Users\\bb\\Downloads\\"

# Find end of year and truncate the rest of file name


def process_name(fname):
    truncatation_idx = 0
    paren_insert_idx = 0
    success = False
    for i in range(len(fname)):
        # Base case the fuck out
        if success:
            break
        # Validation logic
        if fname[i] == ".":
            try:
                attempt = int(fname[i+1:i+5])+1
                truncatation_idx = i+5
                paren_insert_idx = i
                success = True
            except:
                continue

    # Truncated plus titled
    truncated = fname[:truncatation_idx].title()
    # Insert parenthesis around yeaer
    parenthesized = (truncated[:paren_insert_idx] +
                     ' (' + truncated[paren_insert_idx+1:] + ')')
    # Clear period delimiters
    result = parenthesized.replace('.', ' ')

    #  handle multi alterations

    if result == ' ()':
        return fname
    else:
        return result


# Get name of all subdirectories in parent folder
def process_engine(PATH):
    child_folders = os.listdir(PATH)


    # Nest into each folder looking for mp4 files
    for folder_name in child_folders:

        # Nest into grandchildren for mp4 files and rename that
        grandchildren = os.listdir(PATH+folder_name)

        for grandchild in grandchildren:
            # Check that we are aren't processing files more than once
            try:
                if (process_name(grandchild) != grandchild):

                    # Setup work 
                    grandchild_path = PATH+folder_name + '\\' #get grandchild path
                    file_extension = os.path.splitext(grandchild)[1]

                    # Remove trash files
                    if file_extension == ".txt":
                        os.remove(grandchild_path + grandchild + ".txt")
                    if file_extension == ".exe":
                        os.remove(grandchild_path + grandchild + ".exe")

                    # If file_extension is an mp4
                    if file_extension == ".mp4":
                        os.rename(grandchild_path + grandchild,
                                  grandchild_path+process_name(grandchild)+file_extension)
                        print("Renaming {grandchild} now".format(
                            grandchild=grandchild))

                        # Erase all metadata
                        curr_video = MP4(
                            grandchild_path+process_name(grandchild)+file_extension)
                        for metadata in curr_video.tags:
                            curr_video.tags[metadata] = ""
                            curr_video.save()

                    # Handle mkv case, mkvs do not need a metadata change
                    # Might hit edge case late
                    elif file_extension == ".mkv":
                        os.rename(grandchild_path + grandchild,
                                  grandchild_path+process_name(grandchild)+file_extension)

                    # Handle Avi case, no fucking clue if this needs a metadata change
                    elif file_extension == '.avi':
                        os.rename(grandchild_path + grandchild,
                                  grandchild_path+process_name(grandchild)+file_extension)
            except:
                continue
        
        
        # Open log file
        log_file = open("log.txt", "a")

        if (process_name(folder_name) != folder_name):
            try:
                
                os.rename(PATH+folder_name, PATH+process_name(folder_name))
                print("Rename success: {folder}".format(folder=folder_name))
                shutil.move(PATH+process_name(folder_name), PLEX_PATH)
                # Get time
                current_time = datetime.now()
                log_file.write("Succesfully completed {folder} at {current_time} \n".format(folder=folder_name, current_time=current_time))
                print("Move success: {folder}".format(folder=folder_name))
            except:
                print("Move unsuccesfull")
                continue


""" # Move to plex folder
folder_amount=len(os.listdir(PATH))

# Progress Bar
bar=Bar('Files Plexed', max=folder_amount)




def move_engine(PATH, destination):

    log_file = open("log.txt", "a")

    child_folders = os.listdir(PATH)

    for folder in child_folders:
        # Get get time
        current_time = datetime.now()
        try:
            print(" Currently moving", folder)
            shutil.move(PATH+folder, destination)
            bar.next()
            # Write to log
            log_file.write("Succesfully completed {folder} at {current_time} \n".format(
                folder=folder, current_time=current_time))
        except:
            print("File {folder} active in other application ".format(folder=folder))
            continue

    bar.finish()
    # Close Logs
    log_file.close()
 """

def activate_plex_engine():
    file_count=len(os.listdir(PATH))
    print("Checking for files..")
    if(file_count >=1):
        process_engine(PATH)
    else:
        print("Nothing to see here...")


# Run Commands
check_folder=False

while True:
    activate_plex_engine()
    time.sleep(60)
