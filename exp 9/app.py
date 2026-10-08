import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from sklearn.datasets import make_moons
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss

app = Flask(__name__)

# Generate synthetic non-linear dataset (Quality Assurance / Flaw Detection)
np.random.seed(42)
X_raw, y = make_moons(n_samples=180, noise=0.25, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.35, random_state=42)

poly = PolynomialFeatures(degree=6, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Baseline model: No regularization (C -> very large)
model_unreg = LogisticRegression(penalty='none' if hasattr(LogisticRegression, 'penalty') and False else 'l2',
                                 C=1e5, max_iter=2000, random_state=42)
# In modern sklearn, penalty=None is supported or C=1e6 simulates no regularization
try:
    model_unreg = LogisticRegression(penalty=None, max_iter=2000, random_state=42)
    model_unreg.fit(X_train_poly, y_train)
except Exception:
    model_unreg = LogisticRegression(penalty='l2', C=1e6, max_iter=2000, random_state=42)
    model_unreg.fit(X_train_poly, y_train)

train_acc_unreg = accuracy_score(y_train, model_unreg.predict(X_train_poly))
test_acc_unreg = accuracy_score(y_test, model_unreg.predict(X_test_poly))
train_loss_unreg = log_loss(y_train, model_unreg.predict_proba(X_train_poly))
test_loss_unreg = log_loss(y_test, model_unreg.predict_proba(X_test_poly))


def generate_plots(reg_type, lambda_val):
    # Regularized model: C = 1 / lambda
    C_val = 1.0 / max(lambda_val, 1e-4)
    penalty_type = 'l2' if reg_type == 'L2' else 'l1'
    solver = 'liblinear' if penalty_type == 'l1' else 'lbfgs'
    
    model_reg = LogisticRegression(penalty=penalty_type, C=C_val, solver=solver, max_iter=2000, random_state=42)
    model_reg.fit(X_train_poly, y_train)
    
    train_acc_reg = accuracy_score(y_train, model_reg.predict(X_train_poly))
    test_acc_reg = accuracy_score(y_test, model_reg.predict(X_test_poly))
    train_loss_reg = log_loss(y_train, model_reg.predict_proba(X_train_poly))
    test_loss_reg = log_loss(y_test, model_reg.predict_proba(X_test_poly))
    
    # 1. Decision Boundary Comparison Plot
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), dpi=130)
    
    # Grid for decision boundary
    x_min, x_max = X_raw[:, 0].min() - 0.5, X_raw[:, 0].max() + 0.5
    y_min, y_max = X_raw[:, 1].min() - 0.5, X_raw[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 250), np.linspace(y_min, y_max, 250))
    grid_poly = poly.transform(np.c_[xx.ravel(), yy.ravel()])
    
    # Panel 1: Unregularized
    Z_unreg = model_unreg.predict_proba(grid_poly)[:, 1].reshape(xx.shape)
    axes[0].contourf(xx, yy, Z_unreg, levels=20, cmap='RdBu', alpha=0.25)
    axes[0].contour(xx, yy, Z_unreg, levels=[0.5], colors='#b30000', linewidths=2.2)
    axes[0].scatter(X_train[y_train == 0, 0], X_train[y_train == 0, 1], c='#0055ff', edgecolors='k', s=35, label='Class 0 (Pass)')
    axes[0].scatter(X_train[y_train == 1, 0], X_train[y_train == 1, 1], c='#ff3300', edgecolors='k', s=35, label='Class 1 (Fail)')
    axes[0].set_title(f'1) Before Regularization (λ = 0)\nTrain Acc: {train_acc_unreg*100:.1f}% | Test Acc: {test_acc_unreg*100:.1f}%\n(Severe Overfitting: Complex & Jagged Boundary)', fontsize=9, fontweight='bold', color='#900')
    axes[0].set_xlabel('Feature 1 (Test 1 Score)')
    axes[0].set_ylabel('Feature 2 (Test 2 Score)')
    axes[0].grid(True, linestyle='--', alpha=0.4)
    axes[0].legend(loc='lower left', fontsize=8)
    
    # Panel 2: Regularized
    Z_reg = model_reg.predict_proba(grid_poly)[:, 1].reshape(xx.shape)
    axes[1].contourf(xx, yy, Z_reg, levels=20, cmap='RdBu', alpha=0.25)
    axes[1].contour(xx, yy, Z_reg, levels=[0.5], colors='#006600', linewidths=2.2)
    axes[1].scatter(X_train[y_train == 0, 0], X_train[y_train == 0, 1], c='#0055ff', edgecolors='k', s=35, label='Class 0 (Pass)')
    axes[1].scatter(X_train[y_train == 1, 0], X_train[y_train == 1, 1], c='#ff3300', edgecolors='k', s=35, label='Class 1 (Fail)')
    axes[1].set_title(f'2) After Regularization ({reg_type}, λ = {lambda_val})\nTrain Acc: {train_acc_reg*100:.1f}% | Test Acc: {test_acc_reg*100:.1f}%\n(Smooth Generalization: Robust Boundary)', fontsize=9, fontweight='bold', color='#006600')
    axes[1].set_xlabel('Feature 1 (Test 1 Score)')
    axes[1].set_ylabel('Feature 2 (Test 2 Score)')
    axes[1].grid(True, linestyle='--', alpha=0.4)
    axes[1].legend(loc='lower left', fontsize=8)
    
    plt.tight_layout()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', bbox_inches='tight')
    buf1.seek(0)
    boundary_plot_url = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close()
    
    # 2. Performance Comparison Plot (Accuracy & Loss)
    fig2, axes2 = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
    
    # Subplot A: Accuracy Comparison
    labels = ['Before (λ=0)', f'After ({reg_type}, λ={lambda_val})']
    train_accs = [train_acc_unreg * 100, train_acc_reg * 100]
    test_accs = [test_acc_unreg * 100, test_acc_reg * 100]
    x = np.arange(len(labels))
    width = 0.32
    
    rects1 = axes2[0].bar(x - width/2, train_accs, width, label='Training Acc (%)', color='#2b5c8f')
    rects2 = axes2[0].bar(x + width/2, test_accs, width, label='Test Acc (%)', color='#2e8b57')
    axes2[0].set_ylabel('Accuracy (%)')
    axes2[0].set_title('Performance Comparison: Accuracy', fontsize=10, fontweight='bold')
    axes2[0].set_xticks(x)
    axes2[0].set_xticklabels(labels)
    axes2[0].set_ylim(50, 105)
    axes2[0].grid(True, linestyle='--', alpha=0.4, axis='y')
    axes2[0].legend(loc='upper right', fontsize=8)
    for rect in rects1 + rects2:
        h = rect.get_height()
        axes2[0].annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                          xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
        
    # Subplot B: Loss Comparison
    train_losses = [train_loss_unreg, train_loss_reg]
    test_losses = [test_loss_unreg, test_loss_reg]
    rects3 = axes2[1].bar(x - width/2, train_losses, width, label='Training Loss (CE)', color='#cc5500')
    rects4 = axes2[1].bar(x + width/2, test_losses, width, label='Test Loss (CE)', color='#b22222')
    axes2[1].set_ylabel('Cross-Entropy Loss')
    axes2[1].set_title('Performance Comparison: Generalization Loss', fontsize=10, fontweight='bold')
    axes2[1].set_xticks(x)
    axes2[1].set_xticklabels(labels)
    axes2[1].grid(True, linestyle='--', alpha=0.4, axis='y')
    axes2[1].legend(loc='upper left', fontsize=8)
    for rect in rects3 + rects4:
        h = rect.get_height()
        axes2[1].annotate(f'{h:.3f}', xy=(rect.get_x() + rect.get_width()/2, h),
                          xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', bbox_inches='tight')
    buf2.seek(0)
    perf_plot_url = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close()
    
    # Weight norm comparisons
    norm_w_unreg = np.linalg.norm(model_unreg.coef_)
    norm_w_reg = np.linalg.norm(model_reg.coef_)
    
    metrics = {
        'train_acc_unreg': round(train_acc_unreg * 100, 2),
        'test_acc_unreg': round(test_acc_unreg * 100, 2),
        'train_loss_unreg': round(train_loss_unreg, 4),
        'test_loss_unreg': round(test_loss_unreg, 4),
        'norm_unreg': round(norm_w_unreg, 3),
        'train_acc_reg': round(train_acc_reg * 100, 2),
        'test_acc_reg': round(test_acc_reg * 100, 2),
        'train_loss_reg': round(train_loss_reg, 4),
        'test_loss_reg': round(test_loss_reg, 4),
        'norm_reg': round(norm_w_reg, 3),
        'test_acc_gain': round((test_acc_reg - test_acc_unreg) * 100, 2)
    }
    
    return boundary_plot_url, perf_plot_url, metrics


@app.route('/', methods=['GET', 'POST'])
def index():
    reg_type = request.form.get('reg_type', 'L2')
    try:
        lambda_val = float(request.form.get('lambda_val', 1.0))
    except (ValueError, TypeError):
        lambda_val = 1.0
        
    boundary_plot, perf_plot, metrics = generate_plots(reg_type, lambda_val)
    
    return render_template('index.html',
                           reg_type=reg_type,
                           lambda_val=lambda_val,
                           boundary_plot=boundary_plot,
                           perf_plot=perf_plot,
                           metrics=metrics)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)
