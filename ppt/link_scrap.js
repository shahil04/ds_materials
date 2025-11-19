
const data = [];

document.querySelectorAll('div.col-md-6').forEach(section => {
  const h3 = section.querySelector('h3[id]');
  const listItems = section.querySelectorAll('p.list-group-item');

  if (h3 && listItems.length) {
    // Extract and clean heading
    const headingClone = h3.cloneNode(true);
    headingClone.querySelectorAll('i, span').forEach(el => el.remove());
    const heading = headingClone.textContent.trim();

    const items = Array.from(listItems).map(p => {
      const pClone = p.cloneNode(true);
      pClone.querySelectorAll('i, a').forEach(el => el.remove());
      const title = pClone.textContent.trim();
      const link = p.querySelector('a')?.href || '';
      return { title, link };
    });

    data.push({ heading, items });
  }
});

console.log(data);



// =============








// const items = Array.from(document.querySelectorAll('p.list-group-item'));
// const results = items.map(p => {
//   const title = p.cloneNode(true); 
//   title.querySelectorAll('i, a').forEach(el => el.remove()); 
//   const text = title.textContent.trim();
//   const link = p.querySelector('a')?.href || '';
//   return { title: text, link };
// });

// console.log(results);
