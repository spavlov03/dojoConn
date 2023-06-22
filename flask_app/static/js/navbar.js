// let viewportWidth = window.innerWidth || document.documentElement.clientWidth;

// scroll animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show')
        } else {
            entry.target.classList.remove('show')
        }
    })
})

const hiddenElements = document.querySelectorAll('.hidden')
const navElements = document.querySelectorAll('.navHidden')
hiddenElements.forEach((el) => observer.observe(el))
navElements.forEach((el) => observer.observe(el))

// dropdown
let nav = document.querySelector('nav');
let dropdownToggle = nav.querySelector(".dropdown");
let dropdownMenu = nav.querySelector('.dropdown-menu');
let navToggle = nav.querySelector("[data-action='nav-toggle']");

dropdownToggle.addEventListener('click', () => {
    dropdownToggle.classList.toggle('active')
    dropdownMenu.classList.toggle('active');
})


navToggle.addEventListener('click', () => {
    if (nav.classList.contains('opened')) {
        nav.classList.toggle('opened');
    } else {
        nav.classList.add('opened');
    }
})


// searchbar
let searchBtn = document.querySelector('.searchBtn');
let closeBtn = document.querySelector('.closeBtn');
let searchBox = document.querySelector('.searchBox');

searchBtn.addEventListener('click', () => {
    searchBox.classList.toggle('active');
    closeBtn.classList.toggle('active');
    searchBtn.classList.toggle('active');
})

closeBtn.addEventListener('click', () => {
searchBox.classList.toggle('active');
closeBtn.classList.toggle('active');
searchBtn.classList.toggle('active');
}) 


// usertab & dropdown
let userBtn = document.querySelector('.userTabBtn');
let userTabMenu = document.querySelector(".userTabDropdownMenu");

userBtn.addEventListener('click', () => {
    userTabMenu.classList.toggle('active');
    userBtn.classList.toggle('active')
})


// select menu
const selectToggle = document.querySelector('.selectToggle');
const selectMenu = document.querySelector('.selectMenu');
const selectedOptionInput = document.getElementById('selectedOption');
const menuItems = document.querySelectorAll('.menuItem');
const textArea = document.querySelector('.textArea');

selectToggle.addEventListener('click', () => {
    selectMenu.classList.toggle('open');
    textArea.classList.toggle('faded');
});

menuItems.forEach((menuItem) => {
    menuItem.addEventListener('click', (event) => {
        const selectedOption = event.target.getAttribute('data-value');
        textArea.classList.toggle('faded')
        selectedOptionInput.value = selectedOption;
        selectToggle.textContent = menuItem.textContent;
        selectMenu.classList.remove('open');
    });
});