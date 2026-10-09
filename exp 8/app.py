import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from flask import Flask, render_template, request

app = Flask(__name__)

# =============================================================
# PART 1: BINARY LOGISTIC REGRESSION (FROM SCRATCH)
# Application: Medical Diabetes / Disease Risk Prediction
# X: [Blood Sugar Level (mg/dL / 100), BMI / 10]
# y: 1 (High Risk / Positive), 0 (Low Risk / Negative)
# =============================================================
np.random.seed(42)
m_binary = 100
# Generate synthetic clinical data
X_neg = np.random.normal(loc=[1.0, 2.3], scale=[0.25, 0.35], size=(50, 2))
X_pos = np.random.normal(loc=[1.6, 3.2], scale=[0.25, 0.35], size=(50, 2))
X_binary = np.vstack([X_neg, X_pos])
y_binary = np.array([0]*50 + [1]*50, dtype=np.float64)

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -250, 250)))

def train_binary_logistic_regression(X, y, alpha=0.1, epochs=800):
    m, d = X.shape
    w = np.zeros(d, dtype=np.float64)
    b = 0.0
    
    cost_history = []
    
    for epoch in range(epochs):
        # Forward pass
        z = np.dot(X, w) + b
        y_hat = sigmoid(z)
        
        # Binary Cross-Entropy Cost: J = -(1/m) * sum(y*log(y_hat) + (1-y)*log(1-y_hat))
        eps = 1e-15
        cost = - (1.0 / m) * np.sum(y * np.log(y_hat + eps) + (1.0 - y) * np.log(1.0 - y_hat + eps))
        cost_history.append(float(cost))
        
        # Gradients
        error = y_hat - y
        dw = (1.0 / m) * np.dot(X.T, error)
        db = (1.0 / m) * np.sum(error)
        
        # Parameter updates
        w = w - alpha * dw
        b = b - alpha * db
        
    y_preds = (sigmoid(np.dot(X, w) + b) >= 0.5).astype(int)
    acc = float(np.mean(y_preds == y)) * 100.0
    return w, b, cost_history, acc

# =============================================================
# PART 2: MULTICLASS LOGISTIC REGRESSION (SOFTMAX FROM SCRATCH)
# Application: Iris 3-Class Floral Classification
# X: [Petal Length, Sepal Length] (d=2 for 2D visualization)
# y: 3 classes (0: Setosa, 1: Versicolor, 2: Virginica)
# =============================================================
iris = load_iris()
X_multi = iris.data[:, [2, 0]]  # Petal Length, Sepal Length
y_multi_int = iris.target
m_multi, d_multi = X_multi.shape
K_classes = 3
iris_class_names = ['Setosa', 'Versicolor', 'Virginica']

# One-hot encode targets
Y_one_hot = np.zeros((m_multi, K_classes), dtype=np.float64)
for i in range(m_multi):
    Y_one_hot[i, y_multi_int[i]] = 1.0

def softmax(Z):
    # Stabilized Softmax
    exp_Z = np.exp(Z - np.max(Z, axis=1, keepdims=True))
    return exp_Z / np.sum(exp_Z, axis=1, keepdims=True)

def train_multiclass_logistic_regression(X, Y, alpha=0.08, epochs=1200):
    m, d = X.shape
    K = Y.shape[1]
    
    W = np.zeros((d, K), dtype=np.float64)
    b = np.zeros(K, dtype=np.float64)
    
    cost_history = []
    
    for epoch in range(epochs):
        # Linear logits: Z = XW + b
        Z = np.dot(X, W) + b
        P_hat = softmax(Z)
        
        # Categorical Cross-Entropy: J = -(1/m) * sum(Y * log(P_hat))
        eps = 1e-15
        cost = - (1.0 / m) * np.sum(Y * np.log(P_hat + eps))
        cost_history.append(float(cost))
        
        # Gradients
        error = P_hat - Y
        dW = (1.0 / m) * np.dot(X.T, error)
        db = (1.0 / m) * np.sum(error, axis=0)
        
        # Parameter updates
        W = W - alpha * dW
        b = b - alpha * db
        
    P_final = softmax(np.dot(X, W) + b)
    preds = np.argmax(P_final, axis=1)
    acc = float(np.mean(preds == np.argmax(Y, axis=1))) * 100.0
    return W, b, cost_history, acc

# -------------------------------------------------------------
# PLOT GENERATION: DUAL GRADIENT DESCENT CURVES & DECISION BOUNDARIES
# -------------------------------------------------------------
def generate_plots(costs_bin, costs_multi, w_bin, b_bin, W_multi, b_multi, bin_test_x, multi_test_x):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    
    # Panel 1: Binary Gradient Descent Curve
    axes[0, 0].plot(costs_bin, color='#1565c0', linewidth=2.2, label='Binary Cross-Entropy Loss')
    axes[0, 0].set_title('Binary Logistic Regression: Gradient Descent Curve', fontsize=11, fontweight='bold')
    axes[0, 0].set_xlabel('Epochs', fontsize=10, fontweight='bold')
    axes[0, 0].set_ylabel('Loss J(w, b)', fontsize=10, fontweight='bold')
    axes[0, 0].grid(True, linestyle='--', alpha=0.5)
    axes[0, 0].legend(loc='upper right', fontsize=8)
    axes[0, 0].annotate(f"Initial: {costs_bin[0]:.4f}", (0, costs_bin[0]), textcoords="offset points", xytext=(15, -10), fontsize=8)
    axes[0, 0].annotate(f"Final: {costs_bin[-1]:.4f}", (len(costs_bin)-1, costs_bin[-1]), textcoords="offset points", xytext=(-65, 15), fontsize=8, fontweight='bold')

    # Panel 2: Multiclass Gradient Descent Curve
    axes[0, 1].plot(costs_multi, color='#2e7d32', linewidth=2.2, label='Categorical Cross-Entropy Loss')
    axes[0, 1].set_title('Multiclass (Softmax) Regression: Gradient Descent Curve', fontsize=11, fontweight='bold')
    axes[0, 1].set_xlabel('Epochs', fontsize=10, fontweight='bold')
    axes[0, 1].set_ylabel('Loss J(W, b)', fontsize=10, fontweight='bold')
    axes[0, 1].grid(True, linestyle='--', alpha=0.5)
    axes[0, 1].legend(loc='upper right', fontsize=8)
    axes[0, 1].annotate(f"Initial: {costs_multi[0]:.4f}", (0, costs_multi[0]), textcoords="offset points", xytext=(15, -10), fontsize=8)
    axes[0, 1].annotate(f"Final: {costs_multi[-1]:.4f}", (len(costs_multi)-1, costs_multi[-1]), textcoords="offset points", xytext=(-65, 15), fontsize=8, fontweight='bold')

    # Panel 3: Binary Decision Boundary
    axes[1, 0].scatter(X_binary[y_binary==0, 0], X_binary[y_binary==0, 1], color='#1976d2', label='Class 0 (Negative)', s=35, edgecolors='k')
    axes[1, 0].scatter(X_binary[y_binary==1, 0], X_binary[y_binary==1, 1], color='#d32f2f', label='Class 1 (Positive)', s=35, edgecolors='k')
    # Decision boundary line: w1*x1 + w2*x2 + b = 0 => x2 = -(w1*x1 + b) / w2
    x1_line = np.linspace(min(X_binary[:, 0]), max(X_binary[:, 0]), 100)
    x2_line = - (w_bin[0] * x1_line + b_bin) / w_bin[1]
    axes[1, 0].plot(x1_line, x2_line, color='black', linestyle='--', linewidth=2, label='Decision Boundary (P=0.5)')
    axes[1, 0].scatter([bin_test_x[0]], [bin_test_x[1]], color='#ffeb3b', edgecolors='#d81b60', marker='*', s=250, label='Test Sample', zorder=10)
    axes[1, 0].set_title('Binary Logistic Regression Decision Boundary', fontsize=11, fontweight='bold')
    axes[1, 0].set_xlabel('Normalized Blood Glucose (Feature 1)', fontsize=10, fontweight='bold')
    axes[1, 0].set_ylabel('Normalized BMI (Feature 2)', fontsize=10, fontweight='bold')
    axes[1, 0].legend(loc='lower right', fontsize=8)
    axes[1, 0].grid(True, linestyle='--', alpha=0.5)

    # Panel 4: Multiclass Classification Scatter
    colors_k = ['#1e88e5', '#43a047', '#e53935']
    for k in range(3):
        mask = (y_multi_int == k)
        axes[1, 1].scatter(X_multi[mask, 0], X_multi[mask, 1], color=colors_k[k], label=iris_class_names[k], s=35, edgecolors='k')
    axes[1, 1].scatter([multi_test_x[0]], [multi_test_x[1]], color='#ffeb3b', edgecolors='#d81b60', marker='*', s=250, label='Test Sample', zorder=10)
    axes[1, 1].set_title('Multiclass (Softmax) Scatter & Classified Test Point', fontsize=11, fontweight='bold')
    axes[1, 1].set_xlabel('Petal Length (cm) [Feature 1]', fontsize=10, fontweight='bold')
    axes[1, 1].set_ylabel('Sepal Length (cm) [Feature 2]', fontsize=10, fontweight='bold')
    axes[1, 1].legend(loc='lower right', fontsize=8)
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    # Train both models from scratch
    w_bin, b_bin, costs_bin, acc_bin = train_binary_logistic_regression(X_binary, y_binary, alpha=0.1, epochs=800)
    W_multi, b_multi, costs_multi, acc_multi = train_multiclass_logistic_regression(X_multi, Y_one_hot, alpha=0.08, epochs=1200)
    
    # Default test samples
    bin_x1, bin_x2 = 1.45, 2.85
    multi_x1, multi_x2 = 4.5, 6.0
    
    if request.method == 'POST':
        try:
            bin_x1 = float(request.form.get('bin_x1', 1.45))
            bin_x2 = float(request.form.get('bin_x2', 2.85))
            multi_x1 = float(request.form.get('multi_x1', 4.5))
            multi_x2 = float(request.form.get('multi_x2', 6.0))
        except ValueError:
            pass
            
    bin_test_vec = np.array([bin_x1, bin_x2])
    multi_test_vec = np.array([multi_x1, multi_x2])
    
    # Binary Inference
    bin_prob = float(sigmoid(np.dot(bin_test_vec, w_bin) + b_bin))
    bin_pred_class = 1 if bin_prob >= 0.5 else 0
    bin_pred_label = "Class 1: High Clinical Risk" if bin_pred_class == 1 else "Class 0: Low Risk / Normal"
    
    # Multiclass Inference
    multi_logits = np.dot(multi_test_vec.reshape(1, -1), W_multi) + b_multi
    multi_probs = softmax(multi_logits)[0]
    multi_pred_class = int(np.argmax(multi_probs))
    multi_pred_label = iris_class_names[multi_pred_class]
    
    # Generate visualization plots
    plot_b64 = generate_plots(costs_bin, costs_multi, w_bin, b_bin, W_multi, b_multi, bin_test_vec, multi_test_vec)
    
    return render_template(
        'index.html',
        w_bin=[round(v, 4) for v in w_bin],
        b_bin=round(b_bin, 4),
        acc_bin=round(acc_bin, 2),
        initial_cost_bin=round(costs_bin[0], 4),
        final_cost_bin=round(costs_bin[-1], 4),
        bin_x1=bin_x1, bin_x2=bin_x2,
        bin_prob=round(bin_prob, 4),
        bin_pred_label=bin_pred_label,
        W_multi=[[round(v, 4) for v in row] for row in W_multi],
        b_multi=[round(v, 4) for v in b_multi],
        acc_multi=round(acc_multi, 2),
        initial_cost_multi=round(costs_multi[0], 4),
        final_cost_multi=round(costs_multi[-1], 4),
        multi_x1=multi_x1, multi_x2=multi_x2,
        multi_probs=[round(p, 4) for p in multi_probs],
        multi_pred_label=multi_pred_label,
        iris_class_names=iris_class_names,
        plot_b64=plot_b64
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5008))
    print(f"Starting Experiment 8 Logistic Regression Server on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)
