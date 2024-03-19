document.addEventListener("DOMContentLoaded", function() {
  console.log("Hellow");
  const closeWindow = document.getElementById("close");
  const open = document.getElementById("open");
  const modal = document.getElementById("modal");
  const container = document.querySelector(".modal-container");
  const images = document.getElementsByClassName("shop-img");



  Array.from(images).forEach(image => {
    image.addEventListener("click", function() {   
      const imgUrl = image.src;
      open.dataset.imageUrl = image.alt;
      const alttext = image.alt;
      
      container.classList.add("show-modal");
    });
  });

  closeWindow.addEventListener("click", function() {
      container.classList.remove("show-modal");
  });

});