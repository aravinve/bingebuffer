M.AutoInit();

const toggleSwitch = document.querySelector('#theme-switch');
const toggleSwitchMobile = document.querySelector('#theme-switch-mobile');
const bbLogo = document.querySelector('#bb-logo');

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

toggleSwitch.addEventListener('change', switchTheme, false);
toggleSwitchMobile.addEventListener('change', switchTheme, false);
