const API = "/auth";

// ================= SIGNUP =================
function signup() {
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;

  if (!email || !password) {
    alert("Please fill all fields");
    return;
  }

  fetch(API + "/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.msg);

    if (data.msg && data.msg.includes("OTP")) {
      localStorage.setItem("email", email);

      // Show OTP box (for signup page)
      let signupBox = document.getElementById("signupBox");
      let otpBox = document.getElementById("otpBox");

      if (signupBox && otpBox) {
        signupBox.style.display = "none";
        otpBox.style.display = "block";
      }
    }
  })
  .catch(() => alert("Signup error"));
}


// ================= VERIFY OTP =================
function verifyOTP() {
  let email = localStorage.getItem("email");
  let otp = document.getElementById("otp").value;

  if (!otp) {
    alert("Enter OTP");
    return;
  }

  fetch(API + "/verify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, otp })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.msg);

    if (data.msg && data.msg.includes("verified")) {
      window.location.href = "/login";
    }
  })
  .catch(() => alert("OTP verification error"));
}


// ================= LOGIN =================
function login() {
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;

  if (!email || !password) {
    alert("Please fill all fields");
    return;
  }

  fetch(API + "/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.token) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("userEmail", email);

      alert("Login successful");

      window.location.href = "/index.html";  //This is fine for Flask
      // But also store token for API calls:
      localStorage.setItem("token", data.token);
    } else {
      alert(data.msg);
    }
  })
  .catch(() => alert("Login error"));
}


// ================= FORGOT PASSWORD =================
function forgot() {
  let email = document.getElementById("email").value;

  if (!email) {
    alert("Enter email");
    return;
  }

  fetch(API + "/forgot", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.msg);

    if (data.msg && data.msg.includes("OTP")) {
      localStorage.setItem("email", email);

      // Redirect to reset page
      window.location.href = "/reset";
    }
  })
  .catch(() => alert("Error sending OTP"));
}


// ================= RESET PASSWORD =================
function resetPassword() {
  let email = document.getElementById("email").value;
  let otp = document.getElementById("otp").value;
  let password = document.getElementById("password").value;

  if (!email || !otp || !password) {
    alert("Fill all fields");
    return;
  }

  fetch(API + "/reset", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, otp, password })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.msg);

    if (data.msg && data.msg.includes("updated")) {
      window.location.href = "/login";
    }
  })
  .catch(() => alert("Reset error"));
}


// ================= LOGOUT =================
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("email");
  localStorage.removeItem("userEmail");

  alert("Logged out");
  window.location.href = "/login";
}


// ================= TOKEN HELPER =================
function getToken() {
  return localStorage.getItem("token");
}