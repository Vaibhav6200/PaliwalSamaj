const login_submit_btn = document.getElementById("login_submit_btn");
const mobile_number = document.getElementById("mobile_number");
const click_here_btn = document.getElementById("click_here_btn");
const password = document.getElementById("password");

password.addEventListener("input", function () {
    if (password.value.trim() !== "" && mobile_number.value.trim() !== "") {
        login_submit_btn.classList.remove("disabled");
        click_here_btn.disabled = true;
    } else {
        login_submit_btn.classList.add("disabled");
        click_here_btn.disabled = false;
    }
});

click_here_btn.addEventListener("click",function(){
    $("#login-form").valid();
})