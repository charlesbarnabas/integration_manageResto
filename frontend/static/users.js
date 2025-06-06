async function fetchUsers() {
  const response = await fetch("http://user_service:5000/graphql", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      query: `
        query {
          allUsers {
            id
            name
            email
            role
          }
        }
      `
    })
  });

  const result = await response.json();
  const users = result.data.allUsers;

  const list = document.getElementById("user-list");
  list.innerHTML = "";
  users.forEach(user => {
    const div = document.createElement("div");
    div.textContent = `${user.name} (${user.email}) - ${user.role}`;
    list.appendChild(div);
  });
} 

fetchUsers();
