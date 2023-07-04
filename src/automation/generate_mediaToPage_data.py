
#%%
import os, glob, re, lxml.etree
from lxml import html
#from html.parser import HTMLParser

page_number = 7
folderpath = r"C:/Users/Mubarak Salley/Documents\Accede/Tenacity-Book-11/src/assets/pagesBeforeAudioAndVideo"
#filepath = fr"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\pages\{page_number}.html"

html_file_names = glob.glob(folderpath + "/*.html" )
html_file_names.sort( key = lambda x : int(x.split("\\")[-1].replace(".html","")) )
#print(html_file_names)


ids_list = [None] * page_number
unit_specific_class = ""
for i in range(page_number, len(html_file_names) ):
  #search_results = None;
  with open(html_file_names[i-1], 'r', encoding="utf-8") as thefile:
    #output = html.unescape(thefile.read())
    #html_parser.feed(thefile.read())
    output = thefile.read()
    tree = html.fromstring(output)

    # Extracts ID for each page
    results = re.search(pattern=r"^<div.*?id=\"(\w+?)\".*?>.*</div>", string=output, flags=re.DOTALL)
    # Extacts All Div With the Format AX.X <heading> or BX.X <heading> .... etc
    results2 = re.findall(pattern=r"(<div([^<>]*?)>([ABCDEF]\d+\.\d+).*?</div>)", string=output, flags=re.DOTALL)
    #print(results2)
    if results2 != []:
      # Extracts a particular class name the has the pattern ffXX, this is important for each page
      res = re.search(pattern=r"ff\w+", string=results2[0][1])
      unit_specific_class = res.group(0)

      # treedd = html.fromstring(results2.group(0))
      # arr = treedd.xpath("//span")
      # if len(arr) > 0:
      #     print("PRINTING TEXT CONTENT : ", arr[0].text_content() )

      ##print("Class " , res)
    print("Page Number : ", i , " - " , unit_specific_class)

    # Extract A elements that cocan potentially have a video or audio file under it
    elements = tree.xpath(f'.//div[contains(@class,"{unit_specific_class}") and contains(@class,"fc0") and contains(@class,"fs6")]|.//div[contains(@class,"{unit_specific_class}") and contains(@class,"fs1") and contains(@class,"h1f")]')
    # TODO : For the Ex1 matching, it will be best to also extract the text attached with the exercise number


    elements_results = list(map( lambda x: html.tostring(x).decode('utf-8'), elements))



    temp_res = []
    temp_res.append(i)
    if results != None  :
      temp_res.append(results.groups()[0])

    # else:
    #    temp_res.append(None)
    if results2 != []:
      temp_res.append(list(map(lambda inp : inp[0] , results2)))
      #print(results2[0])
    else:
      temp_res.append(None)
    temp_res.append(elements_results)
    #temp_res.append(elements)
    if temp_res == []:
      temp_res = None

    ids_list.append( temp_res )

#print(ids_list)

#%%
import glob, os, re
import Levenshtein as lvsh

# MANUAL INPUT
AUDIO_FOLDER_PATH = r"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\audio"
PVIDEO_FOLDER_PATH = r"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\video"
PAGE_FOLDER_PATH = r"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\pages"

# This Variable will be used By another python file wich imports this out
GENERATED_PAGES_OUTPUT = r"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\gpages"

#WORDS that dont help with fuzzy text matching
WORDS_TO_REMOVE_FROM_VIDEO_NAME = ["Increaseyourwordpower","LearningStrategies","Vocabulary", "StudySkills", "LanguageFocus", "Listening", "Reading", "Speaking" , "Writing", "_"]
MATCHING_THRESHOLD = 0.70 # a value from 0 - 1

audio_files_path = glob.glob(AUDIO_FOLDER_PATH + r"\*.mp3")
video_files_path = glob.glob(PVIDEO_FOLDER_PATH + r"\*.mp4")

list_of_audio_files = []
list_of_video_files = []



for audio_file in audio_files_path:
    list_of_audio_files.append( audio_file.split("\\")[-1][0:-4:1] )
for video_file in video_files_path:
    list_of_video_files.append( video_file.split("\\")[-1][0:-4:1] )

pages_offset = 6

page_files_path = glob.glob( PAGE_FOLDER_PATH + r"\*.html" )
page_numbers = [  i - (pages_offset-1) for i in range(1, len(page_files_path)+1)]

page_one_index = pages_offset -1

start_page_number = 1
end_page_number = page_numbers[-1]

## MANUAL INPUT
unit_pagesm = {
    # Note these page number are actual page number on the page, but to get
    # the page you might have to add some offset value
    "u-1"  : (1,28),
    "u-2"  : (29,57),
    "u-3"  : (57,90),
    "u-4"  : (97,119),
    "u-5"  : (120,140),
    "u-6"  : (141,160),
    "u-7"  : (167, 196),
    "u-8"  : (197,220),
    "u-9"  : (221,241),
    "u-10" : (248,265),
    "u-11" : (266,286),
    "u-12" : (287,300)
}

unit_tized_videonames = dict()
unit_tized_audionames = dict()

matched_medias = set()

for key, vals in unit_pagesm.items():
    u_num= int(key.replace("u-", ""))
    unit_tized_videonames.update({u_num : []})
    unit_tized_audionames.update({u_num : []})

## Divide Video Paths Into Units
for video_name in list_of_video_files:
    re_sult = re.search("U(\d+)", video_name)
    print(re_sult)
    if re_sult != None:
        unit_number = int(re_sult.group(1))
        if unit_number != None:
            unit_tized_videonames[unit_number].append(video_name)

## Divide Audio Paths Into Units
for audio_name in list_of_audio_files:
    re_sult = re.search("U(\d+)", audio_name)

    if re_sult != None:
        unit_number = int(re_sult.group(1))
        if unit_number != None:
            unit_tized_audionames[unit_number].append(audio_name)


def get_list_for_page( page_number ):
    """
    this function look at each page of the book
    and determines whether, a media file belongs there,
    we can filter the media files buy unit number first ( using unit_pages )
    and then page number.
    """
    Local_audio_files = None
    Local_video_files = None
    unit_number = None
    #Find Page unit Number
    for key, val in unit_pagesm.items():
        if val[0] <= page_number and page_number<= val[1]:
            unit_number = int(key.replace("u-", ""))
            break

    if isinstance(unit_number,int):
        # Get path to All Media Files With that Unit Number
        Local_audio_files = unit_tized_audionames[unit_number].copy()
        Local_video_files = unit_tized_videonames[unit_number].copy()

        #filter Audio file names by pages
        # if an audio file is assigned to page 10, that means that it could also be pressent on the next page
        qs = f"P0*({page_number+0}|{page_number+0-1})(\D|$)"
        filtered_audio_files = [fn+".mp3" for fn in list(filter(lambda x: re.search(qs,x) != None, list_of_audio_files ))]
        filtered_video_files = []
        temp = ids_list[ page_number + pages_offset]

        if temp[2] != None:
            for head_elem_str in temp[2]:
              text_output = html.fromstring(head_elem_str).text_content()

              #region StringFormatingCode
              #EDITABLE
              string_to_match = ""
              if ":" in text_output:
                  string_to_match = text_output.split(":")[-1]
              else:
                  string_to_match = text_output
              #endregion

              #Remove All spaces
              string_to_match = string_to_match.replace(" ", "")

              for video_name in Local_video_files:

                #region EDITABLE
                temp_video_name = video_name.split(" ")[-1]
                for word in WORDS_TO_REMOVE_FROM_VIDEO_NAME:
                   ind = temp_video_name.find(word, 0, 2*len(word))
                   if ind != -1:
                      cutting_id = ind + len(word)
                      temp_video_name = temp_video_name[cutting_id:]
                      break #The moment one is matched break, because they sometimes a text can contain two matches but we only want to remove the first one

                #endregion

                res = lvsh.ratio(string_to_match, temp_video_name)


                if res > MATCHING_THRESHOLD:
                    #MATCH FOUND ADD FILE TO
                    #print(res , string_to_match, video_name)
                    filtered_video_files.append(video_name+".mp4")

        return filtered_audio_files, filtered_video_files



        #TEMP IS AN ARRAY OF [ page_number , unique_class, main_headers list, listof mainheader elements and subheader elements]
        # Get Headings

        #Get A Unit Names And Topic Names on The page

        # NOTE :: Further processing can be done here to identify specific pages for
        # each media file, but we are gona stop here, and do the rest of the stuff
        # manually

        # You can filter the video files using fuzzy string modules
    else:
       qs = f"P0*({page_number+pages_offset}|{page_number+pages_offset+1})(\D|$)"
       print(qs)
       filtered_audio_files = [ fn+".mp3" for fn in list(filter(lambda x: re.search(qs,x) != None, list_of_audio_files ))]
       return filtered_audio_files, []
    return None










# %%
#get_list_for_page(7)
# %%

# %%
def get_data () :
    matched_medias = set()
    res_dict = dict()
    for i in range(1,301):
      results = get_list_for_page(i+0)
      res_dict.update({i+pages_offset:results})
      print(i+pages_offset,results )
      if results != None:
          for d in results[1]:
            matched_medias.add(d)
          for b in results[0]:
            matched_medias.add(b)

    list_of_unassigned_audio = set([i+".mp3" for i in list_of_audio_files]).difference(matched_medias)
    list_of_unassigned_video = set([i+".mp4" for i in list_of_video_files]).difference(matched_medias)
    return res_dict , list_of_unassigned_video, list_of_unassigned_audio, ids_list

# %%
get_data()
