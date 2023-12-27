let slideIndex = 0;
const slides = document.querySelectorAll(".slide");
let slideInterval;

function showSlide(n) {
  if (n < 0) {
    slideIndex = slides.length - 1;
  } else if (n >= slides.length) {
    slideIndex = 0;
  }

  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  slides[slideIndex].style.display = "block";
}

function changeSlide(n) {
  showSlide((slideIndex += n));
}

function autoSlide() {
  changeSlide(1);
}

// Initial slide display
showSlide(slideIndex);

slideInterval = setInterval(autoSlide, 4000);

document.querySelector(".prev").addEventListener("click", () => {
  clearInterval(slideInterval);
});

document.querySelector(".next").addEventListener("click", () => {
  clearInterval(slideInterval);
});

/* Dark Mode  */

const darkModeToggleRadio = document.getElementById("dark-mode-toggle");
const body = document.body;

darkModeToggleRadio.addEventListener("change", () => {
  if (darkModeToggleRadio.checked) {
    body.classList.add("dark-mode");
  } else {
    body.classList.remove("dark-mode");
  }

  // Toggle the 'checked' state manually
  darkModeToggleRadio.checked = !darkModeToggleRadio.checked;
});

//   mouseover and mouseout
function mouseOver() {
  document.getElementById("demo").style.color = "red";
}

function mouseOut() {
  document.getElementById("demo").style.color = "black";
}
//mouseup and mouseover
function mouseDown() {
  document.getElementById("myP").style.color = "red";
}

function mouseUp() {
  document.getElementById("myP").style.color = "blue";
}

function myFunction() {
  alert("Please register. if your register signin to select product.");
}



//Search Box Js

  function searchConditioners() {
    // Get the user's input from the search box
    const searchInput = document.getElementById("searchInput").value.toLowerCase();

    // Get all conditioner card elements
    const conditionerCards = document.querySelectorAll(".card");

    // Loop through each card and check if it matches the search input
    conditionerCards.forEach((card) => {
      const cardTitle = card.querySelector(".card-title").textContent.toLowerCase();

      // Show the card if it contains the search input, or hide it if it doesn't
      if (cardTitle.includes(searchInput)) 
      {
        card.style.display = "block";
      } 
      else 
      {
        card.style.display = "none";
      }

    });
  }




  function searchConditioners() {
    // Get the user's input from the search box
    const searchInput = document.getElementById("searchInput").value.toLowerCase();

    // Get all conditioner card elements
    const conditionerCards = document.querySelectorAll(".card");

    // Loop through each card and check if it matches the search input
    conditionerCards.forEach((card) => {
      const cardTitle = card.querySelector(".card-title").textContent.toLowerCase();

      // Show the card if it contains the search input, or hide it if it doesn't
      if (cardTitle.includes(searchInput)) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  }

/*   Add to cart   */

const addToCartButtons = document.querySelectorAll(".add-to-cart");
addToCartButtons.forEach((button) => {
  button.addEventListener("click", addToCart);
});

function addToCart(event) {
  const productCard = event.target.closest(".card");
  const productName = productCard.querySelector(".card-title").textContent;
  const productPrice = productCard.querySelector("p").textContent;
  const quantity = parseInt(productCard.querySelector("#quantity").value);

  // Create an object to represent the product
  const product = {
    name: productName,
    price: productPrice,
    quantity: quantity,
  };

  // Retrieve the existing cart or create an empty cart if it doesn't exist
  let cart = JSON.parse(localStorage.getItem("cart")) || [];

  // Check if the product is already in the cart, and update the quantity
  let existingProduct = cart.find((item) => item.name === product.name);
  if (existingProduct) {
    existingProduct.quantity += quantity;
  } else {
    cart.push(product);
  }

  // Store the updated cart in local storage
  localStorage.setItem("cart", JSON.stringify(cart));

  // Optionally, you can provide some feedback to the user
  alert("Product added to cart!");
}

const cartIcon = document.getElementById("cart-icon");
const cartCount = document.getElementById("cart-count");
const cartContent = document.getElementById("cart-content"); // Create a container for cart content

let isCartOpen = false;
const selectedProducts = [];

function toggleCart() {
  if (isCartOpen) {
    // Close the cart
    cartContent.style.display = "none";
    isCartOpen = false;
  } else {
    // Open the cart (you can replace this with your cart content)
    // For example, you can dynamically generate cart items here
    cartContent.innerHTML = "Cart is empty"; // Replace with actual cart content
    cartContent.style.display = "block";
    isCartOpen = true;
  }
}



