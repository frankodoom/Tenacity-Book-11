const dictionaryPath = String.raw`C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\automation\dictionary-scripts\dictionary.json`;
const destinationDir = String.raw`C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\audio\dictionary2`;

const fs = require("fs");
const dictionary = JSON.parse(fs.readFileSync(dictionaryPath));

const words = [];

for (const v of Object.values(dictionary)) {
  const entry = v.entries[0];
  const p = entry?.pronunciations?.find((x) => x.audio?.url);
  if (p && p.audio.url.startsWith("http"))
    words.push({ word: entry.entry, audio: p.audio });
}

console.log(`Number of files to download: ${words.length}`);

if (!words.length) return;

const axios = require("axios").default;
const pipeline = require("util").promisify(require("stream").pipeline);
const path = require("path");

let count = 0;
fs.mkdirSync(destinationDir);

Promise.all(
  words.map(async ({ word, audio }) => {
    try {
      const response = await axios.get(audio.url, { responseType: "stream" });
      const filename = word.concat(path.parse(audio.url).ext);
      await pipeline(
        response.data,
        fs.createWriteStream(path.join(destinationDir, filename))
      );

      audio.url = "assets/audio/dictionary/".concat(filename);
      count++;
      console.log(`Downloaded ${filename} (${count} out of ${words.length})`);
    } catch (err) {
      console.error(`Failed to download file: ${audio.url}`);
      console.error(err);
    }
  })
).then(() => {
  console.log(`Done. (failCount=${words.length - count})`);

  fs.writeFileSync(dictionaryPath, JSON.stringify(dictionary, null, 4));
});
