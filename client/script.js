// script.js
function updateExpenseList() {
    fetch('http://localhost:8000')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            document.getElementById('remaining-budget').textContent = (data.budget - data.expenses.reduce((sum, exp) => sum + exp.amount, 0)).toFixed(2);

            const expenseList = document.getElementById('expenses');
            expenseList.innerHTML = data.expenses
                .map(exp => 
                    `<li>
                        ${exp.name} - $${exp.amount} (${exp.category})
                        <button onclick="deleteExpense(${exp.id})">Delete</button>
                    </li>`
                ).join('');

                const categorySummary = document.getElementById('category-summary');

                Object.entries(data.categorySummary).forEach(([category, total]) => {
                    console.log(category, total);
                });
                
                categorySummary.innerHTML = Object.entries(data.categorySummary)
                    .map(([category, total]) => `<li>${category}: $${total.toFixed(2)}</li>`)
                    .join('');
        });
}

function setBudget() {
    const budget = parseFloat(document.getElementById('budget').value);
    fetch('http://localhost:8000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: "budget", amount: budget })
    }).then(() => {
        updateExpenseList();
    });
}

function addExpense() {
    const name = document.getElementById('expense-name').value;
    const amount = parseFloat(document.getElementById('expense-amount').value);
    const category = document.getElementById('expense-category').value;

    fetch('http://localhost:8000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: "expense", name, amount, category })
    }).then(() => {
        document.getElementById('expense-name').value = '';
        document.getElementById('expense-amount').value = '';
        document.getElementById('expense-category').value = '';

        updateExpenseList();
    });
}

function deleteExpense(expenseId) {
    fetch(`http://localhost:8000/${expenseId}`, {
        method: 'DELETE'
    }).then(() => {
        updateExpenseList(); 
    });
}

document.addEventListener('DOMContentLoaded', updateExpenseList);
