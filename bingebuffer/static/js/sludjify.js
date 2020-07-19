const titleInput = document.querySelector('#review-title');
const slugInput = document.querySelector('#review-slug');

const slugify = (val) => {
  return val
    .toString()
    .toLowerCase()
    .trim()
    .replace(/&/g, '-and-')
    .replace(/[\s\W-]+/g, '-');
};

if (titleInput !== null && slugInput !== null) {
  titleInput.addEventListener('keyup', (e) => {
    slugInput.setAttribute('value', slugify(titleInput.value));
  });
}
