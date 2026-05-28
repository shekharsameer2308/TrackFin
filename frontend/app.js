const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:5000/api' : '/api';
let expenseChartInstance = null;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    // Set default date for input to today
    document.getElementById('date').valueAsDate = new Date();
    
    // Form submission
    document.getElementById('transaction-form').addEventListener('submit', handleAddTransaction);
    
    // Fetch initial data
    fetchDashboardData();
});

// Modal Logic
function openModal() {
    document.getElementById('add-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('add-modal').classList.remove('active');
    document.getElementById('transaction-form').reset();
    document.getElementById('date').valueAsDate = new Date();
}

// Data Fetching
async function fetchDashboardData() {
    try {
        const [summaryRes, txRes] = await Promise.all([
            fetch(`${API_URL}/summary`),
            fetch(`${API_URL}/transactions`)
        ]);
        
        const summary = await summaryRes.json();
        const transactions = await txRes.json();
        
        updateSummaryCards(summary);
        updateChart(summary.expensesByCategory);
        updateTransactionList(transactions);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// UI Updates
function updateSummaryCards(summary) {
    const formatMoney = (amount) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
    
    document.getElementById('net-amount').innerText = formatMoney(summary.net);
    document.getElementById('income-amount').innerText = '+' + formatMoney(summary.income);
    document.getElementById('expense-amount').innerText = '-' + formatMoney(summary.expenses);
}

function getCategoryIcon(category) {
    const icons = {
        'Food': '🍔',
        'Transport': '🚗',
        'Housing': '🏠',
        'Entertainment': '🎬',
        'Shopping': '🛍️',
        'Salary': '💰',
        'Other': '✨'
    };
    return icons[category] || '📌';
}

function updateTransactionList(transactions) {
    const list = document.getElementById('transaction-list');
    list.innerHTML = '';
    
    if (transactions.length === 0) {
        list.innerHTML = '<div style="text-align:center; padding: 20px; color: var(--text-muted)">No transactions yet. Add one to get started!</div>';
        return;
    }
    
    transactions.slice(0, 10).forEach(tx => {
        const dateObj = new Date(tx.date);
        const dateString = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        
        const isExpense = tx.type === 'expense';
        const amountSign = isExpense ? '-' : '+';
        const amountColorClass = isExpense ? 'text-danger' : 'text-success';
        
        const item = document.createElement('div');
        item.className = 'transaction-item';
        item.innerHTML = `
            <div class="tx-info">
                <div class="tx-icon ${tx.type}">
                    ${getCategoryIcon(tx.category)}
                </div>
                <div class="tx-details">
                    <h4>${tx.category}</h4>
                    <p>${tx.notes || (isExpense ? 'Expense' : 'Income')} • ${dateString}</p>
                </div>
            </div>
            <div class="tx-amount ${amountColorClass}">
                ${amountSign}$${tx.amount.toFixed(2)}
            </div>
        `;
        list.appendChild(item);
    });
}

function updateChart(categories) {
    const ctx = document.getElementById('expenseChart').getContext('2d');
    
    const labels = Object.keys(categories);
    const data = Object.values(categories);
    
    if (expenseChartInstance) {
        expenseChartInstance.destroy();
    }
    
    if (labels.length === 0) {
        // Render a placeholder empty chart
        labels.push("No Data");
        data.push(1);
    }
    
    expenseChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#d946ef', // magenta primary
                    '#ec4899', // pinkish accent
                    '#c026d3', // darker magenta
                    '#10b981', // success green
                    '#f472b6', // lighter pink
                    '#3b82f6', // blue
                    '#9ca3af'  // grey
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#94a3b8',
                        font: { family: 'Outfit' }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleFont: { family: 'Outfit' },
                    bodyFont: { family: 'Outfit' },
                    padding: 12,
                    cornerRadius: 8
                }
            },
            cutout: '70%'
        }
    });
}

// Handlers
async function handleAddTransaction(e) {
    e.preventDefault();
    
    const typeNode = document.querySelector('input[name="type"]:checked');
    const type = typeNode ? typeNode.value : 'expense';
    
    const amount = document.getElementById('amount').value;
    const category = document.getElementById('category').value;
    const date = document.getElementById('date').value;
    const notes = document.getElementById('notes').value;
    
    const payload = { type, amount, category, date, notes };
    
    try {
        const response = await fetch(`${API_URL}/transactions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            closeModal();
            fetchDashboardData();
        } else {
            alert("Error saving transaction.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the server.");
    }
}
