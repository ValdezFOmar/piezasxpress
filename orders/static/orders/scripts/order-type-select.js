const selectInput = document.getElementById("data-orden");
const idLabel = document.getElementById("data-id-label");

selectInput.addEventListener("change", () => {
    idLabel.innerText = `ID de ${selectInput.value}`;
});
