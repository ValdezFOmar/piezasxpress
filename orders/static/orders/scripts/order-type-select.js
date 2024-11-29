// @ts-check

/** @type {HTMLSelectElement|null} **/
const selectInput = document.querySelector("#data-orden");

/** @type {HTMLLabelElement|null} **/
const idLabel = document.querySelector("#data-id-label");

selectInput?.addEventListener("change", () => {
    if (idLabel) {
        const orderType = selectInput.selectedOptions[0].innerText;
        idLabel.innerText = `ID de ${orderType}`;
    }
});
