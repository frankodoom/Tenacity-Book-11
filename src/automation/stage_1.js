function getData(startIndex, startPageNumber) {
  const container = document.getElementById("page-container");
  const pages = [];
  let pageNumber = startPageNumber || startIndex + 1;

  // Get page html & background image
  for (let i = startIndex; i < container.children.length; i++) {
    const div = container.children.item(i);
    const img = div.firstElementChild.firstElementChild;
    const imgData = img.src;
    img.src = `assets/images/page_${pageNumber}.png`;
    pages.push({
      id: pageNumber,
      html: div.outerHTML,
      img: imgData.replace(/^data:image\/png;base64,/, ""),
    });
    img.src = imgData;
    pageNumber++;

    // IF CAPTURING ONE PAGE UNCOMMENT THE BREAK
    //break;
  }

  // Save results as json
  var a = document.createElement("a");
  var file = new Blob([JSON.stringify(pages)], { type: "text/plain" });
  a.href = URL.createObjectURL(file);
  a.download = "pages.json";
  a.click();
}
