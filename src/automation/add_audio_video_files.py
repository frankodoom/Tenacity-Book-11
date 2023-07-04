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
from selenium.webdriver.common.keys import Keys
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

GLOBAL_ADDED_ITEM = new Array();

var cumulativeOffset = function(element , tillparent = undefined) {
  var top = 0, left = 0;
  do {
      top += element.offsetTop  || 0;
      left += element.offsetLeft || 0;
      if (element == tillparent){
          break;
      }

      element = element.offsetParent;
  } while(element);

  return {
      top: top,
      left: left
  };
};

function sortdividers (a,b){ if (a.type == b.type && a.type == "divider"){return 0}else if (a.type == "divider"){return 1;}else if(b.type == "divider"){return -1;}else{return 0}}

function removeElementsBetweenDividers(page_id,page_element = undefined){
  if (page_element == undefined){
    rootelement = $("#"+page_id);
  }
  else{
    rootelement = page_element;
  }

  dividers = rootelement.find("div.divider");
  startpos = -1
  stoppos = -1
  if( dividers.length == 1){
    stoppos = 99999999;
    startpox = cumulativeOffset(dividers[0], rootelement[0]).top;
  }
  if(dividers.length == 2){
    topArray = new Array();
    dividers.each(function(index){
      topArray.push(cumulativeOffset(this, rootelement[0]).top)
    })
    topArray.sort(function(a,b){ if(a>b){return 1;}else{return -1} });
    startpos = topArray[0];
    stoppos = topArray[1];
  }

  toremove = new Array();
  topush = new Array();
  rootelement.find("div.t").each(
    function (index){
      pos = cumulativeOffset(this,rootelement[0]).top;
      console.log(pos);
      if( startpos <pos && pos < stoppos){
          toremove.push(this);
      }
      if (pos > stoppos ){
          topush.push(this);
      }
    }
  )

  GLOBAL_ADDED_ITEM.forEach( function (i){
    console.log("ADDING GLOBAL ITEMS : ")
    pos = cumulativeOffset(i[0], rootelement[0]).top;
    console.log(pos);

    if( startpos <pos && pos < stoppos){
      //toremove.push(i);
      console.log("Skip Reomve");
    }
    if (pos > stoppos ){
        console.log("Added item");
        topush.push(i);
    }
  });

  // toremove.forEach( function(i){
  //   console.log(i)
  //   i.remove();
  // })

  image_holders = rootelement.find("div.imageholder").each(
    function(index){
      pos = cumulativeOffset(this,rootelement[0]).top;
      posbot = pos + this.getBoundingClientRect().height
      if (pos < stoppos && pos > startpos){
        toremove.push(this);
      }
      else if( posbot < stoppos && posbot > startpos){
        toremove.push(this);
      }
      else if ( posbot > stoppos && pos > stoppos){
        topush.push(this);
      }



    });
  // if (image_holders.length >= 2){
  //   topush.push(image_holders[0]);
  //   //image_holders[1].remove()
  //   toremove.push(image_holders[1]);

  // }

  // topush.forEach( function(i){
  //   var jqel = $(i);
  //   if (jqel.hasClass("imageholder")){
  //     console.log("Image Element Gotten : ");
  //     console.log(jqel);
  //     var current_val = Number(jqel.css("top").replace("px",""));
  //     var new_val = current_val - ( stoppos - startpos);
  //     jqel.css("top", String(new_val)+"px");
  //   }
  //   else{
  //     var current_val = Number(jqel.css("bottom").replace("px",""));
  //     var new_val = current_val + ( stoppos - startpos);
  //     jqel.css("bottom", String(new_val)+"px");
  //   }

  // });


  //original_height = rootelement.height();
  //rootelement.height( original_height - (stoppos - startpos))

  return [ toremove , topush, stoppos - startpos ]
}

function performDividerRemoveAction( rootelement , thearray ){
  toremove = thearray[0];
  topush = thearray[1];
  heightDiff = thearray[2];

  toremove.forEach( function(i){
    console.log(i)
    i.remove();
  });

  topush.forEach( function(i){
    var jqel = $(i);
    if (!jqel.hasClass("t")){
      console.log("Image Element Gotten : ");
      console.log(jqel);
      var current_val = Number(jqel.css("top").replace("px",""));
      var new_val = current_val - ( heightDiff);
      jqel.css("top", String(new_val)+"px");
    }
    else{
      var current_val = Number(jqel.css("bottom").replace("px",""));
      var new_val = current_val + ( heightDiff );
      jqel.css("bottom", String(new_val)+"px");
    }

  });

  original_height = rootelement.height();
  rootelement.height( original_height - heightDiff);

}

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
  image.css("visibility", "hidden");

  function addImage(section, shiftAmount) {
    shiftAmount = shiftAmount || 0;
    const image = $(document.createElement("div"));
    image.addClass("imageholder");
    const top = section.start + shiftAmount;
    const height = (section.end || imageHeight) - section.start;
    image.css({
      position: "absolute",
      top: top,
      width: imageWidth,
      height: height,
      background: `url('${imageSource}')`,
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
  return rootElement;
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

      case "divider":
        break;

      case "inh":
        item.height =60;
        break;

      case "dict":
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
    case "divider":
      element=$(document.createElement("div"));
      element.addClass("divider");
      break;
    case "dict":
      elementdd = document.createElement("app-dictation");
      elementdd.setAttribute("title", item.title);
      elementdd.setAttribute("text", item.text);
      elementdd.setAttribute("src", item.src)
      //elementdd.setAttribute("src", item);
      //item.type = "audio"
      element = $(elementdd)
      break

    case "inh":
      elementdd = document.createElement("div")
      elementdd.setAttribute("style","width:100%;")
      elementdd.innerHTML = item.text
      element = $(elementdd)
      break;

    default:
      element = $(document.createElement("iframe"));
      break;
  }

  element
    .prop("src", item.src)
    .css({ position: "absolute", height: item.height });

  GLOBAL_ADDED_ITEM.push(element);
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

  pageset_val = pageDiv.attr("page-set") == "true"

  if( !pageset_val){
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
        console.log(event)
        guide.css({ top: event.offsetY });
      },
      click: function () {
        console.log("Position:", guide.css("top"));
        pageDiv.off("click mousemove");
      },
    });
  });
  pageDiv.attr("page-set", true)
  }

}

function removeGuide(rootElement) {
  $(rootElement).children("div#guide").remove();
}

function sortdividers (a,b){ if (a.type == b.type && a.type == "divider"){return 0;}else if (a.type == "divider"){return 1;}else if(b.type == "divider"){return -1;}else{return 0;}}

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
import threading, generate_mediaToPage_data, test_vosk, re, audio_to_text
from tkinter import messagebox, filedialog, simpledialog
import json

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
        self.positioned_medias = dict()


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
        nextpagebtn = tk.Button(self, text="Generate New Page", command= lambda : self.onGeneratePageButton() )
        nextpagebtn.grid(column=1 , row=5)

        #Save On Next Page ?
        self.onSavePageCheckbuttonVaraibe = tk.IntVar(value=0)
        self.saveOnNextPage = tk.Checkbutton(self, text="Save on Change Page", command=lambda : self.on_pagechage_checkbox(), variable=self.onSavePageCheckbuttonVaraibe )
        self.saveOnNextPage.grid(column=2, row=5)

        #Add Divider Button
        prevPagebtn = tk.Button(self, text="Add Divider", command= lambda : self.add_dividers())
        prevPagebtn.grid(column=1, row=6)

        #Done Divider Button
        prevMediaPagebtn = tk.Button(self, text="Done Divider",command= lambda : self.done_divider())
        prevMediaPagebtn.grid(column=2, row=6)

        #Clear Divider Button
        nextMediaPagebtn = tk.Button(self, text="Clear Dividers" , command= lambda : self.clear_dividers() )
        nextMediaPagebtn.grid(column=3, row=6)


        #Add Divider Button
        prevPagebtn = tk.Button(self, text="Split Selected Media", command= lambda : self.onSplitSelectedMedia() )
        prevPagebtn.grid(column=1, row=7)

        self.fromMinVar = tk.IntVar()
        self.fromSecVar = tk.IntVar()

        #From Min Spin
        self.from_minspin = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.fromMinVar, width=2,command=lambda : self.time_duration_update())
        self.from_minspin.grid(column=2, row=7)

        #From Sec Spin
        self.from_secspin = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.fromSecVar, width=2,command=lambda : self.time_duration_update())
        self.from_secspin.grid(column=3, row=7)

        self.toMinVar = tk.IntVar()
        self.toSecVar = tk.IntVar()

        #to Min Spin
        self.to_minspin = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.toMinVar, width=2,command=lambda : self.time_duration_update())
        self.to_minspin.grid(column=4, row=7)

        #From Sec Spin
        self.to_secspin = tk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.toSecVar, width=2,command=lambda : self.time_duration_update())
        self.to_secspin.grid(column=5, row=7)

        #Add Dictation Button
        self.add_dictation_button = tk.Button(self, text="Add Dictation", command= lambda : self.insert_dictation())
        self.add_dictation_button.grid(column=1, row=9)

        #Add Quizz header
        self.add_dictation_button = tk.Button(self, text="Add Quizz Header",command= lambda : self.insert_interactionquizz_header())
        self.add_dictation_button.grid(column=2, row=9)

        #Add H5pHtml
        self.add_h5pframe_button = tk.Button(self, text="Add H5p Html",command= lambda : self.insert_h5p())
        self.add_h5pframe_button.grid(column=3, row=10)

        #Clear Stage 3 Json
        self.add_h5pframe_button = tk.Button(self, text="Clear Stage 3 Json",command= lambda : self.clear_stage3json())
        self.add_h5pframe_button.grid(column=3, row=9)


        #Add Dictation Button
        self.gotoPage = tk.Button(self, text="Go To Specific Page Number", command= lambda : self.onGoToSpecificPage())
        self.gotoPage.grid(column=1, row=10)

        #Shift Media Button
        self.shiftMedia = tk.Button(self, text="Shift Media to Next Page", command= lambda : self.shift_media_to_page(next_page=True))
        self.shiftMedia.grid(column=1, row=11)


        # #Add Quizz header
        # self.add_dictation_button = tk.Button(self, text="Add Quizz Header",command= lambda : self.insert_interactionquizz_header())
        # self.add_dictation_button.grid(column=2, row=9)

        #Clear Divider Button
        # nextMediaPagebtn = tk.Button(self, text="Clear Dividers" , command= lambda : self.clear_dividers() )
        # nextMediaPagebtn.grid(column=3, row=6)


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
      try:
          self.driver.close()
      except:
         pass
      print("DONE WITH ")

    def onGoToSpecificPage(self):
       resultsss = simpledialog.askinteger("Select Page", "What is the Specific Page number ?")
       if isinstance(resultsss,int) and resultsss > 0:
          self.set_page(resultsss , False)

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

  pageset_val = pageDiv.attr("page-set") == "true"

  if( !pageset_val){
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
        console.log(event)
        guide.css({ top: event.offsetY });
      },
      click: function () {
        console.log("Position:", guide.css("top"));
        pageDiv.off("click mousemove");
      },
    });
  });
  pageDiv.attr("page-set", true)
  }

}

function removeGuide(rootElement) {
  $(rootElement).children("div#guide").remove();
}
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
      #ActionChains(driver=self.driver).context_click(element)

    def add_dividers(self):
      """A divider is a element used to help determine which elements to delete from a page"""
      self.initiate_position_code()

    def done_divider(self):
       list_positions = []
       px = -1
       for entry in self.driver.get_log('browser'):
        print("console: ",entry)
        search_ress = re.search( r"\"Position:\"\s*\"(\d*)px",entry["message"] )
        if search_ress != None:
           px = search_ress.group(1)
           print("px ",px)
           list_positions.append(px)

       if list_positions != []:
          last_div = 0
          for divider in list_positions:
             height = 1
             if last_div == None:
                height =  last_div  - int(divider)
             gened_json = test_vosk.generate_main_mediafilejson("", "", "div", 0, height=height, position=[self._pagenum, int(divider)])
             last_div = int(divider)
             if self._pagenum in self.generated_stage3json.keys():
                self.generated_stage3json[self._pagenum].append(gened_json)
             else:
                self.generated_stage3json.update({self._pagenum:[]})
                self.generated_stage3json[self._pagenum].append(gened_json)


       print(list_positions)

    def clear_dividers(self):
       if self._pagenum in self.generated_stage3json.keys():
          temp = self.generated_stage3json[self._pagenum]
          self.generated_stage3json[self._pagenum] = [i for i in temp if i["mediaType"] != "div"]

    def time_duration_update(self):
       print("from : ", f"{self.fromMinVar.get():02}", f"{self.fromSecVar.get():02}")
       print("to : ", f"{self.toMinVar.get():02}" , f"{self.toSecVar.get():02}")

    def onSplitSelectedMedia(self):
       from_sec = (self.fromMinVar.get() * 60 ) + self.fromSecVar.get()
       to_sec = (self.toMinVar.get() * 60 ) + self.toSecVar.get()

       if to_sec > from_sec and self.selectedItem != None :
          #Proceed
          if self.selectedItem[-3:] == "mp4":
              filename = generate_mediaToPage_data.PVIDEO_FOLDER_PATH +"\\"+ self.selectedItem
          elif self.selectedItem[-3:] == "mp3":
              filename = generate_mediaToPage_data.AUDIO_FOLDER_PATH + "\\"+ self.selectedItem
          else:
              messagebox.showwarning("Split Media", "SELECTED IT IS NOT AUDIO OR VIDEO FILE ? Click Done Again After selecting an item." )
              return
          ftstartTime = time.strftime("%M_%S", time.gmtime(from_sec))
          ftstopTime = time.strftime("%M_%S", time.gmtime(to_sec))
          appendication = f"{ftstartTime}__{ftstopTime}"
          #test_vosk.generate_splited_medifilejson()
          new_filename= filename[::-1].replace(".", f"{appendication}."[::-1],1)[::-1]

          if not messagebox.askokcancel("Proceed ? ", f"Are you sure you want to create : {new_filename}"):
            return

          int_res = test_vosk.split_media(filename , from_sec, to_sec, new_filename)

          if int_res == 0:
             listss = self.list_items_var.get()
             listss = list(listss)
             indx = listss.index(self.selectedItem)
             listss.insert(indx + 1, new_filename.split("\\")[-1])
             self.list_items_var.set(listss)

             indx = 0 if self.selectedItem[-3:] == "mp3" else 1
             self.result_data[self._pagenum][indx].append(new_filename.split("\\")[-1])
             self.result_data[self._pagenum +1][indx].append(new_filename.split("\\")[-1])
             self.result_data[self._pagenum -1][indx].append(new_filename.split("\\")[-1])

    def save_page_data (self):
       data = json.dumps(self.result_data[self._pagenum], indent=4)
       stage_3json = json.dumps(self.generated_stage3json[self._pagenum])

       with open(f"./saved_data/page{self._pagenum}.json", "w") as opejsn:
          opejsn.write(data)
       with open(f"./saved_data/page{self._pagenum}s3.json", "w") as opejsn:
          opejsn.write(data)

       messagebox.showinfo("Save","Save Successfull")

    def load_page_data (self):
       if os.path.exists(f"./saved_data/page{self._pagenum}.json"):
          self.result_data[self._pagenum]= json.load(f"./saved_data/page{self._pagenum}.json")
          self.generated_stage3json[self._pagenum] = json.load(f"./saved_data/page{self._pagenum}s3.json")
          self.set_page(self._pagenum,False)

    def load_h5p (self):
       pass

    def insert_dictation(self):
       audio_file_path = filedialog.askopenfilename(initialdir="./", title="Select Dictation Audio File", filetypes=[("audio", "*.mp3")])
       audio_filename = audio_file_path.split("/")[-1]
       resultt = audio_to_text.convert_audio_to_text(audio_file_path)
       if not isinstance(resultt,str):
          messagebox.showerror("AudioToText", "Audio to text transformation failed")
          return
       title_str = simpledialog.askstring("Dictation Title", "What is the title of the dictation ?",initialvalue="")


       self.initiate_position_code()
       messagebox.showinfo("Select Position", "Select the position of the dictation then close the dialog")

       px = None
       for entry in self.driver.get_log('browser'):
        print("console: ",entry)
        search_ress = re.search( r"\"Position:\"\s*\"(\d*)px",entry["message"] )
        if search_ress != None:
           px = search_ress.group(1)
           print("px ",px)

       if px != None:
          #prefered_height = simpledialog.askstring("Dictation Title", "What is the title of the dictation ?",initialvalue="")
          height = 4 * 54 + (len(resultt)/92) * 29

          dict_obj = test_vosk.generate_main_mediafilejson(audio_filename,audio_file_path,"dict",height=height,title=title_str, text=resultt,position=[self._pagenum, px])
          print("Dict obj", dict_obj)

          if self._pagenum in self.generated_stage3json.keys():
              self.generated_stage3json[self._pagenum].append(dict_obj)
          else:
              self.generated_stage3json.update({self._pagenum : []})
              self.generated_stage3json[self._pagenum].append(dict_obj)

    def insert_interactionquizz_header(self):
       htmlstring = """<h1 class="exercise">INTERACTIVE EXERCISES</h1>"""
       typeee = "inh" #innerhtml element
       posi = None

       self.initiate_position_code()
       messagebox.showinfo("Select Position", "Select the position of the dictation then close the dialog")

       px = None
       for entry in self.driver.get_log('browser'):
        print("console: ",entry)
        search_ress = re.search( r"\"Position:\"\s*\"(\d*)px",entry["message"] )
        if search_ress != None:
           px = search_ress.group(1)
           print("px ",px)

       if px!=None:
         generated_json = test_vosk.generate_main_mediafilejson("", "", typeee, text=htmlstring, position=[ self._pagenum, px])

         print("Header obj", generated_json)

         if self._pagenum in self.generated_stage3json.keys():
              self.generated_stage3json[self._pagenum].append(generated_json)
         else:
            self.generated_stage3json.update({self._pagenum : []})
            self.generated_stage3json[self._pagenum].append(generated_json)

    def insert_h5p(self):
       h5p_file_path = filedialog.askopenfilename(initialdir="./", title="Select H5p File", filetypes=[("html", "*.html")])
       h5p_filename = h5p_file_path.split("/")[-1]

      #  if not isinstance(resultt,str):
      #     messagebox.showerror("AudioToText", "Audio to text transformation failed")
      #     return
       #title_str = simpledialog.askstring("Dictation Title", "What is the title of the dictation ?",initialvalue="")


       self.initiate_position_code()
       messagebox.showinfo("Select Position", "Select the position of the dictation then close the dialog")

       px = None
       for entry in self.driver.get_log('browser'):
        print("console: ",entry)
        search_ress = re.search( r"\"Position:\"\s*\"(\d*)px",entry["message"] )
        if search_ress != None:
           px = search_ress.group(1)
           print("px ",px)

       selectLinkOpeninNewTab = Keys.COMMAND + "t"
       #self.driver.find_element(By.TAG_NAME, "body").send_keys(selectLinkOpeninNewTab)


       #self.driver.execute_script("window.open()")
       self.driver.switch_to.new_window(type_hint="tab")
       #WebDriverWait(self.driver)
       self.driver.get(h5p_file_path)

       height = simpledialog.askinteger("H5p Html", "What is the height of the h5p html in px ?",initialvalue="")
       #self.driver.switch_to.window( self.driver.window_handles[0])
       self.driver.close()
       self.driver.switch_to.window(self.driver.window_handles[0])
       #self.driver_get_page(self._pagenum)
       if px != None:
          #prefered_height = simpledialog.askstring("Dictation Title", "What is the title of the dictation ?",initialvalue="")
          #height = 4 * 54 + (len(resultt)/92) * 29

          dict_obj = test_vosk.generate_main_mediafilejson(h5p_filename,h5p_file_path,"h5p",height=height,title=None, text=None, position=[self._pagenum, px])
          print("Dict obj", dict_obj)

          if self._pagenum in self.generated_stage3json.keys():
              self.generated_stage3json[self._pagenum].append(dict_obj)
          else:
              self.generated_stage3json.update({self._pagenum : []})
              self.generated_stage3json[self._pagenum].append(dict_obj)

    def clear_stage3json(self):
       self.generated_stage3json.update({self._pagenum : []})
       self.positioned_medias.update({self._pagenum: set()})
       self.format_list()
      #  if self._pagenum in self.generated_stage3json.keys():
      #         self.generated_stage3json[self._pagenum].append(dict_obj)
      #     else:
      #         self.generated_stage3json.update({self._pagenum : []})
      #         self.generated_stage3json[self._pagenum].append(dict_obj)

    def done(self):
      generated_json = None
      px = -1 # position pixels
      # Get Position
      # Create Data Structure
      if self.selectedItem[-3:] == "mp4":
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
          if self.selectedItem not in self.positioned_medias.get(self._pagenum):
              generated_json = test_vosk.generate_main_mediafilejson(filename.split("\\")[-1],filename,filename[-3:],duration=dur, position=[ self._pagenum, px ])
          else:
             for i in range(len(self.generated_stage3json[self._pagenum])):
                if self.generated_stage3json[self._pagenum][i][test_vosk.mfjf.MEDIAFILENAME.value] == self.selectedItem:
                   print("Updating Existing Value")
                   self.generated_stage3json[self._pagenum][i][test_vosk.mfjf.POSITION.value] = [self._pagenum, int(px)]
                   break

      else:
         messagebox.showwarning("Selected Item", f"Test_vosk says the file does not exist, are your paths correct ? {filename}" )
         return

      print(generated_json)

      if generated_json != None:
          if self._pagenum not in self.generated_stage3json.keys():
            self.generated_stage3json.update({ self._pagenum : []} )
          self.generated_stage3json[self._pagenum].append(generated_json)
          self.positioned_medias.get(self._pagenum).add(self.selectedItem)

      self.selectedItem = "None Selected"
      print(self.generated_stage3json)
      print(self.positioned_medias)
      self.format_list() # Formats the list with coloring

    def onGeneratePageButton(self):

       page_id = self.ids_list[self._pagenum][1]
       page_number = self._pagenum
       if page_number in self.generated_stage3json.keys():
          page_data = self.generated_stage3json[page_number]
       else:
          messagebox.showinfo("Info", "Generated page dict does not contain page number")
          return

       self.driver.refresh()
       WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, page_id)))

       item_list = []
       if page_data != []:
          for data in page_data:
            print("Data" , data)
            item = test_vosk.convert_mfj_to_stage3item(data)
            if item != None:
               item_list.append(item)


       items_json_string = json.dumps(item_list)
       print("ITEMS JSON STRING\n", items_json_string)

       #TIME TO RUN SCRIPTS
       # SCRIPT STAGE 2 is modifiable
      #  STAGE3_JS_SCRIPT_2 = """
      #   rootElement = undefined;
      #   items = undefined;
      #   insertContent(rootElement, items);
      #   """

       #paddd_script = STAGE3_JS_SCRIPT_1+ f"rootElement = document.getElementById(\"{page_id}\");"+ f"items = JSON.parse({json.dumps(items_json_string)});"+ "insertContent(rootElement,"+"items.filter( function(i){ return i.type == \"divider\" ; }));"+ "reElmrem = removeElementsBetweenDividers("+f"\"{page_id}\""+");" +"subitems = items.filter( function(i){ return i.type != \"divider\" ; });if(subitems.length > 0){output_element = insertContent(rootElement, subitems );}"+"performDividerRemoveAction( $(rootElement),reElmrem);"
       paddd_script = STAGE3_JS_SCRIPT_1+ f"rootElement = document.getElementById(\"{page_id}\");"+ f"items = JSON.parse({json.dumps(items_json_string)});"+ "output_element = insertContent(rootElement, items );"+f"reElmrem = removeElementsBetweenDividers(\"{page_id}\");performDividerRemoveAction( $(rootElement),reElmrem);"

       print(paddd_script)
       self.driver.execute_script(
          paddd_script
       )

       #GET POSITION DATA
      #  for entry in self.driver.get_log('browser'):
      #     print("clearing console: ",entry)
          # search_ress = re.search( r"\"Position:\"\s*\"(\d*)px",entry["message"] )
          # if search_ress != None:
          #   px = search_ress.group(1)
          #   print("px ",px)
          #   break
       #self.driver.execute_script(f"console.log('{paddd_script}')")

       #self.driver.execute_script(f"output_element = $('#{page_id}');output_element.prop(\"outerHTML\");")\
       element_obj = self.driver.find_element(By.ID, page_id)
       strring = element_obj.get_property("outerHTML")
      #  for entry in self.driver.get_log('browser'):
      #     print("html output console: ",entry)

       print(strring)
       with open( generate_mediaToPage_data.GENERATED_PAGES_OUTPUT + f"\\{page_number}.html", "w", encoding="utf-8") as store_generated:
          store_generated.write(strring)


       self.clear_listbox_selection()

    def clear_listbox_selection(self):
       self.listbox.selection_clear(0, "end")

    def clear_all_assigned_positions (self):
       removed_set = set()
      #  for i in self.generated_stage3json[self._pagenum]:
      #     if i["mediaFileName"] in self.positioned_medias and i["mediaFileName"] not in removed_set:
      #        i["position"] = None
      #  self.positioned_medias = self.positioned_medias.difference(removed_set)

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
        if self._pagenum not in self.positioned_medias.keys():
             self.positioned_medias.update({self._pagenum: set() })
        for i in range(len(listss)):
          self.listbox.itemconfig( i , { "bg":"green" if listss[i] in self.positioned_medias.get(self._pagenum) else "white"}  )

    def get_unassigned_list(self):
       return [ "", "UNASSIGNED ITEMS" , "" ] + list(self.u_audio) + list(self.u_videos)

    def shift_media_to_page ( self , page = False, next_page = True):
      if self.selectedItem in self.list_items_var.get():
        if page:
            page_num = simpledialog.askinteger("Media Shifting", "What Page should the selected Media be shifted To ?")
            self.result_data[page_num][0].append(self.selectedItem)
        elif next_page:
            self.result_data[self._pagenum + 1][0].append(self.selectedItem)
      else:
         messagebox.showwarning("Media Shifting", "Unable to shift media, are you sure you have selected a media file ?")


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
          if self._pagenum not in self.positioned_medias.keys():
             self.positioned_medias.update({self._pagenum: set() })
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
myframe.mainloop()
## COMMAND FOR SPLITTING MEDIA FILE FROM ONE TIMESTAMP TO ANOTHER
## ffmpeg -i "./src/assets/audio/SB11 R1 G1 P91.mp3" -acodec copy -ss 00:00:00 -t 00:00:30 "./src/assets/audio/SB11 R1 G1 P91_plus30.mp3"
## COMMAND FOR GETTING AUDIO DURATION
## ffprobe -i "./src/assets/audio/SB11 R1 G1 P91.mp3" -show_entries format=duration -v quiet -of csv="p=0" -sexagesimal
## duration output is in the format hours : minutes : seconds . microseconds

# %%
