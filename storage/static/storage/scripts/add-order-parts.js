// @ts-check

document.querySelector('#add-parts')?.addEventListener('click', async () => {
    const table = document.querySelector('#parts');
    if (!table) {
        console.error('No #parts table found');
        return;
    }
    const parts = table.querySelectorAll('tbody tr');

    /** @type {string[]} **/
    const addedParts = [];
    for (const part of parts) {
        /** @type {HTMLInputElement|null} **/
        const checkbox = part.querySelector('input[type=checkbox]');
        if (checkbox?.checked) {
            addedParts.push(checkbox.value);
        }
    }
    if (addedParts.length === 0) {
        console.warn('No parts added, aborting');
        return;
    }

    const partIds = addedParts.map(part => Number.parseInt(part));
    const csrfToken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1] ?? '';

    const response = await fetch('/orders/add-parts', {
        method: 'POST',
        redirect: 'follow',
        headers: { 'X-CSRFToken': csrfToken },
        body: JSON.stringify(partIds),
    });
    if (response.redirected) {
        window.location.assign(response.url);
    }
});
