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

function removeElementsBetweenDividers(page_id){
  dividers = $("div.divider")
  startpos = -1
  stoppos = -1
  if( dividers.length == 1){
    stoppos = 99999999;
    startpox = cumulativeOffset(dividers[0]).top;
  }
  if(dividers.length == 2){
    topArray = new Array();
    dividers.each(function(index){
      topArray.push(cumulativeOffset(this).top)
    })
    topArray.sort(function(a,b){ if(a>b){return 1;}else{return -1} });
    startpos = topArray[0];
    stoppos = topArray[1];
  }

  toremove = new Array();
  $(page_id).find("div.t").each(
    function (index){
      pos = cumulativeOffset(this).top;
      console.log(pos);
      if( startpos <pos && pos < stoppos){
          toremove.push(this);
      }
    }
  )

  toremove.foreach( function(i){
    i.remove();
  })

  image_holders = $("div.imageholder")
  if (image_holders.length >= 2){
    image_holders[1].remove()
  }
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
  image.remove();

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
        item.height = 1;
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


console.log("HI")
