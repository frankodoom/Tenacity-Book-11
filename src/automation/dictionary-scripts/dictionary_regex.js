const fs = require("fs/promises");
const path = require("path");
const pagesDir = String.raw`C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\assets\pages`;
//const units = [[7, 34], [35, 63], [63, 96], [103, 125], [126, 146], [147, 166], [173, 202], [203, 226], [227, 247], [254, 271], [272, 292], [293, 306]];
const units = [[319, 320]];
const wordsGrouped = require("./words_grouped.json");
//const wordsGrouped = require("./words_grouped_nestedfix.json");

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
      let mystr = String(pageText);
      // GLOBAL ARRAY
      let asdds = new Array();
      let genArr = new Array();

      words.map((word) => {
        if (Array.isArray(word)){

          // word.forEach( function(i) {  });

          word.forEach( function(item){
              // let genArr = new Array();
              //console.log(item);
              //let matchValue = new Array();
              if ( typeof item === "string"){
                  let regexx = new RegExp(`(?<=>[^<>]*?)\\b${item}\\b(?=[^<>]*?<)`,"g");
                  let gen = mystr.matchAll(regexx);
                  genArr.push(gen);

              }else{
                  item.forEach( function(subitem){
                      //console.log(subitem);
                      let regexx = new RegExp(`(?<=>[^<>]*?)\\b${subitem}\\b(?=[^<>]*?<)`,"g");
                      let gen = mystr.matchAll(regexx);
                      genArr.push(gen);
                  });
              }


          });

        }
        else{
        const regex = new RegExp(`(?<=>[^<>]*?)\\b${word}\\b(?=[^<>]*?<)`, "g");
        //const regex = new RegExp(`\\b${word}\\w?\\b`, "g");
        // pageText = pageText.replace(
        //   regex,
        //   `<a onclick="showDictionary('${word}'); return false;">$&</a>`
        // );}
        let genobb = pageText.matchAll(regex);
        genArr.push(genobb)
        }

      });

      genArr.forEach(function(genitem){
        matchitem = genitem.next();
        while( matchitem.done != true){
            asdds.push(matchitem.value);
            matchitem = genitem.next();
          }
      });

      asdds.map( function(item){ item.endindex =item.index + item[0].length; return item } );

      str_copy = String(mystr);
      new_asds_arr = Array.from( asdds, function (item) { let isnotsub = true; asdds.forEach( function(itt){ if(item.index >= itt.index && item.endindex <= itt.endindex && !( item.index == itt.index && item.endindex == itt.endindex )){ console.log("falsified");isnotsub = false; }   }); if (isnotsub){ return item;}else{return undefined;} } );
      new_asds_arr.sort( function(a,b){
          if( a == b){
              return 0;
          }else if (a == undefined){
              return -1;
          }else if (b == undefined){
              return 1;
          }
          else if ( a.index > b.index){
              return 1;
          }
          else{
              return -1;
          }
      });
      previousEndIndex = 0;
      str_arr = new Array();
      new_asds_arr.forEach( function(item){
          if ( item ){
              //newstr = str_copy.slice(0,item.index) + "<p>" + item[0] + "</p>" + str_copy.slice(item.endindex);
              //console.log(newstr);
              str_arr.push( str_copy.slice(previousEndIndex,item.index));
              str_arr.push( "<a onclick=\"showDictionary('" + item[0] + "'); return false;\">"+item[0]+"</a>"  );
              previousEndIndex = item.endindex;
          }else{
              console.log("missed");
          }
      });
      str_arr.push ( str_copy.slice(previousEndIndex));
      pageText = str_arr.join("");

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
