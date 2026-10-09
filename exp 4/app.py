import os
import io
import base64
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm, multivariate_normal
from sklearn.datasets import load_iris
from flask import Flask, render_template, request

app = Flask(__name__)

# Load and prepare Iris Dataset
iris = load_iris(as_frame=True)
df = iris.frame.copy()
classes = ['Setosa', 'Versicolor', 'Virginica']
df['class_name'] = df['target'].map({0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'})

# 1. Single Feature: 'petal length (cm)'
single_feat = 'petal length (cm)'
single_params = {}
priors = {}
total_samples = len(df)

for c_idx, c_name in enumerate(classes):
    sub = df[df['target'] == c_idx][single_feat]
    single_params[c_name] = {
        'mean': float(sub.mean()),
        'std': float(sub.std()),
        'var': float(sub.var())
    }
    priors[c_name] = float(len(sub) / total_samples)

# 2. Multiple Features (2D): 'petal length (cm)' and 'sepal length (cm)'
multi_feats = ['petal length (cm)', 'sepal length (cm)']
multi_params = {}

for c_idx, c_name in enumerate(classes):
    sub = df[df['target'] == c_idx][multi_feats]
    mean_vec = sub.mean().values
    cov_mat = sub.cov().values
    multi_params[c_name] = {
        'mean': mean_vec,
        'cov': cov_mat
    }

# -------------------------------------------------------------
# BAYESIAN CLASSIFIER LOGIC
# -------------------------------------------------------------
def classify_single_feature(test_val):
    likelihoods = {}
    numerator = {}
    
    for c_name in classes:
        mu = single_params[c_name]['mean']
        sigma = single_params[c_name]['std']
        # Univariate Gaussian Likelihood
        p_x_given_w = norm.pdf(test_val, loc=mu, scale=sigma)
        likelihoods[c_name] = p_x_given_w
        numerator[c_name] = p_x_given_w * priors[c_name]
        
    evidence = sum(numerator.values())
    posteriors = {}
    for c_name in classes:
        posteriors[c_name] = numerator[c_name] / evidence if evidence > 0 else 0.0
        
    predicted_class = max(posteriors, key=posteriors.get)
    return {
        'test_val': test_val,
        'likelihoods': likelihoods,
        'evidence': evidence,
        'posteriors': posteriors,
        'predicted_class': predicted_class,
        'confidence': posteriors[predicted_class] * 100
    }

def classify_multi_feature(test_vec):
    likelihoods = {}
    numerator = {}
    
    for c_name in classes:
        mu = multi_params[c_name]['mean']
        cov = multi_params[c_name]['cov']
        # Multivariate Gaussian Likelihood
        p_x_given_w = multivariate_normal.pdf(test_vec, mean=mu, cov=cov)
        likelihoods[c_name] = p_x_given_w
        numerator[c_name] = p_x_given_w * priors[c_name]
        
    evidence = sum(numerator.values())
    posteriors = {}
    for c_name in classes:
        posteriors[c_name] = numerator[c_name] / evidence if evidence > 0 else 0.0
        
    predicted_class = max(posteriors, key=posteriors.get)
    return {
        'test_vec': test_vec,
        'likelihoods': likelihoods,
        'evidence': evidence,
        'posteriors': posteriors,
        'predicted_class': predicted_class,
        'confidence': posteriors[predicted_class] * 100
    }

# -------------------------------------------------------------
# PLOT GENERATION
# -------------------------------------------------------------
def generate_plots(test_x1, test_x2, single_res, multi_res):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # 1. Single Feature Gaussian Distributions Plot
    x_range = np.linspace(0.5, 7.5, 500)
    colors = {'Setosa': '#1e88e5', 'Versicolor': '#43a047', 'Virginica': '#e53935'}
    
    for c_name in classes:
        mu = single_params[c_name]['mean']
        sigma = single_params[c_name]['std']
        pdf_curve = norm.pdf(x_range, loc=mu, scale=sigma)
        axes[0].plot(x_range, pdf_curve, label=f"{c_name} (μ={mu:.2f}, σ={sigma:.2f})", color=colors[c_name], linewidth=2.2)
        axes[0].fill_between(x_range, pdf_curve, alpha=0.15, color=colors[c_name])
        
    # Mark test sample on 1D plot
    axes[0].axvline(test_x1, color='#d81b60', linestyle='--', linewidth=2, label=f"Test Sample x={test_x1}")
    axes[0].scatter([test_x1], [norm.pdf(test_x1, loc=single_params[single_res['predicted_class']]['mean'],
                                        scale=single_params[single_res['predicted_class']]['std'])],
                    color='#d81b60', s=100, zorder=5)
    axes[0].set_title(f"Single Feature Bayesian Decision: {single_res['predicted_class']}", fontsize=11, fontweight='bold')
    axes[0].set_xlabel('Petal Length (cm)', fontsize=10, fontweight='bold')
    axes[0].set_ylabel('Probability Density p(x|ω)', fontsize=10, fontweight='bold')
    axes[0].legend(loc='upper right', fontsize=8)
    axes[0].grid(True, linestyle='--', alpha=0.5)
    
    # 2. Multi-Feature 2D Scatter & Decision Regions
    for c_idx, c_name in enumerate(classes):
        sub = df[df['target'] == c_idx]
        axes[1].scatter(sub['petal length (cm)'], sub['sepal length (cm)'],
                        label=c_name, color=colors[c_name], alpha=0.7, edgecolors='k', s=40)
        # Plot mean center
        mu = multi_params[c_name]['mean']
        axes[1].scatter([mu[0]], [mu[1]], color=colors[c_name], marker='X', s=120, edgecolors='black', linewidth=1.5)

    # Plot test point on 2D plot
    axes[1].scatter([test_x1], [test_x2], color='#ffeb3b', edgecolors='#d81b60', marker='*', s=250, linewidth=2,
                    label=f"Test Point ({test_x1}, {test_x2})", zorder=10)
    axes[1].set_title(f"Multi-Feature Bayesian Decision: {multi_res['predicted_class']}", fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Petal Length (cm) [Feature 1]', fontsize=10, fontweight='bold')
    axes[1].set_ylabel('Sepal Length (cm) [Feature 2]', fontsize=10, fontweight='bold')
    axes[1].legend(loc='lower right', fontsize=8)
    axes[1].grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# -------------------------------------------------------------
# FLASK ROUTE
# -------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    # Default test sample values
    test_x1 = 4.2  # Petal length
    test_x2 = 5.8  # Sepal length
    
    if request.method == 'POST':
        try:
            test_x1 = float(request.form.get('petal_length', 4.2))
            test_x2 = float(request.form.get('sepal_length', 5.8))
        except ValueError:
            test_x1, test_x2 = 4.2, 5.8

    # Perform Single Feature Classification
    single_res = classify_single_feature(test_x1)
    
    # Perform Multi-Feature Classification
    multi_res = classify_multi_feature([test_x1, test_x2])
    
    # Generate visualization plot
    plot_b64 = generate_plots(test_x1, test_x2, single_res, multi_res)
    
    # Pre-defined benchmark samples for quick interactive testing
    presets = [
        {'name': 'Preset 1: Likely Setosa', 'petal_len': 1.5, 'sepal_len': 5.0},
        {'name': 'Preset 2: Likely Versicolor', 'petal_len': 4.2, 'sepal_len': 5.9},
        {'name': 'Preset 3: Likely Virginica', 'petal_len': 5.6, 'sepal_len': 6.7},
        {'name': 'Preset 4: Borderline Versicolor/Virginica', 'petal_len': 4.9, 'sepal_len': 6.2}
    ]
    
    return render_template(
        'index.html',
        classes=classes,
        single_params=single_params,
        multi_params=multi_params,
        priors=priors,
        test_x1=test_x1,
        test_x2=test_x2,
        single_res=single_res,
        multi_res=multi_res,
        plot_b64=plot_b64,
        presets=presets
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    print(f"Starting Experiment 4 Bayesian Classifier on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)
