document.addEventListener('DOMContentLoaded', function () {
  const tbody = document.getElementById('order-table-body');
  const searchInput = document.getElementById('search');
  const orderModal = document.getElementById('order-detail-modal');
  let cart = [];

  function fetchOrders(query = '') {
    fetch('/api/transaction/orders')
      .then(res => res.json())
      .then(data => {
        tbody.innerHTML = '';
        data
          .filter(order => order.customer_name.toLowerCase().includes(query.toLowerCase()))
          .forEach(order => {
            const tr = document.createElement('tr');
            let aksiBtn = '';
            if (order.status === 'pending' || order.status === 'unpaid') {
              aksiBtn = `<button class="btn-pay styled-btn" data-id="${order.id}">💳 Bayar</button>`;
            } else {
              aksiBtn = `<button class="btn-view styled-btn" data-id="${order.id}">👁️ Lihat</button>`;
            }
            tr.innerHTML = `
              <td>${order.id}</td>
              <td>${order.customer_name}</td>
              <td>${order.status}</td>
              <td>${new Date(order.created_at).toLocaleString()}</td>
              <td style="display:flex;gap:0.5em;">${aksiBtn}</td>
            `;
            tbody.appendChild(tr);
          });
      });
  }

  searchInput?.addEventListener('input', function () {
    fetchOrders(this.value);
  });

  tbody.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-view')) {
      const id = e.target.dataset.id;
      showOrderDetail(id);
    }
    if (e.target.classList.contains('btn-pay')) {
      const id = e.target.dataset.id;
      showConfirmModal(
        'Konfirmasi Pembayaran',
        'Proses pembayaran untuk order #' + id + '?',
        () => payOrder(id)
      );
    }
  });

  function showConfirmModal(title, message, onYes) {
    const modal = document.getElementById('confirm-modal');
    document.getElementById('confirm-modal-title').textContent = title;
    document.getElementById('confirm-modal-message').textContent = message;
    modal.classList.remove('hidden');
    const yesBtn = document.getElementById('confirm-modal-yes');
    const noBtn = document.getElementById('confirm-modal-no');
    function cleanup() {
      modal.classList.add('hidden');
      yesBtn.removeEventListener('click', yesHandler);
      noBtn.removeEventListener('click', noHandler);
    }
    function yesHandler() {
      cleanup();
      if (onYes) onYes();
    }
    function noHandler() {
      cleanup();
    }
    yesBtn.addEventListener('click', yesHandler);
    noBtn.addEventListener('click', noHandler);
  }

  function payOrder(orderId) {
    fetch(`/api/transaction/orders/${orderId}/pay`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ method: 'cash' })
    })
      .then(res => res.ok ? res.json() : res.json().then(err => Promise.reject(err)))
      .then(data => {
        alert(`Pembayaran berhasil! ID Transaksi: ${data.transaction_id}, Jumlah: Rp${data.amount}`);
        fetchOrders();
      })
      .catch(err => alert('Error: ' + (err.error || err.message)));
  }

  function fetchMenus() {
    return fetch('http://localhost:5001/api/menus')
      .then(res => res.json());
  }

  function renderMenuOptions(menus) {
    const select = document.getElementById('menu-select');
    if (!select) return;
    select.innerHTML = '';
    menus.forEach(menu => {
      const option = document.createElement('option');
      option.value = menu.id;
      option.textContent = `${menu.name} (Rp${menu.price})`;
      select.appendChild(option);
    });
  }

  function addToCart() {
    const menuSelect = document.getElementById('menu-select');
    const menuId = menuSelect.value;
    const menuName = menuSelect.selectedOptions[0].textContent;
    const quantity = parseInt(document.getElementById('menu-qty').value, 10);
    if (!menuId || quantity < 1) return alert('Pilih menu dan masukkan jumlah yang valid!');

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
    let total = 0;
    cartBody.innerHTML = '';
    cart.forEach((item, idx) => {
      const price = parseInt((item.menu_item_name.match(/Rp(\d+)/) || [0,0])[1], 10) || 0;
      total += price * item.quantity;
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${item.menu_item_name}</td><td>${item.quantity}</td><td><button class="btn-remove styled-btn" title="Hapus" onclick="removeFromCart(${idx})"><span style='color:#e11d48;font-size:1.2em;'>&#128465;</span></button></td>`;
      cartBody.appendChild(tr);
    });
    document.getElementById('cart-total').textContent = total;
  }

  window.removeFromCart = function (idx) {
    cart.splice(idx, 1);
    renderCart();
  }

  function submitOrder() {
    const customerName = document.getElementById('customer-name').value;
    if (!customerName || cart.length === 0) return alert('Isi nama dan keranjang!');

    const items = cart.map(i => ({ menu_item_id: i.menu_item_id, quantity: i.quantity }));
    fetch('/api/transaction/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customer_name: customerName, items })
    })
      .then(res => res.ok ? res.json() : res.json().then(err => Promise.reject(err)))
      .then(data => {
        alert(`Order berhasil! ID Order: ${data.order_id}, Total: Rp${data.total}`);
        window.location.reload();
      })
      .catch(err => alert('Error: ' + (err.error || err.message)));
  }

  function showOrderDetail() {
    window.location.href = '/transactions';
  }

  if (document.getElementById('menu-select')) {
    fetchMenus().then(renderMenuOptions);
    document.getElementById('add-to-cart').onclick = addToCart;
    document.getElementById('submit-order').onclick = submitOrder;
  }

  fetchOrders();

  // Tambahkan style untuk tombol aksi
  const style = document.createElement('style');
  style.textContent = `
    .styled-btn {
      background: #6366f1;
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 0.4em 1em;
      font-size: 1em;
      cursor: pointer;
      transition: background 0.2s;
      margin: 0 2px;
      box-shadow: 0 1px 4px #0001;
      display: inline-flex;
      align-items: center;
      gap: 0.3em;
    }
    .styled-btn:hover {
      background: #4338ca;
    }
    .btn-remove {
      background: #fff0f3;
      color: #e11d48;
      border: 1px solid #e11d48;
      padding: 0.2em 0.7em;
      border-radius: 6px;
      font-size: 1em;
      transition: background 0.2s, color 0.2s;
    }
    .btn-remove:hover {
      background: #e11d48;
      color: #fff;
    }
    .modal.hidden { display: none !important; }
    .modal { z-index: 1000; }
  `;
  document.head.appendChild(style);
});
