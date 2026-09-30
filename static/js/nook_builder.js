// Style My Cozy Nook - Interactive Room & Desk Visualizer
document.addEventListener('DOMContentLoaded', function() {
    const activeItems = new Map(); // slotName -> { id, name, price, imgUrl }
    
    const slots = {
        'lamp': document.getElementById('slot-lamp'),
        'vase': document.getElementById('slot-vase'),
        'cup': document.getElementById('slot-cup'),
        'wallmate': document.getElementById('slot-wallmate'),
        'bowl': document.getElementById('slot-bowl'),
    };

    const harmonyProgress = document.getElementById('harmony-progress');
    const harmonyText = document.getElementById('harmony-percentage');
    const bundleSubtotalEl = document.getElementById('nook-subtotal');
    const bundleDiscountEl = document.getElementById('nook-discount');
    const bundleTotalEl = document.getElementById('nook-total');
    const addBundleBtn = document.getElementById('btn-add-bundle');
    const bundleIdsInput = document.getElementById('bundle-product-ids');

    // Item selection cards
    document.querySelectorAll('.nook-item-card').forEach(card => {
        card.addEventListener('click', function() {
            const id = this.dataset.id;
            const slot = this.dataset.slot;
            const name = this.dataset.name;
            const price = parseFloat(this.dataset.price);
            const imgUrl = this.dataset.img;

            // If already selected, toggle off
            if (activeItems.has(slot) && activeItems.get(slot).id === id) {
                removeItemFromSlot(slot);
                this.classList.remove('selected');
            } else {
                // Remove existing selection on this slot
                document.querySelectorAll(`.nook-item-card[data-slot="${slot}"]`).forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                placeItemInSlot(slot, { id, name, price, imgUrl });
            }

            updateNookSummary();
        });
    });

    function placeItemInSlot(slot, item) {
        activeItems.set(slot, item);
        const slotEl = slots[slot];
        if (slotEl) {
            slotEl.innerHTML = `
                <div class="placed-item-wrapper" title="${item.name} ($${item.price.toFixed(2)})">
                    <img src="${item.imgUrl}" alt="${item.name}" class="placed-img" />
                    <button type="button" class="remove-slot-btn" data-slot="${slot}" title="Remove item">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="placed-tag">${item.name}</div>
                </div>
            `;
            slotEl.classList.add('occupied');

            // Attach remove listener
            slotEl.querySelector('.remove-slot-btn').addEventListener('click', function(e) {
                e.stopPropagation();
                removeItemFromSlot(slot);
                const activeCard = document.querySelector(`.nook-item-card[data-slot="${slot}"][data-id="${item.id}"]`);
                if (activeCard) activeCard.classList.remove('selected');
                updateNookSummary();
            });
        }
    }

    function removeItemFromSlot(slot) {
        activeItems.delete(slot);
        const slotEl = slots[slot];
        if (slotEl) {
            slotEl.innerHTML = `<span class="empty-slot-label"><i class="fa-solid fa-plus"></i> Place ${slot}</span>`;
            slotEl.classList.remove('occupied');
        }
    }

    function updateNookSummary() {
        const count = activeItems.size;
        let subtotal = 0;
        const ids = [];

        activeItems.forEach(item => {
            subtotal += item.price;
            ids.push(item.id);
        });

        // Harmony Score
        let harmonyPercent = 20;
        if (count === 1) harmonyPercent = 65;
        else if (count === 2) harmonyPercent = 82;
        else if (count === 3) harmonyPercent = 94;
        else if (count >= 4) harmonyPercent = 100;

        if (harmonyProgress) harmonyProgress.style.width = `${harmonyPercent}%`;
        if (harmonyText) harmonyText.textContent = `${harmonyPercent}% Japandi Harmony`;

        // 15% Cozy Nook Bundle Discount
        const discountRate = 0.15;
        const discount = subtotal * discountRate;
        const total = subtotal - discount;

        if (bundleSubtotalEl) bundleSubtotalEl.textContent = `$${subtotal.toFixed(2)}`;
        if (bundleDiscountEl) bundleDiscountEl.textContent = `-$${discount.toFixed(2)} (15% OFF)`;
        if (bundleTotalEl) bundleTotalEl.textContent = `$${total.toFixed(2)}`;

        if (bundleIdsInput) {
            bundleIdsInput.value = JSON.stringify(ids);
        }

        if (addBundleBtn) {
            addBundleBtn.disabled = (count === 0);
            if (count === 0) {
                addBundleBtn.classList.add('opacity-50', 'cursor-not-allowed');
            } else {
                addBundleBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            }
        }
    }

    // Auto-select hero items on page load for instant aesthetic satisfaction
    const initialLamp = document.querySelector('.nook-item-card[data-slot="lamp"][data-id="1"]');
    const initialVase = document.querySelector('.nook-item-card[data-slot="vase"][data-id="2"]');
    const initialCup = document.querySelector('.nook-item-card[data-slot="cup"][data-id="3"]');

    if (initialLamp) initialLamp.click();
    if (initialVase) initialVase.click();
    if (initialCup) initialCup.click();
});
