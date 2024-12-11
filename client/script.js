function login(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    }).then(response => {
        if (response.status === 200) {
            return response.json().then(data => {
                localStorage.setItem('token', data.token); 
                alert('Login successful!');
                window.location.href = 'index.html';
            });
        } else {
            return response.json().then(data => {
                alert('Login failed: ' + data.message);
            });
        }
    });
}

function register(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        document.getElementById('register-error').textContent = 'Passwords do not match!';
        return;
    }

    fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password,confirmPassword })
    }).then(response => {
        if (response.status === 200) {
            return response.json().then(data => {
                alert('Registration successful!');
                window.location.href = 'login.html';
            });
        } else {
            return response.json().then(data => {
                document.getElementById('register-error').textContent = 'Registration failed: ' + data.message;
            });
        }
    });
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

function updateExpenseList() {
    if (!localStorage.getItem('token')) {
        window.location.href = 'login.html';
        return;
    }

    fetch('http://localhost:8000', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('remaining-budget').textContent = 
                (data.budget - data.expenses.reduce((sum, exp) => sum + exp.amount, 0)).toFixed(2);

            const expenseList = document.getElementById('expenses');
            expenseList.innerHTML = data.expenses
                .map(exp => 
                    `<li>
                        ${exp.name} - $${exp.amount} (${exp.category})
                        <button onclick="deleteExpense(${exp.id})">Delete</button>
                    </li>`
                ).join('');

            const categorySummary = document.getElementById('category-summary');
            categorySummary.innerHTML = Object.entries(data.categorySummary)
                .map(([category, total]) => `<li>${category}: $${total.toFixed(2)}</li>`)
                .join('');
        });
}

if (!window.location.href.includes('login.html') && !window.location.href.includes('register.html')) {
    document.addEventListener('DOMContentLoaded', updateExpenseList);
}
