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
    mutation($id: ID!, $name: String, $quantity: Int) {
        updateIngredient(id: $id, name: $name, quantity: $quantity) {
            id
            name
            quantity
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
                    <button class="btn btn-sm btn-warning btn-action" onclick="editIngredient('${ingredient.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger btn-action" onclick="deleteIngredient('${ingredient.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
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

// Function to edit ingredient
async function editIngredient(id) {
    // Implementation for edit functionality
    // This would typically open a modal with the ingredient's current data
    showToast('Fitur edit akan segera hadir', 'info');
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
