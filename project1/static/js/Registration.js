function validateForm() {
  var x = document.forms["register"]["username"].value;
  var password = document.forms["register"]["password"].value;
  var email = document.forms["register"]["email"].value;

  var fun1 = validateUser(x);
  var fun2 = validatePassword(password);
  var fun3 = validateEmail(email);

  if (fun1 == true && fun2 == true && fun3 == true) {
    return true;
  }
  return false;
}

function validateUser(x) {
  if (x == "") {
    document.querySelector(".usermessage").innerHTML = "Enter username.";
    // alert("Name must be filled out");
    return false;
  }
  return true;
}

function validatePassword(password) {
  var password = password;
  var cap = 0;
  var num = 0;
  var small = 0;
  var special = 0;

  if (password == "") {
    document.querySelector(".passmessage").innerHTML = "Enter password.";
    // alert("password must be filled out");
    return false;
  }

  if (password.length < 6) {
    document.querySelector(".passmessage").innerHTML =
      "Password should alteast contain 6 characters.";
    return false;
  }

  for (let i = 0; i < password.length; i++) {
    // console.log(password)
    var t = password.charCodeAt(i); //kR1shna
    // console.log(i)
    if (t >= 49 && t <= 57) {
      num++;
    }
    if (t >= 65 && t <= 90) {
      cap++;
    }
    if (t >= 97 && t <= 122) {
      small++;
    }
    if (t == 42 || t == 64 || t == 46 || t == 95) {
      special++;
    }
  }

  if (num >= 1 && cap >= 1 && small >= 1 && special >= 1) {
    return true;
  } else {
    var msg =
      "Password should contain atleast one [A-Z],[a-z],[1-0],special characters.";
    //console.log(num + cap + small + special)
    document.querySelector(".passmessage").innerHTML = msg;
    // alert("reached")

    return false;
  }
}

//email validation
function validateEmail(email) {
  var e = email;
  var parts = e.split("@"); //chaitu.krish4@gmail.com

  var message = "Invalid Email";
  var atSymbol = e.indexOf("@");

  // check for @
  if (atSymbol < 1) {
    document.querySelector(".emailmessage").innerHTML = message;
    return false;
  }
  var dot = atSymbol + parts[1].indexOf(".");
  if (dot <= atSymbol + 2) {
    document.querySelector(".emailmessage").innerHTML = message;
    return false;
  }

  // check that the dot is not at the end
  if (dot === e.length - 1) {
    //g
    document.querySelector(".emailmessage").innerHTML = message;
    return false;
  }

  return true;
}
