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
    MEDIATYPE = "mediaType"
    MEDIAPATHNAME = "mediaPathName"
    HEIGHT ="height"
    TITLE = "title"
    TEXT = "text"

mfjf = MediaFileJsonFields

def convert_mfj_to_stage3item( mfj_json : dict):
    results = [ True for i in mfj_json.keys() if i in [mfjf.MEDIAFILENAME.value   ,mfjf.DURATION.value ,mfjf.SPLITTED_MEDIAS.value ,mfjf.ISMAINFILE.value ,mfjf.POSITION.value, mfjf.MEDIATYPE.value, mfjf.MEDIAPATHNAME.value, mfjf.HEIGHT, mfjf.TEXT, mfjf.TITLE ]       ]
    return_data = None
    media_types = {
        "mp3":"audio",
        "wmv":"video",
        "mp4":"video",
        "div":"divider", #Divider used to clear elements on the screen between two dividers
        "inh":"inh", #Inner Html
        "divider":"divider",
        "dict":"dict", #Dictation component
        "h5p":"h5phtml",
        "html":"h5phtml"
    }
    if len(results) == len( mfj_json.keys() ):
        return_data = {
          #"type": "video" if mfj_json[mfjf.MEDIAFILENAME.value][-3:] =="wmv" else ( "audio" if mfj_json[mfjf.MEDIAFILENAME.value][-3:] == "mp3" else "h5p" ) ,
          "type" : media_types[mfj_json[mfjf.MEDIATYPE.value]],
          "name": mfj_json[mfjf.MEDIAFILENAME.value],
          "position": int( mfj_json[mfjf.POSITION.value][1]),
        }

        remaining = { i[0]:i[1] for i in mfj_json.items() if i[0] not in [mfjf.MEDIATYPE.value,mfjf.MEDIAFILENAME.value,mfjf.POSITION.value] and i[1] != None}
        if return_data["type"] == "video":
            return_data["name"] = return_data["name"][0:-3] + "mp4"
        print("remaning",remaining)
        return_data.update(remaining)


        # if return_data["type"] == "divider":
        #     return_data.update({"height":1})
    return return_data



def generate_main_mediafilejson ( filename , mediapathname,mediatype, duration = 0, splitted_medias = [] , isMainFile = True, position=None, height=None, title=None, text=None):
    """
      file name with extention eg: file.mp3 or movie.mp4
      duration should be int of seconds
      splitted_medias is an array of json files of similar structure to the json output by this function
      postion should be a list of [ page_number , position ]
    """
    json_dict = {
        mfjf.MEDIAFILENAME.value    : filename,
        mfjf.DURATION.value         : duration, #int of seconds,
        mfjf.SPLITTED_MEDIAS.value  : splitted_medias ,
        mfjf.ISMAINFILE.value       : isMainFile,
        mfjf.POSITION.value         : position, #pixel postion should be a list of [ page_number , position ]
        mfjf.MEDIATYPE.value        : mediatype,
        mfjf.MEDIAPATHNAME.value    : mediapathname,
        mfjf.HEIGHT.value           : height,
        mfjf.TEXT.value             : text,
        mfjf.TITLE.value            : title
    }
    return json_dict

def generate_shifted_mediafile_to_page ( mediajsonrep : dict , oldPageNumber : int , newPageNumber : int ) :
    name : str = mediajsonrep.get(mfjf.MEDIAFILENAME.value)
    name = name.replace(f"P{oldPageNumber}" , f"P{newPageNumber}")
    mediajsonrep.update({mfjf.MEDIAFILENAME.value:name})
    return mediajsonrep

def add_position_to_mediefilejson ( mediajsonrep : dict , pageNumber, pixelPosition ):
    copy = generate_main_mediafilejson(
        filename= mediajsonrep.get(mfjf.MEDIAFILENAME.value) ,
        mediapathname= mediajsonrep.get(mfjf.MEDIAPATHNAME.value),
        mediatype=mediajsonrep.get(mfjf.MEDIATYPE.value),
        duration= mediajsonrep.get(mfjf.DURATION.value) ,
        splitted_medias= mediajsonrep.get(mfjf.SPLITTED_MEDIAS.value),
        isMainFile= mediajsonrep.get(mfjf.ISMAINFILE.value),
        position= [ pageNumber, pixelPosition] ,
        height=  mediajsonrep.get(mfjf.HEIGHT.value),
        title=  mediajsonrep.get(mfjf.TITLE.value),
        text =  mediajsonrep.get(mfjf.TEXT.value)
    )
    return copy

def generate_splited_medifilejson ( parentMediaFileJson : dict, startTime :int , stopTime : int ):
    name : str = parentMediaFileJson.get(mfjf.MEDIAFILENAME.value)
    mediapath : str = parentMediaFileJson.get(mfjf.MEDIAPATHNAME.value)
    mediatype : str = parentMediaFileJson.get(mfjf.MEDIATYPE.value)
    ftstartTime = time.strftime("%M_%S", time.gmtime(startTime))
    ftstopTime = time.strftime("%M_%S", time.gmtime(stopTime))
    appendication = f"{ftstartTime}__{ftstopTime}"
    name = name[::-1].replace(".", f"{appendication}."[::-1],1)[::-1]
    mediapath = mediapath[::-1].replace(".", f"{appendication}."[::-1], 1)[::-1]

    result = generate_main_mediafilejson(
        filename=name,
        mediapathname= mediapath,
        duration=stopTime - startTime,
        splitted_medias=[],
        isMainFile=False,
        mediatype=mediatype
    )

    #Command
    #return_code = split_media(parentMediaFileJson.get(mfjf.MEDIAPATHNAME.value) , startTime, stopTime,mediapath)

    #if return_code == 0:
    #    return result
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

def split_media( media_path, from_, to, new_media_path ):
    command = [
        "ffmpeg",
        "-y",
         "-ss",
         str(from_), # int secoonds
         "-i",
         media_path,
         "-t",
         str(to - from_) , # int seconds
        "-c",
         "copy",
         new_media_path]

    results = subprocess.run( command, check=True, stdout=subprocess.PIPE)
    return results.returncode

# %%

# # # # STRUCTURE OF MEDIA FILE NAMES # # # #
# VIDOE NAMES = ENG %BookVersion% %UnitNumber% %somerandomnumber%
# AUDIO NAMES = SB11 %SOMECODE% %SUB UNIT TEXT% %PAGES%



