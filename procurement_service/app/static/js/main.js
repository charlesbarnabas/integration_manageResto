document.addEventListener('DOMContentLoaded', () => {
    const orderForm = document.getElementById('orderForm');
    const ordersTableBody = document.getElementById('ordersTableBody');
    const ingredientSelect = document.getElementById('ingredientName');
    const quantityInput = document.getElementById('quantityOrdered');
    const supplierInput = document.getElementById('supplier');

    let inventoryData = [];

    // Fetch inventory ingredients from inventory_service
    async function fetchInventory() {
        try {
            const response = await fetch('http://localhost:5002/api/inventory');
            const data = await response.json();
            inventoryData = data;
            populateIngredientDropdown();
        } catch (error) {
            console.error('Error fetching inventory:', error);
        }
    }

    // Populate ingredient dropdown
    function populateIngredientDropdown() {
        ingredientSelect.innerHTML = '<option value="">Select Ingredient</option>';
        inventoryData.forEach(item => {
            const option = document.createElement('option');
            option.value = item.name;
            option.textContent = item.name;
            option.dataset.reorderQuantity = item.reorder_quantity || 1;
            ingredientSelect.appendChild(option);
        });
    }

    // On ingredient change, update quantity input with reorder quantity
    ingredientSelect.addEventListener('change', () => {
        const selectedOption = ingredientSelect.options[ingredientSelect.selectedIndex];
        const reorderQty = selectedOption.dataset.reorderQuantity || 1;
        quantityInput.value = reorderQty;
    });

    // Fetch and display procurement orders
    async function fetchOrders() {
        const query = `
        query {
            procurementOrders {
                id
                ingredientName
                quantityOrdered
                status
                orderDate
                supplier
            }
        }`;
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query})
        });
        const result = await response.json();
        const orders = result.data.procurementOrders;
        ordersTableBody.innerHTML = '';
        orders.forEach(order => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${order.ingredientName}</td>
                <td>${order.quantityOrdered}</td>
                <td>${order.status}</td>
                <td>${new Date(order.orderDate).toLocaleString()}</td>
                <td>${order.supplier || ''}</td>
                <td>
                    <select data-id="${order.id}" class="status-select">
                        <option value="pending" ${order.status === 'pending' ? 'selected' : ''}>Pending</option>
                        <option value="ordered" ${order.status === 'ordered' ? 'selected' : ''}>Ordered</option>
                        <option value="received" ${order.status === 'received' ? 'selected' : ''}>Received</option>
                    </select>
                </td>
            `;
            ordersTableBody.appendChild(tr);
        });

        // Add event listeners to status selects
        document.querySelectorAll('.status-select').forEach(select => {
            select.addEventListener('change', async (e) => {
                const id = e.target.getAttribute('data-id');
                const newStatus = e.target.value;
                const mutation = `
                mutation {
                    updateProcurementOrderStatus(id: "${id}", status: "${newStatus}") {
                        id
                        status
                    }
                }`;
                await fetch('/graphql', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: mutation})
                });
                fetchOrders();
            });
        });
    }

    // Handle form submission to create new order
    orderForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const ingredientName = ingredientSelect.value;
        const quantityOrdered = parseInt(quantityInput.value);
        const supplier = supplierInput.value;

        if (!ingredientName) {
            alert('Please select an ingredient.');
            return;
        }

        const mutation = `
        mutation {
            createProcurementOrder(ingredientName: "${ingredientName}", quantityOrdered: ${quantityOrdered}, supplier: "${supplier}") {
                id
                ingredientName
                quantityOrdered
                status
                orderDate
                supplier
            }
        }`;

        await fetch('/graphql', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query: mutation})
        });

        orderForm.reset();
        fetchOrders();
    });

    fetchInventory();
    fetchOrders();
});
