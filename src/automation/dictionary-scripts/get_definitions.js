const fs = require("fs");
const axios = require("axios").default.create({
  baseURL: "https://lingua-robot.p.rapidapi.com/language/v1/entries/en",
  headers: {
    "x-rapidapi-host": "lingua-robot.p.rapidapi.com",
    "x-rapidapi-key": "e18eb20f52msh9b21702f259ecfbp155d87jsna8475a6b3b37"
  }
});

const words = ["observer"
,"education"
,"bachelor's degree"
,"bimonthly"
,"cut"
,"resistant"
, "noninfectious"
, "snakebite"
, "stomachache"
, "X-ray"
, "confined"
, "campsite"
, "ecolodge"
, "Buddhist"
, "apply"
, "get down"
, "get off"
, "peal"
, "deculturize"
, "destructive"
, "radio"
]// require("./words.json");
//const words = require("./words.json");
const dictionary = {};

(async () => {
  console.log("Fetching definitions...");

  let count = 1;
  for (let i = 0; i < words.length; i++) {
    const word = words[i];
    const response = await axios.get(`/${word}`);
    dictionary[word] = response.data;
    console.log(`${count} out of ${words.length}`);
    count++;
  }

  console.log("Saving to file...");
  fs.writeFileSync("dictionary_temp.json", JSON.stringify(dictionary));
  console.log("Done.");
})();
