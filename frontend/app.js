const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:5000/api' : '/api';
let expenseChartInstance = null;
let isLoginMode = true;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('date').valueAsDate = new Date();
    document.getElementById('transaction-form').addEventListener('submit', handleAddTransaction);
    document.getElementById('goal-form').addEventListener('submit', handleAddGoal);
    document.getElementById('auth-form').addEventListener('submit', handleAuthSubmit);
    document.getElementById('toggle-auth-mode').addEventListener('click', toggleAuthMode);
    document.getElementById('guest-btn').addEventListener('click', handleGuestLogin);
    
    checkAuthStatus();
});

// Auth Logic
function toggleAuthMode(e) {
    e.preventDefault();
    isLoginMode = !isLoginMode;
    document.getElementById('auth-title').innerText = isLoginMode ? 'Welcome to TrackFin' : 'Create an Account';
    document.getElementById('auth-submit-btn').innerText = isLoginMode ? 'Login' : 'Sign Up';
    e.target.innerText = isLoginMode ? 'Sign up' : 'Login';
    e.target.previousSibling.textContent = isLoginMode ? "Don't have an account? " : "Already have an account? ";
}

async function handleAuthSubmit(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const endpoint = isLoginMode ? '/auth/login' : '/auth/register';

    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (isLoginMode) {
                localStorage.setItem('token', data.token);
                document.getElementById('auth-modal').classList.remove('active');
                fetchDashboardData();
            } else {
                alert('Registration successful! Please login.');
                toggleAuthMode(new Event('click')); // Switch back to login
            }
        } else {
            alert(data.message || 'Authentication failed');
        }
    } catch (error) {
        console.error("Auth error:", error);
        alert("Failed to connect to server.");
    }
}

async function handleGuestLogin(e) {
    e.preventDefault();
    try {
        const response = await fetch(`${API_URL}/auth/guest`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('token', data.token);
            document.getElementById('auth-modal').classList.remove('active');
            fetchDashboardData();
        } else {
            alert('Guest login failed');
        }
    } catch (error) {
        console.error("Guest Auth error:", error);
        alert("Failed to connect to server.");
    }
}

function checkAuthStatus() {
    const token = localStorage.getItem('token');
    if (token) {
        document.getElementById('auth-modal').classList.remove('active');
        fetchDashboardData();
    } else {
        document.getElementById('auth-modal').classList.add('active');
    }
}

function logout() {
    localStorage.removeItem('token');
    document.getElementById('auth-modal').classList.add('active');
    document.getElementById('transaction-list').innerHTML = '';
}

// Intercept fetch to add token
async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('token');
    if (!token) return logout();
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };
    
    const response = await fetch(url, { ...options, headers });
    if (response.status === 401) {
        logout();
        throw new Error('Unauthorized');
    }
    return response;
}

// Modal Logic
function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
    if (id === 'add-modal') {
        document.getElementById('transaction-form').reset();
        document.getElementById('date').valueAsDate = new Date();
    }
}

// Data Fetching
async function fetchDashboardData() {
    try {
        const [summaryRes, txRes, healthRes, subsRes, goalsRes] = await Promise.all([
            fetchWithAuth(`${API_URL}/summary`),
            fetchWithAuth(`${API_URL}/transactions`),
            fetchWithAuth(`${API_URL}/analytics/health`),
            fetchWithAuth(`${API_URL}/analytics/subscriptions`),
            fetchWithAuth(`${API_URL}/goals`)
        ]);
        
        const summary = await summaryRes.json();
        const transactions = await txRes.json();
        const health = await healthRes.json();
        const subs = await subsRes.json();
        const goals = await goalsRes.json();
        
        updateSummaryCards(summary, health, subs);
        updateChart(summary.expensesByCategory);
        updateTransactionList(transactions);
        updateGoalsList(goals);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// UI Updates
function updateSummaryCards(summary, health, subs) {
    const formatMoney = (amount) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
    document.getElementById('net-amount').innerText = formatMoney(summary.net);
    document.getElementById('income-amount').innerText = '+' + formatMoney(summary.income);
    document.getElementById('expense-amount').innerText = '-' + formatMoney(summary.expenses);
    
    // Health Score
    document.getElementById('health-score').innerText = health.score || '--';
    document.getElementById('health-status').innerText = health.status || 'Analyzing...';
    
    // Burn Rate
    document.getElementById('burn-amount').innerText = formatMoney(subs.monthly_burn || 0);
    document.getElementById('subs-count').innerText = `${subs.active_subscriptions ? subs.active_subscriptions.length : 0} Subscriptions`;
}

function getCategoryIcon(category) {
    const icons = {
        'Food': '🍔', 'Transport': '🚗', 'Housing': '🏠',
        'Entertainment': '🎬', 'Shopping': '🛍️', 'Salary': '💰', 'Other': '✨'
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
                <div class="tx-icon ${tx.type}">${getCategoryIcon(tx.category)}</div>
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

function updateGoalsList(goals) {
    const list = document.getElementById('goals-list');
    list.innerHTML = '';
    
    if (goals.length === 0) {
        list.innerHTML = '<div style="text-align:center; padding: 20px; color: var(--text-muted)">No active savings goals.</div>';
        return;
    }
    
    goals.forEach(goal => {
        const percentage = Math.min((goal.current_amount / goal.target_amount) * 100, 100).toFixed(1);
        const formatMoney = (amount) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
        
        const item = document.createElement('div');
        item.className = 'goal-item';
        item.style.marginBottom = '15px';
        item.innerHTML = `
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <strong>${goal.name}</strong>
                <span>${formatMoney(goal.current_amount)} / ${formatMoney(goal.target_amount)}</span>
            </div>
            <div style="width: 100%; background-color: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; overflow: hidden;">
                <div style="width: ${percentage}%; background: var(--primary); height: 100%; border-radius: 10px; transition: width 0.5s ease;"></div>
            </div>
            <div style="text-align: right; font-size: 0.8rem; color: var(--text-muted); margin-top: 5px;">${percentage}% Complete</div>
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
        labels.push("No Data"); data.push(1);
    }
    
    expenseChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#d946ef', '#ec4899', '#c026d3', '#10b981', '#f472b6', '#3b82f6', '#9ca3af'
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#6b7280', font: { family: 'Outfit' } } },
                tooltip: { backgroundColor: 'rgba(255, 255, 255, 0.9)', titleColor: '#1f2937', bodyColor: '#1f2937', titleFont: { family: 'Outfit' }, bodyFont: { family: 'Outfit' }, padding: 12, cornerRadius: 8, borderColor: 'rgba(0,0,0,0.1)', borderWidth: 1 }
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
        const response = await fetchWithAuth(`${API_URL}/transactions`, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            closeModal('add-modal');
            fetchDashboardData();
        } else {
            alert("Error saving transaction.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

async function handleAddGoal(e) {
    e.preventDefault();
    const name = document.getElementById('goal-name').value;
    const target_amount = document.getElementById('goal-amount').value;
    
    try {
        const response = await fetchWithAuth(`${API_URL}/goals`, {
            method: 'POST',
            body: JSON.stringify({ name, target_amount })
        });
        
        if (response.ok) {
            closeModal('add-goal-modal');
            document.getElementById('goal-form').reset();
            fetchDashboardData();
        } else {
            alert("Error saving goal.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}
