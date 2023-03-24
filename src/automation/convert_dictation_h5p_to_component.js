const path = require("path");
const fs = require("fs");

convert("204 SB10 R4 L4 E1 P225", 310);

function convert(name, top) {
  const htmlContent = fs.readFileSync(
    path.join(__dirname, "../assets", "h5p", name + ".html"),
    { encoding: "utf8" }
  );

  let json = htmlContent.substring(
    htmlContent.indexOf("{"),
    htmlContent.indexOf("};") + 1
  );

  const data = JSON.parse(json);
  json = data.contents[Object.keys(data.contents)[0]].jsonContent;
  const dictationContent = JSON.parse(json);
  const title = dictationContent.taskDescription
    .replace(/(<p>)|(<\/p>)/g, "")
    .replace(/\n+/g, "<br/>");
  debugger;
  const text = dictationContent.sentences[0].text;
  const audioUrl = "assets/h5p/" + dictationContent.sentences[0].sample[0].path;

  const result = `<app-dictation title="${title}" text="${text}" src="${audioUrl}" style="position: absolute; top: ${top}px"></app-dictation>`;
  console.log(result);
}
