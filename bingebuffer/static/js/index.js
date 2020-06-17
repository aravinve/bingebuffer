M.AutoInit();

const toggleSwitch = document.querySelector('#theme-switch');
const toggleSwitchMobile = document.querySelector('#theme-switch-mobile');
const bbLogo = document.querySelector('#bb-logo');
const seats = document.querySelectorAll('.seat');
const seatContent = document.querySelector('#seat-content');
const seatSelecter = document.querySelector('#seat-selecter');
const seatInput = document.querySelector('#seats');
const timeSelecter = document.querySelectorAll('.show-time');
const timeInput = document.querySelector('#show-time');
const screenNameInput = document.querySelector('#screen-name');
const screenLocationInput = document.querySelector('#screen-location');
const dateSelecter = document.querySelector('#date-selecter');
const dateSelecterInput = document.querySelector('#show-date');
const confirmSeatNumbersInput = document.querySelector('#confirm-seat-numbers');

document.onreadystatechange = () => {
  const theme = localStorage.getItem('data-theme');
  if (theme !== null) {
    if (theme === 'dark') {
      toggleSwitch.checked = true;
      toggleSwitchMobile.checked = true;
      setThemeDark();
    } else {
      toggleSwitch.checked = false;
      toggleSwitchMobile.checked = false;
      setThemeLight();
    }
  }
  changeActiveClass();
};

function switchTheme(e) {
  if (e.target.checked) {
    setThemeDark();
  } else {
    setThemeLight();
  }
  if (e.target.id === 'theme-switch') {
    toggleSwitchMobile.checked = e.target.checked;
  } else {
    toggleSwitch.checked = e.target.checked;
  }
}

function setThemeDark() {
  document.documentElement.setAttribute('data-theme', 'dark');
  localStorage.setItem('data-theme', 'dark');
  const imgsrc = bbLogo.getAttribute('src');
  let imgarr = imgsrc.split('/');
  imgarr[3] = 'whole-logo-white.png';
  bbLogo.setAttribute('src', imgarr.join('/'));
}

function setThemeLight() {
  document.documentElement.setAttribute('data-theme', 'light');
  localStorage.setItem('data-theme', 'light');
  const imgsrc = bbLogo.getAttribute('src');
  let imgarr = imgsrc.split('/');
  imgarr[3] = 'whole-logo.png';
  bbLogo.setAttribute('src', imgarr.join('/'));
}

function changeActiveClass() {
  const currentActiveElement = document.querySelector('.pagination li.active');
  const pagination = document.querySelectorAll('.pagination li a');
  if (
    currentActiveElement !== null &&
    pagination !== null &&
    currentActiveElement.children[0].href !== window.location.href
  ) {
    currentActiveElement.classList.remove('active');
    pagination.forEach((page) => {
      if (page.href === window.location.href) {
        page.parentElement.classList.add('active');
      }
    });
  }
}

function selectSeat(e) {
  const element = e.target;
  element.classList.toggle('active');
  if (element.classList.contains('active')) {
    const span = document.createElement('span');
    const textContent = e.target.parentElement.id;
    const textElement = document.createTextNode(textContent);
    span.appendChild(textElement);
    const classes = ['badger', 'bg-primary', 'col', 's3'];
    span.classList.add(...classes);
    seatContent.appendChild(span);
    confirmSeatNumbersInput.value =
      confirmSeatNumbersInput.value !== ''
        ? confirmSeatNumbersInput.value + ',' + textContent
        : textContent;
  } else {
    let elementToBeRemoved = '';
    seatContent.childNodes.forEach((seat, index) => {
      if (seat.innerText === e.target.parentElement.id) {
        elementToBeRemoved = index;
      }
    });
    seatContent.removeChild(seatContent.childNodes[elementToBeRemoved]);
    const seatNumbers = confirmSeatNumbersInput.value.split(',');
    const updateSeatNumbers = seatNumbers.filter(
      (seatNumber) => seatNumber !== e.target.parentElement.id
    );
    confirmSeatNumbersInput.value = updateSeatNumbers.join(',');
  }
}

function seatSelecterFunction() {
  seatInput.value = seatSelecter.value;
}

function dateSelecterFunction() {
  dateSelecterInput.value = dateSelecter.value;
}

function timeSelecterFunction(e) {
  timeInput.value = e.target.innerText;
  let data = e.target.parentElement.id;
  const screenData = data.split('/');
  screenNameInput.value = screenData[0];
  screenLocationInput.value = screenData[1];
}
toggleSwitch.addEventListener('change', switchTheme, false);
toggleSwitchMobile.addEventListener('change', switchTheme, false);
seats.forEach((seat) => {
  seat.addEventListener('click', selectSeat, false);
});
if (seatSelecter !== null && timeSelecter !== null && dateSelecter !== null) {
  seatSelecter.addEventListener('change', seatSelecterFunction, false);
  timeSelecter.forEach((timeInput) => {
    timeInput.addEventListener('click', timeSelecterFunction, false);
  });
  dateSelecter.addEventListener('change', dateSelecterFunction, false);
}
