// Contains all the JS for the user home page.

const passwordArea = document.getElementById('usersPassword');
const passwordHandlerBtn = document.getElementById('passwordHandlerBtn');
const originalPassword = passwordArea.textContent; // Save the original password in a variable to show later
const albanianSound = document.getElementById('albanianSound');
let timesClicked = 0; // I will add one to this and check whether its an even or odd number after every click, and that will determine whether to hide or show

// Set the pasword area text to a placeholder at first
let placeholderText = "";
let usersPassLength = passwordArea.textContent.length
let asterisk = "*";
placeholderText += asterisk.repeat(usersPassLength); // Let there be an asterisk for however many chacracters are in the user's pass
passwordArea.textContent = placeholderText;

// Add button logic on click (ODD NUMBERS SHOW PASSWORD, EVEN ONES HIDE IT)
passwordHandlerBtn.addEventListener('click', (event) => {
    timesClicked += 1;
    console.log(`Button clicked ${timesClicked} times.`);
    if (timesClicked % 2 != 0) {
       passwordHandlerBtn.textContent = "Hide Password!🗿"
       passwordArea.textContent = originalPassword;
    }
    else {
        passwordHandlerBtn.textContent = "Show Password!😀";
        passwordArea.textContent = placeholderText;
    }
});

// Loop the albania song
albanianSound.volume = 0.25; // 25% original volume, its loud
albanianSound.loop = true;
albanianSound.play();