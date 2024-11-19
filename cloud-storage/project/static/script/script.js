const closePopUp = (el) => {
    el.style.opacity = '0'
    setTimeout(() => el.remove(), 500)
}