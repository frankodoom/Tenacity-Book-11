import { Page, Section } from './types';

const sections: Section[] = [
  { name: 'Cover', start: 1 },
  { name: 'Best Experience for Mobile Devices', start: 2 },
  { name: 'Authors', start: 3 },
  { name: 'Dedication', start: 4 },
  { name: 'Introduction', start: 5 },
  { name: 'Table of Contents', start: 6 },
  { name: 'Unit 1', start: 7, end: 34 },
  { name: 'Unit 2', start: 35, end: 63 },
  { name: 'Unit 3', start: 64, end: 96 },
  { name: 'Revision 1 (Units 1 - 3)', start: 97, end: 102 },
  { name: 'Unit 4', start: 103, end: 125 },
  { name: 'Unit 5', start: 126, end: 146 },
  { name: 'Unit 6', start: 147, end: 166 },
  { name: 'Revision 2 (Units 4 - 6)', start: 167, end: 172 },
  { name: 'Unit 7', start: 173, end: 202 },
  { name: 'Unit 8', start: 203, end: 226 },
  { name: 'Unit 9', start: 227, end: 247 },
  { name: 'Revision 3 (Units 7 - 9)', start: 248, end: 253 },
  { name: 'Unit 10', start: 254, end: 271 },
  { name: 'Unit 11', start: 272, end: 292 },
  { name: 'Unit 12', start: 293, end: 306 },
  { name: 'Revision 4 (Units 10 - 12)', start: 307, end: 311 },
  { name: 'Appendix 1', start: 312, end: 314 },
  { name: 'Appendix 2', start: 315, end: 318 },
  { name: 'Appendix 3', start: 319, end: 320 },
  { name: 'Appendix 4', start: 321, end: 333 },
  // { name: 'Appendix 5', start: 256, end: 257 },
  { name: 'Acknowledgements', start: 334},
];

const pages: Page[] = [];

sections.forEach((section) => {
  if (!section.end) {
    pages.push({ title: section.name, index: section.start });
    return;
  }

  for (let i = section.start; i <= section.end; i++) {
    pages.push({
      index: i,
      title: `${section.name} - p. ${i - 6}`,
    });
  }

  section.name += ` - p. ${section.start - 6}`;
});

export default { sections, pages };
