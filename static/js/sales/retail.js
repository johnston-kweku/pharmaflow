/**
 * Wholesale Cart Management
 */

class RetailCart {
    constructor() {
        this.items = JSON.parse(localStorage.getItem('retail_cart')) || [];
        this.cartItemsContainer = document.getElementById('cart-items');
        this.searchInput = document.getElementById('id_query');
        this.productRows = document.querySelectorAll('div[data-drug-id]');
        
        this.init();
    }

    init() {
        this.renderCart();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Add to cart buttons
        document.querySelectorAll('button[data-drug-id]').forEach(button => {
            button.addEventListener('click', (e) => {
                // Find the parent container that has all the data attributes
                // We exclude the button itself by looking for the closest div with the attribute
                const productRow = button.closest('div[data-drug-id]');
                
                if (!productRow) {
                    console.error('Could not find parent row for button:', button);
                    return;
                }

                const drugId = productRow.getAttribute('data-drug-id');
                const name = productRow.getAttribute('data-drug-name');
                const price = parseFloat(productRow.getAttribute('data-drug-price'));
                const stock = parseInt(productRow.getAttribute('data-drug-stock'));

                if (!name || isNaN(price) || isNaN(stock)) {
                    console.error('Could not find product details for row:', productRow);
                    return;
                }

                this.addItem({
                    id: drugId,
                    name: name,
                    price: price,
                    stock: stock,
                    quantity: 1
                });
            });
        });

        // Search filtering
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase();
                this.productRows.forEach(row => {
                    const name = row.getAttribute('data-drug-name').toLowerCase();
                    if (name.includes(query)) {
                        row.classList.remove('hidden');
                    } else {
                        row.classList.add('hidden');
                    }
                });
            });
        }
    }

    addItem(product) {
        const existingItem = this.items.find(item => item.id === product.id);
        if (existingItem) {
            if (existingItem.quantity < existingItem.stock) {
                existingItem.quantity += 1;
            } else {
                toast.show('Cannot add more than available stock', 'error');
                return;
            }
        } else {
            this.items.push(product);
        }
        this.saveAndRender();
    }

    removeItem(id) {
        this.items = this.items.filter(item => item.id !== id);
        this.saveAndRender();
    }

    updateQuantity(id, delta) {
        const item = this.items.find(item => item.id === id);
        if (item) {
            const newQuantity = item.quantity + delta;
            if (newQuantity > 0 && newQuantity <= item.stock) {
                item.quantity = newQuantity;
                this.saveAndRender();
            } else if (newQuantity <= 0) {
                this.removeItem(id);
            } else {
                toast.show('Cannot exceed available stock', 'error');
            }
        }
    }

    saveAndRender() {
        localStorage.setItem('retail_cart', JSON.stringify(this.items));
        this.renderCart();
    }

    renderCart() {
        if (!this.cartItemsContainer) return;

        if (this.items.length === 0) {
            this.cartItemsContainer.innerHTML = '<p class="text-sm text-gray-400 text-center py-8">Your cart is empty</p>';
            this.updateTotal(0);
            return;
        }

        let html = '';
        let total = 0;

        this.items.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            html += `
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-100">
                    <div class="flex flex-col flex-1">
                        <p class="font-bold text-slate-700">${item.name}</p>
                        <p class="text-xs text-blue-600 font-medium">¢${item.price} x ${item.quantity}</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="cart.updateQuantity('${item.id}', -1)" class="w-6 h-6 flex items-center justify-center bg-white border border-gray-200 rounded-lg text-gray-500 hover:bg-gray-50">-</button>
                        <span class="text-sm font-bold w-4 text-center">${item.quantity}</span>
                        <button onclick="cart.updateQuantity('${item.id}', 1)" class="w-6 h-6 flex items-center justify-center bg-white border border-gray-200 rounded-lg text-gray-500 hover:bg-gray-50">+</button>
                        <button onclick="cart.removeItem('${item.id}')" class="ml-2 text-red-400 hover:text-red-600">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-0.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v0.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>
                        </button>
                    </div>
                </div>
            `;
        });

        this.cartItemsContainer.innerHTML = html;
        this.updateTotal(total);
    }

    updateTotal(total) {
        const totalContainer = document.getElementById('cart-total');
        if (totalContainer) {
            totalContainer.textContent = `¢${total.toFixed(2)}`;
        }
    }

    async checkout() {
        if (this.items.length === 0) return;

        const button = document.getElementById('checkout-btn');
        const customerSelect = document.getElementById('customer-select');
        const customerId = customerSelect ? customerSelect.value : null;
        const originalText = button.textContent;
        button.disabled = true;
        button.textContent = 'Processing...';
        const url = button.getAttribute('data-checkout-url')

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    customer_id: customerId,
                    items: this.items.map(item => ({
                        id: item.id,
                        quantity: item.quantity
                    }))
                })
            });

            const data = await response.json();

            if (data.success) {
                toast.show(data.message);
                this.items = [];
                this.saveAndRender();
                
                // Open receipt in new window
                if (data.sale_id) {
                    window.open(`/sales/receipt/${data.sale_id}/`, '_blank');
                }

                data.updated_stock.forEach(drug => {
                    const row = document.querySelector(`[data-drug-id="${drug.id}"]`)
                    if (row) {
                        row.setAttribute('data-drug-stock', drug.inventory);
                        const stockText = row.querySelector('.stock-text');
                        if (stockText) stockText.textContent = `Stock: ${drug.inventory}`
                    }
                })
            } else {
                toast.show(`Error: ${data.message}`, 'error');
            }
        } catch (error) {
            console.error('Checkout error:', error);
            toast.show('An error occurred during checkout.', 'error');
        } finally {
            button.disabled = false;
            button.textContent = originalText;
        }
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

const cart = new RetailCart();
window.cart = cart;
