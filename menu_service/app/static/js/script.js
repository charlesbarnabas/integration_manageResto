document.getElementById('search').addEventListener('input', function (e) {
  const keyword = e.target.value.toLowerCase();
  filterMenu(keyword);
});

function filterMenu(keyword) {
  const rows = document.querySelectorAll('#menu-container tr');
  rows.forEach(row => {
    const name = row.querySelector('td:nth-child(1)').textContent.toLowerCase();
    const ingredients = row.querySelector('td:nth-child(3)').textContent.toLowerCase();
    if (name.includes(keyword) || ingredients.includes(keyword)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

async function fetchInventory() {
    try {
        const response = await fetch('http://localhost:5002/api/inventory');
        if (!response.ok) throw new Error('Failed to fetch inventory');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching inventory:', error);
        return [];
    }
}

function addIngredientRow(containerId, ingredient = null) {
    const container = document.getElementById(containerId);
    const row = document.createElement('div');
    row.className = 'ingredient-row';

    const ingredientInput = document.createElement('input');
    ingredientInput.type = 'text';
    ingredientInput.name = 'ingredient_name';
    ingredientInput.placeholder = 'Nama bahan';
    ingredientInput.required = true;
    if (ingredient) {
        ingredientInput.value = ingredient.ingredient_name;
    }

    const quantityInput = document.createElement('input');
    quantityInput.type = 'number';
    quantityInput.name = 'quantity';
    quantityInput.min = '0';
    quantityInput.step = 'any';
    quantityInput.placeholder = 'Jumlah';
    quantityInput.required = true;
    if (ingredient) {
        quantityInput.value = ingredient.quantity;
    }

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.innerHTML = '🗑️ Hapus';
    removeBtn.className = 'btn delete-ingredient';
    removeBtn.onclick = () => container.removeChild(row);

    row.appendChild(ingredientInput);
    row.appendChild(quantityInput);
    row.appendChild(removeBtn);

    container.appendChild(row);
}

async function submitForm(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value;
    const price = parseFloat(document.getElementById('price').value);

    const ingredientRows = document.querySelectorAll('#ingredients-container .ingredient-row');
    const ingredients = [];
    for (const row of ingredientRows) {
        const ingredient_name = row.querySelector('input[name="ingredient_name"]').value.trim();
        const quantity = parseFloat(row.querySelector('input[name="quantity"]').value);
        if (!ingredient_name || !quantity) {
            alert('Semua bahan harus diisi dan jumlah harus diisi.');
            return false;
        }
        ingredients.push({ ingredient_name, quantity });
    }

    const response = await fetch('/api/menus', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description, price, ingredients })
    });

    if (response.ok) {
        alert('Menu berhasil ditambahkan');
        window.location.href = '/';
    } else {
        const errorText = await response.text();
        console.error('Error adding menu:', errorText);
        alert('Gagal menambahkan menu: ' + errorText);
    }
    return false;
}



async function loadMenu() {
    const response = await fetch('/api/menus');
    if (!response.ok) {
        console.error('Failed to load menus');
        return;
    }
    const menus = await response.json();
    const container = document.getElementById('menu-container');
    container.innerHTML = '';

menus.forEach(menu => {
    const row = document.createElement('tr');
    const ingredientsText = menu.ingredients.map(ing => `${ing.ingredient_name} (${ing.quantity})`).join(', ');
    row.innerHTML = `
        <td>${menu.name}</td>
        <td>Rp ${menu.price.toLocaleString('id-ID')}</td>
        <td>${ingredientsText}</td>
        <td>
            <a href="#" class="link edit" onclick="editMenu(${menu.id})">Edit</a>
            <a href="#" class="link delete" onclick="deleteMenu(${menu.id})">Hapus</a>
        </td>
    `;
    container.appendChild(row);
});
}

async function editMenu(id) {
    const response = await fetch(`/api/menus/${id}`);
    if (!response.ok) {
        alert('Gagal mengambil data menu');
        return;
    }
    const menu = await response.json();
    document.getElementById('edit-id').value = menu.id;
    document.getElementById('edit-name').value = menu.name;
    document.getElementById('edit-price').value = menu.price;
    document.getElementById('edit-description').value = menu.description;

    const ingredientsContainer = document.getElementById('edit-ingredients');
    ingredientsContainer.innerHTML = '';
    menu.ingredients.forEach(ingredient => {
        addIngredientRow('edit-ingredients', ingredient);
    });

    document.getElementById('edit-form').classList.remove('hidden');
    window.scrollTo({ top: document.getElementById('edit-form').offsetTop, behavior: 'smooth' });
}

async function submitEdit() {
    const id = document.getElementById('edit-id').value;
    const name = document.getElementById('edit-name').value;
    const price = parseFloat(document.getElementById('edit-price').value);
    const description = document.getElementById('edit-description').value;

    const ingredientRows = document.querySelectorAll('#edit-ingredients .ingredient-row');
    const ingredients = [];
    for (const row of ingredientRows) {
        const ingredient_name = row.querySelector('input[name="ingredient_name"]').value.trim();
        const quantity = parseFloat(row.querySelector('input[name="quantity"]').value);
        if (!ingredient_name || !quantity) {
            alert('Semua bahan harus diisi dan jumlah harus diisi.');
            return;
        }
        ingredients.push({ ingredient_name, quantity });
    }

    const response = await fetch(`/api/menus/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description, price, ingredients })
    });

    if (response.ok) {
        alert('Menu berhasil diperbarui');
        loadMenu();
        document.getElementById('edit-form').classList.add('hidden');
    } else {
        alert('Gagal memperbarui menu');
    }
}

async function deleteMenu(id) {
    if (!confirm('Yakin ingin menghapus menu ini?')) return;
    const response = await fetch(`/api/menus/${id}`, { method: 'DELETE' });
    if (response.ok) {
        alert('Menu berhasil dihapus');
        loadMenu();
    } else {
        alert('Gagal menghapus menu');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadMenu();
});
