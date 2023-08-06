import os
import time


def relocateNow():
    try:
        source = os.getcwd()
        for path,dir1,files in os.walk(source):
            if files and path==source:
                for file in files:
                    try:
                        parts = file.split(".")
                        file_type = parts[-1].upper()
                        source_folder = os.path.join(path,file)
                        ctime = time.ctime(os.path.getctime(source_folder)).split(" ")
                        file_time = ""+ctime[1].upper()+" "+ctime[-1]
                        target_folder = os.path.join(source,"RELOCATED")
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_time)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file_type)
                        if not os.path.exists(target_folder):
                            os.mkdir(target_folder)
                        target_folder = os.path.join(target_folder, file)
                        if not os.path.isfile(target_folder):
                            os.rename(source_folder , target_folder)
                    except:
                        print("Failed to relocate "+file)
        print("ALL FILES RELOCATED")
    except Exception as e:
        print(e)