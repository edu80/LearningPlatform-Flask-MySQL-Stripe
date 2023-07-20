const header= document.querySelector("header");

window.addEventListener ("scroll", function(){
    header.classList.toggle ("sticky", window.scrollY > 0);
    });

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
  xhr.open("POST", "register.py", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      // Registration success message or error handling
      console.log(xhr.responseText);
    }
  };
  var data = "name=" + encodeURIComponent(name) + "&email=" + encodeURIComponent(email) + "&password=" + encodeURIComponent(password);
  xhr.send(data);
}

// Login form submission
function loginUser() {
  // Retrieve form data
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  // Send form data to the server using AJAX
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "login.py", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      // Login success message or error handling
      console.log(xhr.responseText);
    }
  };
  var data = "email=" + encodeURIComponent(email) + "&password=" + encodeURIComponent(password);
  xhr.send(data);
}
