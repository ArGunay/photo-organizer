'''
Author: Ardil Günay

Reads images in a folder and organizes them by year and month.

USAGE: python3 photo_organizer.py <absolute_folderPath>

'''
import sys, os, shutil
from PIL import Image
from PIL.ExifTags import TAGS ,GPSTAGS


from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from sys import  stderr, exit

image_types = ["jpg" ,"jpeg","heic","png","tiff"]
movie_types = ['mov','mp4','3gp', 'avi']
count = 0



# move files from source to destination
def move_file(source, destination):

    shutil.move(source,destination)
    global count
    count += 1
    




def file_type(path):
    if os.path.isdir(path):
        return False
    splt = path.split('.')
    name, type = splt[0] ,splt[-1]
    type = type.lower()
    if type in image_types:
        return 1
    elif type in movie_types:
        return 2
    else:
        return 3


# returns month string
def getMonth(M):
    months = ['1_Gennaio','2_Febbraio','3_Marzo','4_Aprile','5_Maggio','6_Giugno','7_Luglio','8_Agosto','9_Settembre','10_Ottobre','11_Novembre','12_Dicembre']
    return months[int(M)-1]



def manage_spartition(file_path ,year_folder, month_folder, new_destination):
    # if year_folder Exists
    if os.path.exists(year_folder):
        # if month_folder Exists
        if os.path.exists(month_folder):
            move_file(file_path, new_destination)
        else:
            # Create montFolder and move file
            os.mkdir(month_folder)
            move_file(file_path, new_destination)

    else:
        # create year_folder
        os.mkdir(year_folder)
        # create month_folder
        os.mkdir(month_folder)
        # move file
        move_file(file_path, new_destination)


def manage_image(file_path, folder_path, file_name):
  
    # open image
    img = Image.open(file_path)
    exifdata = img._getexif()
    info = None
    datainfo = None
    if exifdata is not None:
        info = {TAGS.get(tag): value for tag, value in exifdata.items()}
        if 'DateTimeOriginal' in info:
            datainfo = info['DateTimeOriginal']
        else:
            print('not present')


        
    Y,M,D  = 0,0,0
    if datainfo is None or exifdata == {}:
        print(f"\nno exif or datafinfo for {file_name} \n {'exif':20}: {exifdata} \n {'datainfo':20}: {datainfo}")
        print("Attempt of filename date Decomposition Now - NO GUARANTEE OF SUCCESS\n")
        try:

            com_date = "".join(file_name.split('.')[0].split('_')[0].split(' ')[0].split('-'))
  
            # quick integer check
            int(com_date)
            if len(com_date) < 8: # date string length
                print(f'{com_date} not a date')
                return
                
            Y, M, D = com_date[0:4], com_date[4:6],com_date[6:8]
        except Exception:
            print(f"===== Impossible to parse for this file {file_name} =====")
            return
    else:   
 
        date, time = datainfo.split(" ")
        # Year, Month, Day
        Y , M, D = date.split(":")
        # hour, minutes, seconds
        # h, m, s = time.split(":")


    year_folder = os.path.join(folder_path,Y)
    
    month_folder = os.path.join(year_folder ,getMonth(M))

    new_destination = os.path.join(month_folder, file_name)

    manage_spartition(file_path ,year_folder, month_folder, new_destination)
    
  


def manage_video(file_path, folder_path, file_name):
    print(f"Managing Video {file_name}")
    parser = createParser(file_path)
    if not parser:
        print("Unable to parse file", file=stderr)
        exit(1)

    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            print("Metadata extraction error: %s" % err)
            metadata = None
    if not metadata:
        print("Unable to extract metadata")
        exit(1)

    meta = metadata.exportPlaintext()
    
    print(meta)
    # print(f'\n meta: {meta}\n')
    print(meta[4].split(' ')[3].split('-'))
    Y, M , D = meta[4].split(' ')[3].split('-')


    year_folder = os.path.join(folder_path,Y)
    
    month_folder = os.path.join(year_folder ,getMonth(M))

    new_destination = os.path.join(month_folder, file_name)

    manage_spartition(file_path ,year_folder, month_folder, new_destination)
  







def main():
    folder_path  = sys.argv[1]

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path , file_name)

        flag = file_type(file_path)
        

        if flag == 3:
            continue
        elif flag == 2:
            manage_video(file_path, folder_path, file_name)
        elif flag == 1:
            manage_image(file_path, folder_path, file_name)






# ================= MAIN ===============
if __name__ == "__main__":
    import timeit
    main()
    # print(timeit.timeit(main, number=1))


    # print(f"ORGANISING DONE FOR YOU WITH <3, {count} files moved")

