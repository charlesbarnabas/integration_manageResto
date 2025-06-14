document.addEventListener('DOMContentLoaded', function() {
  const tbody = document.getElementById('order-table-body');
  const searchInput = document.getElementById('search');
  let cart = [];

  function fetchOrders(query = '') {
    fetch('/api/transaction/orders')
      .then(res => res.json())
      .then(data => {
        tbody.innerHTML = '';
        data.filter(order => order.customer_name.toLowerCase().includes(query.toLowerCase()))
          .forEach(order => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${order.id}</td>
              <td>${order.customer_name}</td>
              <td>${order.status}</td>
              <td>${new Date(order.created_at).toLocaleString()}</td>
              <td>
                <a href="#" class="link edit" onclick="showOrderDetail(${order.id})">Detail</a>
              </td>
            `;
            tbody.appendChild(tr);
          });
      });
  }

  searchInput.addEventListener('input', function() {
    fetchOrders(this.value);
  });

  function fetchMenus() {
    return fetch('http://localhost:5001/api/menus')
      .then(res => res.json());
  }

  function renderMenuOptions(menus) {
    const select = document.getElementById('menu-select');
    select.innerHTML = '';
    menus.forEach(menu => {
      const option = document.createElement('option');
      option.value = menu.id;
      option.textContent = `${menu.name} (Rp${menu.price})`;
      select.appendChild(option);
    });
  }

  function addToCart() {
    const menuId = document.getElementById('menu-select').value;
    const menuName = document.getElementById('menu-select').selectedOptions[0].textContent;
    const quantity = parseInt(document.getElementById('menu-qty').value, 10);
    if (!menuId || quantity < 1) return;
    const existing = cart.find(item => item.menu_item_id == menuId);
    if (existing) {
      existing.quantity += quantity;
    } else {
      cart.push({ menu_item_id: menuId, menu_item_name: menuName, quantity });
    }
    renderCart();
  }

  function renderCart() {
    const cartBody = document.getElementById('cart-body');
    cartBody.innerHTML = '';
    cart.forEach((item, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${item.menu_item_name}</td><td>${item.quantity}</td><td><button onclick="removeFromCart(${idx})">Hapus</button></td>`;
      cartBody.appendChild(tr);
    });
  }

  function removeFromCart(idx) {
    cart.splice(idx, 1);
    renderCart();
  }

  function submitOrder() {
    const customerName = document.getElementById('customer-name').value;
    if (!customerName || cart.length === 0) return alert('Isi nama dan keranjang!');
    fetch('/api/transaction/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customer_name: customerName, items: cart.map(i => ({ menu_item_id: i.menu_item_id, quantity: i.quantity })) })
    })
      .then(res => res.json())
      .then(data => {
        alert('Order berhasil!');
        window.location.reload();
      });
  }

  if (document.getElementById('menu-select')) {
    fetchMenus().then(renderMenuOptions);
    document.getElementById('add-to-cart').onclick = addToCart;
    document.getElementById('submit-order').onclick = submitOrder;
  }

  fetchOrders();
});

function showOrderDetail(orderId) {
  // Placeholder: fetch and show order detail in modal
  alert('Show detail for order #' + orderId);
}
