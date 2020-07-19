M.AutoInit();

const toggleSwitch = document.querySelector('#theme-switch');
const toggleSwitchMobile = document.querySelector('#theme-switch-mobile');
const reviewStatusSwitch = document.querySelector('#review-status-switch');
const bbLogo = document.querySelector('#bb-logo');
const seats = document.querySelectorAll('.seat');
const seatContent = document.querySelector('#seat-content');
const seatSelecter = document.querySelector('#seat-selecter');
const seatInput = document.querySelector('#id_seats_count');
const movieInput = document.querySelector('#id_movie_name');
const movieName = document.querySelector('h4.text-secondary');
const timeSelecter = document.querySelectorAll('.show-time');
const timeInput = document.querySelector('#id_show_time');
const screenNameInput = document.querySelector('#id_screen_name');
const screenLocationInput = document.querySelector('#id_screen_location');
const dateSelecter = document.querySelector('#date-selecter');
const dateSelecterInput = document.querySelector('#id_show_date');
const confirmSeatNumbersInput = document.querySelector('#id_seats');
const confirmSeats = document.querySelector('#confirm-seats');
const continueBookingBtnOne = document.querySelector(
  '#show-continue-booking-btn'
);
const continueBookingBtnTwo = document.querySelector(
  '#seat-continue-booking-btn'
);
const autoMovieName = document.querySelector('.autocomplete');
const autoMovieId = document.querySelector('#auto-movie-id');
const reviewChips = document.querySelector('#review-chips');
const reviewHashTagsInput = document.querySelector('#review-hashtags');
const reviewPublicStatusInput = document.querySelector('#review-public-status');

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
  if (dateSelecter !== null) {
    setLimitToDateSelector();
  }
  if (reviewChips !== null) {
    M.Chips.init(reviewChips, {
      placeholder: 'Enter a tag',
      secondaryPlaceholder: '+Tag',
      limit: 10,
      onChipAdd: setDataInHiddenInput,
      onChipDelete: setDataInHiddenInput,
    });
  }
};

function setDataInHiddenInput(e) {
  const chipsData = e[0].M_Chips.chipsData;
  reviewHashTagsInput.value = JSON.stringify(chipsData);
}

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

function setLimitToDateSelector() {
  const dtToday = new Date();
  let month = dtToday.getMonth() + 1;
  let day = dtToday.getDate();
  let maxDay = dtToday.getDate() + 10;
  let year = dtToday.getFullYear();
  if (month < 10) month = '0' + month.toString();
  if (day < 10) day = '0' + day.toString();
  if (maxDay < 10) maxDay = '0' + maxDay.toString();
  let minDate = year + '-' + month + '-' + day;
  let maxDate = year + '-' + month + '-' + maxDay;
  dateSelecter.setAttribute('min', minDate);
  dateSelecter.setAttribute('max', maxDate);
  var elems = document.querySelectorAll('.datepicker');
  var options = { minDate: new Date(minDate), maxDate: new Date(maxDate) };
  M.Datepicker.init(elems, options);
}

function selectSeat(e) {
  const element = e.target;
  const totalSeatCount = Number(confirmSeats.value);
  if (seatContent.children.length < totalSeatCount) {
    element.classList.toggle('active');
    if (element.classList.contains('active')) {
      const span = document.createElement('span');
      const textContent = e.target.parentElement.id;
      if (textContent !== '') {
        const textElement = document.createTextNode(textContent);
        span.appendChild(textElement);
        const classes = ['badger', 'bg-primary', 'col', 's3'];
        span.classList.add(...classes);
        seatContent.appendChild(span);
        confirmSeatNumbersInput.value =
          confirmSeatNumbersInput.value !== ''
            ? confirmSeatNumbersInput.value + ',' + textContent
            : textContent;
      }
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
  } else if (element.classList.contains('active')) {
    element.classList.toggle('active');
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
  } else {
    M.toast({
      html: 'Seat Limit Reached!',
      classes: 'bg-danger text-white',
    });
  }
}

function seatSelecterFunction() {
  seatInput.value = Number(seatSelecter.value);
  movieInput.value = movieName.innerText;
}

function dateSelecterFunction() {
  dateSelecterInput.value = dateSelecter.value;
}

function timeSelecterFunction(e) {
  e.target.classList.toggle('bg-primary');
  e.target.classList.toggle('text-white');
  e.target.classList.toggle('bg-nav');
  Array.from(e.target.parentElement.children).forEach((button) => {
    if (e.target !== button && button.classList.contains('bg-primary')) {
      button.classList.remove('bg-primary');
      button.classList.remove('text-white');
      button.classList.add('bg-nav');
    }
  });
  if (e.target.classList.contains('bg-primary')) {
    timeInput.value = e.target.innerText;
    let data = e.target.parentElement.id;
    const screenData = data.split('/');
    screenNameInput.value = screenData[0];
    screenLocationInput.value = screenData[1];
  } else {
    timeInput.value = '';
    screenNameInput.value = '';
    screenLocationInput.value = '';
  }
}

function validateBooking() {
  if (
    seatInput.value !== '' &&
    movieInput.value !== '' &&
    timeInput.value !== '' &&
    screenNameInput.value !== '' &&
    screenLocationInput.value !== '' &&
    dateSelecterInput.value !== ''
  ) {
    M.toast({
      html: 'Success',
      classes: 'bg-success text-white',
    });
  } else {
    M.toast({
      html: 'Failed To Continue Booking',
      classes: 'bg-danger text-white',
    });
  }
}

function validateSeatSelection(e) {
  const totalSeatCount = Number(confirmSeats.value);
  if (
    confirmSeatNumbersInput.value !== '' &&
    seatContent.children.length === totalSeatCount
  ) {
    M.toast({
      html: 'Success',
      classes: 'bg-success text-white',
    });
  } else {
    e.preventDefault();
    M.toast({
      html: 'Failed To Continue Booking, Select Required Seats',
      classes: 'bg-danger text-white',
    });
  }
}

function autocompleteSearch(e) {
  fetch(
    `https://api.themoviedb.org/3/search/movie?api_key=27a15e97323cf3d6f95c3e08935d876d&language=en-US&query=${e.target.value}&page=1&include_adult=false`
  )
    .then((res) => {
      return res.json();
    })
    .then((body) => {
      let apiData = {};
      body.results.forEach((result) => {
        const { title, poster_path } = result;
        apiData[title] =
          poster_path !== null
            ? `https://image.tmdb.org/t/p/w185_and_h278_bestv2/${poster_path}`
            : `https://placehold.it/250x250`;
      });
      var instances = M.Autocomplete.init(autoMovieName, {
        data: apiData,
        limit: 10,
      });
      instances.open();
      autoMovieId.value = JSON.stringify(body.results);
    });
}

function updateReviewStatus(e) {
  reviewPublicStatusInput.value = e.target.checked;
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

if (continueBookingBtnOne !== null) {
  continueBookingBtnOne.addEventListener('click', validateBooking, false);
}
if (continueBookingBtnTwo !== null) {
  continueBookingBtnTwo.addEventListener('click', validateSeatSelection, false);
}

if (autoMovieName !== null) {
  autoMovieName.addEventListener('input', autocompleteSearch, false);
}

if (reviewStatusSwitch !== null) {
  reviewStatusSwitch.addEventListener('change', updateReviewStatus, false);
}
