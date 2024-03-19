document.addEventListener("DOMContentLoaded", function() {
  console.log("Hellow");
  const closeWindow = document.getElementById("close");
  const open = document.getElementById("open");
  const container = document.querySelector(".modal-container");
  const images = document.getElementsByClassName("shop-img");


  Array.from(images).forEach(image => {
    image.addEventListener("click", function() {  
      const imgUrl = image.src;
      const alttext = image.alt;
      
      // Image displayed in pop up
      const imgDisplayedInForm = document.getElementById("modal-item-img");
      imgDisplayedInForm.src = imgUrl;
      // Price of the image in pop up
      const priceDisplayedInForm = document.getElementById("modal-item-price");
      priceDisplayedInForm.textContent = alttext + " points";
      
      container.classList.add("show-modal");
    });
  });

  closeWindow.addEventListener("click", function() {
      container.classList.remove("show-modal");
  });

});