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
from sys import argv, stderr, exit

image_types = ["jpg" ,"jpeg","heic","png","tiff"]
movie_types = ['mov','mp4','3gp', 'avi']
count = 0

folder_path  = sys.argv[1]


# move files from source to destination
def move_file(source, destination):
    print('file moved')
    shutil.move(source,destination)
    global count
    count += 1
    




def filetype(path):
    if os.path.isdir(path):
        return False
    splt = path.split('.')
    name,type = splt[0] ,splt[-1]
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
  
    print(f'Managing Image {file_name}')
    # open image
    img = Image.open(file_path)
    # get exif data
    exifdata = img._getexif()
    info = None
    datainfo = None
    if exifdata is not None:
        info = {TAGS.get(tag): value for tag, value in exifdata.items()}
        # print(f'info: {info}')
        if 'DateTimeOriginal' in info:
            # print('present')
            datainfo = info['DateTimeOriginal']
        else:
            print('not present')
    # exif timestamp key
    # key = 0x0132 #"DateTimeOriginal"
    # get exif tags
    # tag = TAGS.get(key,key)
    # get exif image time tag
    # datainfo = exifdata.get(key)
        
    # print(f'--++-- {tag:20}: {datainfo}')
    Y,M,D  = 0,0,0
    if datainfo is None or exifdata == {}:
        print(f"\nno exif or datafinfo for {file_name} \n {'exif':20}: {exifdata} \n {'datainfo':20}: {datainfo}")
        print("Attempt of filename date Decomposition Now - NO GUARANTEE OF SUCCESS\n")
        try:
            # info = img._getexif()
            # inf = {TAGS.get(tag): value for tag, value in info.items()}
            # print('===========')
            # print(inf['DateTimeOriginal'])
            # print('===========')
            # com_date = file_name.split(".")[0].split("_")[0]
            com_date = "".join(file_name.split('.')[0].split('_')[0].split(' ')[0].split('-'))
            # print(f'{"1":10}: {com_date}')
            
            # quick integer check
            int(com_date)
            if len(com_date) < 8: # date string length
                print(f'{com_date} not a date')
                return
                
            # print(f'{"2":10}: {com_date}')
            Y, M, D = com_date[0:4], com_date[4:6],com_date[6:8]
            print(Y,M,D)
        except:
            print("===== Impossible to parse for this version =====")
            return
    else:   
 
        date, time = datainfo.split(" ")
        # Year, Month, Day
        Y , M, D = date.split(":")
        # hour, minutes, seconds
        h, m, s = time.split(":")
        print(f'{Y} - {M}')

    year_folder = folder_path + "/" + Y
    
    month_folder = year_folder + '/'+ getMonth(M)

    new_destination = month_folder+"/"+ file_name

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
    
    # print(f'\n meta: {meta}\n')
    print(meta[4].split(' ')[3].split('-'))
    Y, M ,D = meta[4].split(' ')[3].split('-')

    year_folder = folder_path + "/" + Y
    
    month_folder = year_folder + '/'+ getMonth(M)

    new_destination = month_folder+"/"+ file_name

    manage_spartition(file_path ,year_folder, month_folder, new_destination)
  
    # for line in metadata.exportPlaintext():
        # print(line)


# ================= MAIN LOOP ===============
if __name__ == "__main__":

    


    for file_name in os.listdir(folder_path):
        file_path = folder_path + "/" + file_name
        flag = filetype(file_path)

        if flag == 3:
            continue
        elif flag == 2:
            manage_video(file_path, folder_path, file_name)
        elif flag == 1:
            manage_image(file_path, folder_path, file_name)
    # ===========================================
 

        
print(f"ORGANISING DONE FOR YOU WITH <3, {count} files moved")

