import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

# State of Nature (Classes)
CLASSES = ['Normal (w1)', 'Suspicious (w2)', 'Fraudulent (w3)']

# Available Actions
ACTIONS = [
    'a1: Approve Immediately',
    'a2: Hold for Verification / Review',
    'a3: Block & Terminate Session'
]

# Default Loss Matrix Lambda[action_idx][class_idx]
DEFAULT_LOSS_MATRIX = [
    [0,   25, 100],  # a1: Approve
    [10,   2,  15],  # a2: Review
    [50,  20,   0]   # a3: Block
]

def compute_bayesian_risk(posteriors, loss_matrix):
    P = np.array(posteriors)
    L = np.array(loss_matrix)
    
    # Conditional Risk R(alpha_i | x) = sum_j lambda(alpha_i | w_j) * P(w_j | x)
    risks = np.dot(L, P)
    
    optimal_idx = int(np.argmin(risks))
    optimal_action = ACTIONS[optimal_idx]
    optimal_risk = float(risks[optimal_idx])
    
    # Action consequence and triggered system state
    if optimal_idx == 0:
        triggered_state = {
            'code': 'ACTION_APPROVED',
            'title': 'ACTION TRIGGERED: AUTOMATED CLEARANCE (a1)',
            'color': '#1b5e20',
            'bg_color': '#e8f5e9',
            'border_color': '#4caf50',
            'icon': 'APPROVED',
            'status_msg': 'Payment clearance token #TXN-90241 granted. Zero user friction introduced.',
            'event_log': [
                'Payment gateway authorized clearance protocol.',
                'Transaction token dispatched to settlement ledger.',
                'Fraud risk deemed acceptable under minimal Bayes loss.'
            ]
        }
    elif optimal_idx == 1:
        triggered_state = {
            'code': 'ACTION_REVIEW',
            'title': 'ACTION TRIGGERED: STEP-UP VERIFICATION & HUMAN REVIEW (a2)',
            'color': '#e65100',
            'bg_color': '#fff3e0',
            'border_color': '#ff9800',
            'icon': 'REVIEW_REQUIRED',
            'status_msg': 'Transaction temporarily held in escrow queue #ESC-41829. 2FA challenge dispatched.',
            'event_log': [
                'Risk threshold triggered escalation pathway.',
                'Dispatched biometric SMS / Push OTP challenge to user.',
                'Case appended to Senior Fraud Analyst active review ticket.'
            ]
        }
    else:
        triggered_state = {
            'code': 'ACTION_BLOCKED',
            'title': 'ACTION TRIGGERED: IMMEDIATE ACCESS TERMINATION & SHIELD LOCKOUT (a3)',
            'color': '#b71c1c',
            'bg_color': '#ffebee',
            'border_color': '#f44336',
            'icon': 'BLOCKED',
            'status_msg': 'Transaction rejected immediately. Originating IP and session locked out.',
            'event_log': [
                'High conditional risk prevented automated or review pathways.',
                'Session terminated with HTTP 403 Security Lockdown.',
                'Compliance SAR (Suspicious Activity Report) entry logged.'
            ]
        }
        
    return risks.tolist(), optimal_idx, optimal_action, optimal_risk, triggered_state

def generate_risk_plot(risks, optimal_idx):
    fig, ax = plt.subplots(figsize=(8, 4))
    
    action_labels = ['a1: Approve', 'a2: Review', 'a3: Block']
    colors = ['#2e7d32' if i == optimal_idx else '#546e7a' for i in range(3)]
    
    bars = ax.bar(action_labels, risks, color=colors, width=0.45, edgecolor='black')
    ax.set_ylabel('Conditional Risk R(α|x)', fontsize=10, fontweight='bold')
    ax.set_title('Bayesian Conditional Risk Comparison Across Actions', fontsize=11, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for idx, bar in enumerate(bars):
        h = bar.get_height()
        star = " ★ OPTIMAL" if idx == optimal_idx else ""
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, f"R={h:.2f}{star}",
                ha='center', va='bottom', fontsize=9, fontweight='bold',
                color='#1b5e20' if idx == optimal_idx else '#333333')
                
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

PRESETS = [
    {
        'name': 'Case A: Low-Risk Legitimate Transaction',
        'p1': 0.85, 'p2': 0.12, 'p3': 0.03,
        'description': 'Verified device, standard geo-location, regular purchase behavior.'
    },
    {
        'name': 'Case B: Ambiguous / Anomalous Transaction',
        'p1': 0.30, 'p2': 0.55, 'p3': 0.15,
        'description': 'Foreign IP address, new merchant, unusual purchase time.'
    },
    {
        'name': 'Case C: High-Confidence Fraudulent Exploit',
        'p1': 0.05, 'p2': 0.15, 'p3': 0.80,
        'description': 'Tor exit node, velocity burst attack, card-not-present anomaly.'
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    p1 = 0.30
    p2 = 0.55
    p3 = 0.15
    
    if request.method == 'POST':
        try:
            p1 = float(request.form.get('p1', 0.30))
            p2 = float(request.form.get('p2', 0.55))
            p3 = float(request.form.get('p3', 0.15))
            # Normalize to ensure valid distribution sum = 1.0
            total = p1 + p2 + p3
            if total > 0:
                p1, p2, p3 = p1/total, p2/total, p3/total
        except ValueError:
            p1, p2, p3 = 0.30, 0.55, 0.15
            
    posteriors = [p1, p2, p3]
    risks, optimal_idx, optimal_action, optimal_risk, triggered_state = compute_bayesian_risk(posteriors, DEFAULT_LOSS_MATRIX)
    plot_b64 = generate_risk_plot(risks, optimal_idx)
    
    # Calculation breakdown rows
    breakdown = []
    for i, a_name in enumerate(ACTIONS):
        terms = [f"{DEFAULT_LOSS_MATRIX[i][j]} &times; {posteriors[j]:.3f}" for j in range(3)]
        formula_str = " + ".join(terms)
        breakdown.append({
            'action': a_name,
            'formula_str': formula_str,
            'risk_val': round(risks[i], 3),
            'is_optimal': (i == optimal_idx)
        })
        
    return render_template(
        'index.html',
        classes=CLASSES,
        actions=ACTIONS,
        loss_matrix=DEFAULT_LOSS_MATRIX,
        posteriors=posteriors,
        risks=risks,
        breakdown=breakdown,
        optimal_action=optimal_action,
        optimal_risk=optimal_risk,
        triggered_state=triggered_state,
        plot_b64=plot_b64,
        presets=PRESETS
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    print(f"Starting Experiment 6 Bayesian Risk Minimization Server on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)
