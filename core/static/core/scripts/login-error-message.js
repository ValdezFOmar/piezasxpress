// @ts-check

(function() {
    const errorContainer = document.querySelector('#error-container');
    const overlay = document.querySelector('.overlay');

    if (!errorContainer) {
        return;
    }

    /** @param {Event} event **/
    const handler = (event) => {
        event.stopPropagation();
        errorContainer.remove();
        document.body.classList.remove('displaying-error');
    };

    errorContainer.addEventListener('click', handler);
    overlay?.addEventListener('click', handler);
})();
