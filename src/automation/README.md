# automation

Steps to generate pages automatically:

1. Open the HTML version of the textbook PDF
2. Open developer tools & paste the content of **stage_1.js** into the console.
3. Run **getData(startIndex, startPageNumber)** where _startIndex_ is the index of the page you want to start generating from, and _startPageNumber_ is the number of that page. Both parameters are optional; you can run **getData()** to generate all pages, or run **getData(startIndex)** to exclude pages with a lower index than _startIndex_. _startPageNumber_ is there because certain blank pages in the intro section were skipped, so the page number is not necessarily _startIndex + 1_.
4. If the command completes successfully, a JSON file will be downloaded. Move that json file to the automation folder (same folder this README is in).
5. Open a terminal in this folder and run **node stage_2.js**.
6. The script will use the data in the JSON file to generate the page images & html in the project.

##### Please note that this should only be used with pages that only contain non-interactive content!
