const GRAPHQL_ENDPOINT = '/graphql';

// GraphQL queries and mutations
const GET_INGREDIENTS = `
    query {
        ingredients {
            id
            name
            quantity
            minimumStockLevel
            reorderQuantity
            unitOfMeasure
        }
    }
`;

const ADD_INGREDIENT = `
    mutation($name: String!, $quantity: Int!, $minimumStockLevel: Int!, $reorderQuantity: Int!, $unitOfMeasure: String!) {
        addIngredient(name: $name, quantity: $quantity, minimumStockLevel: $minimumStockLevel, reorderQuantity: $reorderQuantity, unitOfMeasure: $unitOfMeasure) {
            id
            name
            quantity
            minimumStockLevel
            reorderQuantity
            unitOfMeasure
        }
    }
`;

const UPDATE_INGREDIENT = `
    mutation($id: ID!, $name: String!, $quantity: Int!, $minimumStockLevel: Int!, $reorderQuantity: Int!, $unitOfMeasure: String!) {
        updateIngredient(
            id: $id, 
            name: $name, 
            quantity: $quantity,
            minimumStockLevel: $minimumStockLevel,
            reorderQuantity: $reorderQuantity,
            unitOfMeasure: $unitOfMeasure
        ) {
            id
            name
            quantity
            minimumStockLevel
            reorderQuantity
            unitOfMeasure
        }
    }
`;

const DELETE_INGREDIENT = `
    mutation($id: ID!) {
        deleteIngredient(id: $id) {
            success
        }
    }
`;

// New GraphQL query to fetch menus from menu_service
const MENU_SERVICE_GRAPHQL_ENDPOINT = 'http://localhost:5001/graphql';

const GET_MENUS = `
    query {
        allMenus {
            id
            name
        }
    }
`

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

function filterIngredients(keyword) {
    const rows = document.querySelectorAll('#ingredientList tr');
    const lowerKeyword = keyword.toLowerCase();
    rows.forEach(row => {
        const cellsText = row.textContent.toLowerCase();
        if (cellsText.includes(lowerKeyword)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch of ingredients
    fetchIngredients();
    
    // Fetch ingredient names from menu_service to populate dropdown
    fetchIngredientNamesFromMenuService();
    
    // Form submission handler
    document.getElementById('ingredientForm').addEventListener('submit', addIngredient);

    // Search bar handler: filter saat mengetik
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            filterIngredients(this.value);
        });
    }

    // Event listener for when the edit modal is shown
    const editModalElement = document.getElementById('editModal');
    if (editModalElement) {
        editModalElement.addEventListener('shown.bs.modal', () => {
            // Populate the form fields here, after the modal is fully shown
            const ingredient = editModalElement.dataset.currentIngredient ? JSON.parse(editModalElement.dataset.currentIngredient) : null;
            if (ingredient) {
                document.getElementById('editIngredientId').value = ingredient.id;
                document.getElementById('editIngredientName').value = ingredient.name;
                document.getElementById('editIngredientQuantity').value = ingredient.quantity;
                document.getElementById('editMinimumStockLevel').value = ingredient.minimumStockLevel;
                document.getElementById('editReorderQuantity').value = ingredient.reorderQuantity;
                document.getElementById('editUnitOfMeasure').value = ingredient.unitOfMeasure;
            }
        });
    }
});

async function fetchIngredients() {
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: GET_INGREDIENTS
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        const ingredientList = document.getElementById('ingredientList');
        ingredientList.innerHTML = '';
        
        data.data.ingredients.forEach(ingredient => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${ingredient.name}</td>
                <td>${ingredient.quantity}</td>
                <td>${ingredient.minimumStockLevel !== null ? ingredient.minimumStockLevel : ''}</td>
                <td>${ingredient.reorderQuantity !== null ? ingredient.reorderQuantity : ''}</td>
                <td>${ingredient.unitOfMeasure !== null ? ingredient.unitOfMeasure : ''}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn-action btn-edit" onclick="editIngredient('${ingredient.id}')">Edit</button>
                        <button class="btn-action btn-delete" onclick="deleteIngredient('${ingredient.id}')">Hapus</button>
                    </div>
                </td>
            `;
            ingredientList.appendChild(row);
        });
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

const MENU_SERVICE_GRAPHQL_ENDPOINT_2 = 'http://localhost:5001/graphql';

const GET_INGREDIENTS_FROM_MENU_SERVICE_2 = `
    query {
        allMenus {
            ingredients {
                ingredientName
            }
        }
    }
`;

async function fetchIngredientNamesFromMenuService() {
    try {
        const response = await fetch(MENU_SERVICE_GRAPHQL_ENDPOINT_2, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: GET_INGREDIENTS_FROM_MENU_SERVICE_2
            })
        });
        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }
        const menus = result.data.allMenus;
        const ingredientSet = new Set();
        menus.forEach(menu => {
            menu.ingredients.forEach(ing => {
                ingredientSet.add(ing.ingredientName);
            });
        });
        const ingredientSelect = document.getElementById('ingredientName');
        ingredientSelect.innerHTML = '<option value="" disabled selected>Pilih bahan</option>';
        ingredientSet.forEach(name => {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            ingredientSelect.appendChild(option);
        });
    } catch (error) {
        showToast(`Gagal memuat bahan: ${error.message}`, 'danger');
    }
}

async function addIngredient(event) {
    event.preventDefault();
    
    const name = document.getElementById('ingredientName').value;
    const quantity = parseInt(document.getElementById('ingredientQuantity').value);
    const minimumStockLevel = parseInt(document.getElementById('minimumStockLevel').value);
    const reorderQuantity = parseInt(document.getElementById('reorderQuantity').value);
    const unitOfMeasure = document.getElementById('unitOfMeasure').value;
    
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: ADD_INGREDIENT,
                variables: { name, quantity, minimumStockLevel, reorderQuantity, unitOfMeasure }
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        showToast('Bahan berhasil ditambahkan');
        event.target.reset();
        fetchIngredients();
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

document.getElementById('ingredientForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const name = document.getElementById('ingredientName').value;
    const quantity = document.getElementById('ingredientQuantity').value;
    const minimumStockLevel = document.getElementById('minimumStockLevel').value;
    const reorderQuantity = document.getElementById('reorderQuantity').value;
    const unitOfMeasure = document.getElementById('unitOfMeasure').value;

    const response = await fetch('/api/inventory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name,
            quantity: Number(quantity),
            minimumStockLevel: Number(minimumStockLevel),
            reorderQuantity: Number(reorderQuantity),
            unitOfMeasure
        })
    });

    if (response.ok) {
        // Refresh tabel dan reset form
        fetchIngredients();
        this.reset();
    } else {
        const data = await response.json();
        alert(data.error || 'Gagal menambah bahan');
    }
});

// Function to edit ingredient
async function editIngredient(id) {
    console.log('editIngredient called with id:', id);
    try {
        const ingredientIdNum = parseInt(id); // Parse the ID to an integer
        console.log('Parsed ingredientIdNum:', ingredientIdNum);
        // Find the ingredient in the current list
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: GET_INGREDIENTS
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        console.log('Fetched ingredients:', data.data.ingredients);
        const ingredient = data.data.ingredients.find(i => parseInt(i.id) === ingredientIdNum);
        console.log('Found ingredient:', ingredient);
        if (!ingredient) {
            throw new Error('Bahan tidak ditemukan');
        }
        
        // Store ingredient data in the modal dataset for access when modal is shown
        const editModalElement = document.getElementById('editModal');
        editModalElement.dataset.currentIngredient = JSON.stringify(ingredient);
        
        // Show the modal
        const editModal = new bootstrap.Modal(editModalElement);
        editModal.show();
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

// Function to submit edit
async function submitEdit() {
    const id = document.getElementById('editIngredientId').value;
    const name = document.getElementById('editIngredientName').value;
    const quantity = parseInt(document.getElementById('editIngredientQuantity').value);
    const minimumStockLevel = parseInt(document.getElementById('editMinimumStockLevel').value);
    const reorderQuantity = parseInt(document.getElementById('editReorderQuantity').value);
    const unitOfMeasure = document.getElementById('editUnitOfMeasure').value;
    
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: UPDATE_INGREDIENT,
                variables: { 
                    id, 
                    name, 
                    quantity, 
                    minimumStockLevel, 
                    reorderQuantity, 
                    unitOfMeasure 
                }
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        // Close the modal
        const editModal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
        editModal.hide();
        
        showToast('Bahan berhasil diperbarui');
        fetchIngredients(); // Refresh the list
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

// Function to delete ingredient
async function deleteIngredient(id) {
    if (!confirm('Apakah Anda yakin ingin menghapus bahan ini?')) {
        return;
    }
    
    try {
        const response = await fetch(GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: DELETE_INGREDIENT,
                variables: { id }
            })
        });
        
        const data = await response.json();
        if (data.errors) {
            throw new Error(data.errors[0].message);
        }
        
        if (data.data.deleteIngredient.success) {
            showToast('Bahan berhasil dihapus');
            fetchIngredients();
        } else {
            showToast('Bahan tidak ditemukan', 'warning');
        }
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch of ingredients
    fetchIngredients();
    
    // Fetch ingredient names from menu_service to populate dropdown
    fetchIngredientNamesFromMenuService();
    
    // Form submission handler
    document.getElementById('ingredientForm').addEventListener('submit', addIngredient);
});
