// @ts-check

/** @type {HTMLElement|null} **/
const partsContainer = document.querySelector('#parts-container');
/** @type {HTMLButtonElement|null} **/
const addPartButton = document.querySelector('#button-add');
/** @type {HTMLInputElement|null} **/
const partIdInput = document.querySelector('#part-id');
/** @type {HTMLElement|null} **/
const noPartsMessage = document.querySelector('#no-parts-message');
/** @type {HTMLButtonElement|null} **/
const submitButton = document.querySelector('#submit-button');

if (
    !partIdInput ||
    !submitButton ||
    !addPartButton ||
    !noPartsMessage ||
    !partsContainer
) {
    throw new Error('Elements missing');
}

/**
 * @typedef Part
 * @property {number} id
 * @property {string} name
 */

/**
 * @typedef CarPart
 * @property {number} partId
 * @property {number} price
 * @property {number} quantity
 * @property {string} comment
 */

/**
 * List of selected part ID's that are used to search the required fields for
 * all car parts in the DOM.
 * @type {Set<number>}
 */
const selectedPartsId = new Set();

getParts().then(parts => {
    if (parts === null) {
        throw new Error('List of parts is null');
    }
    const integerPattern = /^[0-9]+$/;
    const partsMap = new Map(parts.map(part => [part.id, part]));

    addPartButton.addEventListener('click', () => {
        const value = partIdInput.value.trim();
        if (!integerPattern.test(value)) {
            return;
        }
        const id = parseInt(value);
        const part = partsMap.get(id);
        if (part === undefined) {
            return;
        }
        addPart(partsContainer, part);
        partIdInput.value = '';
    });
});

submitButton.addEventListener('click', async () => {
    if (selectedPartsId.size === 0) {
        return;
    }

    /** @type {HTMLInputElement|null} **/
    const carIdElement = document.querySelector('#car-id');
    if (!carIdElement) {
        throw new Error('Element with id "car-id" missing');
    }
    const carId = carIdElement.value;

    /** @type {CarPart[]} **/
    const carParts = [];

    for (const id of selectedPartsId) {
        const body = document.getElementById(`body-${id}`);
        if (!body) {
            throw new Error(`No body for part with id = ${id}`);
        }
        /** @type {HTMLInputElement|null} **/
        const price = body.querySelector(`#price-${id}`);
        /** @type {HTMLInputElement|null} **/
        const comment = body.querySelector(`#comment-${id}`);
        /** @type {HTMLInputElement|null} **/
        const quantity = body.querySelector(`#quantity-${id}`);
        if (!price || !quantity || !comment) {
            throw new Error('One or more of price, quantity and comment values missing');
        }
        const priceValue = parseFloat(price.value);
        const quantityValue = parseInt(quantity.value);
        if (Number.isNaN(priceValue) || Number.isNaN(quantityValue)) {
            throw new Error('Price or quantiy value is not valid');
        }
        carParts.push({
            partId: id,
            price: priceValue,
            quantity: quantityValue,
            comment: comment.value,
        });
    }

    const csrfToken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1] ?? '';

    const response = await fetch(`/storage/car/${carId}/parts`, {
        method: 'POST',
        redirect: 'follow',
        headers: { 'X-CSRFToken': csrfToken },
        body: JSON.stringify(carParts),
    });
    if (response.redirected) {
        window.location.assign(response.url);
    }
});

const updateMessage = () => {
    noPartsMessage.style.display = partsContainer.innerHTML.replace(/\s/g, '') ? 'none' : 'block';
};

/**
 * @returns {Promise<Part[]|null>}
 */
async function getParts() {
    try {
        const response = await fetch('/storage/part/list');
        const content = await response.json();
        return content;
    } catch (error) {
        console.error(error);
        return null;
    }
}

/**
 * @param {HTMLElement} container
 * @param {Part} part
 */
function addPart(container, part) {
    if (selectedPartsId.has(part.id)) {
        console.warn(`A car part with part id "${part.id}" already exists, ignoring`);
        return;
    }

    const newPart = document.createElement('li');
    newPart.id = `body-${part.id}`;
    newPart.className = 'data-part flex-column';
    newPart.innerHTML = getPartStructure(part);
    container.appendChild(newPart);

    document.getElementById(`button-delete-${part.id}`)?.addEventListener('click', e => {
        deletePart(/** @type {any} **/(e.target))
    });
    document.getElementById(`button-comment-${part.id}`)?.addEventListener('click', e => {
        toggleComment(/** @type {any} **/(e.target))
    });
    document.getElementById(`comment-underlay-${part.id}`)?.addEventListener('click', e => {
        toggleComment(/** @type {any} **/(e.target))
    });

    selectedPartsId.add(part.id);
    updateMessage();
}

/**
 * @param {HTMLElement} button
 */
function deletePart(button) {
    const id = parseInt(button.dataset.id ?? '');
    const partBody = document.getElementById(`body-${id}`);
    if (!Number.isNaN(id) && partBody) {
        selectedPartsId.delete(id);
        partBody.remove();
        updateMessage();
    }
}

/**
 * @param {HTMLElement} element
 */
function toggleComment(element) {
    const partId = element.dataset.id;
    document.getElementById(`comment-${partId}`)?.classList.toggle('active');
    document.getElementById(`comment-underlay-${partId}`)?.classList.toggle('active');
}

/**
 * @param {Part} param0
 */
function getPartStructure({ id, name }) {
    const displayId = id.toString().padStart(3, '0');
    return `<div class="id flex-column">
                <p class="number">${displayId}</p>
                <p class="name">${name}</p>
            </div>
            <div class="item flex-row">
                <div class="user-input flex-column">
                    <div class="flex-column">
                        <label for="price-${id}">Precio</label>
                        <div class="currency-field">
                            <p class="sign">$</p>
                            <input id="price-${id}" class="currency" type="number" min="0" step="1" value="0.00">
                        </div>
                    </div>
                    <div class="flex-column">
                        <label for="quantity-${id}">Cantidad</label>
                        <input id="quantity-${id}" class="quantity-field" type="number" min="1" value="1">
                    </div>
                </div>
            </div>
            <div class="comment-section">
                <button id="button-comment-${id}" class="button-base button-outline button-comment" type="button" data-id="${id}">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="32px"
                        height="32px"
                        viewBox="0 -960 960 960">
                        <path d="M240-400h480v-80H240v80Zm0-120h480v-80H240v80Zm0-120h480v-80H240v80ZM880-80 720-240H160q-33 0-56.5-23.5T80-320v-480q0-33 23.5-56.5T160-880h640q33 0 56.5 23.5T880-800v720ZM160-320h594l46 45v-525H160v480Zm0 0v-480 480Z"/>
                    </svg>
                </button>
                <textarea id="comment-${id}" class="comment-textarea" spellcheck="false"></textarea>
                <div id="comment-underlay-${id}" class="comment-underlay" data-id="${id}"></div>
            </div>
            <button id="button-delete-${id}" class="button-base button-outline button-delete" type="button" data-id="${id}">
                <svg
                    class="icon"
                    xmlns="http://www.w3.org/2000/svg"
                    width="35px"
                    height="35px"
                    viewBox="0 -960 960 960">
                    <path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/>
                </svg>
            </button>`;
}
