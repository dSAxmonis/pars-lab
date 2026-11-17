import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, session, redirect, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
app.secret_key = 'pars_lab_exp21_sgd_matrix_factorization_secret_key'

# ==============================================================================
# MOVIES DATASET (20 Movies across 8+ Genres)
# Genres: Action, Comedy, Drama, Sci-Fi, Horror, Romance, Thriller, Animation
# ==============================================================================
MOVIES_DATASET = [
    {
        'id': 0,
        'title': 'The Matrix',
        'year': 1999,
        'genres': ['Sci-Fi', 'Action'],
        'director': 'Lana & Lilly Wachowski',
        'cast': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
        'rating': 8.7,
        'plot_keywords': 'cyberpunk, simulated reality, artificial intelligence, martial arts rebellion',
        'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
        'poster_bg': '#0f2b1d',
        'poster_accent': '#22c55e',
        'initials': 'MX',
        'emoji': '🕶️'
    },
    {
        'id': 1,
        'title': 'Inception',
        'year': 2010,
        'genres': ['Sci-Fi', 'Thriller'],
        'director': 'Christopher Nolan',
        'cast': 'Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page',
        'rating': 8.8,
        'plot_keywords': 'dream architecture, subconscious heist, spinning totem, memory labyrinth',
        'description': 'A thief who steals corporate secrets through dream-sharing technology is tasked with the inverse job of planting an idea into a CEO\'s mind.',
        'poster_bg': '#1e1b4b',
        'poster_accent': '#6366f1',
        'initials': 'IC',
        'emoji': '🌀'
    },
    {
        'id': 2,
        'title': 'Interstellar',
        'year': 2014,
        'genres': ['Sci-Fi', 'Drama'],
        'director': 'Christopher Nolan',
        'cast': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain',
        'rating': 8.7,
        'plot_keywords': 'wormhole exploration, black hole Gargantua, relativity, father-daughter bond',
        'description': 'A team of explorers travels through a wormhole in space in an attempt to ensure humanity\'s survival beyond a dying Earth.',
        'poster_bg': '#091e3a',
        'poster_accent': '#38bdf8',
        'initials': 'IS',
        'emoji': '🚀'
    },
    {
        'id': 3,
        'title': 'The Dark Knight',
        'year': 2008,
        'genres': ['Action', 'Thriller'],
        'director': 'Christopher Nolan',
        'cast': 'Christian Bale, Heath Ledger, Aaron Eckhart',
        'rating': 9.0,
        'plot_keywords': 'Gotham vigilante, chaos agent Joker, psychological warfare, moral dilemma',
        'description': 'When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests.',
        'poster_bg': '#18181b',
        'poster_accent': '#f59e0b',
        'initials': 'DK',
        'emoji': '🦇'
    },
    {
        'id': 4,
        'title': 'Avengers: Endgame',
        'year': 2019,
        'genres': ['Action', 'Sci-Fi'],
        'director': 'Anthony & Joe Russo',
        'cast': 'Robert Downey Jr., Chris Evans, Mark Ruffalo',
        'rating': 8.4,
        'plot_keywords': 'quantum time heist, Infinity stones, superhero assembly, cosmic redemption',
        'description': 'After the devastating galactic snap of Thanos, the remaining Avengers assemble once more to reverse the catastrophic destruction.',
        'poster_bg': '#450a0a',
        'poster_accent': '#ef4444',
        'initials': 'AE',
        'emoji': '⚡'
    },
    {
        'id': 5,
        'title': 'Gladiator',
        'year': 2000,
        'genres': ['Action', 'Drama'],
        'director': 'Ridley Scott',
        'cast': 'Russell Crowe, Joaquin Phoenix, Connie Nielsen',
        'rating': 8.5,
        'plot_keywords': 'Roman general, Colosseum arena, imperial betrayal, bloody vengeance',
        'description': 'A betrayed Roman general sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.',
        'poster_bg': '#422006',
        'poster_accent': '#d97706',
        'initials': 'GL',
        'emoji': '⚔️'
    },
    {
        'id': 6,
        'title': 'Pulp Fiction',
        'year': 1994,
        'genres': ['Crime', 'Thriller'],
        'director': 'Quentin Tarantino',
        'cast': 'John Travolta, Samuel L. Jackson, Uma Thurman',
        'rating': 8.9,
        'plot_keywords': 'nonlinear narrative, hitmen philosophical banter, glowing briefcase, diner heist',
        'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
        'poster_bg': '#3b0764',
        'poster_accent': '#c084fc',
        'initials': 'PF',
        'emoji': '🔫'
    },
    {
        'id': 7,
        'title': 'The Godfather',
        'year': 1972,
        'genres': ['Crime', 'Drama'],
        'director': 'Francis Ford Coppola',
        'cast': 'Marlon Brando, Al Pacino, James Caan',
        'rating': 9.2,
        'plot_keywords': 'mafia dynasty, Corleone family, Sicilian code of honor, ruthless succession',
        'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant youngest son.',
        'poster_bg': '#262626',
        'poster_accent': '#fbbf24',
        'initials': 'GF',
        'emoji': '🎩'
    },
    {
        'id': 8,
        'title': 'Parasite',
        'year': 2019,
        'genres': ['Thriller', 'Drama'],
        'director': 'Bong Joon-ho',
        'cast': 'Song Kang-ho, Lee Sun-kyun, Choi Woo-shik',
        'rating': 8.5,
        'plot_keywords': 'subterranean class divide, architectural deception, rainstorm tragedy, social satire',
        'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
        'poster_bg': '#042f2e',
        'poster_accent': '#2dd4bf',
        'initials': 'PS',
        'emoji': '🏠'
    },
    {
        'id': 9,
        'title': 'Fight Club',
        'year': 1999,
        'genres': ['Drama', 'Thriller'],
        'director': 'David Fincher',
        'cast': 'Brad Pitt, Edward Norton, Helena Bonham Carter',
        'rating': 8.8,
        'plot_keywords': 'insomnia, anti-consumerist revolt, soap maker alter-ego, project mayhem',
        'description': 'An insomniac office worker looking for a way to change his life crosses paths with a devil-may-care soap maker and forms an underground fight club.',
        'poster_bg': '#4c0519',
        'poster_accent': '#fb7185',
        'initials': 'FC',
        'emoji': '🥊'
    },
    {
        'id': 10,
        'title': 'The Shawshank Redemption',
        'year': 1994,
        'genres': ['Drama'],
        'director': 'Frank Darabont',
        'cast': 'Tim Robbins, Morgan Freeman, Bob Gunton',
        'rating': 9.3,
        'plot_keywords': 'wrongful imprisonment, geological rock hammer, tunnel escape, Pacific ocean hope',
        'description': 'Over the course of several years, two convicts form a lifelong bond, seeking solace and eventual redemption through acts of common decency.',
        'poster_bg': '#172554',
        'poster_accent': '#60a5fa',
        'initials': 'SR',
        'emoji': '🗝️'
    },
    {
        'id': 11,
        'title': 'Forrest Gump',
        'year': 1994,
        'genres': ['Drama', 'Romance'],
        'director': 'Robert Zemeckis',
        'cast': 'Tom Hanks, Robin Wright, Gary Sinise',
        'rating': 8.8,
        'plot_keywords': 'box of chocolates, ping-pong diplomacy, Vietnam heroism, cross-country run',
        'description': 'The historical events of the 20th century unfold from the gentle perspective of an Alabama man with an IQ of 75 yearning for his childhood sweetheart.',
        'poster_bg': '#14532d',
        'poster_accent': '#4ade80',
        'initials': 'FG',
        'emoji': '🍫'
    },
    {
        'id': 12,
        'title': 'La La Land',
        'year': 2016,
        'genres': ['Romance', 'Comedy'],
        'director': 'Damien Chazelle',
        'cast': 'Ryan Gosling, Emma Stone, John Legend',
        'rating': 8.0,
        'plot_keywords': 'jazz pianist, Hollywood auditions, vibrant city of stars, bittersweet dream',
        'description': 'While navigating their careers in Los Angeles, a jazz pianist and an aspiring actress fall in love while attempting to reconcile their dreams.',
        'poster_bg': '#581c87',
        'poster_accent': '#e879f9',
        'initials': 'LL',
        'emoji': '🎷'
    },
    {
        'id': 13,
        'title': 'Titanic',
        'year': 1997,
        'genres': ['Romance', 'Drama'],
        'director': 'James Cameron',
        'cast': 'Leonardo DiCaprio, Kate Winslet, Billy Zane',
        'rating': 7.9,
        'plot_keywords': 'luxury ocean liner, iceberg collision, heart of the ocean diamond, tragic romance',
        'description': 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.',
        'poster_bg': '#0c4a6e',
        'poster_accent': '#38bdf8',
        'initials': 'TT',
        'emoji': '🚢'
    },
    {
        'id': 14,
        'title': 'The Hangover',
        'year': 2009,
        'genres': ['Comedy'],
        'director': 'Todd Phillips',
        'cast': 'Bradley Cooper, Ed Helms, Zach Galifianakis',
        'rating': 7.7,
        'plot_keywords': 'Las Vegas bachelor party, missing groom, tiger in bathroom, wild hangover mystery',
        'description': 'Three buddies wake up from a bachelor party in Las Vegas with no memory of the previous night and the groom missing just hours before the wedding.',
        'poster_bg': '#713f12',
        'poster_accent': '#facc15',
        'initials': 'HO',
        'emoji': '🍸'
    },
    {
        'id': 15,
        'title': 'Superbad',
        'year': 2007,
        'genres': ['Comedy'],
        'director': 'Greg Mottola',
        'cast': 'Jonah Hill, Michael Cera, Christopher Mintz-Plasse',
        'rating': 7.6,
        'plot_keywords': 'high school fake ID, McLovin legend, party alcohol mission, friendship anxiety',
        'description': 'Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes wildly awry.',
        'poster_bg': '#831843',
        'poster_accent': '#f472b6',
        'initials': 'SB',
        'emoji': '🍺'
    },
    {
        'id': 16,
        'title': 'The Conjuring',
        'year': 2013,
        'genres': ['Horror', 'Thriller'],
        'director': 'James Wan',
        'cast': 'Vera Farmiga, Patrick Wilson, Lili Taylor',
        'rating': 7.5,
        'plot_keywords': 'paranormal demonologists, haunted farmhouse, wardrobe entity, exorcism ritual',
        'description': 'Paranormal investigators Ed and Lorraine Warren work to help a terrorized family confronted by a dark presence in their secluded Rhode Island farmhouse.',
        'poster_bg': '#312e81',
        'poster_accent': '#a5b4fc',
        'initials': 'CJ',
        'emoji': '👻'
    },
    {
        'id': 17,
        'title': 'A Quiet Place',
        'year': 2018,
        'genres': ['Horror', 'Sci-Fi'],
        'director': 'John Krasinski',
        'cast': 'Emily Blunt, John Krasinski, Millicent Simmonds',
        'rating': 7.5,
        'plot_keywords': 'sound-hunting blind creatures, barefoot sand paths, silent sign language survival',
        'description': 'A family must navigate their lives in absolute silence while hiding from blind extraterrestrial monsters with ultra-sensitive hearing.',
        'poster_bg': '#1e293b',
        'poster_accent': '#94a3b8',
        'initials': 'QP',
        'emoji': '🤫'
    },
    {
        'id': 18,
        'title': 'Spirited Away',
        'year': 2001,
        'genres': ['Animation', 'Fantasy'],
        'director': 'Hayao Miyazaki',
        'cast': 'Rumi Hiiragi, Miyu Irino, Mari Natsuki',
        'rating': 8.6,
        'plot_keywords': 'spirit bathhouse, Yubaba witch contract, river dragon Haku, no-face phantom',
        'description': 'During her family\'s move to the suburbs, a sullen 10-year-old girl wanders into a magical spirit bathhouse and must work to free her parents.',
        'poster_bg': '#064e3b',
        'poster_accent': '#34d399',
        'initials': 'SA',
        'emoji': '🐉'
    },
    {
        'id': 19,
        'title': 'Coco',
        'year': 2017,
        'genres': ['Animation', 'Comedy'],
        'director': 'Lee Unkrich',
        'cast': 'Anthony Gonzalez, Gael García Bernal, Benjamin Bratt',
        'rating': 8.4,
        'plot_keywords': 'Land of the Dead, marigold bridge, acoustic guitar memory, Dia de los Muertos',
        'description': 'Aspiring young musician Miguel enters the vibrant Land of the Dead to unlock the real story behind his family\'s generations-old ban on music.',
        'poster_bg': '#701a75',
        'poster_accent': '#f0abfc',
        'initials': 'CC',
        'emoji': '🎸'
    }
]

# ==============================================================================
# USER NAMES & INITIAL RATINGS MATRIX (8 Users x 20 Movies)
# Scale: 1 to 5. 0 represents unknown/unrated rating.
# ==============================================================================
USERS = [
    {'id': 0, 'name': 'Alice (Sci-Fi & Action)'},
    {'id': 1, 'name': 'Bob (Crime & Noir)'},
    {'id': 2, 'name': 'Charlie (Comedy & Romance)'},
    {'id': 3, 'name': 'Diana (Horror & Thriller)'},
    {'id': 4, 'name': 'Ethan (Animation & Family)'},
    {'id': 5, 'name': 'Fiona (Action Blockbusters)'},
    {'id': 6, 'name': 'George (Drama Connoisseur)'},
    {'id': 7, 'name': 'Monis (Active Student - 2023UIT3027)'}
]

DEFAULT_RATINGS = [
    # Alice: Sci-Fi / Action heavy
    [5, 5, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 4, 0, 0],
    # Bob: Crime / Noir heavy
    [0, 4, 0, 4, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    # Charlie: Comedy / Romance heavy
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 5, 5, 5, 1, 0, 0, 4],
    # Diana: Horror / Suspense heavy
    [0, 4, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 0, 0, 5, 5, 0, 0],
    # Ethan: Animation / Whimsical heavy
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 5, 4, 0, 0, 0, 0, 0, 5, 5],
    # Fiona: Action Blockbusters heavy
    [4, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    # George: Drama Connoisseur heavy
    [0, 0, 0, 0, 0, 4, 4, 5, 5, 0, 5, 5, 0, 3, 0, 0, 0, 0, 0, 0],
    # Monis: Active student user (Sci-Fi, Action, Drama known ratings, rest unrated 0)
    [5, 5, 5, 4, 4, 0, 0, 0, 0, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


# ==============================================================================
# MATRIX FACTORIZATION VIA STOCHASTIC GRADIENT DESCENT (Pure NumPy from scratch)
# Objective: R ≈ P * Q^T
# ==============================================================================
def train_matrix_factorization_sgd(R_matrix, k=3, epochs=15, lr=0.02, reg=0.04, seed=42):
    """
    Implements Matrix Factorization using Stochastic Gradient Descent from scratch.
    
    Parameters:
      R_matrix: 2D numpy array (m x n) with 0 indicating unknown ratings.
      k: Number of latent factors.
      epochs: Training iterations (must be >= 3).
      lr: Learning rate (gamma / alpha).
      reg: L2 Regularization parameter (lambda).
      seed: Random seed for reproducible latent factor initialization.
      
    Returns:
      P: User latent matrix (m x k)
      Q: Item latent matrix (n x k)
      loss_history: list of dicts recording epoch metrics
      R_reconstructed: Reconstructed matrix (m x n) clipped to [1.0, 5.0]
    """
    R = np.array(R_matrix, dtype=float)
    m, n = R.shape
    
    # Identify observed entries (non-zero ratings)
    observed = [(u, i) for u in range(m) for i in range(n) if R[u, i] > 0]
    num_observed = len(observed)
    
    # Calculate global mean of observed ratings
    global_mean = float(np.mean([R[u, i] for u, i in observed])) if num_observed > 0 else 3.5
    
    # Latent matrices initialization around sqrt(global_mean / k) with small variance
    np.random.seed(seed)
    init_center = np.sqrt(global_mean / k)
    P = np.random.normal(loc=init_center, scale=0.1, size=(m, k))
    Q = np.random.normal(loc=init_center, scale=0.1, size=(n, k))
    
    loss_history = []
    
    for epoch in range(1, epochs + 1):
        # Shuffle observed ratings to guarantee stochastic gradient path
        indices = list(range(num_observed))
        np.random.shuffle(indices)
        
        for idx in indices:
            u, i = observed[idx]
            r_true = R[u, i]
            r_pred = float(np.dot(P[u], Q[i]))
            err = r_true - r_pred
            
            # Simultaneous SGD update with L2 regularization
            p_prev = P[u].copy()
            q_prev = Q[i].copy()
            
            P[u] += lr * (err * q_prev - reg * p_prev)
            Q[i] += lr * (err * p_prev - reg * q_prev)
            
        # Compute epoch training metrics
        current_errors = [R[u, i] - np.dot(P[u], Q[i]) for u, i in observed]
        mse = float(np.mean(np.square(current_errors)))
        frob_penalty = float((reg / num_observed) * (np.sum(P**2) + np.sum(Q**2)))
        total_loss = mse + frob_penalty
        rmse = float(np.sqrt(mse))
        
        # Loss reduction compared to epoch 1
        initial_loss = loss_history[0]['total_loss'] if len(loss_history) > 0 else total_loss
        pct_drop = float(((initial_loss - total_loss) / initial_loss) * 100.0) if initial_loss > 0 else 0.0
        
        loss_history.append({
            'epoch': epoch,
            'mse': round(mse, 4),
            'rmse': round(rmse, 4),
            'frob_penalty': round(frob_penalty, 4),
            'total_loss': round(total_loss, 4),
            'pct_drop': round(pct_drop, 2)
        })
        
    # Reconstruct dense rating matrix R_hat = P * Q^T
    R_reconstructed = np.dot(P, Q.T)
    R_reconstructed_clipped = np.clip(R_reconstructed, 1.0, 5.0)
    
    return P, Q, loss_history, R_reconstructed_clipped


# ==============================================================================
# MATPLOTLIB VISUALIZATIONS GENERATOR
# ==============================================================================
def generate_visualizations(loss_history, P, Q, R_original, R_reconstructed, active_user_idx=7):
    """
    Generates 4 rich diagnostic plots for Matrix Factorization SGD:
    1. SGD Loss Convergence Curve (at least 3 epochs)
    2. 2D Item & User Latent Factor Embedding
    3. Sparse Input vs Reconstructed Full Matrix Heatmap
    4. Learned Latent Factor Matrices (P and Q^T)
    """
    plots = {}
    epochs_list = [entry['epoch'] for entry in loss_history]
    mse_list = [entry['mse'] for entry in loss_history]
    loss_list = [entry['total_loss'] for entry in loss_history]
    
    # --------------------------------------------------------------------------
    # PLOT 1: SGD Training Loss Convergence Curve
    # --------------------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(8.0, 4.2), dpi=120)
    ax1.plot(epochs_list, mse_list, color='#003366', marker='o', linewidth=2.4, label='Training MSE Loss')
    ax1.plot(epochs_list, loss_list, color='#b91c1c', marker='s', linestyle='--', linewidth=2.0, label='Total Regularized Loss (J)')
    
    # Highlight initial and final epochs
    ax1.scatter([epochs_list[0]], [mse_list[0]], color='#dc2626', s=100, zorder=5, label=f'Initial MSE ({mse_list[0]:.3f})')
    ax1.scatter([epochs_list[-1]], [mse_list[-1]], color='#16a34a', s=120, marker='*', zorder=5, label=f'Converged MSE ({mse_list[-1]:.3f})')
    
    # Annotate loss drop
    total_drop = ((loss_list[0] - loss_list[-1]) / loss_list[0]) * 100.0 if loss_list[0] > 0 else 0
    ax1.set_title(f'Stochastic Gradient Descent Loss Convergence ({len(epochs_list)} Epochs, Loss Drop: {total_drop:.1f}%)',
                  fontsize=12, fontweight='bold', color='#003366', pad=10)
    ax1.set_xlabel('Epoch Number (t)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Objective Loss', fontsize=10, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', fontsize=8.5)
    plt.tight_layout()
    
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', bbox_inches='tight')
    buf1.seek(0)
    plots['loss_curve'] = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)
    
    # --------------------------------------------------------------------------
    # PLOT 2: 2D Latent Factor Embedding Space (Factor 1 vs Factor 2)
    # --------------------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(8.5, 5.0), dpi=120)
    
    genre_colors = {
        'Sci-Fi': '#6366f1',
        'Action': '#dc2626',
        'Drama': '#16a34a',
        'Crime': '#854d0e',
        'Comedy': '#eab308',
        'Horror': '#9333ea',
        'Romance': '#ec4899',
        'Animation': '#06b6d4'
    }
    
    # Plot movies in latent space (using first 2 latent dimensions)
    for m_idx, movie in enumerate(MOVIES_DATASET):
        primary_genre = movie['genres'][0] if movie['genres'] else 'Drama'
        col = genre_colors.get(primary_genre, '#475569')
        ax2.scatter(Q[m_idx, 0], Q[m_idx, 1], color=col, edgecolors='black', s=90, alpha=0.85, zorder=3)
        ax2.annotate(movie['title'], (Q[m_idx, 0], Q[m_idx, 1]),
                     xytext=(5, 4), textcoords='offset points', fontsize=7.5, fontweight='bold', alpha=0.85)
        
    # Plot users in latent space
    for u_idx, user in enumerate(USERS):
        is_active = (u_idx == active_user_idx)
        user_col = '#b91c1c' if is_active else '#003366'
        marker = 'P' if is_active else '^'
        size = 140 if is_active else 80
        ax2.scatter(P[u_idx, 0], P[u_idx, 1], color=user_col, edgecolors='white', s=size, marker=marker, zorder=4)
        label_text = f"★ {user['name'].split(' ')[0]}" if is_active else user['name'].split(' ')[0]
        ax2.annotate(label_text, (P[u_idx, 0], P[u_idx, 1]),
                     xytext=(6, -8), textcoords='offset points', fontsize=8, color=user_col, fontweight='bold')
        
    ax2.set_title('Learned Latent Factor Space (Latent Dim 1 vs Dim 2)', fontsize=12, fontweight='bold', color='#003366', pad=10)
    ax2.set_xlabel('Latent Factor 1 (Genre/Tone Dimension)', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Latent Factor 2 (Style/Pacing Dimension)', fontsize=10, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    # Custom legend for genres
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c, markersize=8, label=g)
               for g, c in genre_colors.items()]
    handles.append(plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='#003366', markersize=8, label='Other Users'))
    handles.append(plt.Line2D([0], [0], marker='P', color='w', markerfacecolor='#b91c1c', markersize=9, label='Active User'))
    ax2.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.02, 1.0), fontsize=7.5)
    plt.tight_layout()
    
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', bbox_inches='tight')
    buf2.seek(0)
    plots['latent_space'] = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)
    
    # --------------------------------------------------------------------------
    # PLOT 3: Sparse Input Matrix R vs Completed Reconstructed Matrix R_hat
    # --------------------------------------------------------------------------
    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(11.0, 4.5), dpi=120)
    
    movie_short_titles = [m['initials'] for m in MOVIES_DATASET]
    user_short_names = [u['name'].split(' ')[0] for u in USERS]
    
    # Subplot 3a: Original Sparse Matrix
    masked_R = np.ma.masked_where(R_original == 0, R_original)
    cmap_orig = plt.cm.YlGnBu.copy()
    cmap_orig.set_bad(color='#cbd5e1')
    
    im1 = ax3a.imshow(masked_R, cmap=cmap_orig, vmin=1.0, vmax=5.0, aspect='auto')
    ax3a.set_title('1. Original Sparse Matrix R (Grey = Unknown/0)', fontsize=9.5, fontweight='bold', color='#003366')
    ax3a.set_xticks(range(len(movie_short_titles)))
    ax3a.set_xticklabels(movie_short_titles, rotation=90, fontsize=7.5)
    ax3a.set_yticks(range(len(user_short_names)))
    ax3a.set_yticklabels(user_short_names, fontsize=8)
    fig3.colorbar(im1, ax=ax3a, fraction=0.046, pad=0.04, label='Observed Rating (1-5★)')
    
    # Subplot 3b: Reconstructed Full Matrix
    im2 = ax3b.imshow(R_reconstructed, cmap='YlGnBu', vmin=1.0, vmax=5.0, aspect='auto')
    ax3b.set_title('2. SGD Completed Matrix R̂ = P × Qᵀ (All Filled)', fontsize=9.5, fontweight='bold', color='#003366')
    ax3b.set_xticks(range(len(movie_short_titles)))
    ax3b.set_xticklabels(movie_short_titles, rotation=90, fontsize=7.5)
    ax3b.set_yticks(range(len(user_short_names)))
    ax3b.set_yticklabels(user_short_names, fontsize=8)
    fig3.colorbar(im2, ax=ax3b, fraction=0.046, pad=0.04, label='Predicted Rating (1-5★)')
    
    plt.tight_layout()
    
    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png', bbox_inches='tight')
    buf3.seek(0)
    plots['matrix_heatmaps'] = base64.b64encode(buf3.getvalue()).decode('utf-8')
    plt.close(fig3)
    
    # --------------------------------------------------------------------------
    # PLOT 4: User Matrix P & Movie Matrix Q Heatmaps
    # --------------------------------------------------------------------------
    fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=120)
    
    # User Latent Matrix P (m x k)
    k_dim = P.shape[1]
    factor_labels = [f'F{f+1}' for f in range(k_dim)]
    
    im_p = ax4a.imshow(P, cmap='Blues', aspect='auto')
    ax4a.set_title(f'User Latent Factor Matrix P ({P.shape[0]} × {k_dim})', fontsize=10, fontweight='bold', color='#003366')
    ax4a.set_xticks(range(k_dim))
    ax4a.set_xticklabels(factor_labels, fontsize=8)
    ax4a.set_yticks(range(len(user_short_names)))
    ax4a.set_yticklabels(user_short_names, fontsize=8)
    fig4.colorbar(im_p, ax=ax4a, fraction=0.046, pad=0.04, label='Latent Factor Weight')
    
    # Movie Latent Matrix Q^T (k x n)
    im_q = ax4b.imshow(Q.T, cmap='Purples', aspect='auto')
    ax4b.set_title(f'Movie Latent Matrix Qᵀ ({k_dim} × {Q.shape[0]})', fontsize=10, fontweight='bold', color='#003366')
    ax4b.set_xticks(range(len(movie_short_titles)))
    ax4b.set_xticklabels(movie_short_titles, rotation=90, fontsize=7.5)
    ax4b.set_yticks(range(k_dim))
    ax4b.set_yticklabels(factor_labels, fontsize=8)
    fig4.colorbar(im_q, ax=ax4b, fraction=0.046, pad=0.04, label='Latent Factor Weight')
    
    plt.tight_layout()
    buf4 = io.BytesIO()
    plt.savefig(buf4, format='png', bbox_inches='tight')
    buf4.seek(0)
    plots['latent_weights'] = base64.b64encode(buf4.getvalue()).decode('utf-8')
    plt.close(fig4)
    
    return plots


# ==============================================================================
# FLASK APPLICATION ROUTES
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize session ratings matrix if not present
    if 'ratings' not in session:
        session['ratings'] = [row.copy() for row in DEFAULT_RATINGS]
        
    R_current = np.array(session['ratings'], dtype=float)
    
    # Retrieve hyperparameters from request or default
    active_user_idx = int(request.form.get('active_user_idx', 7))
    epochs = int(request.form.get('epochs', 15))
    k_factors = int(request.form.get('k_factors', 3))
    learning_rate = float(request.form.get('learning_rate', 0.02))
    reg_param = float(request.form.get('reg_param', 0.04))
    filter_genre = request.form.get('filter_genre', 'All')
    inspected_movie_id = int(request.form.get('inspected_movie_id', 0))
    action = request.form.get('action', 'train')
    
    # Ensure minimum 3 epochs constraint
    if epochs < 3:
        epochs = 3
        
    # Handle user rating submission or reset
    message = None
    if action == 'reset':
        session['ratings'] = [row.copy() for row in DEFAULT_RATINGS]
        R_current = np.array(session['ratings'], dtype=float)
        message = "Ratings matrix reset to default benchmark values."
    elif action == 'rate':
        try:
            m_id = int(request.form.get('movie_to_rate'))
            new_val = float(request.form.get('new_rating', 0.0))
            if 0 <= m_id < len(MOVIES_DATASET) and 0.0 <= new_val <= 5.0:
                current_list = session['ratings']
                current_list[active_user_idx][m_id] = new_val
                session['ratings'] = current_list
                R_current = np.array(current_list, dtype=float)
                inspected_movie_id = m_id
                action_text = f"rated {new_val}★" if new_val > 0 else "cleared to unrated (0)"
                message = f"Updated: {USERS[active_user_idx]['name']} {action_text} for '{MOVIES_DATASET[m_id]['title']}'."
        except (ValueError, TypeError):
            pass
            
    # Run Matrix Factorization via SGD from scratch
    P, Q, loss_history, R_reconstructed = train_matrix_factorization_sgd(
        R_current,
        k=k_factors,
        epochs=epochs,
        lr=learning_rate,
        reg=reg_param,
        seed=42
    )
    
    # Generate diagnostic visualization plots
    plots = generate_visualizations(loss_history, P, Q, R_current, R_reconstructed, active_user_idx)
    
    # Build Top Recommendations for Active User (Unrated movies with highest predicted rating)
    user_observed_ratings = R_current[active_user_idx]
    user_predicted_ratings = R_reconstructed[active_user_idx]
    
    recommendation_candidates = []
    for m_idx, movie in enumerate(MOVIES_DATASET):
        orig_rating = float(user_observed_ratings[m_idx])
        pred_rating = float(user_predicted_ratings[m_idx])
        
        # Recommendation reasoning based on latent dot product
        user_vector = P[active_user_idx]
        movie_vector = Q[m_idx]
        factor_contribs = user_vector * movie_vector
        dominant_factor = int(np.argmax(factor_contribs)) + 1
        
        reason = f"High affinity on Latent Factor #{dominant_factor} (contributes +{factor_contribs[dominant_factor-1]:.2f}★) aligning with your preference for {movie['genres'][0]}."
        
        rec_item = {
            'movie': movie,
            'orig_rating': orig_rating,
            'pred_rating': round(pred_rating, 2),
            'dominant_factor': dominant_factor,
            'reason': reason
        }
        
        if orig_rating == 0.0:
            recommendation_candidates.append(rec_item)
            
    recommendation_candidates.sort(key=lambda x: x['pred_rating'], reverse=True)
    top_recommendations = recommendation_candidates[:5]
    
    # Build Movie Catalog with active user's ratings & predictions
    enriched_catalog = []
    for m_idx, movie in enumerate(MOVIES_DATASET):
        orig = float(user_observed_ratings[m_idx])
        pred = float(user_predicted_ratings[m_idx])
        
        # Filter check
        matches_genre = (filter_genre == 'All' or filter_genre in movie['genres'])
        
        enriched_catalog.append({
            'movie': movie,
            'orig_rating': orig,
            'pred_rating': round(pred, 2),
            'is_rated': (orig > 0.0),
            'matches_genre': matches_genre
        })
        
    # Inspected Movie details & mathematical breakdown
    inspected_movie = MOVIES_DATASET[inspected_movie_id]
    u_vec = P[active_user_idx]
    m_vec = Q[inspected_movie_id]
    latent_terms = []
    for f_idx in range(k_factors):
        p_val = round(float(u_vec[f_idx]), 3)
        q_val = round(float(m_vec[f_idx]), 3)
        prod = round(p_val * q_val, 3)
        latent_terms.append({'factor': f_idx + 1, 'p': p_val, 'q': q_val, 'prod': prod})
        
    inspected_dot_prod = round(float(np.dot(u_vec, m_vec)), 3)
    inspected_clipped = round(float(np.clip(inspected_dot_prod, 1.0, 5.0)), 2)
    inspected_orig = float(user_observed_ratings[inspected_movie_id])
    
    # Build Matrix Table Data (Users x Movies)
    matrix_table = []
    for u_idx, user in enumerate(USERS):
        row_entries = []
        for m_idx, movie in enumerate(MOVIES_DATASET):
            val_orig = float(R_current[u_idx, m_idx])
            val_pred = round(float(R_reconstructed[u_idx, m_idx]), 2)
            row_entries.append({
                'movie_id': m_idx,
                'orig': val_orig,
                'pred': val_pred,
                'is_known': (val_orig > 0.0)
            })
        matrix_table.append({
            'user': user,
            'is_active': (u_idx == active_user_idx),
            'entries': row_entries
        })
        
    # Dataset and training summary stats
    num_total_cells = R_current.size
    num_known_cells = int(np.count_nonzero(R_current))
    sparsity_pct = round((1.0 - (num_known_cells / num_total_cells)) * 100.0, 1)
    
    summary_stats = {
        'total_movies': len(MOVIES_DATASET),
        'total_users': len(USERS),
        'total_ratings': num_known_cells,
        'sparsity_pct': sparsity_pct,
        'epochs': epochs,
        'k_factors': k_factors,
        'learning_rate': learning_rate,
        'reg_param': reg_param,
        'initial_mse': loss_history[0]['mse'],
        'final_mse': loss_history[-1]['mse'],
        'initial_loss': loss_history[0]['total_loss'],
        'final_loss': loss_history[-1]['total_loss'],
        'loss_reduction': round(((loss_history[0]['total_loss'] - loss_history[-1]['total_loss']) / loss_history[0]['total_loss']) * 100.0, 1)
    }
    
    # Available genres list for filtering
    all_genres = ['All', 'Action', 'Sci-Fi', 'Drama', 'Crime', 'Comedy', 'Horror', 'Romance', 'Animation']
    
    return render_template(
        'index.html',
        movies=MOVIES_DATASET,
        users=USERS,
        active_user_idx=active_user_idx,
        active_user=USERS[active_user_idx],
        epochs=epochs,
        k_factors=k_factors,
        learning_rate=learning_rate,
        reg_param=reg_param,
        filter_genre=filter_genre,
        all_genres=all_genres,
        enriched_catalog=enriched_catalog,
        top_recommendations=top_recommendations,
        inspected_movie=inspected_movie,
        inspected_orig=inspected_orig,
        inspected_terms=latent_terms,
        inspected_dot_prod=inspected_dot_prod,
        inspected_clipped=inspected_clipped,
        matrix_table=matrix_table,
        loss_history=loss_history,
        summary_stats=summary_stats,
        plots=plots,
        message=message
    )


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5021))
    print(f"=================================================================")
    print(f"🎓 PARS Lab - Experiment 21: Matrix Factorization via SGD")
    print(f"   Student: Monis (Roll No.: 2023UIT3027) | Port: {port}")
    print(f"   Server running at: http://127.0.0.1:{port}")
    print(f"=================================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
