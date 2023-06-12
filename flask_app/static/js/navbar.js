// let viewportWidth = window.innerWidth || document.documentElement.clientWidth;

// dropdown
let nav = document.querySelector('nav');
let dropdown = nav.querySelector('.dropdown');
let dropdownToggle = nav.querySelector("[data-action='dropdown-toggle']");
let navToggle = nav.querySelector("[data-action='nav-toggle']");

// searchbar
let searchBtn = document.querySelector('.searchBtn');
let closeBtn = document.querySelector('.closeBtn');
let searchBox = document.querySelector('.searchBox');

//mobile searchbar 
let mobilesearchBtn = document.querySelector('.mobilesearchBtn');
let mobilecloseBtn = document.querySelector('.mobilecloseBtn');
// let searchBox = document.querySelector('.searchBox');

// usertab & dropdown
let userBtn = document.querySelector('.userTab li');
let userTabMenu = document.querySelector(".userTabDropdownMenu");



// dropdown events
dropdownToggle.addEventListener('click', () => {
    if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
    } else {
        dropdown.classList.add('show');
    }
})

navToggle.addEventListener('click', () => {
    if (nav.classList.contains('opened')) {
        nav.classList.remove('opened');
    } else {
        nav.classList.add('opened');
    }
})


// search bar events
searchBtn.addEventListener('click', () => {
        searchBox.classList.add('active');
        closeBtn.classList.add('active');
        searchBtn.classList.add('active');
    })

closeBtn.addEventListener('click', () => {
    searchBox.classList.remove('active');
    closeBtn.classList.remove('active');
    searchBtn.classList.remove('active');
}) 

// mobile search events
mobilesearchBtn.addEventListener('click', () => {
    searchBox.classList.add('active');
    mobilecloseBtn.classList.add('active');
    mobilesearchBtn.classList.add('active');
})

mobilecloseBtn.addEventListener('click', () => {
    searchBox.classList.remove('active');
    mobilecloseBtn.classList.remove('active');
    mobilesearchBtn.classList.remove('active');
}) 

// usertab & dropdown events
userBtn.addEventListener('click', () => {
    userTabMenu.classList.add('active')
    if (window.innerWidth >= 960 && userTabMenu.classList.contains('active') && userTabMenu.style.display === 'block') {
        userTabMenu.style.display = 'none';
        userTabMenu.classList.remove('active')
    }
    else if(window.innerWidth <= 960 && userTabMenu.classList.contains('active') &&  userTabMenu.style.display === 'flex') {
        userTabMenu.style.display = 'none';
        userTabMenu.classList.remove('active')
    }
    else if(window.innerWidth <= 960) {
        userTabMenu.style.display = 'flex';
    }
    else {
        userTabMenu.style.display = 'block';
    }
})

// userBtn.addEventListener('click', ()=> {
//     userTabMenu.classList.remove('active')
// })