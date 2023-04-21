#%%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from io import StringIO
#import lxml.etree

# ADDITION UI SUPPORT MODULES
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import time

## ENABLE BROWSER LOGGING
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = {'browser':'ALL'}

# %%
import os
import time
print(os.path.abspath("."))

STAGE3_JS_SCRIPT_1 = """
let items = [
//   {
//     type: "video",
//     name: "ENG.10.02.18A.mp4",
//     position: 710,
//   },
//   {
//     type: "audio",
//     name: "59 SB10 U1 B1.4 P11.mp3",
//     position: 1200,
//   },
//   {
//     type: "h5p",
//     name: "157 SB10 U1 AE1-3.html",
//     position: 1300,
//     height: 500,
//   },
// ];

function insertContent(rootElement, items) {
  rootElement = $(rootElement);

  items.forEach((item) => {
    setItemHeight(item);
    setItemPath(item);
  });

  const sections = getSections(items);
  const sectionElements = sections.map((section) =>
    getElementsInSection(rootElement, section)
  );

  const image = rootElement.find("img");
  const imageWidth = image.width();
  const imageHeight = image.height();
  const imageSource = image
    .prop("src")
    .substring(window.location.origin.length);
  image.remove();

  function addImage(section, shiftAmount) {
    shiftAmount = shiftAmount || 0;
    const image = $(document.createElement("div"));
    const top = section.start + shiftAmount;
    const height = (section.end || imageHeight) - section.start;
    image.css({
      position: "absolute",
      top: top,
      width: imageWidth,
      height: height,
      background: `url('$\{imageSource\}')`,
      "background-size": "cover",
      "background-position-x": 0,
      "background-position-y": -section.start,
      "background-repeat": "no-repeat",
    });

    rootElement.prepend(image);
  }

  addImage({ start: 0, end: items[0].position });
  let totalContentHeight = 0;

  const padding = 10;
  items.forEach((item, index) => {
    const itemElement = createItemElement(item);
    itemElement.css("top", item.position + padding + totalContentHeight);
    rootElement.append(itemElement);

    totalContentHeight += item.height + padding * 2;
    shiftElementsDown(sectionElements[index + 1], totalContentHeight);
    addImage(sections[index + 1], totalContentHeight);
  });

  rootElement.height(rootElement.height() + totalContentHeight);
  removeGuide(rootElement);
}

function setItemHeight(item) {
  if (!item.height) {
    switch (item.type) {
      case "audio":
        item.height = 54;
        break;

      case "video":
        item.height = 491;
        break;

      default:
        throw new Error("Height not specified for item: ", item.name);
    }
  }
}

function setItemPath(item) {
  item.src = `assets/${item.type}/${item.name}`;
}

function createItemElement(item) {
  let element;

  switch (item.type) {
    case "audio":
    case "video":
      element = $(document.createElement(item.type)).prop("controls", true);
      break;

    default:
      element = $(document.createElement("iframe"));
      break;
  }

  element
    .prop("src", item.src)
    .css({ position: "absolute", height: item.height });

  return element;
}

function getSections(content) {
  const positions = content.map((c) => c.position);
  positions.unshift(0);
  const sections = [];

  for (let i = 0; i < positions.length; i++) {
    sections.push({
      start: positions[i],
      end: positions[i + 1],
    });
  }

  return sections;
}

function getElementsInSection(rootElement, section) {
  const baseOffset = rootElement.offset();
  return rootElement.find("div.t").filter(function () {
    const y = $(this).offset().top - baseOffset.top;
    return y > section.start && (section.end === undefined || y <= section.end);
  });
}

function shiftElementsDown(elements, amount) {
  elements.each(function () {
    // Shift element vertically
    let str = $(this).css("bottom");
    str = str.substring(0, str.length - 2);
    const oldPos = Number(str);
    const newPos = oldPos - amount;
    $(this).css("bottom", newPos);
  });
}

function setPage(id) {
  page = "#" + id;
  pageDiv = $(page);
  pageDiv.contextmenu(function (e) {
    e.preventDefault();
    const guide = $(document.createElement("div"))
      .css({
        position: "absolute",
        width: "100%",
        height: 5,
        background: "red",
        top: 300,
      })
      .prop("id", "guide");

    pageDiv.append(guide);

    pageDiv.on({
      mousemove: function (event) {
        guide.css({ top: event.offsetY });
      },
      click: function () {
        console.log("Position:", guide.css("top"));
        pageDiv.off("click mousemove");
      },
    });
  });
}

function removeGuide(rootElement) {
  $(rootElement).children("div#guide").remove();
}
"""

STAGE3_JS_SCRIPT_2 = """
rootElement = undefined;
items = undefined;
insertContent(rootElement, items);
"""
#%%
options = Options()
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe', options=options,desired_capabilities=d)


# %%
driver.close()

# %%
#driver.implicitly_wait()
driver.get('http://localhost:4200/?page=8')
# %%
#parser = lxml.etree.HTMLParser()

html = driver.execute_script("return document.documentElement.outerHTML")
#tree = lxml.etree.parse(StringIO(html), parser)

#print(tree)
# %%
####### AUDIO PROCESS EXCEL
## We have to be able to search by AX.X
## We have to be able to seerch by AX.X then Ex. X
## If we find Pp XX - XX then we ignore the above and put the audio at the top

####### VIDEO PROCESS EXCEL
## We have to be able to searh by AX.X|BX.X|CX.X etc.


# %%
#### THIS SECTION GOES Through the local html files in the source directory
#### THIS SECTION GETS ALL THE IDS OF THE MAIN PAGE CONTENT
#### IT also gets all elements that can potentially have an audio file under it.
import os, glob, re, lxml.etree
from lxml import html
#from html.parser import HTMLParser

page_number = 7
folderpath = r"C:/Users/Mubarak Salley/Documents\Accede/Tenacity-Book-11/src/assets/pagesBeforeAudioAndVideo"
#filepath = fr"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\pages\{page_number}.html"

html_file_names = glob.glob(folderpath + "/*.html" )
html_file_names.sort( key = lambda x : int(x.split("\\")[-1].replace(".html","")) )
print(html_file_names)


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
    print(results2)
    if results2 != []:
      # Extracts a particular class name the has the pattern ffXX, this is important for each page
      res = re.search(pattern=r"ff\w+", string=results2[0][1])
      unit_specific_class = res.group(0)

      # treedd = html.fromstring(results2.group(0))
      # arr = treedd.xpath("//span")
      # if len(arr) > 0:
      #     print("PRINTING TEXT CONTENT : ", arr[0].text_content() )

      ##print("Class " , res)
    #print("Page Number : ", i , " - " , unit_specific_class)

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
      print(results2[0])
    else:
      temp_res.append(None)
    temp_res.append(elements_results)
    #temp_res.append(elements)
    if temp_res == []:
      temp_res = None

    ids_list.append( temp_res )

print(ids_list)





# Get all the html file names in the directory using Glob




# %%
# Get Console.Log Stuff

driver.refresh()
WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# %%
#driver.execute_script( r'console.log("SUCKER")')

# %%
#time.sleep(1)
driver.execute_script( """
function setPage(id) {
  page = "#" + id;
  pageDiv = $(page);
  pageDiv.contextmenu(function (e) {
    e.preventDefault();
    const guide = $(document.createElement("div"))
      .css({
        position: "absolute",
        width: "100%",
        height: 5,
        background: "red",
        top: 300,
      })
      .prop("id", "guide");

    pageDiv.append(guide);

    pageDiv.on({
      mousemove: function (event) {
        guide.css({ top: event.offsetY });
      },
      click: function () {
        console.log("Position:", guide.css("top"));
        pageDiv.off("click mousemove");
      },
    });
  });
};

setPage("pf8")
""")

time.sleep(0.2)

# %%
for entry in driver.get_log('browser'):

    print("console: ",entry)

# %%
print("console.log(\"SUCKER\")")

# %%
ress = driver.get_screenshot_as_png()

# %%
driver.get_screenshot_as_file("last.png")

# %%
element = driver.find_element(by=By.ID, value="pf8")
print(element)
# %%
element.screenshot("pageimage.png")
# %%
import tkinter as tk
import threading, generate_mediaToPage_data, test_vosk, re
from tkinter import messagebox

#root = tk.Tk() # create root window

def center_window(root , width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):

       if messagebox.askokcancel("Quit", "Do you want to quit?"):
          for F in self.frames.items():
             F[1].on_closing()
          self.destroy()

class StartPage(tk.Frame):
    """
      This Gets the Starting Page Number And then begins the
      webdriver on
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()

    def on_closing(self):
       print("Done")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.generated_stage3json = dict()
        self._selectedItem = None
        self._pagenum = 1
        self.result_data, self.u_videos, self.u_audio, self.ids_list = generate_mediaToPage_data.get_data()
        self.positioned_medias = set()


        #List ITEM
        self.list_items_var = tk.Variable(value = [] ) # This creates a variable, kinda like an observable

        self.listbox = tk.Listbox( self , height=15, listvariable = self.list_items_var, selectmode=tk.SINGLE)
        self.listbox.config()
        self.listbox.grid(row=0,column=0,rowspan=10)
        self.listbox.bind("<<ListboxSelect>>", lambda x , y=self : y.on_listbox_itemselected(x) )
        self.listbox.bind("")

        if self._pagenum in self.result_data.keys():
            self.set_listitem( self.result_data[self._pagenum][0]+self.result_data[self._pagenum][1])
        else:
            self.set_listitem( ["NOTHING AVAILABLE"] )


        print("LIST BOX CUR SELECTED : ", self.listbox.curselection())

        #CURRENTLY SELECTED ITEM
        self.currentlySelectedVariabe = tk.StringVar(value="Non Selected")
        currentlySelected_tk = tk.Label( self , textvariable=self.currentlySelectedVariabe )
        currentlySelected_tk.grid(row=0, column=2, columnspan=3)

        #CURRENTLY PAGE NUMBER
        self.pageNumberVariabe = tk.StringVar(value=f"Page - {self._pagenum} ( {self._pagenum - generate_mediaToPage_data.pages_offset } )")
        currentlySelected_tk = tk.Label( self , textvariable=self.pageNumberVariabe )
        currentlySelected_tk.grid(row=0, column=1, columnspan=1)

        #SPLIT MEDIA BUTTON
        self.splitMediabutton = tk.Button(self, text="SPLIT MEDIA BY TIME")
        self.splitMediabutton.grid(column=2, row=1, columnspan=2)
        self.splitMediabutton["state"] = "disabled"

        #INITIATE POSITION SELECT BUTTON
        self.positionSelectbtn = tk.Button( self, text="INITIATE POSITION SELECTION",  command = lambda : self.initiate_position_code() )
        self.positionSelectbtn.grid(column=1,row=2, columnspan=3)
        self.positionSelectbtn["state"] = "disabled"

        #INITIATE POSITION DONE BUTTON
        self.donebtn = tk.Button( self, text="DONE", command= lambda : self.done() )
        self.donebtn.grid(column=4,row=2)
        self.donebtn["state"] = "disabled"

        #CLEAN ALL POSITION BUTTON
        clearAll = tk.Button(self, text="Clear All Assigned Positions")
        clearAll.grid(column=1,row=3, columnspan=4 )

        #Previous Page Button
        prevPagebtn = tk.Button(self, text="Previous Page", command= lambda : self.nextPage(isIncrement=False))
        prevPagebtn.grid(column=1, row=4)

        #Previous Media Page Button
        prevMediaPagebtn = tk.Button(self, text="Previous Media Page",command= lambda : self.nextMediaPage(isIncreament=False))
        prevMediaPagebtn.grid(column=2, row=4)

        #Next Media Page Button
        nextMediaPagebtn = tk.Button(self, text="Next Media Page" , command= lambda : self.nextMediaPage(isIncreament=True))
        nextMediaPagebtn.grid(column=3, row=4)

        #Next Page Button
        nextpagebtn = tk.Button(self, text="Next Page", command= lambda : self.nextPage(isIncrement=True))
        nextpagebtn.grid(column=4 , row=4)

        #Generate Page Button
        nextpagebtn = tk.Button(self, text="Generate New Page", command= lambda : print("t"))
        nextpagebtn.grid(column=1 , row=5)

        #Save On Next Page ?
        self.onSavePageCheckbuttonVaraibe = tk.IntVar(value=0)
        self.saveOnNextPage = tk.Checkbutton(self, text="Save on Change Page", command=lambda : self.on_pagechage_checkbox(), variable=self.onSavePageCheckbuttonVaraibe )
        self.saveOnNextPage.grid(column=2, row=5)


        # label = tk.Label(self, text="This is page 1")
        # label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Go to the start page",
        #                    command=lambda: controller.show_frame("StartPage"))
        # button.pack()

        ## INIT BROWSER
        options = Options()
        options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        self.driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe', options=options,desired_capabilities=d)

        # self.driver.get(self.get_urlstring(self._pagenum))
        # self.

    def on_closing(self):
      self.driver.close()
      print("DONE WITH ")


    @property
    def selectedItem(self):
       return self._selectedItem

    def driver_get_page( self, num ):
      try:
          url =  f'http://localhost:4200/?page={self._pagenum}'
          self.driver.get(url)
          #  driver.refresh()
          WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
      except Exception as ex:
          print("DRIVER EXCEPTiOn : " , ex)

    def initiate_position_code(self):
      page_id = self.ids_list[self._pagenum][1]
      self.driver.execute_script( """
        function setPage(id) {
          page = "#" + id;
          pageDiv = $(page);
          pageDiv.contextmenu(function (e) {
            e.preventDefault();
            const guide = $(document.createElement("div"))
              .css({
                position: "absolute",
                width: "100%",
                height: 5,
                background: "red",
                top: 300,
              })
              .prop("id", "guide");

            pageDiv.append(guide);

            pageDiv.on({
              mousemove: function (event) {
                guide.css({ top: event.offsetY });
              },
              click: function () {
                console.log("Position:", guide.css("top"));
                pageDiv.off("click mousemove");
              },
            });
          });
        };
        console.log("SETTING TO PAGE " );
        """ + f"setPage(\"{page_id}\")")
      WebDriverWait(self.driver, 5).until( EC.presence_of_all_elements_located((By.ID, "page" )) )
      element = self.driver.find_element( By.ID, page_id)

      self.driver.execute_script("""
      var targetElement =document.getElementById(""" + f"\"{page_id}\"" + """ );

      // Create a new mouse event
      var event = new MouseEvent("contextmenu", {
        bubbles: true,
        cancelable: true,
        view: window
      });

      // Dispatch the event to the target element
      targetElement.dispatchEvent(event);
      """)
      ActionChains(driver=self.driver).context_click(element)

    def done(self):
      generated_json = None
      px = -1 # position pixels
      # Get Position
      # Create Data Structure
      if self.selectedItem[-3:] == "wmv":
          filename = generate_mediaToPage_data.PVIDEO_FOLDER_PATH +"\\"+ self.selectedItem
      elif self.selectedItem[-3:] == "mp3":
          filename = generate_mediaToPage_data.AUDIO_FOLDER_PATH + "\\"+ self.selectedItem
      else:
         messagebox.showwarning("Selected Item", "SELECTED IT IS NOT AUDIO OR VIDEO FILE ? Click Done Again After selecting an item." )
         return

      #GET POSITION DATA
      for entry in self.driver.get_log('browser'):
        print("console: ",entry)
        search_ress = re.search( r"\"Position:\"\s*\"(\d*)px",entry["message"] )
        if search_ress != None:
           px = search_ress.group(1)
           print("px ",px)
           break

      if px == -1:
          messagebox.showwarning("Done Operation", f"position value is -1")
          return


      if test_vosk.file_exists(filename):
          dur = test_vosk.get_file_duration_ffmpeg(filename)
          generated_json = test_vosk.generate_main_mediafilejson(filename, duration=dur, position=[ self._pagenum, px ])
      else:
         messagebox.showwarning("Selected Item", f"Test_vosk says the file does not exist, are your paths correct ? {filename}" )
         return

      print(generated_json)

      if generated_json != None:
          if self._pagenum not in self.generated_stage3json.keys():
            self.generated_stage3json.update({ self._pagenum : []} )
          self.generated_stage3json[self._pagenum].append(generated_json)
          self.positioned_medias.add(self.selectedItem)

      self.selectedItem = "None Selected"
      print(self.generated_stage3json)
      print(self.positioned_medias)
      self.format_list()

    def onGeneratePageButton(self):
       page_id = self.ids_list[self._pagenum][1]



    @selectedItem.setter
    def selectedItem(self, val):
       self._selectedItem = val
       self.currentlySelectedVariabe.set(val)
       self.on_selectedItem_ButtonStateChange()

    def on_listbox_itemselected(self,event : tk.Event):
       #print("ON LISTBOX ITEM SELECTED TRIGGERED")
       selected_indices = self.listbox.curselection()
       if selected_indices != () :
          selected_object = self.listbox.get(selected_indices)
          self.currentlySelectedVariabe.set(selected_object)
          self.selectedItem = selected_object
       else:
          selected_object = "NONE SELECTED ATM"
          self.selectedItem = None

    def set_listitem (self, val):
       valuess = val + self.get_unassigned_list()
       self.list_items_var.set(valuess)
       self.format_list()

    def format_list(self):
        listss = self.list_items_var.get()
        for i in range(len(listss)):
          self.listbox.itemconfig( i , { "bg":"green" if listss[i] in self.positioned_medias else "white"}  )

    def get_unassigned_list(self):
       return [ "", "UNASSIGNED ITEMS" , "" ] + list(self.u_audio) + list(self.u_videos)

    def set_page ( self,  page , isBookPageNum = True ):
       curr_offset = 0
       if isBookPageNum:
          curr_offset = generate_mediaToPage_data.pages_offset
       if page:
          page_number = page - curr_offset
          self._pagenum = page_number
          #LOAD PAGE - IF PAGE NOT POSSIBLE RETURN
          self.driver_get_page(self._pagenum)

          self.pageNumberVariabe.set(value=f"Page - {self._pagenum} ( {self._pagenum - generate_mediaToPage_data.pages_offset } )")
          if self._pagenum in self.result_data.keys():
             outpp = self.result_data[self._pagenum][0] + self.result_data[self._pagenum][1]
             self.set_listitem( outpp)
             self.selectedItem = "Nothing Selected"
             if outpp == []:
                self.set_listitem(["NOTHING AVAILABLE"])
          else:
             self.set_listitem(["NOTHING AVAILABLE"])
             self.selectedItem = "Nothing Selected"

    def nextMediaPage(self , isIncreament = True ):
       step_direction = 0
       # Requires Extra Logic
       if isIncreament:
          step_direction = 1
          end = len(self.result_data)
       else:
          step_direction =-1
          end = 0

       for i in range( self._pagenum + step_direction , end , step_direction):
          if i in self.result_data.keys():
             if self.result_data[i][0] + self.result_data[i][1] != []:
                self.set_page(i , isBookPageNum=False)
                break
       self.currentlySelectedVariabe.set(value="MEDIA PAGE NOT FOUND, TRY OPPOSITE DIRECTION")

    def nextPage(self , isIncrement = True):
       if isIncrement:
          self.set_page( self._pagenum + 1, isBookPageNum=False)

       else:
          self.set_page( self._pagenum - 1, isBookPageNum=False)

    def on_selectedItem_ButtonStateChange(self ):

       listofbutton = [
          self.splitMediabutton,
          self.donebtn,
          self.positionSelectbtn
       ]

       state = "normal" if self._selectedItem != None else "disabled"

       for i in  listofbutton:
          i["state"] = state

    def on_pagechage_checkbox(self):
       widget : tk.IntVar= self.onSavePageCheckbuttonVaraibe
       state = "Checked" if widget.get() == 1 else "Unchecked"
       print("Check Box State: ", state)






class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def on_closing(self):
       print("Done")



def thread_func():
  root = SampleApp()
  center_window(root, width=700, height=700)
  root.mainloop()

# %%
#thd = threading.Thread(target=thread_func)
#thd.daemon = True # Background thread will exit if main thread closes
#thd.start()
thread_func()
# %%
#thd.is_alive()
# %%
myframe = tk.Frame()

# %%
## COMMAND FOR SPLITTING MEDIA FILE FROM ONE TIMESTAMP TO ANOTHER
## ffmpeg -i "./src/assets/audio/SB11 R1 G1 P91.mp3" -acodec copy -ss 00:00:00 -t 00:00:30 "./src/assets/audio/SB11 R1 G1 P91_plus30.mp3"
## COMMAND FOR GETTING AUDIO DURATION
## ffprobe -i "./src/assets/audio/SB11 R1 G1 P91.mp3" -show_entries format=duration -v quiet -of csv="p=0" -sexagesimal
## duration output is in the format hours : minutes : seconds . microseconds
