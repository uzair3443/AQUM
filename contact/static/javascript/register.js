const passwordInput = document.getElementById("password");
const lengthRequirement = document.getElementById("length");
const uppercaseRequirement = document.getElementById("uppercase");
const lowercaseRequirement = document.getElementById("lowercase");
const numberRequirement = document.getElementById("number");
const specialRequirement = document.getElementById("special");

passwordInput.addEventListener("input", () => {
    const password = passwordInput.value;
    if (password.length >= 8) {
        lengthRequirement.classList.add("green");
    } else {
        lengthRequirement.classList.remove("green");
    }
    if (password.match(/[A-Z]/)) {
        uppercaseRequirement.classList.add("green");
    } else {
        uppercaseRequirement.classList.remove("green");
    }
    if (password.match(/[a-z]/)) {
        lowercaseRequirement.classList.add("green");
    } else {
        lowercaseRequirement.classList.remove("green");
    }
    if (password.match(/\d/)) {
        numberRequirement.classList.add("green");
    } else {
        numberRequirement.classList.remove("green");
    }
    if (password.match(/[^a-zA-Z\d]/)) {
        specialRequirement.classList.add("green");
    } else {
        specialRequirement.classList.remove("green");
    }
});