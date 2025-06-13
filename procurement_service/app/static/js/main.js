const GRAPHQL_ENDPOINT = '/graphql';

// GraphQL queries and mutations for Procurement Service
const GET_PROCUREMENT_ORDERS = `
    query {
        procurementOrders {
            id
            ingredientName
            quantityOrdered
            supplier
            status
            orderDate
        }
    }
`;

const CREATE_PROCUREMENT_ORDER = `
    mutation($ingredientName: String!, $quantityOrdered: Int!, $supplier: String!) {
        createProcurementOrder(ingredientName: $ingredientName, quantityOrdered: $quantityOrdered, supplier: $supplier) {
            procurementOrder {
                id
                ingredientName
                quantityOrdered
                supplier
                status
                orderDate
            }
        }
    }
`;

const UPDATE_PROCUREMENT_ORDER_STATUS = `
    mutation($id: ID!, $status: String!) {
        updateProcurementOrderStatus(id: $id, status: $status) {
            procurementOrder {
                id
                ingredientName
                quantityOrdered
                supplier
                status
                orderDate
            }
        }
    }
`;

const GET_INGREDIENTS_FROM_INVENTORY_SERVICE = `
    query {
        ingredients {
            name
        }
    }
`;

const INVENTORY_SERVICE_GRAPHQL_ENDPOINT = 'http://localhost:5002/graphql';

// Utility function to show toast notifications
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Function to fetch procurement orders and populate the table
async function fetchProcurementOrders() {
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: GET_PROCUREMENT_ORDERS
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        const procurementOrderList = document.getElementById('procurementOrderList');
        procurementOrderList.innerHTML = '';
        
        data.data.procurementOrders.forEach(order => {
            const row = document.createElement('tr');
            const orderDate = new Date(order.orderDate).toLocaleString();
            row.innerHTML = `
                <td>${order.ingredientName}</td>
                <td>${order.quantityOrdered}</td>
                <td>${order.status}</td>
                <td>${orderDate}</td>
                <td>${order.supplier}</td>
                <td>
                    <select class="form-select form-select-sm" onchange="showUpdateStatusModal('${order.id}', this.value)">
                        <option value="pending" ${order.status === 'pending' ? 'selected' : ''}>Pending</option>
                        <option value="approved" ${order.status === 'approved' ? 'selected' : ''}>Approved</option>
                        <option value="rejected" ${order.status === 'rejected' ? 'selected' : ''}>Rejected</option>
                        <option value="delivered" ${order.status === 'delivered' ? 'selected' : ''}>Delivered</option>
                    </select>
                </td>
            `;
            procurementOrderList.appendChild(row);
        });
    } catch (error) {
        showToast(`Error fetching procurement orders: ${error.message}`, 'danger');
    }
}

// Function to fetch ingredient names from Inventory Service
async function fetchIngredientNames() {
    try {
        const response = await fetch(INVENTORY_SERVICE_GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: GET_INGREDIENTS_FROM_INVENTORY_SERVICE
            })
        });
        
        console.log('Raw response from inventory_service:', response);
        const data = await response.json();
        console.log('Parsed data from inventory_service:', data);

        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        const ingredientSelect = document.getElementById('ingredientName');
        data.data.ingredients.forEach(ingredient => {
            const option = document.createElement('option');
            option.value = ingredient.name;
            option.textContent = ingredient.name;
            ingredientSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error in fetchIngredientNames:', error);
        showToast(`Error fetching ingredients: ${error.message}`, 'danger');
    }
}

// Function to handle creating a new procurement order
async function createProcurementOrder(event) {
    event.preventDefault();
    
    const ingredientName = document.getElementById('ingredientName').value;
    const quantityOrdered = parseInt(document.getElementById('quantityOrdered').value);
    const supplier = document.getElementById('supplier').value;
    
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: CREATE_PROCUREMENT_ORDER,
                variables: { ingredientName, quantityOrdered, supplier }
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        showToast('Procurement order created successfully!');
        event.target.reset();
        fetchProcurementOrders();
    } catch (error) {
        showToast(`Error creating order: ${error.message}`, 'danger');
    }
}

let currentOrderId = null;
let currentOrderStatus = null;

// Function to show update status modal
function showUpdateStatusModal(orderId, currentStatus) {
    currentOrderId = orderId;
    currentOrderStatus = currentStatus; // Store current status

    const editStatusModal = new bootstrap.Modal(document.getElementById('editStatusModal'));
    document.getElementById('editOrderId').value = orderId;
    document.getElementById('orderStatus').value = currentStatus; // Set current status in dropdown
    editStatusModal.show();
}

// Function to submit status update
async function submitStatusUpdate() {
    const newStatus = document.getElementById('orderStatus').value;
    
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: UPDATE_PROCUREMENT_ORDER_STATUS,
                variables: { id: currentOrderId, status: newStatus }
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        showToast('Order status updated successfully!');
        const editStatusModal = bootstrap.Modal.getInstance(document.getElementById('editStatusModal'));
        editStatusModal.hide();
        fetchProcurementOrders();
    } catch (error) {
        showToast(`Error updating status: ${error.message}`, 'danger');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    fetchProcurementOrders();
    fetchIngredientNames();
    
    const procurementOrderForm = document.getElementById('procurementOrderForm');
    if (procurementOrderForm) {
        procurementOrderForm.addEventListener('submit', createProcurementOrder);
    }
}); 