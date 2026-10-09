#!/usr/bin/env python3
"""
PARS LAB MASTER PORTAL & MULTI-SERVER RUNNER
Netaji Subhas University of Technology (NSUT)
Department of Information Technology
Student: Monis (Roll No: 2023UIT3027)
Course: Pattern Analysis and Recommender Systems (PARS)
Lab Instructor: Dr. Vishal Maheshkar (2026-2027)
"""

import os
import sys
import time
import signal
import socket
import subprocess
import urllib.request
from flask import Flask, render_template_string, jsonify, redirect, send_from_directory

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 11 Experiments Configuration
EXPERIMENTS = [
    {
        "id": 1,
        "port": 5001,
        "title": "Prepare a document by studying any two datasets of different domain, write the description of dataset consisting of purpose. what is source, write Feature description, how many features, work done by various authors and performance achieved by atleast three authors in recent years. Cite References and add references.",
        "badge": "Dataset Analysis & Literature Survey",
        "desc": "Comparative taxonomy of CIFAR-10 (d=3072 raw pixels) vs Iris (d=4 tabular), statistical profiles, and formal citations of SOTA benchmark models (AlexNet, ResNet, ViT).",
        "path": os.path.join(BASE_DIR, "exp 1", "app.py")
    },
    {
        "id": 2,
        "port": 5002,
        "title": "Prepare a page using flask consisting of a code in python to extract and store the two datasets that you studied in Experiment 1, Plot the performance plot, display different features having description",
        "badge": "Data Engineering & Model Benchmarks",
        "desc": "Automatic extraction and local storage of CIFAR-10 images & Iris tabular CSVs, training 4 classifiers with Accuracy, Precision, Recall, F1, and Confusion Matrices.",
        "path": os.path.join(BASE_DIR, "exp 2", "app.py")
    },
    {
        "id": 3,
        "port": 5003,
        "title": "Prepare an informative page using flask consisting of a code in python to extract features from text/video/audio. Extract at least 3 features from various timestamp (at least 10 Samples) justifying the objective for application. text/video/audio file should exist in the page.",
        "badge": "Audio Signal Processing",
        "desc": "Framing and windowing raw acoustic waveforms to compute RMS Energy, Zero Crossing Rate (ZCR), and Spectral Centroid across 10 temporal frames with interactive audio player.",
        "path": os.path.join(BASE_DIR, "exp 3", "app.py")
    },
    {
        "id": 4,
        "port": 5004,
        "title": "Prepare an interactive page using flask consisting of a code in python for Single feature multiple class, Multiple features multiple class and then classify test samples using Bayesian approach.",
        "badge": "Generative Modeling & Decision Surfaces",
        "desc": "Gaussian generative Bayes classification computing Prior, Likelihood, and Posterior distributions with 1D thresholds and 2D non-linear quadratic decision boundary contours.",
        "path": os.path.join(BASE_DIR, "exp 4", "app.py")
    },
    {
        "id": 5,
        "port": 5005,
        "title": "Prepare a page using flask consisting of a code in python to extract text paragraph, separate the sentences, remove various stop words, perform Lemmatization and stemming then classify test samples using Bayesian approach.",
        "badge": "NLP & Text Mining",
        "desc": "End-to-end text preprocessing pipeline (Tokenization, Stop Words, Porter Stemming, WordNet Lemmatization) followed by Multinomial Naive Bayes with Laplace smoothing.",
        "path": os.path.join(BASE_DIR, "exp 5", "app.py")
    },
    {
        "id": 6,
        "port": 5006,
        "title": "Prepare a page using flask consisting of a code in python to perform Bayesian Risk Minimization for at least three classes, three actions. Given loss function, particular action should trigger particular action, that action should reflect in page itself.",
        "badge": "Decision Theory & Asymmetric Costs",
        "desc": "Conditional risk formulation R(a_i | x) = sum(lambda_ij * P(w_j | x)) incorporating an asymmetric loss penalty matrix for safety-critical classification.",
        "path": os.path.join(BASE_DIR, "exp 6", "app.py")
    },
    {
        "id": 7,
        "port": 5007,
        "title": "Implement Linear regression in python (no inbuild function should be used) to find optimized parameters using Gradient descent for any application and Plot Gradient Descent curve.",
        "badge": "NumPy From Scratch",
        "desc": "Vectorized Batch Gradient Descent implemented from first principles without scikit-learn, estimating housing prices and tracking MSE cost function decay curves.",
        "path": os.path.join(BASE_DIR, "exp 7", "app.py")
    },
    {
        "id": 8,
        "port": 5008,
        "title": "Implement Logistic regression for binary class and multiclass classification in python (no inbuild function should be used) to find optimized parameters using Gradient descent for any application and Plot Gradient Descent curve.",
        "badge": "Classification From Scratch",
        "desc": "Sigmoid binary classification and Softmax multiclass classification from first principles with Log Loss / Cross-Entropy gradient updates and decision region meshgrids.",
        "path": os.path.join(BASE_DIR, "exp 8", "app.py")
    },
    {
        "id": 9,
        "port": 5009,
        "title": "Implement regularization for any application show plots of 1)decision boundary and 2) performance before and after applying regularization",
        "badge": "Overfitting Control & Shrinkage",
        "desc": "Demonstrates decision boundary smoothing, feature weight shrinkage (L2 Ridge) vs exact sparsity (L1 Lasso), and before/after performance comparison bar charts.",
        "path": os.path.join(BASE_DIR, "exp 9", "app.py")
    },
    {
        "id": 10,
        "port": 5010,
        "title": "Implement Principal component analysis (PCA) for any application which involves testing. Also show the projected line and new reduced feature mapped on projected line.",
        "badge": "Unsupervised Dimensionality Reduction",
        "desc": "Computes sample covariance matrix and dominant eigenvectors to project 2D data onto the 1st Principal Component line, evaluating test sample reconstruction errors.",
        "path": os.path.join(BASE_DIR, "exp 10", "app.py")
    },
    {
        "id": 11,
        "port": 5011,
        "title": "Implement Linear Discriminant analysis (LDA) for any application which involves testing. Also show the projected line and new reduced feature mapped on projected line.",
        "badge": "Supervised Projection & Fisher Criterion",
        "desc": "Maximizes between-class to within-class scatter ratio S_W^-1(mu_1 - mu_2), projects 2D points onto the optimal discriminant line, and classifies test coordinates.",
        "path": os.path.join(BASE_DIR, "exp 11", "app.py")
    }
]

processes = {}

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_server_status(port):
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/", headers={'User-Agent': 'HealthCheck'})
        with urllib.request.urlopen(req, timeout=0.8) as response:
            return response.status == 200
    except Exception:
        return False

HTML_PORTAL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PARS Lab Master Portal | NSUT (Monis - 2023UIT3027)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #1e3a8a;
            --primary-dark: #0f172a;
            --accent: #2563eb;
            --success: #16a34a;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.5;
            padding: 24px 16px;
        }
        .container {
            max-width: 1240px;
            margin: 0 auto;
        }
        /* Header Card */
        .header-card {
            background: linear-gradient(135deg, #0f2b5c 0%, #1e3a8a 50%, #1e40af 100%);
            color: white;
            border-radius: 16px;
            padding: 32px 36px;
            box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            flex-wrap: wrap;
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 24px;
        }
        .logo-img {
            width: 95px;
            height: 95px;
            background: white;
            border-radius: 50%;
            padding: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            object-fit: contain;
        }
        .header-text h1 {
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .header-text h2 {
            font-size: 14px;
            font-weight: 500;
            color: #bfdbfe;
            margin-bottom: 8px;
            letter-spacing: 0.3px;
        }
        .header-text .course-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.25);
        }
        .header-meta {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 13px;
            min-width: 280px;
        }
        .meta-row {
            display: flex;
            justify-content: space-between;
            padding: 3px 0;
        }
        .meta-label {
            color: #93c5fd;
            font-weight: 500;
        }
        .meta-val {
            font-weight: 700;
            color: #ffffff;
        }

        /* Top Action Bar */
        .action-bar {
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 24px;
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .status-summary {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
            font-weight: 600;
        }
        .pulse-dot {
            width: 12px;
            height: 12px;
            background-color: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7);
            animation: pulse 1.8s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7); }
            70% { box-shadow: 0 0 0 8px rgba(22, 163, 74, 0); }
            100% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }
        }
        .btn-group {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        .btn-pdf {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #dc2626;
            color: white;
            text-decoration: none;
            padding: 9px 18px;
            border-radius: 8px;
            font-size: 13.5px;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
        }
        .btn-pdf:hover {
            background: #b91c1c;
            transform: translateY(-1px);
        }
        .btn-github {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #24292f;
            color: white;
            text-decoration: none;
            padding: 9px 18px;
            border-radius: 8px;
            font-size: 13.5px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .btn-github:hover {
            background: #000000;
            transform: translateY(-1px);
        }

        /* Experiment Grid */
        .exp-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 20px;
        }
        .exp-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s ease;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            position: relative;
            overflow: hidden;
        }
        .exp-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 24px -6px rgba(0,0,0,0.08);
            border-color: #93c5fd;
        }
        .exp-card-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 12px;
        }
        .exp-number {
            font-size: 13px;
            font-weight: 800;
            color: var(--accent);
            background: #eff6ff;
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.5px;
        }
        .server-status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            font-weight: 600;
            color: #16a34a;
            background: #f0fdf4;
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid #bbf7d0;
        }
        .status-light {
            width: 8px;
            height: 8px;
            background-color: #16a34a;
            border-radius: 50%;
        }
        .exp-title {
            font-size: 13.5px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 8px;
            line-height: 1.4;
        }
        .exp-badge {
            font-size: 11.5px;
            font-weight: 600;
            color: #475569;
            background: #f1f5f9;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 12px;
        }
        .exp-desc {
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.45;
            margin-bottom: 20px;
            flex-grow: 1;
        }
        .exp-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 14px;
            border-top: 1px solid #f1f5f9;
        }
        .port-info {
            font-size: 12.5px;
            color: #64748b;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-weight: 600;
        }
        .btn-launch {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--accent);
            color: white;
            text-decoration: none;
            font-size: 13.5px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        .btn-launch:hover {
            background: #1d4ed8;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
        }

        /* Footer */
        .footer {
            margin-top: 40px;
            text-align: center;
            color: #94a3b8;
            font-size: 13px;
            padding: 20px 0;
            border-top: 1px solid var(--border);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Main Header Card -->
        <div class="header-card">
            <div class="header-left">
                <img src="/nsut_logo.png" alt="NSUT Emblem" class="logo-img">
                <div class="header-text">
                    <h1>Netaji Subhas University of Technology</h1>
                    <h2>Department of Information Technology &bull; New Delhi</h2>
                    <span class="course-badge">Pattern Analysis &amp; Recommender Systems (PARS) Lab</span>
                </div>
            </div>
            <div class="header-meta">
                <div class="meta-row">
                    <span class="meta-label">Student Name:</span>
                    <span class="meta-val">Monis</span>
                </div>
                <div class="meta-row">
                    <span class="meta-label">Roll Number:</span>
                    <span class="meta-val">2023UIT3027</span>
                </div>
                <div class="meta-row">
                    <span class="meta-label">Batch &amp; Group:</span>
                    <span class="meta-val">Batch 1 / Group 1</span>
                </div>
                <div class="meta-row">
                    <span class="meta-label">Lab Instructor:</span>
                    <span class="meta-val">Dr. Vishal Maheshkar</span>
                </div>
                <div class="meta-row">
                    <span class="meta-label">Academic Session:</span>
                    <span class="meta-val">2026&ndash;2027</span>
                </div>
            </div>
        </div>

        <!-- Top Action Bar -->
        <div class="action-bar">
            <div class="status-summary">
                <div class="pulse-dot"></div>
                <span>All 11 Experiment Servers Online &amp; Running Concurrently</span>
            </div>
            <div class="btn-group">
                <a href="/download_pdf" target="_blank" class="btn-pdf">
                    📄 View Full Practical File (58-Page PDF)
                </a>
                <a href="https://github.com/dSAxmonis/pars-lab" target="_blank" class="btn-github">
                    ⭐ GitHub Repository
                </a>
            </div>
        </div>

        <!-- 11 Experiments Grid -->
        <div class="exp-grid">
            {% for exp in exps %}
            <div class="exp-card">
                <div>
                    <div class="exp-card-header">
                        <span class="exp-number">EXPERIMENT {{ "%02d" | format(exp.id) }}</span>
                        <span class="server-status">
                            <span class="status-light"></span>
                            Port {{ exp.port }} Live
                        </span>
                    </div>
                    <div class="exp-title">{{ exp.title }}</div>
                    <div class="exp-badge">{{ exp.badge }}</div>
                    <div class="exp-desc">{{ exp.desc }}</div>
                </div>
                <div class="exp-footer">
                    <span class="port-info">http://127.0.0.1:{{ exp.port }}</span>
                    <a href="http://127.0.0.1:{{ exp.port }}" target="_blank" class="btn-launch">
                        🚀 Open Live &rarr;
                    </a>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="footer">
            Netaji Subhas University of Technology &bull; PARS Practical Record File &bull; Monis (2023UIT3027) &bull; Academic Year 2026&ndash;2027
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PORTAL, exps=EXPERIMENTS)

@app.route('/nsut_logo.png')
def serve_logo():
    return send_from_directory(BASE_DIR, 'nsut_logo.png')

@app.route('/download_pdf')
def serve_pdf():
    return send_from_directory(BASE_DIR, 'PARS_LAB_COMPLETE_PRACTICAL_FILE.pdf')

def start_experiment_servers():
    print("=" * 70)
    print("🚀 STARTING ALL 11 PARS LAB EXPERIMENT SERVERS CONCURRENTLY...")
    print("=" * 70)
    for exp in EXPERIMENTS:
        exp_id = exp["id"]
        port = exp["port"]
        script_path = exp["path"]
        env = os.environ.copy()
        env["PORT"] = str(port)

        cmd = [sys.executable, script_path]
        p = subprocess.Popen(cmd, env=env, cwd=os.path.dirname(script_path))
        processes[exp_id] = p
        print(f"  [Exp {exp_id:02d}] Booting on http://127.0.0.1:{port} (PID: {p.pid})")

    # Give them 2 seconds to initialize
    time.sleep(2)
    print("=" * 70)
    print("✅ ALL 11 EXPERIMENT SERVERS ARE RUNNING!")
    print(f"🌟 MASTER PORTAL LAUNCHED: http://127.0.0.1:8000 (and http://localhost:8000)")
    print("=" * 70)

def cleanup(sig=None, frame=None):
    print("\n🛑 Shutting down all experiment servers...")
    for exp_id, p in processes.items():
        try:
            p.terminate()
            p.wait(timeout=1)
        except Exception:
            p.kill()
    print("✅ All servers stopped cleanly.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

if __name__ == '__main__':
    start_experiment_servers()
    app.run(host='0.0.0.0', port=8000, debug=False)
