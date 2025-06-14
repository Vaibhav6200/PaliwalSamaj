const ageField = document.getElementById("age");
ageField.addEventListener("input", function() {
  document.getElementById("selected_age").innerText = this.value;
});