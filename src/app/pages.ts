import { Page, Section } from './types';

const sections: Section[] = [
  { name: 'Cover', start: 1 },
  { name: 'Best Experience for Mobile Devices', start: 2 },
  { name: 'Authors', start: 3 },
  { name: 'Dedication', start: 4 },
  { name: 'Introduction', start: 5 },
  { name: 'Table of Contents', start: 6 },
  // { name: 'Unit 1', start: 7, end: 22 },
  // { name: 'Unit 2', start: 23, end: 38 },
  // { name: 'Unit 3', start: 39, end: 59 },
  // { name: 'Revision 1', start: 60, end: 63 },
  // { name: 'Unit 4', start: 64, end: 81 },
  // { name: 'Unit 5', start: 82, end: 99 },
  // { name: 'Unit 6', start: 100, end: 118 },
  // { name: 'Revision 2', start: 119, end: 123 },
  // { name: 'Unit 7', start: 124, end: 145 },
  // { name: 'Unit 8', start: 146, end: 159 },
  // { name: 'Unit 9', start: 160, end: 175 },
  // { name: 'Revision 3', start: 176, end: 180 },
  // { name: 'Unit 10', start: 181, end: 197 },
  // { name: 'Unit 11', start: 198, end: 213 },
  // { name: 'Unit 12', start: 214, end: 230 },
  // { name: 'Revision 4', start: 231, end: 236 },
  // { name: 'Appendix 1', start: 237, end: 239 },
  // { name: 'Appendix 2', start: 240, end: 242 },
  // { name: 'Appendix 3', start: 243, end: 244 },
  // { name: 'Appendix 4', start: 245, end: 255 },
  // { name: 'Appendix 5', start: 256, end: 257 },
  // { name: 'Acknowledgements', start: 258 },
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
      title: `${section.name} - p. ${i - 5}`,
    });
  }

  section.name += ` - p. ${section.start - 5}`;
});

export default { sections, pages };
