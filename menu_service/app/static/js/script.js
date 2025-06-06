const endpoint = "http://localhost:5000/graphql";

// Ambil dan tampilkan data menu
async function fetchMenu() {
    const query = `
        {
            menu {
                id
                name
                description
                price
            }
        }
    `;

    const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    const data = await response.json();
    const menuList = document.getElementById("menu-list");
    menuList.innerHTML = "";

    data.data.menu.forEach(item => {
        const div = document.createElement("div");
        div.innerHTML = `<strong>${item.name}</strong> - ${item.description} (${item.price})`;
        menuList.appendChild(div);
    });
}

// Tambahkan menu baru
document.getElementById("menu-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;
    const price = parseInt(document.getElementById("price").value);

    const mutation = `
        mutation {
            createMenuItem(name: "${name}", description: "${description}", price: ${price}) {
                menuItem {
                    id
                    name
                }
            }
        }
    `;

    const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: mutation })
    });

    const result = await response.json();
    console.log(result);
    fetchMenu(); // refresh daftar menu
    document.getElementById("menu-form").reset();
});

fetchMenu();
