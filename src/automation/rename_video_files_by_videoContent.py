
"""
OCR ENGINE MODES
0   Legacy engine only
1   Neural nets LSTM engine only
2   Legacy + LSTM engines
3   Default, based on what is availabe
"""

"""
PSM  - Page Segmentation Modes
0
1
2
3
4
5
6     This worked best for Book 11 videos
7
8
9
10
11
12
13
"""

# # # Steps
## Search For the First occerence of the following text ["unit" , "episode"]
## run ocr on those two pages
## use ocr output to create a new file name
## trim video up to the first occurence of the "unit" text
##

# %%
import cv2, PIL, pytesseract, time, subprocess, datetime, re, glob
import numpy as np
myconfig = r"--psm 6 --oem 3 -l eng"

VIDEOS_PATH = r"..\assets\videos"
PROCESSED_VIDEOS_PATH = r"..\assets\pvideos"
UNIT_IMAGE_PATH = r".\unitimg.png"
EPISODE_IMAGE_PATH = r".\episodeimg.png"

# %%
import os
os.path.abspath(VIDEOS_PATH + r"\ENG 11 01 03.wmv")


# %%
# SAMPLE - extracts text from image
text = pytesseract.image_to_string( PIL.Image.open(r"C:\Users\Mubarak Salley\Desktop\testimg.png"), config=myconfig)
print(text)


# %%
circles= []
#cv2.namedWindow("The Image")
def draw_circle(event, x, y, flags, param):
    print("mouse")
    if event == cv2.EVENT_LBUTTONDOWN: # check if mouse event is click
        #cv2.circle(img, (x, y), 10, (255,0,0), -1)
        circles.append((x,y))
        print(circles)

def timestamp_from_frames ( frames, framerate):
    seconds = frames/framerate
    strr = time.strftime("%M:%S", time.gmtime(seconds))
    return strr

#cv2.setMouseCallback("The Image", draw_circle)

def get_template_image( image_file_location ):
    """
    returns w, h, img object
    """
    img = cv2.imread(image_file_location, cv2.IMREAD_GRAYSCALE)
    w, h = img.shape[::-1]
    return w, h, img

def find_image_in_video(video_filename, template_image):
    img = template_image
    # Open the video file
    cap = cv2.VideoCapture(video_filename)


    # Calculate the number of frames in the first minute
    fps = cap.get(cv2.CAP_PROP_FPS)
    tot_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print( "W type", type(w) , " ", w)
    print("H type", type(h), " ", h)
    #cap.set(cv2.CAP_PROP_FPS,fps)
    tot_duration = tot_frames/ fps
    print( tot_duration)
    #fps = cap.get(cv2.CAP_PROP_FPS)
    print("FPS : ", fps)
    num_frames = int(fps * 1.5) # First 1 Mins
    locs = []
    if isinstance(template_image , list):
        list_loc = []
    # Loop through the frames in the first minute
    for i in range(0,num_frames):#, int(fps/2) ):
        # SET FRAME INDEX
        #cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)

        # Read the frame
        ret, frame = cap.read()


        if ret:
            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # cv2.imshow( "The templat" , img)
            cv2.imshow( "The Image" , gray)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            if key == ord('p'):
                while(cv2.waitKey(5) != ord('c')):
                    temp_im = np.copy(gray)
                    for coords in circles:
                        cv2.circle(temp_im,(coords[0],coords[1]), 10, (200,0,0) ,2)
                    cv2.imshow("The Image",temp_im)
                    keyy = cv2.waitKey(1)
                    if keyy == ord('s'):
                        roi = gray[ circles[0][1]:circles[1][1], circles[0][0]:circles[1][0]  ]
                        cv2.imwrite('captimg.png', roi)
            # Try to find the image in the frame
            if isinstance(template_image , list):

                for z in range(len(template_image)):
                    list_loc.append( list())
                for z in range(len(template_image)):
                    res = cv2.matchTemplate(gray, template_image[z], cv2.TM_CCOEFF_NORMED)

                    res11 = cv2.minMaxLoc(res)
                    threshold = 0.8
                    loc = np.where(res >= threshold)
                    if res11[1] > threshold:

                        cv2.imshow(f"MATCH {z}", gray)
                        list_loc[z].append( (cap.get(cv2.CAP_PROP_POS_FRAMES),timestamp_from_frames(i, fps), time.strftime("%M:%S", time.gmtime(time_ms/1000) ), loc, res11) )
            else:
                res = cv2.matchTemplate(gray, template_image, cv2.TM_CCOEFF_NORMED)
                res11 = cv2.minMaxLoc(res)
                threshold = 0.8
                loc = np.where(res >= threshold)
                if res11[1] > threshold:
                    locs.append( ( i,timestamp_from_frames( i,fps), time_ms/1000 , loc, res11) )
        else:
            print("SKIPING")

    #Trim Video
    # GET Lowest Time
    if isinstance(template_image , list):
        first_frame = list_loc[1][0][0] if list_loc[0][0][0] > list_loc[1][0][0] else list_loc[0][0][0]

        time_to_cut_seconds = int((first_frame/tot_frames) * (tot_frames/fps))
        start_time = time.strftime("%H:%M:%S",time.gmtime(time_to_cut_seconds))
        duration = time.strftime("%H:%M:%S",time.gmtime(tot_duration -time_to_cut_seconds))
        input_file = video_filename
        output_file = PROCESSED_VIDEOS_PATH +r'\output.wmv'

        print("COMMAND : \n", f'ffmpeg -y -i "{input_file}" -ss {start_time} -c copy -t {duration} "{output_file}"')
        output = os.system(f'ffmpeg -y -i "{input_file}" -ss {start_time} -c copy -t {duration} "{output_file}"')
        print("OUTPUT : ", output)
        #cap.set(cv2.CAP_PROP_POS_FRAMES, first_frame)

        # writer = cv2.VideoWriter_fourcc)(*"WMV2")
        # out = cv2.VideoWriter(PROCESSED_VIDEOS_PATH +r'\output.wmv', writer, fps, (int(w), int(h)))

        # ret = True

        # for i in range(int(first_frame), int(tot_frames+2)):
        #     ret, frame = cap.read()
        #     if ret:
        #         out.write(frame)

        # out.release()

    else:
        pass

    cap.release()

    cv2.destroyAllWindows()
    if isinstance(template_image , list):
        return list_loc
    return locs


def find_image_in_video_V2(video_filename, template_image):
    img = template_image
    # Open the video file

    # info_command = [
    #     "ffprobe", "-v",
    #     "error", "-select_streams",
    #     "v:0", "-show_entries",
    #     "stream=width,height,r_frame_rate,duration,pix_fmt,bit_rate,bits_per_raw_sample",
    #     "-of", "csv=p=0",
    #     fr'"{os.path.abspath(video_filename)}"'
    #     ]

    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
           'stream=width,height,r_frame_rate,duration,pix_fmt,bit_rate,bits_per_raw_sample',
           '-of', 'csv=p=0', os.path.abspath(video_filename)]
    print("COMMAND \n", " ".join(command))

    pipe=  subprocess.Popen( command, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=100*8)
    pipe.wait()
    info_output = pipe.stdout.read().decode("utf-8").split(",")
    pipe.terminate()

    w,h,pix_fmt,fps,tot_duration, bit_rate, bits_dept = info_output
    frame_size_bytes = (int(bit_rate)/int(fps.split("/")[0])) / 8
    print(w,h,fps,tot_duration,pix_fmt,bit_rate,bits_dept, frame_size_bytes, sep="\n")


    # TIME TO READ FRAMES
    base_time = datetime.datetime.strptime("00:00:00", "%H:%M:%S")
    start_time = '00:00:00'
    end_time = '00:03:30'

    start_sec =  (datetime.datetime.strptime(start_time, "%H:%M:%S") - base_time).total_seconds()
    end_sec =   (datetime.datetime.strptime(end_time, "%H:%M:%S") - base_time).total_seconds()

    print( "TIME " , start_sec , " ", end_sec )
    time_step = '25'
    command_rf = [
    'ffmpeg',
    "-loglevel" , "quiet", # This line prevents some text info data from being printed
    '-ss', start_time,
    '-i', os.path.abspath(video_filename),
    '-t', str(end_sec - start_sec),
    '-vf', f"select=not(mod(n+1\,{time_step}))", #This skips frames #added 1 to n so that modulo skip is consistent
    '-f', 'image2pipe',
    '-pix_fmt', 'gray', # use rgb24 for color
    '-vcodec', 'rawvideo',
    '-']
    print("COMMAND : \n", " ".join(command_rf))
    cc  = 1 # Color Channels
    frame_size = int(h)* int(w)* cc
    frame_shape = (int(h), int(w), cc)
    pipe2 = subprocess.Popen(command_rf, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=(10**6) * 3 ) # Buff Size = 5 mb

    # temphold = pipe.stdin.read(frame_size)
    # for i in range(frame_size):
    #     temphold[i].
    #pipe2.stdout.flush()

    #stdout , err = pipe2.communicate()
    #raw_image = stdout
    raw_image = b''
    count = 0
    frame_step = int(time_step) - 1
    time_per_frame = 1/int(fps.split("/")[0])
    current_frame_time_sec = - time_per_frame
    list_outs = []
    threshold = 0.8
    appending_last = False
    appending_last_stopped = False
    stopped_padding = 50
    for i in range(len(template_image)):
        list_outs.append(list())

    while True:
        current_frame_time_sec += time_per_frame
        next_chunk = pipe2.stdout.read(frame_size)
        time_stp_str =time.strftime("%H:%M:%S", time.gmtime(start_sec + current_frame_time_sec))
        if not next_chunk:
            break
        raw_image = next_chunk
        #image_array = np.frombuffer(raw_image[count * frame_size : (count + 1)*frame_size], dtype='uint8').reshape(*frame_shape )
        image_array = np.frombuffer(raw_image[0 * frame_size : (0 + 1)*frame_size], dtype='uint8').reshape(*frame_shape )

        #region runDetection
        for i in range(len(template_image)):
            res = cv2.matchTemplate( image_array, template_image[i], cv2.TM_CCOEFF_NORMED)
            _ , val, _, pos = cv2.minMaxLoc( res )
            if ( val > threshold):
                list_outs[i].append( ( time_stp_str, current_frame_time_sec , val, pos) )
                # if i == (len(template_image) - 1):
                #     appending_last = True
            # else:
            #     if appending_last == True and stopped_padding == 0:
            #         appending_last_stopped = True
            #     elif appending_last == True:
            #         stopped_padding -= 1
            #         print('reducing')
        #endregion

        # image_array= cv2.putText(image_array, time_stp_str, (100,100),cv2.FONT_HERSHEY_PLAIN, 1, (255,), 1)
        # cv2.imshow("testing", image_array)
        # if cv2.waitKey(1) == ord('q'):
        #     break
        #print("Loped")
        count = count + 1
        # if appending_last_stopped:
        #     break

    #print(raw_image[0:10])
    #cv2.destroyAllWindows()
    pipe2.terminate()


    # Get FRAME and extract Text
    matched_text = []
    for i in range(len(template_image)):
        if len(list_outs[i]) > 2:
            #Get Middle frame
            mid_frame_time_sec = int((list_outs[i][0][1] + list_outs[i][-1][1])/2)
            command_mf = ['ffmpeg', '-ss', time.strftime("%H:%M:%S",time.gmtime(start_sec + mid_frame_time_sec)), '-i', os.path.abspath(video_filename), '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
            processs = subprocess.run(command_mf, bufsize=3*(10**6), stdout=subprocess.PIPE, check=True)
            frame_data = processs.stdout

            image_data = np.frombuffer( frame_data, dtype='uint8').reshape(frame_shape[0], frame_shape[1], 3)
            ret , filtered_img = cv2.threshold(image_data, 200,255,cv2.THRESH_BINARY)

            pil_img = PIL.Image.fromarray(filtered_img)

            #region Testing PSM and OEM Options
            # for z in range(14*4):
            #     try:
            #         i1 = int(z/13)
            #         i2 = z%14
            #         print( i ,"-",i1,".",i2, " " )
            #         myconfig = fr"--psm {i2} --oem {i1} -l eng"
            #         text = pytesseract.image_to_string(pil_img,config=myconfig)
            #         print(text)
            #     except:
            #         pass
            #endregion

            #region FinalDecision
            myconfig = fr"--psm 3 --oem 1 -l eng"
            text = pytesseract.image_to_string(pil_img,config=myconfig)
            print(text)
            matched_text.append(text)
            #endregion


            cv2.imshow("Mid Frame", filtered_img)
            cv2.waitKey(1)
    cv2.destroyAllWindows()


    # Create New File Name and Trim
    final_name = ""
    final_ext = ".wmv"
    #unit_text = ""
    #episode_text = ""
    for i in matched_text:

        res = re.split(r"Unit.*?\n", i)
        res2 = re.split(r"Episode.*?\n", i)
        if len(res) > 1:
            print(re.search(r"(Unit.*?)\n",i).group(1))
            print(res)
            final_name += re.search(r"(Unit.*?)\n",i).group(1)+" "+  res[-1].replace(r"\n","")
        if len(res2) > 1:
            print(res2)
            final_name +=res2[-1].replace(r"\n","")
    final_name = "_".join(final_name.splitlines())
    final_name = final_name.replace(":","__")
    print("FINAL NAME : ", final_name )
    if( final_name != ""):
        file_name = final_name + final_ext

        cmd = ["ffmpeg", "-y", "-ss", time.strftime("%H:%M:%S", time.gmtime(list_outs[0][0][1] + start_sec)), "-i", os.path.abspath(video_filename), "-to", tot_duration, "-avoid_negative_ts", "1", "-c", "copy", os.path.abspath(PROCESSED_VIDEOS_PATH + "\\" + file_name)]
        # -copyts needed to fix synchronization issue
        print(*cmd)
        p1 = subprocess.run(
            cmd, check=True
        )
        print(p1.stdout)
    return list_outs


def find_image_in_video_V3(video_filename, template_image):
    img = template_image
    # Open the video file

    # info_command = [
    #     "ffprobe", "-v",
    #     "error", "-select_streams",
    #     "v:0", "-show_entries",
    #     "stream=width,height,r_frame_rate,duration,pix_fmt,bit_rate,bits_per_raw_sample",
    #     "-of", "csv=p=0",
    #     fr'"{os.path.abspath(video_filename)}"'
    #     ]

    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
           'stream=width,height,r_frame_rate,duration,pix_fmt,bit_rate,bits_per_raw_sample',
           '-of', 'csv=p=0', os.path.abspath(video_filename)]
    print("COMMAND \n", " ".join(command))

    pipe=  subprocess.Popen( command, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=100*8)
    pipe.wait()
    info_output = pipe.stdout.read().decode("utf-8").split(",")
    pipe.terminate()

    w,h,pix_fmt,fps,tot_duration, bit_rate, bits_dept = info_output
    frame_size_bytes = (int(bit_rate)/int(fps.split("/")[0])) / 8
    print(w,h,fps,tot_duration,pix_fmt,bit_rate,bits_dept, frame_size_bytes, sep="\n")


    # TIME TO READ FRAMES
    base_time = datetime.datetime.strptime("00:00:00", "%H:%M:%S")
    start_time = '00:00:00'
    end_time = '00:03:30'
    time_step_ms = 1500

    start_sec =  (datetime.datetime.strptime(start_time, "%H:%M:%S") - base_time).total_seconds()
    end_sec =   (datetime.datetime.strptime(end_time, "%H:%M:%S") - base_time).total_seconds()
    list_of_timestamps = [ (time.strftime("%H:%M:%S", time.gmtime(i/1000)), i/1000) for i in range( int(start_sec)*1000, int(end_sec)*1000, time_step_ms)] #Steps in milliseconds

    cc  = 1 # Color Channels
    frame_size = int(h)* int(w)* cc
    frame_shape = (int(h), int(w), cc)

    threshold = 0.8

    list_outs = []
    for i in template_image:
        list_outs.append(list())

    print( "TIME " , start_sec , " ", end_sec )
    for tstmp in list_of_timestamps:
        get_frame_command = ['ffmpeg',"-loglevel" , "quiet", '-ss', tstmp[0], '-i', os.path.abspath(video_filename), '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-']
        ppf = subprocess.run(get_frame_command, stdout=subprocess.PIPE, check=True)
        frame_data = ppf.stdout
        image_array = np.frombuffer(frame_data, dtype='uint8').reshape(*frame_shape )

        #region runDetection
        for i in range(len(template_image)):
            res = cv2.matchTemplate( image_array, template_image[i], cv2.TM_CCOEFF_NORMED)
            _ , val, _, pos = cv2.minMaxLoc( res )
            if ( val > threshold):
                list_outs[i].append( ( tstmp, tstmp[1] , val, pos) )
        #endregion

        image_array= cv2.putText(image_array, tstmp[0], (100,100),cv2.FONT_HERSHEY_PLAIN, 1, (255,), 1)
        #cv2.imshow("testing", image_array)
        #if cv2.waitKey(1) == ord('q'):
        #    break

    # Get FRAME and extract Text
    matched_text = []
    for i in range(len(template_image)):
        if len(list_outs[i]) > 2:
            #Get Middle frame
            mid_frame_time_sec = int((list_outs[i][0][1] + list_outs[i][-1][1])/2)
            command_mf = ['ffmpeg', '-ss', time.strftime("%H:%M:%S",time.gmtime(start_sec + mid_frame_time_sec)), '-i', os.path.abspath(video_filename), '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-']
            processs = subprocess.run(command_mf, bufsize=3*(10**6), stdout=subprocess.PIPE, check=True)
            frame_data = processs.stdout

            image_data = np.frombuffer( frame_data, dtype='uint8').reshape(frame_shape[0], frame_shape[1], 1)
            ret , filtered_img = cv2.threshold(image_data, 183,255,cv2.THRESH_BINARY)

            pil_img = PIL.Image.fromarray(filtered_img)

            #region Testing PSM and OEM Options
            # for z in range(14*4):
            #     try:
            #         i1 = int(z/13)
            #         i2 = z%14
            #         print( i ,"-",i1,".",i2, " " )
            #         myconfig = fr"--psm {i2} --oem {i1} -l eng"
            #         text = pytesseract.image_to_string(pil_img,config=myconfig)
            #         print(text)
            #     except:
            #         pass
            #endregion

            #region FinalDecision
            myconfig = fr"--psm 3 --oem 1 -l eng"
            text = pytesseract.image_to_string(pil_img,config=myconfig)
            print(text)
            matched_text.append(text)
            #endregion


            cv2.imshow("Mid Frame", filtered_img)
            cv2.waitKey(1)
    cv2.destroyAllWindows()


    # Create New File Name and Trim
    final_name = ""
    final_ext = ".wmv"
    #unit_text = ""
    #episode_text = ""
    filename_p : str = video_filename.split("\\")[-1]
    unit_number = re.search("eng.\d+.(\d+)",filename_p, re.IGNORECASE).group(1)
    # am_spaces = filename_p.count(" ")
    # am_dots = filename_p.count(".")
    # unit_number = -1
    # if am_spaces > 1:
    #     unit_number = filename_p.split(" ")[2]
    # if am_dots > 1:
    #     unit_number = filename_p.split(".")[2]

    for i in matched_text:

        res = re.split(r"Unit.*?\n", i)
        res2 = re.split(r"Episode.*?\n", i)
        if len(res) > 1:
            print(re.search(r"(Unit.*?)\n",i).group(1))
            print(res)
            #final_name += re.search(r"(Unit.*?)\n",i).group(1)+" "+  res[-1].replace(r"\n","")
            #final_name +=  res[-1].replace(r"\n","")
        if len(res2) > 1:
            print(res2)
            final_name +=res2[-1].replace(r"\n","")
    final_name = "_".join(final_name.splitlines())
    final_name = ''.join(e for e in final_name if e.isalnum() or e == "_") # Remove all special characters
    print("FINAL NAME : ", final_name )
    if( final_name != ""):
        file_name = "U"+unit_number+" " + final_name + final_ext

        cmd = ["ffmpeg", "-y", "-ss", time.strftime("%H:%M:%S", time.gmtime(list_outs[0][0][1] + start_sec)), "-i", os.path.abspath(video_filename), "-to", tot_duration, "-avoid_negative_ts", "1", "-c", "copy", os.path.abspath(PROCESSED_VIDEOS_PATH + "\\" + file_name)]
        # -copyts needed to fix synchronization issue
        print(*cmd)
        p1 = subprocess.run(
            cmd, check=True
        )
        print(p1.stdout)
    return list_outs

def convert_all_videos ( from_ext , to_ext, absolute_dir ):
    list_res = glob.glob(absolute_dir + "\\*." + from_ext)

    for vid in list_res:
        command = [
            "ffmpeg",
            "-y",
             "-i",
             vid,
             "-c:v",
             "libx264",
             "-crf"
             , "23"
             , "-c:a"
             , "aac"
             , "-q:a"
             , "100"
             ,
             vid[0:-3] + to_ext,
        ]
        print(*command)
        output = subprocess.run(command, check=True, stdout=subprocess.PIPE)

        print("Conver Video Output : ", output)
        #break

# %%
w, h , img = get_template_image(UNIT_IMAGE_PATH)
w1, h1, img1 = get_template_image(EPISODE_IMAGE_PATH)
#results = find_image_in_video_V3(VIDEOS_PATH + r"\ENG 11 02 24 .wmv", [img,img1])
path_list = glob.glob( VIDEOS_PATH + r"\*.wmv")[61:-1]
for path in path_list:
    results = find_image_in_video_V3(path, [img,img1])
 # %%
results
# %%
# import subprocess
# import numpy as np

# timestamp = '00:01:37'
# input_file = r"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\videos\ENG 11 02 19.wmv"

# command = ['ffmpeg', '-ss', timestamp, '-i', input_file, '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-']

# process = subprocess.run(command, stdout=subprocess.PIPE, check=True)

# frame_data = process.stdout

# width = 352  # replace with actual frame width
# height = 288 # replace with actual frame height
# print(frame_data)
# frame = np.frombuffer(frame_data, dtype='uint8').reshape(height, width, 1)
# frame_cov = frame#cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# _,frame_cov1 = cv2.threshold( frame_cov, 190, 255, cv2.THRESH_BINARY)
# text = pytesseract.image_to_string(PIL.Image.fromarray(frame_cov1,"L"), config = myconfig)
# print( "TEXT : ", text)
# cv2.imshow('Frame', frame_cov1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# %%
