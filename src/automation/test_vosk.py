#!/usr/bin/env python3
#%%
from enum import Enum
import time, os, subprocess
class MediaFileJsonFields(str, Enum):
    MEDIAFILENAME = "mediaFileName"
    DURATION = "duration"
    SPLITTED_MEDIAS = "splittedMedias"
    ISMAINFILE = "isMainFile"
    POSITION = "position"

mfjf = MediaFileJsonFields

def generate_main_mediafilejson ( filename , duration = 0, splitted_medias = [] , isMainFile = True, position=None):
    """
      file name with extention eg: file.mp3 or movie.mp4
      duration should be int of seconds
      splitted_medias is an array of json files of similar structure to the json output by this function
      postion should be a list of [ page_number , position ]
    """
    json_dict = {
        mfjf.MEDIAFILENAME.value()    : filename,
        mfjf.DURATION.value()         : duration, #int of seconds,
        mfjf.SPLITTED_MEDIAS.value()  : splitted_medias ,
        mfjf.ISMAINFILE.value()       : isMainFile,
        mfjf.POSITION.value()         : position #pixel postion should be a list of [ page_number , position ]
    }
    return json_dict

def generate_shifted_mediafile_to_page ( mediajsonrep : dict , oldPageNumber : int , newPageNumber : int ) :
    name : str = mediajsonrep.get(mfjf.MEDIAFILENAME.value())
    name = name.replace(f"P{oldPageNumber}" , f"P{newPageNumber}")
    mediajsonrep.update({mfjf.MEDIAFILENAME.value():name})
    return mediajsonrep

def add_position_to_mediefilejson ( mediajsonrep : dict , pageNumber, pixelPosition ):
    copy = generate_main_mediafilejson(
        filename= mediajsonrep.get(mfjf.MEDIAFILENAME.value()) ,
        duration= mediajsonrep.get(mfjf.DURATION.value()) ,
        splitted_medias= mediajsonrep.get(mfjf.SPLITTED_MEDIAS.value()),
        isMainFile= mediajsonrep.get(mfjf.ISMAINFILE.value()),
        position= [ pageNumber, pixelPosition] ,
    )
    return copy

def generate_splited_medifilejson ( parentMediaFileJson : dict, startTime :int , stopTime : int ):
    name : str = parentMediaFileJson.get(mfjf.MEDIAFILENAME.value())
    ftstartTime = time.strftime("%H_%S", startTime)
    ftstopTime = time.strftime("%H_%S", stopTime)
    appendication = f"{ftstartTime}__{ftstopTime}"
    name = name.replace(".", f"{appendication}.")

    result = generate_main_mediafilejson(
        filename=name,
        duration=stopTime - startTime,
        splitted_medias=[],
        isMainFile=False,
    )
    return result

def file_exists( file_path):
    return os.path.exists(file_path)

def get_file_duration_ffmpeg( file_path ):
    command_str = f"ffprobe -v error -select_streams a:0  -show_entries stream=duration -of csv=p=0 \"{file_path}\""
    print(command_str)
    results = subprocess.run( command_str, check=True, stdout= subprocess.PIPE)
    out_val_seconds = float("".join([ c for c in results.stdout.decode("utf-8") if c.isdecimal() or c == "."]))
    return out_val_seconds
    #     "ffprobe", "-v",
    #     "error", "-select_streams",
    #     "v:0", "-show_entries",
    #     "stream=width,height,r_frame_rate,duration,pix_fmt,bit_rate,bits_per_raw_sample",
    #     "-of", "csv=p=0",
    #     fr'"{os.path.abspath(video_filename)}"'
    #     ]


# %%

# # # # STRUCTURE OF MEDIA FILE NAMES # # # #
# VIDOE NAMES = ENG %BookVersion% %UnitNumber% %somerandomnumber%
# AUDIO NAMES = SB11 %SOMECODE% %SUB UNIT TEXT% %PAGES%



