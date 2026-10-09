import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

# Bivariate industrial sensor inspection dataset: Vibration Amplitude (mm/s) vs Temperature Rise (°C)
np.random.seed(101)
n_samples = 45
# Generate correlated Gaussian data with high primary variance
mean_true = np.array([4.5, 3.2])
cov_true = np.array([[2.2, 1.6], [1.6, 1.5]])
X = np.random.multivariate_normal(mean_true, cov_true, size=n_samples)

# Perform PCA from mathematical fundamentals
mu = np.mean(X, axis=0)
X_centered = X - mu
cov_matrix = np.cov(X_centered, rowvar=False)

# Eigen-decomposition
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
# Sort in descending order
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

v1 = eigenvectors[:, 0]  # 1st Principal Component direction vector
v2 = eigenvectors[:, 1]  # 2nd Principal Component direction vector

total_var = np.sum(eigenvalues)
explained_var_ratio_1 = eigenvalues[0] / total_var
explained_var_ratio_2 = eigenvalues[1] / total_var

# Project dataset onto 1st Principal Component line
# Reduced 1D feature coordinate: z = (x - mu) . v1
z_train = np.dot(X_centered, v1)
# Projected points in original 2D space: x_proj = mu + z * v1
X_projected = mu + np.outer(z_train, v1)


def generate_pca_visualization(test_x1, test_x2):
    test_sample = np.array([test_x1, test_x2])
    test_centered = test_sample - mu
    
    # 1D reduced coordinate
    z_test = float(np.dot(test_centered, v1))
    
    # 2D reconstructed point on projected line
    test_projected = mu + z_test * v1
    
    # Reconstruction residual error
    rec_error = float(np.linalg.norm(test_sample - test_projected))
    
    # Construct dual-panel Matplotlib plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.0), dpi=130)
    
    # PANEL 1: 2D Data Space with Projected Line and Mapped Reduced Features
    # Scatter of original 2D data points
    ax1.scatter(X[:, 0], X[:, 1], c='#1f77b4', edgecolors='k', s=45, alpha=0.75, label='Original 2D Training Points', zorder=3)
    
    # Centroid
    ax1.scatter(mu[0], mu[1], c='#000000', marker='s', s=80, label=f'Centroid μ = [{mu[0]:.2f}, {mu[1]:.2f}]', zorder=5)
    
    # 1st Principal Component Line (passing through mu along v1)
    t_vals = np.linspace(-4.5, 4.5, 100)
    line_pts = mu + np.outer(t_vals, v1)
    ax1.plot(line_pts[:, 0], line_pts[:, 1], color='#006600', linewidth=2.8,
             label=f'PC1 Projected Line (Direction v₁=[{v1[0]:.2f}, {v1[1]:.2f}])', zorder=2)
    
    # Orthogonal projection lines & mapped 1D points on projected line
    for i in range(len(X)):
        ax1.plot([X[i, 0], X_projected[i, 0]], [X[i, 1], X_projected[i, 1]],
                 color='#aaaaaa', linestyle='--', linewidth=0.8, zorder=1)
    ax1.scatter(X_projected[:, 0], X_projected[:, 1], c='#ff7f0e', edgecolors='k', s=30, alpha=0.85,
                label='Reduced Features Mapped on Projected Line', zorder=4)
    
    # Highlight Test Sample & its projection
    ax1.plot([test_sample[0], test_projected[0]], [test_sample[1], test_projected[1]],
             color='#d62728', linestyle=':', linewidth=2.0, zorder=4)
    ax1.scatter(test_sample[0], test_sample[1], c='#d62728', marker='*', s=180, edgecolors='k',
                label=f'Test Sample ({test_sample[0]:.2f}, {test_sample[1]:.2f})', zorder=6)
    ax1.scatter(test_projected[0], test_projected[1], c='#2ca02c', marker='X', s=140, edgecolors='k',
                label=f'Test Mapped on Line (z={z_test:.2f})', zorder=6)
    
    ax1.set_title('2D Feature Space: Data & 1st PC Projected Line', fontsize=10, fontweight='bold')
    ax1.set_xlabel('Feature 1: Vibration Amplitude (mm/s)')
    ax1.set_ylabel('Feature 2: Temperature Rise (°C)')
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend(loc='lower right', fontsize=7.5)
    
    # PANEL 2: 1D Reduced Subspace (Mapped Coordinates along PC1 Axis)
    y_jitter = np.zeros_like(z_train)
    ax2.axhline(0, color='#006600', linewidth=2.2, linestyle='-', alpha=0.8)
    ax2.scatter(z_train, y_jitter, c='#ff7f0e', edgecolors='k', s=55, alpha=0.8,
                label='1D Reduced Training Samples (z)', zorder=3)
    ax2.scatter(z_test, 0, c='#2ca02c', marker='X', s=160, edgecolors='k',
                label=f'1D Test Projection: z = {z_test:.2f}', zorder=5)
    
    ax2.set_title(f'1D Reduced Feature Subspace along PC1\n(Variance Preserved: {explained_var_ratio_1*100:.1f}%)',
                  fontsize=10, fontweight='bold')
    ax2.set_xlabel('New Reduced 1D Feature Coordinate (z = (x - μ) · v₁)')
    ax2.set_yticks([])
    ax2.set_ylim(-0.5, 0.5)
    ax2.grid(True, linestyle='--', alpha=0.4, axis='x')
    ax2.legend(loc='upper right', fontsize=8)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    # Summary of first 5 training sample projections
    sample_table = []
    for i in range(5):
        sample_table.append({
            'idx': i + 1,
            'x1': round(X[i, 0], 3),
            'x2': round(X[i, 1], 3),
            'z': round(z_train[i], 3),
            'proj_x1': round(X_projected[i, 0], 3),
            'proj_x2': round(X_projected[i, 1], 3),
            'error': round(float(np.linalg.norm(X[i] - X_projected[i])), 3)
        })
        
    stats = {
        'mu_1': round(mu[0], 3),
        'mu_2': round(mu[1], 3),
        'cov_00': round(cov_matrix[0, 0], 3),
        'cov_01': round(cov_matrix[0, 1], 3),
        'cov_11': round(cov_matrix[1, 1], 3),
        'eig_1': round(eigenvalues[0], 3),
        'eig_2': round(eigenvalues[1], 3),
        'var_ratio_1': round(explained_var_ratio_1 * 100, 2),
        'var_ratio_2': round(explained_var_ratio_2 * 100, 2),
        'v1_x': round(v1[0], 3),
        'v1_y': round(v1[1], 3),
        'test_x1': round(test_sample[0], 3),
        'test_x2': round(test_sample[1], 3),
        'z_test': round(z_test, 3),
        'test_proj_x1': round(test_projected[0], 3),
        'test_proj_x2': round(test_projected[1], 3),
        'rec_error': round(rec_error, 4)
    }
    
    return plot_url, stats, sample_table


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        test_x1 = float(request.form.get('test_x1', 5.5))
        test_x2 = float(request.form.get('test_x2', 4.0))
    except (ValueError, TypeError):
        test_x1, test_x2 = 5.5, 4.0
        
    plot_url, stats, sample_table = generate_pca_visualization(test_x1, test_x2)
    
    return render_template('index.html',
                           test_x1=test_x1,
                           test_x2=test_x2,
                           plot_url=plot_url,
                           stats=stats,
                           sample_table=sample_table)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5010))
    print(f"Starting Experiment 10 PCA Server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
