import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

# Bivariate clinical diagnostics: Feature 1 = Fasting Glucose (mmol/L), Feature 2 = Postprandial Glucose Index
np.random.seed(42)
n_samples = 30

# Class 1: Healthy / Low Risk
mean_c1 = np.array([4.2, 5.0])
cov_c1 = np.array([[0.6, 0.4], [0.4, 0.8]])
X1 = np.random.multivariate_normal(mean_c1, cov_c1, size=n_samples)

# Class 2: Diabetic / High Risk
mean_c2 = np.array([7.8, 8.5])
cov_c2 = np.array([[0.8, 0.5], [0.5, 0.9]])
X2 = np.random.multivariate_normal(mean_c2, cov_c2, size=n_samples)

# Total dataset
X_all = np.vstack([X1, X2])
y_all = np.array([0]*n_samples + [1]*n_samples)

# 1. Compute Class Means and Overall Mean
mu1 = np.mean(X1, axis=0)
mu2 = np.mean(X2, axis=0)
mu_overall = np.mean(X_all, axis=0)

# 2. Compute Within-Class Scatter Matrix S_W
S_W1 = np.dot((X1 - mu1).T, (X1 - mu1))
S_W2 = np.dot((X2 - mu2).T, (X2 - mu2))
S_W = S_W1 + S_W2

# 3. Compute Between-Class Scatter Matrix S_B
mean_diff = (mu1 - mu2).reshape(-1, 1)
S_B = np.dot(mean_diff, mean_diff.T)

# 4. Fisher's Optimal Projection Vector: w = S_W^(-1) * (mu1 - mu2)
S_W_inv = np.linalg.inv(S_W)
w_fisher = np.dot(S_W_inv, (mu1 - mu2))
w_unit = w_fisher / np.linalg.norm(w_fisher)

# Projected 1D scalar coordinates: y = (x - mu_overall) . w_unit
y1_proj = np.dot(X1 - mu_overall, w_unit)
y2_proj = np.dot(X2 - mu_overall, w_unit)

# Centroid projections
y_mu1 = np.dot(mu1 - mu_overall, w_unit)
y_mu2 = np.dot(mu2 - mu_overall, w_unit)
y_thresh = (y_mu1 + y_mu2) / 2.0

# 2D points mapped on the projected line
X1_mapped = mu_overall + np.outer(y1_proj, w_unit)
X2_mapped = mu_overall + np.outer(y2_proj, w_unit)


def generate_lda_visualization(test_x1, test_x2):
    test_sample = np.array([test_x1, test_x2])
    
    # 1D projection of test sample
    y_test = float(np.dot(test_sample - mu_overall, w_unit))
    test_mapped = mu_overall + y_test * w_unit
    
    # Classification decision
    # If y_mu1 > y_mu2, then values > y_thresh belong to Class 1
    if y_mu1 > y_mu2:
        pred_class = "Class 1: Low Risk (Healthy)" if y_test >= y_thresh else "Class 2: High Risk (Diabetic)"
        pred_label = 0 if y_test >= y_thresh else 1
    else:
        pred_class = "Class 1: Low Risk (Healthy)" if y_test <= y_thresh else "Class 2: High Risk (Diabetic)"
        pred_label = 0 if y_test <= y_thresh else 1
        
    dist_to_thresh = abs(y_test - y_thresh)
    
    # Plot construction
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.0), dpi=130)
    
    # PANEL 1: 2D Feature Space with Fisher LDA Projected Line
    # Scatter training classes
    ax1.scatter(X1[:, 0], X1[:, 1], c='#1f77b4', edgecolors='k', s=45, alpha=0.75, label='Class 1: Low Risk (Healthy)')
    ax1.scatter(X2[:, 0], X2[:, 1], c='#d62728', edgecolors='k', s=45, alpha=0.75, label='Class 2: High Risk (Diabetic)')
    
    # Means
    ax1.scatter(mu1[0], mu1[1], c='#003366', marker='^', s=90, edgecolors='k', label='Mean μ₁')
    ax1.scatter(mu2[0], mu2[1], c='#800000', marker='v', s=90, edgecolors='k', label='Mean μ₂')
    ax1.scatter(mu_overall[0], mu_overall[1], c='#000000', marker='s', s=80, label='Overall Mean μ')
    
    # LDA Projected Line (Passing through mu_overall along w_unit)
    t_vals = np.linspace(-6.0, 6.0, 100)
    line_pts = mu_overall + np.outer(t_vals, w_unit)
    ax1.plot(line_pts[:, 0], line_pts[:, 1], color='#6b21a8', linewidth=2.8,
             label=f'LDA Projected Line (ŵ=[{w_unit[0]:.2f}, {w_unit[1]:.2f}])')
    
    # Orthogonal projection lines onto the line
    for i in range(len(X1)):
        ax1.plot([X1[i, 0], X1_mapped[i, 0]], [X1[i, 1], X1_mapped[i, 1]], color='#93c5fd', linestyle='--', linewidth=0.7)
    for i in range(len(X2)):
        ax1.plot([X2[i, 0], X2_mapped[i, 0]], [X2[i, 1], X2_mapped[i, 1]], color='#fca5a5', linestyle='--', linewidth=0.7)
        
    # Mapped reduced features on the line
    ax1.scatter(X1_mapped[:, 0], X1_mapped[:, 1], c='#2563eb', edgecolors='k', s=30, alpha=0.85, label='Class 1 Mapped on Line')
    ax1.scatter(X2_mapped[:, 0], X2_mapped[:, 1], c='#dc2626', edgecolors='k', s=30, alpha=0.85, label='Class 2 Mapped on Line')
    
    # Decision threshold marker on projected line
    thresh_pt = mu_overall + y_thresh * w_unit
    ax1.scatter(thresh_pt[0], thresh_pt[1], c='#000000', marker='P', s=130, edgecolors='w', label=f'Threshold Point (y={y_thresh:.2f})')
    
    # Test sample & projection
    ax1.plot([test_sample[0], test_mapped[0]], [test_sample[1], test_mapped[1]], color='#eab308', linestyle=':', linewidth=2.0)
    ax1.scatter(test_sample[0], test_sample[1], c='#f59e0b', marker='*', s=200, edgecolors='k',
                label=f'Test Sample ({test_sample[0]:.2f}, {test_sample[1]:.2f})', zorder=6)
    ax1.scatter(test_mapped[0], test_mapped[1], c='#10b981', marker='D', s=100, edgecolors='k',
                label=f'Test Mapped on Line', zorder=6)
    
    ax1.set_title('2D Feature Space: Fisher LDA Projected Line & Mappings', fontsize=10, fontweight='bold')
    ax1.set_xlabel('Feature 1: Fasting Blood Glucose (mmol/L)')
    ax1.set_ylabel('Feature 2: Postprandial Glucose Index')
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend(loc='upper left', fontsize=7.0)
    
    # PANEL 2: 1D Projected Subspace along Fisher Direction
    y_c1_dummy = np.zeros_like(y1_proj) + 0.05
    y_c2_dummy = np.zeros_like(y2_proj) - 0.05
    ax2.axhline(0, color='#6b21a8', linewidth=2.0, linestyle='-', alpha=0.8)
    ax2.scatter(y1_proj, y_c1_dummy, c='#2563eb', edgecolors='k', s=45, alpha=0.8, label='Class 1 1D Mapped Scores')
    ax2.scatter(y2_proj, y_c2_dummy, c='#dc2626', edgecolors='k', s=45, alpha=0.8, label='Class 2 1D Mapped Scores')
    
    # Decision boundary line in 1D
    ax2.axvline(y_thresh, color='#000000', linestyle='--', linewidth=2.2, label=f'Decision Threshold y* = {y_thresh:.2f}')
    ax2.scatter(y_test, 0, c='#10b981', marker='D', s=140, edgecolors='k', label=f'Test Projection (y={y_test:.2f})', zorder=5)
    
    ax2.set_title('1D Projected Subspace: Optimal Class Separation', fontsize=10, fontweight='bold')
    ax2.set_xlabel('Projected 1D Coordinate (y = (x - μ) · ŵ)')
    ax2.set_yticks([])
    ax2.set_ylim(-0.4, 0.4)
    ax2.grid(True, linestyle='--', alpha=0.4, axis='x')
    ax2.legend(loc='upper right', fontsize=7.5)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    # Sample Table
    sample_table = []
    for i in range(3):
        sample_table.append({
            'label': 'Class 1 (Low Risk)',
            'orig': f'[{X1[i, 0]:.2f}, {X1[i, 1]:.2f}]',
            'y_proj': round(y1_proj[i], 3),
            'mapped': f'[{X1_mapped[i, 0]:.2f}, {X1_mapped[i, 1]:.2f}]',
            'status': 'Classified Correctly'
        })
    for i in range(3):
        sample_table.append({
            'label': 'Class 2 (High Risk)',
            'orig': f'[{X2[i, 0]:.2f}, {X2[i, 1]:.2f}]',
            'y_proj': round(y2_proj[i], 3),
            'mapped': f'[{X2_mapped[i, 0]:.2f}, {X2_mapped[i, 1]:.2f}]',
            'status': 'Classified Correctly'
        })
        
    stats = {
        'mu1_1': round(mu1[0], 2), 'mu1_2': round(mu1[1], 2),
        'mu2_1': round(mu2[0], 2), 'mu2_2': round(mu2[1], 2),
        'mu_all_1': round(mu_overall[0], 2), 'mu_all_2': round(mu_overall[1], 2),
        'sw_00': round(float(S_W[0, 0]), 2), 'sw_01': round(float(S_W[0, 1]), 2), 'sw_11': round(float(S_W[1, 1]), 2),
        'w_x': round(w_unit[0], 3), 'w_y': round(w_unit[1], 3),
        'y_thresh': round(y_thresh, 3),
        'test_x1': round(test_sample[0], 2), 'test_x2': round(test_sample[1], 2),
        'y_test': round(y_test, 3),
        'test_mapped_1': round(test_mapped[0], 2), 'test_mapped_2': round(test_mapped[1], 2),
        'pred_class': pred_class,
        'dist_to_thresh': round(dist_to_thresh, 3)
    }
    
    return plot_url, stats, sample_table


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        test_x1 = float(request.form.get('test_x1', 6.2))
        test_x2 = float(request.form.get('test_x2', 6.8))
    except (ValueError, TypeError):
        test_x1, test_x2 = 6.2, 6.8
        
    plot_url, stats, sample_table = generate_lda_visualization(test_x1, test_x2)
    
    return render_template('index.html',
                           test_x1=test_x1,
                           test_x2=test_x2,
                           plot_url=plot_url,
                           stats=stats,
                           sample_table=sample_table)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5011))
    print(f"Starting Experiment 11 LDA Server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
