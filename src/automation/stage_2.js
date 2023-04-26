const path = require("path");
const fs = require("fs");
const results = require(String.raw`C:\Users\Mubarak Salley\Downloads\pages (4).json`);
const assetsDir = path.resolve(__dirname, "../assets");
const imagesDir = path.resolve(assetsDir, "images");
const pagesDir = path.resolve(assetsDir, "pages");

let count = 0;
results.forEach((page) => {
  fs.writeFileSync(path.resolve(pagesDir, `${page.id}.html`), page.html);
  fs.writeFileSync(
    path.resolve(imagesDir, `page_${page.id}.png`),
    page.img,
    "base64"
  );
  count++;
  console.log(`Completed ${count} of ${results.length}`);
});

console.log("DONE!");
