document.addEventListener('DOMContentLoaded', function() {
  const txTbody = document.getElementById('transaction-table-body');
  const procurementTbody = document.getElementById('procurement-table-body');
  const searchInput = document.getElementById('search');

  function fetchOrderTransactions(query = '') {
    fetch('/api/transaction/transactions')
      .then(res => res.json())
      .then(data => {
        txTbody.innerHTML = '';
        data.filter(tx => {
          // Cari berdasarkan nama pelanggan
          return (tx.customer_name || '').toLowerCase().includes(query.toLowerCase());
        })
        .forEach(tx => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${tx.id}</td>
            <td>${tx.order_id}</td>
            <td>${tx.customer_name || ''}</td>
            <td>${tx.order_status || ''}</td>
            <td>${tx.amount}</td>
            <td>${tx.method}</td>
            <td>${tx.status}</td>
            <td>${new Date(tx.created_at).toLocaleString()}</td>
          `;
          txTbody.appendChild(tr);
        });
      });
  }

  function fetchProcurementTransactions(query = '') {
    fetch('/api/transaction/procurement')
      .then(res => res.json())
      .then(data => {
        procurementTbody.innerHTML = '';
        data.filter(tx => {
          // Cari berdasarkan nama bahan
          return (tx.ingredient_name || '').toLowerCase().includes(query.toLowerCase());
        })
        .forEach(tx => {
          const createdAt = tx.created_at ? (isNaN(Date.parse(tx.created_at)) ? tx.created_at : new Date(tx.created_at).toLocaleString()) : '';
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${tx.id}</td>
            <td>${tx.procurement_order_id ?? ''}</td>
            <td>${tx.ingredient_name ?? ''}</td>
            <td>${tx.quantity ?? ''}</td>
            <td>${tx.supplier ?? ''}</td>
            <td>${tx.amount ?? ''}</td>
            <td>${tx.status ?? ''}</td>
            <td>${createdAt}</td>
          `;
          procurementTbody.appendChild(tr);
        });
      });
  }

  searchInput.addEventListener('input', function() {
    fetchOrderTransactions(this.value);
    fetchProcurementTransactions(this.value);
  });

  fetchOrderTransactions();
  fetchProcurementTransactions();
  showTab('order');
});

function showTab(tab) {
  document.getElementById('order-transactions').style.display = tab === 'order' ? '' : 'none';
  document.getElementById('procurement-transactions').style.display = tab === 'procurement' ? '' : 'none';
  document.getElementById('tab-order').classList.toggle('active', tab === 'order');
  document.getElementById('tab-procurement').classList.toggle('active', tab === 'procurement');
}
