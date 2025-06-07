// GraphQL endpoint
const GRAPHQL_ENDPOINT = '/graphql';

// GraphQL queries and mutations
const GET_INVENTORY = `
    query {
        inventory {
            id
            name
            quantity
            price
        }
    }
`;

const ADD_ITEM = `
    mutation($name: String!, $quantity: Int!, $price: Float!) {
        addItem(name: $name, quantity: $quantity, price: $price) {
            id
            name
            quantity
            price
        }
    }
`;

const UPDATE_ITEM = `
    mutation($id: ID!, $name: String!, $quantity: Int!, $price: Float!) {
        updateItem(id: $id, name: $name, quantity: $quantity, price: $price) {
            id
            name
            quantity
            price
        }
    }
`;

const DELETE_ITEM = `
    mutation($id: ID!) {
        deleteItem(id: $id) {
            success
        }
    }
`;

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

// Function to fetch and display inventory
async function fetchInventory() {
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: GET_INVENTORY
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        const inventoryList = document.getElementById('inventoryList');
        inventoryList.innerHTML = '';
        
        data.data.inventory.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>Rp ${item.price.toLocaleString()}</td>
                <td>
                    <button class="btn btn-sm btn-warning btn-action" onclick="editItem('${item.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger btn-action" onclick="deleteItem('${item.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            inventoryList.appendChild(row);
        });
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

// Function to add new item
async function addItem(event) {
    event.preventDefault();
    
    const name = document.getElementById('itemName').value;
    const quantity = parseInt(document.getElementById('quantity').value);
    const price = parseFloat(document.getElementById('price').value);
    
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: ADD_ITEM,
                variables: { name, quantity, price }
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        showToast('Item berhasil ditambahkan');
        event.target.reset();
        fetchInventory();
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

// Function to edit item
async function editItem(id) {
    // Implementation for edit functionality
    // This would typically open a modal with the item's current data
    showToast('Fitur edit akan segera hadir', 'info');
}

// Function to delete item
async function deleteItem(id) {
    if (!confirm('Apakah Anda yakin ingin menghapus item ini?')) {
        return;
    }
    
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: DELETE_ITEM,
                variables: { id }
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        if (data.data.deleteItem.success) {
            showToast('Item berhasil dihapus');
            fetchInventory();
        } else {
            showToast('Item tidak ditemukan', 'warning');
        }
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch of inventory
    fetchInventory();
    
    // Form submission handler
    document.getElementById('inventoryForm').addEventListener('submit', addItem);
}); 