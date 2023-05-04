const fs = require("fs/promises");
const path = require("path");
const pagesDir = String.raw`C:\Users\Joe\Documents\Visual Studio Code\ACCEDE\ETLearns\etlearns-book\src\assets\pages`;
const units = [
  [5, 20],
  [21, 36],
  [37, 57],
  [62, 79],
  [80, 97],
  [98, 116],
  [122, 143],
  [144, 157],
  [158, 173],
  [179, 195],
  [196, 211],
  [212, 228]
];
const wordsGrouped = require("./words_grouped.json");

let totalPageCount = units.reduce(
  (prev, unit) => prev + unit[1] - unit[0] + 1,
  0
);
let donePageCount = 0;

Promise.all(
  units.map(async (unit, i) => {
    const words = wordsGrouped[i];
    const [startPage, endPage] = unit;
    for (let pageNumber = startPage; pageNumber <= endPage; pageNumber++) {
      /// SINGLE PAGE SCRIPT At A time
      /// if (pageNumber != 29) continue;
      const pagePath = path.join(pagesDir, `${pageNumber}.html`);
      let pageText = await fs.readFile(pagePath, { encoding: "utf-8" });
      words.map((word) => {
        const regex = new RegExp(`\\b${word}\\w?\\b`, "g");
        pageText = pageText.replace(
          regex,
          `<a onclick="showDictionary('${word}'); return false;">$&</a>`
        );
      });
      await fs.writeFile(pagePath, pageText, { encoding: "utf-8" });
      donePageCount++;
      const percentage = (100 * donePageCount) / totalPageCount;
      console.log(
        `Done ${donePageCount} out of ${totalPageCount}. (${percentage.toFixed(
          2
        )}%)`
      );
    }
  })
).then(() => console.log("Done."));
