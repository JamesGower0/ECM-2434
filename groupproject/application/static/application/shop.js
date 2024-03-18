const close = document.getElementById("close");
const open = document.getElementById("open");
const modal = document.getElementById("modal");

const images = document.getElementsByClassName("item-shop");

images.addEventListener("click", () => images.classList.add("show-modal"));
close.addEventListener("click", () => images.classList.remove("show-modal"));

window.addEventListener("click", (e) => {
  e.target === images ? images.classList.remove("show-modal") : false;
});