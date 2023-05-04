// let items = [
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
    //  {
    //     type:"divider",
    //     position:500,
    //     height:1
    //  }
// ];

//const { HighlightSpanKind } = require("typescript");

// const { root } = require("postcss");

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

  dividers = rootElement.find("div.divider");
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

console.log("HI")
