import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------------------------------------------
# APPLICATION DATASET: Real Estate House Price Prediction
# X: House Living Area (in 1000 square feet)
# y: Selling Price (in $10,000s)
# -------------------------------------------------------------
X_data = np.array([1.0, 1.2, 1.5, 1.8, 2.0, 2.3, 2.5, 2.8, 3.0, 3.2, 3.5, 3.8, 4.0, 4.2, 4.5], dtype=np.float64)
# Ground truth with noise: Price ~ 2.5 * Area + 3.0 + noise
y_data = np.array([5.6, 6.1, 6.7, 7.4, 8.1, 8.9, 9.3, 10.1, 10.5, 11.2, 11.9, 12.6, 13.0, 13.5, 14.3], dtype=np.float64)
m = len(X_data)

# -------------------------------------------------------------
# PURE NUMPY LINEAR REGRESSION VIA GRADIENT DESCENT (NO INBUILT)
# -------------------------------------------------------------
def compute_cost(X, y, w, b):
    # J(w, b) = (1 / 2m) * sum( (w*x + b - y)^2 )
    y_pred = w * X + b
    cost = (1.0 / (2.0 * m)) * np.sum((y_pred - y) ** 2)
    return cost

def compute_gradients(X, y, w, b):
    # dj/dw = (1/m) * sum( (w*x + b - y) * x )
    # dj/db = (1/m) * sum( w*x + b - y )
    y_pred = w * X + b
    error = y_pred - y
    dj_dw = (1.0 / m) * np.sum(error * X)
    dj_db = (1.0 / m) * np.sum(error)
    return dj_dw, dj_db

def train_linear_regression(X, y, alpha=0.03, iterations=1000, init_w=0.0, init_b=0.0):
    w = float(init_w)
    b = float(init_b)
    
    cost_history = []
    iteration_history = []
    
    initial_cost = compute_cost(X, y, w, b)
    
    for i in range(iterations):
        dj_dw, dj_db = compute_gradients(X, y, w, b)
        
        # Parameter update rule
        w = w - alpha * dj_dw
        b = b - alpha * dj_db
        
        # Log cost
        if i % (max(1, iterations // 100)) == 0 or i == iterations - 1:
            cost = compute_cost(X, y, w, b)
            cost_history.append(float(cost))
            iteration_history.append(i + 1)
            
    final_cost = compute_cost(X, y, w, b)
    return w, b, initial_cost, final_cost, iteration_history, cost_history

def generate_plots(X, y, w, b, iters, costs, test_x, test_y):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # Plot 1: Gradient Descent Convergence Curve (Cost vs Iterations)
    axes[0].plot(iters, costs, color='#b71c1c', linewidth=2.2, label='MSE Cost J(w,b)')
    axes[0].set_title('Gradient Descent Convergence Curve', fontsize=11, fontweight='bold')
    axes[0].set_xlabel('Iterations / Epochs', fontsize=10, fontweight='bold')
    axes[0].set_ylabel('Cost J(w, b) [Mean Squared Error]', fontsize=10, fontweight='bold')
    axes[0].grid(True, linestyle='--', alpha=0.5)
    axes[0].legend(loc='upper right', fontsize=9)
    # Annotate initial and final cost
    axes[0].scatter([iters[0], iters[-1]], [costs[0], costs[-1]], color='#b71c1c', s=60, zorder=5)
    axes[0].annotate(f"Initial: {costs[0]:.2f}", (iters[0], costs[0]), textcoords="offset points", xytext=(10, 5), fontsize=8)
    axes[0].annotate(f"Converged: {costs[-1]:.4f}", (iters[-1], costs[-1]), textcoords="offset points", xytext=(-60, 15), fontsize=8, fontweight='bold')

    # Plot 2: Fitted Linear Regression Line vs Data Points
    axes[1].scatter(X, y, color='#1565c0', label='Observed Data Points (Houses)', s=50, edgecolors='black')
    x_line = np.linspace(min(X) - 0.2, max(X) + 0.5, 100)
    y_line = w * x_line + b
    axes[1].plot(x_line, y_line, color='#2e7d32', linewidth=2.5, label=f'Model Fit: y = {w:.2f}x + {b:.2f}')
    
    # Plot test prediction
    axes[1].scatter([test_x], [test_y], color='#ffeb3b', edgecolors='#d81b60', marker='*', s=250, linewidth=2,
                    label=f'Predicted Sample ({test_x}k sq ft &rarr; ${test_y*10:.1f}k)', zorder=10)
    axes[1].set_title('Fitted Linear Regression Model on Housing Data', fontsize=11, fontweight='bold')
    axes[1].set_xlabel('House Area (1,000 sq ft)', fontsize=10, fontweight='bold')
    axes[1].set_ylabel('Price ($10,000s)', fontsize=10, fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5)
    axes[1].legend(loc='lower right', fontsize=8)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    alpha = 0.03
    iterations = 1000
    test_x = 2.6  # 2,600 sq ft
    
    if request.method == 'POST':
        try:
            alpha = float(request.form.get('alpha', 0.03))
            iterations = int(request.form.get('iterations', 1000))
            test_x = float(request.form.get('test_x', 2.6))
        except ValueError:
            alpha, iterations, test_x = 0.03, 1000, 2.6
            
    # Train from scratch using Gradient Descent
    w, b, initial_cost, final_cost, iters, costs = train_linear_regression(
        X_data, y_data, alpha=alpha, iterations=iterations, init_w=0.0, init_b=0.0
    )
    
    # Make prediction
    test_y = w * test_x + b
    predicted_price_dollars = test_y * 10000.0
    
    # Generate Plots
    plot_b64 = generate_plots(X_data, y_data, w, b, iters, costs, test_x, test_y)
    
    # Dataset rows for table
    data_rows = [{'id': i+1, 'x': X_data[i], 'y': y_data[i], 'pred': round(w * X_data[i] + b, 2)} for i in range(m)]
    
    return render_template(
        'index.html',
        alpha=alpha,
        iterations=iterations,
        test_x=test_x,
        w=round(w, 4),
        b=round(b, 4),
        initial_cost=round(initial_cost, 4),
        final_cost=round(final_cost, 4),
        test_y=round(test_y, 4),
        predicted_price_dollars=round(predicted_price_dollars, 2),
        data_rows=data_rows,
        plot_b64=plot_b64
    )

if __name__ == '__main__':
    print("Starting Experiment 7 Linear Regression Server on http://127.0.0.1:5009")
    app.run(host='127.0.0.1', port=5009, debug=True)
