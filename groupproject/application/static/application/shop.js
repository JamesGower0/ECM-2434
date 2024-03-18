document.addEventListener("DOMContentLoaded", function() {
  console.log("Hellow");
  const closeWindow = document.getElementById("close");
  const open = document.getElementById("open");
  const modal = document.getElementById("modal");
  const container = document.querySelector(".modal-container");
  const images = document.getElementsByClassName("item-shop");



  Array.from(images).forEach(image => {
    image.addEventListener("click", function() {   
      container.classList.add("show-modal");
    });
  });

  closeWindow.addEventListener("click", function() {
      container.classList.remove("show-modal");
  });

});