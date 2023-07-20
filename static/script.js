// Sticky header on scroll
const header = document.querySelector("header");
window.addEventListener("scroll", function () {
    header.classList.toggle("sticky", window.scrollY > 0);
});

// Mobile menu toggle
let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('open');
};

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navbar.classList.remove('open');
};

// JavaScript code for handling form submission using AJAX

// Registration form submission
function registerUser() {
    // Retrieve form data
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Send form data to the server using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/register", true); // Replace "/register" with the actual Flask route for user registration
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Registration success message
                console.log(xhr.responseText);
                alert("Registration successful!");
                // Optionally, redirect to a success page after registration
                window.location.href = "/success";
            } else {
                // Registration failed or encountered an error
                console.error(xhr.responseText);
                alert("Registration failed. Please try again later.");
            }
        }
    };
    var data = "name=" + encodeURIComponent(name) + "&email=" + encodeURIComponent(email) + "&password=" + encodeURIComponent(password);
    xhr.send(data);
}

// Cart data object to store the items added to the cart and the total amount
const cartData = {
  items: [],
  total: 0,
};

// Function to get course details by title
function getCourseByTitle(title) {
  const courses = [
    {
      title: "The Complete ReactJs Course",
      price: "$30.00",
      duration: "10 hours 30 minutes",
      rating: "{2 Review}",
    },
    {
      title: "The Complete JavaScript Course 2023",
      price: "$30.00",
      duration: "07 hours 30 minutes",
      rating: "{1 Review}",
    },
    {
      title: "The Complete HTML and CSS Course 2023",
      price: "$20.00",
      duration: "06 hours 20 minutes",
      rating: "{2 Review}",
    },
    {
      title: "The Complete Angular 2023",
      price: "$30.00",
      duration: "07 hours",
      rating: "{3 Review}",
    },
    {
      title: "The Complete C# Programming Course",
      price: "$40.00",
      duration: "12 hours 20 minutes",
      rating: "{4 Review}",
    },
    {
      title: "The Complete Python Course",
      price: "$50.00",
      duration: "10 hours",
      rating: "{5 Review}",
    },
  ];

  return courses.find((course) => course.title === title);
}

// Function to add an item to the cart
function addToCart(title) {

  const course = getCourseByTitle(title);

  if (course) {
    const cartItems = document.getElementById("cart-items");
    const cartItem = document.createElement("div");
    cartItem.classList.add("cart-item");
    cartItem.innerHTML = `
      <div class="cart-item-details">
        <h4>${course.title}</h4>
        <p>${course.price}</p>
      </div>
      <button class="remove-btn" onclick="removeFromCart(this)">Remove</button>
    `;
    cartItems.appendChild(cartItem);

    // Extract the price from the course data and add it to the cart total
    const priceString = course.price.substring(1); // Removing the dollar sign from the price string
    const coursePrice = parseFloat(priceString);
    cartData.total += coursePrice;
    cartData.items.push(course);

    // Update the cart icon with the number of items
    const cartIcon = document.querySelector(".bx-cart span");
    cartIcon.innerText = cartData.items.length;

    // Update the cart total amount
    const totalAmount = document.getElementById("total-amount");
    totalAmount.innerText = "$" + cartData.total.toFixed(2);

    // Show the cart modal
    openCartModal();
  }
}

// Function to remove an item from the cart
function removeFromCart(button) {
  const cartItem = button.parentElement;
  const courseTitle = cartItem.querySelector("h4").innerText;

  // Find the course in the cartData array and remove it
  const removedCourse = cartData.items.find((course) => course.title === courseTitle);
  if (removedCourse) {
    const priceString = removedCourse.price.substring(1); // Removing the dollar sign from the price string
    const removedCoursePrice = parseFloat(priceString);
    cartData.total -= removedCoursePrice;
    cartData.items = cartData.items.filter((course) => course.title !== courseTitle);
  }

  const cartItems = document.getElementById("cart-items");
  cartItems.removeChild(cartItem);

  // Update the cart icon with the number of items
  const cartIcon = document.querySelector(".bx-cart span");
  cartIcon.innerText = cartData.items.length;

  // Update the cart total amount
  const totalAmount = document.getElementById("total-amount");
  totalAmount.innerText = "$" + cartData.total.toFixed(2);

  // If the cart is empty, close the cart modal
  if (cartData.items.length === 0) {
    closeCartModal();
  }
}

// Function to open the cart modal
function openCartModal() {
  const cartModal = document.getElementById("cart-modal");
  cartModal.style.display = "block";
}

// Function to close the cart modal
function closeCartModal() {
  const cartModal = document.getElementById("cart-modal");
  cartModal.style.display = "none";
}

// Function to update the cart icon with the number of items
function updateCartIcon() {
  const cartIcon = document.querySelector(".cart-icon span");
  cartIcon.innerText = cartData.items.length;
}

// Function to extract the 'totalAmount' parameter from the URL
function getTotalAmountFromURL() {
  var urlParams = new URLSearchParams(window.location.search);
  var totalAmount = urlParams.get('totalAmount');
  return parseFloat(totalAmount) || 0;
}

// Function to update the total amount displayed on the page
function updateTotalAmount() {
  var totalAmount = getTotalAmountFromURL();
  document.getElementById('total-amount').innerText = "$" + totalAmount.toFixed(2);
}

// Call the function to update the total amount when the page loads
window.onload = updateTotalAmount;

// Function to redirect to the checkout page and pass the total amount
function redirectToCheckout() {
  var totalAmount = cartData.total.toFixed(2);
  var checkoutURL = "/checkout.html?totalAmount=" + totalAmount;
  window.location.href = checkoutURL;
}


function processPayment() {
            // Add any necessary payment processing logic here
            alert('Payment successful!');
        }

        // Function to redirect to index.html
        function redirectToIndex() {
            window.location.href = '/index.html'; // Replace '/index.html' with the actual URL of your index.html
        }

