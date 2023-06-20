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

let technologySelect = document.querySelector('#technologySelect')
document.getElementsByClassName('createForm').addEventListener('submit', (event)=> {
    event.preventDefault()
    let selectedValue = document.getElementById('technologySelect').value
})

let selectToggle = document.querySelector('selectToggle')
let menuItems = document.querySelectorAll('.menuItem')
let selectMenu = document.querySelector('.selectMenu')
let selectedValueInput = document.querySelector('#selectedValueInput')

menuItems.forEach((item) => {
    item.addEventListener('click', ()=> {
        let selectedValue = this.getAttribute('data-value')

        selectedValueInput.value = selectedValue;

        document.querySelector('form').submit();
    })
})

selectToggle.addEventListener('click', ()=> {
    // let selectMenu = this.nextElementSibling;
    selectMenu.classList.toggle('active')
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


