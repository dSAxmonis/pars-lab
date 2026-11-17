import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

# ==============================================================================
# 1. MOVIES DATASET DEFINITION (20 benchmark films across diverse genres)
# ==============================================================================
MOVIES = [
    {
        'id': 0, 'title': 'Inception', 'year': 2010,
        'genres': ['Sci-Fi', 'Action', 'Thriller'],
        'director': 'Christopher Nolan',
        'cast': 'Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page',
        'imdb_rating': 8.8,
        'synopsis': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.',
        'keywords': 'Dream heist, Subconscious, Reality layers, Nolan',
        'initials': 'INC', 'color': '#1e3a8a', 'emoji': '🌀'
    },
    {
        'id': 1, 'title': 'The Dark Knight', 'year': 2008,
        'genres': ['Action', 'Crime', 'Drama'],
        'director': 'Christopher Nolan',
        'cast': 'Christian Bale, Heath Ledger, Aaron Eckhart',
        'imdb_rating': 9.0,
        'synopsis': 'When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests.',
        'keywords': 'Gotham vigilante, Joker, Chaos, Moral dilemma',
        'initials': 'TDK', 'color': '#0f172a', 'emoji': '🦇'
    },
    {
        'id': 2, 'title': 'Interstellar', 'year': 2014,
        'genres': ['Sci-Fi', 'Drama', 'Adventure'],
        'director': 'Christopher Nolan',
        'cast': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain',
        'imdb_rating': 8.7,
        'synopsis': "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival as Earth faces catastrophic blight.",
        'keywords': 'Wormhole, Black hole, Time dilation, Father-daughter bond',
        'initials': 'INT', 'color': '#172554', 'emoji': '🚀'
    },
    {
        'id': 3, 'title': 'The Matrix', 'year': 1999,
        'genres': ['Sci-Fi', 'Action'],
        'director': 'Lana & Lilly Wachowski',
        'cast': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
        'imdb_rating': 8.7,
        'synopsis': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
        'keywords': 'Cyberpunk, Simulated reality, Red pill, AI rebellion',
        'initials': 'MTX', 'color': '#064e3b', 'emoji': '🕶️'
    },
    {
        'id': 4, 'title': 'Pulp Fiction', 'year': 1994,
        'genres': ['Crime', 'Drama'],
        'director': 'Quentin Tarantino',
        'cast': 'John Travolta, Samuel L. Jackson, Uma Thurman',
        'imdb_rating': 8.9,
        'synopsis': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
        'keywords': 'Nonlinear narrative, Hitmen, Diner heist, Cult classic',
        'initials': 'PLF', 'color': '#7c2d12', 'emoji': '💼'
    },
    {
        'id': 5, 'title': 'The Godfather', 'year': 1972,
        'genres': ['Crime', 'Drama'],
        'director': 'Francis Ford Coppola',
        'cast': 'Marlon Brando, Al Pacino, James Caan',
        'imdb_rating': 9.2,
        'synopsis': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant youngest son.',
        'keywords': 'Mafia family, Power succession, Corleone, Italian mob',
        'initials': 'GDF', 'color': '#451a03', 'emoji': '🌹'
    },
    {
        'id': 6, 'title': 'Forrest Gump', 'year': 1994,
        'genres': ['Drama', 'Romance'],
        'director': 'Robert Zemeckis',
        'cast': 'Tom Hanks, Robin Wright, Gary Sinise',
        'imdb_rating': 8.8,
        'synopsis': 'The history of the United States from the 1950s to the 1970s unfolds from the perspective of an Alabama man with an IQ of 75.',
        'keywords': 'Heartwarming, Life journey, Historical events, Box of chocolates',
        'initials': 'FGP', 'color': '#14532d', 'emoji': '🍫'
    },
    {
        'id': 7, 'title': 'Titanic', 'year': 1997,
        'genres': ['Romance', 'Drama'],
        'director': 'James Cameron',
        'cast': 'Leonardo DiCaprio, Kate Winslet, Billy Zane',
        'imdb_rating': 7.9,
        'synopsis': 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.',
        'keywords': 'Shipwreck disaster, Star-crossed lovers, Ocean luxury',
        'initials': 'TTN', 'color': '#155e75', 'emoji': '🚢'
    },
    {
        'id': 8, 'title': 'La La Land', 'year': 2016,
        'genres': ['Romance', 'Comedy', 'Drama'],
        'director': 'Damien Chazelle',
        'cast': 'Ryan Gosling, Emma Stone, John Legend',
        'imdb_rating': 8.0,
        'synopsis': 'While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations.',
        'keywords': 'Jazz musician, Hollywood dreamers, Bittersweet love',
        'initials': 'LLL', 'color': '#831843', 'emoji': '🎷'
    },
    {
        'id': 9, 'title': 'The Hangover', 'year': 2009,
        'genres': ['Comedy'],
        'director': 'Todd Phillips',
        'cast': 'Bradley Cooper, Ed Helms, Zach Galifianakis',
        'imdb_rating': 7.7,
        'synopsis': 'Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing.',
        'keywords': 'Las Vegas bachelor party, Missing groom, Wild morning',
        'initials': 'HNG', 'color': '#b45309', 'emoji': '🎰'
    },
    {
        'id': 10, 'title': 'Superbad', 'year': 2007,
        'genres': ['Comedy'],
        'director': 'Greg Mottola',
        'cast': 'Jonah Hill, Michael Cera, Christopher Mintz-Plasse',
        'imdb_rating': 7.6,
        'synopsis': 'Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.',
        'keywords': 'High school friends, McLovin, Wild party adventure',
        'initials': 'SBD', 'color': '#a16207', 'emoji': '🍻'
    },
    {
        'id': 11, 'title': 'Parasite', 'year': 2019,
        'genres': ['Thriller', 'Drama'],
        'director': 'Bong Joon-ho',
        'cast': 'Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong',
        'imdb_rating': 8.5,
        'synopsis': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
        'keywords': 'Class divide, South Korea, Social satire, Shocking twists',
        'initials': 'PAR', 'color': '#27272a', 'emoji': '🏠'
    },
    {
        'id': 12, 'title': 'The Silence of the Lambs', 'year': 1991,
        'genres': ['Thriller', 'Horror', 'Crime'],
        'director': 'Jonathan Demme',
        'cast': 'Jodie Foster, Anthony Hopkins, Scott Glenn',
        'imdb_rating': 8.6,
        'synopsis': 'A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.',
        'keywords': 'Hannibal Lecter, Psychological interrogation, FBI profiler',
        'initials': 'SOL', 'color': '#4c0519', 'emoji': '🦋'
    },
    {
        'id': 13, 'title': 'The Shining', 'year': 1980,
        'genres': ['Horror', 'Drama'],
        'director': 'Stanley Kubrick',
        'cast': 'Jack Nicholson, Shelley Duvall, Danny Lloyd',
        'imdb_rating': 8.4,
        'synopsis': 'A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrors.',
        'keywords': 'Overlook Hotel, Cabin fever madness, Redrum, Kubrick',
        'initials': 'SHN', 'color': '#581c87', 'emoji': '🪓'
    },
    {
        'id': 14, 'title': 'A Quiet Place', 'year': 2018,
        'genres': ['Horror', 'Sci-Fi', 'Drama'],
        'director': 'John Krasinski',
        'cast': 'Emily Blunt, John Krasinski, Millicent Simmonds',
        'imdb_rating': 7.5,
        'synopsis': 'In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing.',
        'keywords': 'Acoustic monsters, Silent survival, Family resilience',
        'initials': 'AQP', 'color': '#312e81', 'emoji': '🤫'
    },
    {
        'id': 15, 'title': 'Avengers: Endgame', 'year': 2019,
        'genres': ['Action', 'Sci-Fi', 'Adventure'],
        'director': 'Anthony & Joe Russo',
        'cast': 'Robert Downey Jr., Chris Evans, Mark Ruffalo',
        'imdb_rating': 8.4,
        'synopsis': 'After the devastating events of Infinity War, the remaining Avengers assemble once more in order to reverse Thanos actions and restore balance.',
        'keywords': 'Infinity stones, Time heist, Superhero climax, Marvel',
        'initials': 'AVG', 'color': '#701a75', 'emoji': '🛡️'
    },
    {
        'id': 16, 'title': 'Gladiator', 'year': 2000,
        'genres': ['Action', 'Drama', 'Adventure'],
        'director': 'Ridley Scott',
        'cast': 'Russell Crowe, Joaquin Phoenix, Connie Nielsen',
        'imdb_rating': 8.5,
        'synopsis': 'A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.',
        'keywords': 'Roman Colosseum, Betrayed general, Honor, Arena swordplay',
        'initials': 'GLD', 'color': '#78350f', 'emoji': '⚔️'
    },
    {
        'id': 17, 'title': 'The Grand Budapest Hotel', 'year': 2014,
        'genres': ['Comedy', 'Drama', 'Adventure'],
        'director': 'Wes Anderson',
        'cast': 'Ralph Fiennes, Tony Revolori, Willem Dafoe',
        'imdb_rating': 8.1,
        'synopsis': 'A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy under an exceptional concierge.',
        'keywords': 'Whimsical aesthetic, Stolen painting, Concierge, Pastel',
        'initials': 'GBH', 'color': '#9d174d', 'emoji': '🏨'
    },
    {
        'id': 18, 'title': 'Fight Club', 'year': 1999,
        'genres': ['Drama', 'Thriller'],
        'director': 'David Fincher',
        'cast': 'Brad Pitt, Edward Norton, Helena Bonham Carter',
        'imdb_rating': 8.8,
        'synopsis': 'An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.',
        'keywords': 'Tyler Durden, Anti-consumerism, Alter ego, Fincher cult',
        'initials': 'FCL', 'color': '#1e293b', 'emoji': '🧼'
    },
    {
        'id': 19, 'title': 'Goodfellas', 'year': 1990,
        'genres': ['Crime', 'Drama', 'Biography'],
        'director': 'Martin Scorsese',
        'cast': 'Robert De Niro, Ray Liotta, Joe Pesci',
        'imdb_rating': 8.7,
        'synopsis': 'The story of Henry Hill and his life in the mafia, covering his relationship with his wife Karen and his mob partners Jimmy Conway and Tommy DeVito.',
        'keywords': 'Mob life, Scorsese, Lufthansa heist, Brooklyn mafia',
        'initials': 'GFL', 'color': '#581c87', 'emoji': '🔫'
    }
]

# ==============================================================================
# 2. USER PERSONAS AND HARDCODED RATINGS MATRIX (8 Users x 20 Movies)
# ==============================================================================
USERS = [
    {'id': 0, 'name': 'Alice', 'role': 'Sci-Fi Critic', 'description': 'Strict rater; loves high-concept sci-fi and cerebral thrillers, rates romances/comedies harshly.'},
    {'id': 1, 'name': 'Bob', 'role': 'Action Buff', 'description': 'Generous enthusiast; awards high marks to superhero blockbusters, epics, and gritty thrillers.'},
    {'id': 2, 'name': 'Charlie', 'role': 'Crime Cinephile', 'description': 'Discerning connoisseur; adores classic mafia epics, noir mysteries, and auteur dramas.'},
    {'id': 3, 'name': 'Diana', 'role': 'Romance & Comedy Fan', 'description': 'Warm-hearted rater; loves musicals, heartwarming dramas, and lighthearted comedy adventures.'},
    {'id': 4, 'name': 'Evan', 'role': 'Horror & Suspense Seeker', 'description': 'High-intensity enthusiast; prioritizes psychological chills, supernatural terror, and plot twists.'},
    {'id': 5, 'name': 'Fiona', 'role': 'Blockbuster Explorer', 'description': 'Casual mainstream rater; rates visually spectacular sci-fi and action epics very positively.'},
    {'id': 6, 'name': 'George', 'role': 'Arthouse Critic', 'description': 'Stern academic evaluator; high standards, prizes Wes Anderson, Tarantino, and Bong Joon-ho.'},
    {'id': 7, 'name': 'Hannah', 'role': 'Target Active User', 'description': 'Our active subject who has watched 5 movies (likes Sci-Fi/Action, dislikes Romances/Comedies).'}
]

# Rows = Users (0..7), Columns = Movies (0..19), 0 represents unrated
BASE_RATINGS_MATRIX = np.array([
    # INC TDK INT MTX PLF GDF FGP TTN LLL HNG SBD PAR SOL SHN AQP AVG GLD GBH FCL GFL
    [  5,  4,  5,  5,  0,  3,  2,  1,  2,  1,  0,  4,  0,  3,  4,  4,  3,  0,  4,  0 ], # 0: Alice (Mean ~ 3.33)
    [  4,  5,  4,  4,  4,  4,  3,  2,  0,  4,  4,  0,  4,  0,  3,  5,  5,  0,  5,  4 ], # 1: Bob (Mean ~ 4.00)
    [  3,  4,  0,  3,  5,  5,  4,  3,  0,  2,  2,  5,  5,  4,  0,  2,  4,  4,  5,  5 ], # 2: Charlie (Mean ~ 3.82)
    [  2,  2,  3,  1,  2,  3,  5,  5,  5,  4,  4,  3,  1,  1,  1,  3,  2,  5,  2,  2 ], # 3: Diana (Mean ~ 2.80)
    [  4,  4,  3,  3,  4,  4,  1,  1,  1,  2,  2,  5,  5,  5,  5,  2,  3,  3,  5,  4 ], # 4: Evan (Mean ~ 3.30)
    [  5,  5,  5,  4,  3,  0,  4,  4,  4,  3,  3,  0,  2,  2,  3,  5,  4,  0,  4,  3 ], # 5: Fiona (Mean ~ 3.71)
    [  3,  3,  3,  4,  5,  5,  2,  1,  3,  1,  2,  5,  4,  5,  3,  1,  2,  5,  4,  5 ], # 6: George (Mean ~ 3.30)
    [  5,  5,  0,  4,  0,  0,  0,  2,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ]  # 7: Hannah (Default Target)
], dtype=float)

# ==============================================================================
# 3. CORE RECOMMENDER ALGORITHMS (IMPLEMENTED FROM SCRATCH USING NUMPY)
# ==============================================================================

def compute_user_means(R):
    """
    Computes mean rating \bar{R}_u for each user across their rated items (> 0).
    """
    n_users = R.shape[0]
    user_means = np.zeros(n_users)
    for u in range(n_users):
        rated_idx = R[u] > 0
        if np.any(rated_idx):
            user_means[u] = np.mean(R[u, rated_idx])
        else:
            user_means[u] = 3.0
    return user_means


def compute_adjusted_cosine_matrix(R, user_means):
    """
    Computes Item-Item Adjusted Cosine Similarity Matrix:
    sim_adj(i, j) = sum_{u in U_ij} (R_ui - \bar{R}_u)(R_uj - \bar{R}_u) /
                    [ sqrt(sum_{u in U_ij} (R_ui - \bar{R}_u)^2) * sqrt(sum_{u in U_ij} (R_uj - \bar{R}_u)^2) ]
    """
    n_items = R.shape[1]
    adj_sim = np.zeros((n_items, n_items))

    for i in range(n_items):
        for j in range(n_items):
            if i == j:
                adj_sim[i, j] = 1.0
                continue
            
            # Find co-raters who rated both item i and item j
            co_raters = np.where((R[:, i] > 0) & (R[:, j] > 0))[0]
            if len(co_raters) < 2:
                adj_sim[i, j] = 0.0
                continue
            
            r_ui = R[co_raters, i]
            r_uj = R[co_raters, j]
            u_m = user_means[co_raters]
            
            dev_i = r_ui - u_m
            dev_j = r_uj - u_m
            
            num = np.sum(dev_i * dev_j)
            den = np.sqrt(np.sum(dev_i**2)) * np.sqrt(np.sum(dev_j**2))
            
            if den > 1e-9:
                adj_sim[i, j] = float(num / den)
            else:
                adj_sim[i, j] = 0.0
                
    return adj_sim


def compute_raw_cosine_matrix(R):
    """
    Computes Standard (Raw) Cosine Similarity Matrix without user-mean subtraction:
    sim_raw(i, j) = sum_{u in U_ij} R_ui * R_uj /
                    [ sqrt(sum_{u in U_ij} R_ui^2) * sqrt(sum_{u in U_ij} R_uj^2) ]
    """
    n_items = R.shape[1]
    raw_sim = np.zeros((n_items, n_items))

    for i in range(n_items):
        for j in range(n_items):
            if i == j:
                raw_sim[i, j] = 1.0
                continue
            
            co_raters = np.where((R[:, i] > 0) & (R[:, j] > 0))[0]
            if len(co_raters) < 2:
                raw_sim[i, j] = 0.0
                continue
            
            r_ui = R[co_raters, i]
            r_uj = R[co_raters, j]
            
            num = np.sum(r_ui * r_uj)
            den = np.sqrt(np.sum(r_ui**2)) * np.sqrt(np.sum(r_uj**2))
            
            if den > 1e-9:
                raw_sim[i, j] = float(num / den)
            else:
                raw_sim[i, j] = 0.0
                
    return raw_sim


def predict_item_knn(active_ratings, adj_sim, k=3, user_mean=3.5):
    r"""
    Predicts ratings for all unrated items for the active user using Item-Based kNN.
    Weighted average formula:
    \hat{R}_i = sum_{j in N_k(i)} sim_adj(i, j) * R_j / sum_{j in N_k(i)} sim_adj(i, j)
    (considering only positive similarity neighbors sim_adj > 0).
    """
    rated_items = np.where(active_ratings > 0)[0]
    unrated_items = np.where(active_ratings == 0)[0]
    
    predictions = []
    
    for item in unrated_items:
        # Candidate neighbors are items the user has rated that have positive adjusted cosine similarity
        candidate_neighbors = []
        for r_item in rated_items:
            sim = adj_sim[item, r_item]
            if sim > 0.0:
                candidate_neighbors.append((r_item, sim, active_ratings[r_item]))
                
        # Sort candidates descending by similarity
        candidate_neighbors.sort(key=lambda x: x[1], reverse=True)
        top_k = candidate_neighbors[:k]
        
        sim_sum = sum(s for _, s, _ in top_k)
        
        if len(top_k) > 0 and sim_sum > 1e-9:
            num = sum(s * r for _, s, r in top_k)
            pred_rating = num / sim_sum
            
            # Also calculate deviation from mean prediction:
            dev_pred = user_mean + (sum(s * (r - user_mean) for _, s, r in top_k) / sim_sum)
        else:
            # Fallback to user mean if no positive neighbors exist
            pred_rating = user_mean
            dev_pred = user_mean
            top_k = []
            
        # Clamp rating to [1.0, 5.0]
        clamped_rating = min(5.0, max(1.0, pred_rating))
        
        # Prepare neighbor details for explanation
        neighbor_details = []
        for n_id, s, r in top_k:
            neighbor_details.append({
                'id': int(n_id),
                'title': MOVIES[n_id]['title'],
                'similarity': round(float(s), 3),
                'user_rating': float(r),
                'contribution': round(float(s * r), 3)
            })
            
        predictions.append({
            'item_id': int(item),
            'movie': MOVIES[item],
            'predicted_rating': round(float(clamped_rating), 2),
            'raw_pred': round(float(pred_rating), 3),
            'dev_pred': round(float(dev_pred), 2),
            'neighbors': neighbor_details,
            'k_used': len(top_k),
            'sim_sum': round(float(sim_sum), 3)
        })
        
    # Sort predictions descending by predicted rating
    predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
    return predictions


# ==============================================================================
# 4. MATPLOTLIB VISUALIZATION GENERATORS
# ==============================================================================

def generate_visualization_plots(R, adj_sim, raw_sim, active_user_idx, predictions, user_means, target_movie_id=0):
    """
    Renders 4 analytical plots demonstrating recommender system internals:
    1. Adjusted Cosine Similarity Heatmap (20x20)
    2. Raw vs Adjusted Cosine Distribution & Focal Movie Comparison
    3. Top-N Predicted Ratings for Active User
    4. User Rating Mean Disparities & Scaling Biases
    """
    initials = [m['initials'] for m in MOVIES]
    n_items = len(MOVIES)
    
    # --------------------------------------------------------------------------
    # PLOT 1: Adjusted Cosine Similarity Matrix Heatmap
    # --------------------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(10.5, 7.5), dpi=130)
    im1 = ax1.imshow(adj_sim, cmap='coolwarm', vmin=-1.0, vmax=1.0)
    
    ax1.set_xticks(np.arange(n_items))
    ax1.set_yticks(np.arange(n_items))
    ax1.set_xticklabels(initials, fontsize=8.5, rotation=45, ha='right')
    ax1.set_yticklabels(initials, fontsize=8.5)
    
    ax1.set_title("Item-Item Adjusted Cosine Similarity Matrix ($sim_{adj}$)\nRange: [-1.0 (Opposite Taste) to +1.0 (Identical Taste)]",
                  fontsize=12, fontweight='bold', pad=12, color='#003366')
    ax1.set_xlabel("Item $j$ (Movie Initials)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Item $i$ (Movie Initials)", fontsize=10, fontweight='bold')
    
    # Add colorbar
    cbar1 = fig1.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label("Adjusted Cosine Similarity", fontsize=9, fontweight='bold')
    
    fig1.tight_layout()
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='png', bbox_inches='tight')
    buf1.seek(0)
    plot1_b64 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)

    # --------------------------------------------------------------------------
    # PLOT 2: Raw Cosine vs Adjusted Cosine Analysis (Dual Subplots)
    # --------------------------------------------------------------------------
    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(11.5, 5.0), dpi=130)
    
    # Extract unique off-diagonal pairs
    triu_idx = np.triu_indices(n_items, k=1)
    raw_vals = raw_sim[triu_idx]
    adj_vals = adj_sim[triu_idx]
    
    # Left subplot: Histograms of similarity values
    bins = np.linspace(-1.0, 1.0, 25)
    ax2a.hist(raw_vals, bins=bins, color='#d97706', alpha=0.7, edgecolor='black', label=f'Raw Cosine (Mean = {np.mean(raw_vals):.2f})')
    ax2a.hist(adj_vals, bins=bins, color='#0284c7', alpha=0.7, edgecolor='black', label=f'Adjusted Cosine (Mean = {np.mean(adj_vals):.2f})')
    ax2a.axvline(0, color='gray', linestyle='--', linewidth=1)
    ax2a.set_title("Distribution of All Item-Pair Similarities\n(Raw Cosine Heavily Shifted Positive)", fontsize=10, fontweight='bold', color='#003366')
    ax2a.set_xlabel("Similarity Value", fontsize=9, fontweight='bold')
    ax2a.set_ylabel("Frequency (Item Pairs)", fontsize=9, fontweight='bold')
    ax2a.grid(True, linestyle=':', alpha=0.6)
    ax2a.legend(loc='upper left', fontsize=8.5)
    
    # Right subplot: Focal movie comparison (e.g., Inception vs contrasting genres)
    focal_idx = target_movie_id
    contrast_ids = [2, 3, 1, 15, 7, 8, 9, 10]  # Interstellar, Matrix, Dark Knight, Avengers vs Titanic, La La Land, Hangover, Superbad
    contrast_titles = [MOVIES[cid]['initials'] for cid in contrast_ids]
    
    raw_focal = [raw_sim[focal_idx, cid] for cid in contrast_ids]
    adj_focal = [adj_sim[focal_idx, cid] for cid in contrast_ids]
    
    x = np.arange(len(contrast_ids))
    width = 0.35
    
    ax2b.bar(x - width/2, raw_focal, width, label='Raw Cosine', color='#f59e0b', edgecolor='black')
    ax2b.bar(x + width/2, adj_focal, width, label='Adjusted Cosine', color='#0284c7', edgecolor='black')
    ax2b.axhline(0, color='black', linewidth=0.8)
    ax2b.set_xticks(x)
    ax2b.set_xticklabels(contrast_titles, fontsize=8.5)
    ax2b.set_title(f"Focal Movie: {MOVIES[focal_idx]['title']} ({MOVIES[focal_idx]['initials']})\nRaw vs Adjusted Cosine against Contrasting Films",
                   fontsize=10, fontweight='bold', color='#003366')
    ax2b.set_xlabel("Comparison Movies", fontsize=9, fontweight='bold')
    ax2b.set_ylabel("Similarity with Focal Movie", fontsize=9, fontweight='bold')
    ax2b.grid(True, linestyle=':', alpha=0.6)
    ax2b.legend(loc='lower left', fontsize=8.5)
    
    fig2.tight_layout()
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png', bbox_inches='tight')
    buf2.seek(0)
    plot2_b64 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)

    # --------------------------------------------------------------------------
    # PLOT 3: Top Recommended Movie Predictions for Active User
    # --------------------------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(10.5, 4.5), dpi=130)
    
    if len(predictions) > 0:
        top_preds = predictions[:8]  # Show top 8
        pred_titles = [p['movie']['title'] for p in top_preds]
        pred_scores = [p['predicted_rating'] for p in top_preds]
        
        # Color bars by rating score
        bar_colors = ['#15803d' if s >= 4.5 else '#16a34a' if s >= 4.0 else '#0284c7' if s >= 3.5 else '#d97706' for s in pred_scores]
        
        y_pos = np.arange(len(top_preds))
        bars = ax3.barh(y_pos, pred_scores, color=bar_colors, edgecolor='black', height=0.6)
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(pred_titles, fontsize=9, fontweight='bold')
        ax3.invert_yaxis()  # Highest rating on top
        ax3.set_xlim(0, 5.5)
        ax3.set_xlabel("Predicted Rating (Scale: 1.0 to 5.0 Stars)", fontsize=9, fontweight='bold')
        ax3.set_title(f"Top Recommended Movies for {USERS[active_user_idx]['name']} (Item-Based kNN with Adjusted Cosine)",
                      fontsize=11, fontweight='bold', color='#003366')
        ax3.grid(True, linestyle=':', alpha=0.6, axis='x')
        
        # Add score labels on bars
        for bar in bars:
            width = bar.get_width()
            ax3.text(width + 0.08, bar.get_y() + bar.get_height()/2, f"{width:.2f} ★",
                     va='center', ha='left', fontsize=8.5, fontweight='bold', color='#111827')
    else:
        ax3.text(0.5, 0.5, "All movies already rated by user!", ha='center', va='center', fontsize=12)
        
    fig3.tight_layout()
    buf3 = io.BytesIO()
    fig3.savefig(buf3, format='png', bbox_inches='tight')
    buf3.seek(0)
    plot3_b64 = base64.b64encode(buf3.getvalue()).decode('utf-8')
    plt.close(fig3)

    # --------------------------------------------------------------------------
    # PLOT 4: User Rating Tendencies & Bias Offsets
    # --------------------------------------------------------------------------
    fig4, ax4 = plt.subplots(figsize=(10.5, 3.8), dpi=130)
    user_labels = [f"{u['name']}" for u in USERS]
    u_colors = ['#1e40af' if i != active_user_idx else '#b91c1c' for i in range(len(USERS))]
    
    bars4 = ax4.bar(user_labels, user_means, color=u_colors, edgecolor='black', width=0.55)
    global_mean = np.mean([m for m in user_means if m > 0])
    ax4.axhline(global_mean, color='#dc2626', linestyle='--', linewidth=1.5, label=f'Global Dataset Average ({global_mean:.2f})')
    
    ax4.set_ylim(0, 5.2)
    ax4.set_ylabel(r"Mean Rating ($\bar{R}_u$)", fontsize=9, fontweight='bold')
    ax4.set_title(r"User Rating Tendencies & Subjective Baseline Offsets ($\bar{R}_u$)" + "\n(Red Bar = Current Active User)",
                  fontsize=11, fontweight='bold', color='#003366')
    ax4.grid(True, linestyle=':', alpha=0.6, axis='y')
    ax4.legend(loc='lower right', fontsize=8.5)
    
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"{height:.2f}",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold')
                 
    fig4.tight_layout()
    buf4 = io.BytesIO()
    fig4.savefig(buf4, format='png', bbox_inches='tight')
    buf4.seek(0)
    plot4_b64 = base64.b64encode(buf4.getvalue()).decode('utf-8')
    plt.close(fig4)

    return plot1_b64, plot2_b64, plot3_b64, plot4_b64


# ==============================================================================
# 5. FLASK ROUTES AND CONTROLLER LOGIC
# ==============================================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    # Load base ratings matrix clone
    R = BASE_RATINGS_MATRIX.copy()
    
    # Determine active user index and parameters
    try:
        active_user_idx = int(request.form.get('user_id', 7))
        if active_user_idx < 0 or active_user_idx >= len(USERS):
            active_user_idx = 7
    except (ValueError, TypeError):
        active_user_idx = 7
        
    try:
        k_neighbors = int(request.form.get('k_neighbors', 3))
        if k_neighbors < 1:
            k_neighbors = 1
        elif k_neighbors > 8:
            k_neighbors = 8
    except (ValueError, TypeError):
        k_neighbors = 3

    try:
        target_movie_id = int(request.form.get('target_movie_id', 0))
        if target_movie_id < 0 or target_movie_id >= len(MOVIES):
            target_movie_id = 0
    except (ValueError, TypeError):
        target_movie_id = 0

    # Handle custom rating overrides from movie cards
    if request.method == 'POST' and 'update_ratings' in request.form:
        for m in MOVIES:
            field_name = f"rating_{m['id']}"
            if field_name in request.form:
                try:
                    val = float(request.form.get(field_name, 0))
                    if 0 <= val <= 5:
                        R[active_user_idx, m['id']] = val
                except (ValueError, TypeError):
                    pass

    # Quick action presets
    action = request.form.get('action', '')
    if action == 'preset_hannah':
        active_user_idx = 7
        R[7] = np.array([5, 5, 0, 4, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
    elif action == 'preset_diana':
        active_user_idx = 3
    elif action == 'preset_alice':
        active_user_idx = 0
    elif action == 'clear_ratings':
        R[active_user_idx] = np.zeros(len(MOVIES), dtype=float)

    # Compute Recommender Metrics
    user_means = compute_user_means(R)
    adj_sim = compute_adjusted_cosine_matrix(R, user_means)
    raw_sim = compute_raw_cosine_matrix(R)
    
    active_ratings = R[active_user_idx]
    active_user_mean = user_means[active_user_idx]
    
    # Predict ratings for unrated movies
    predictions = predict_item_knn(active_ratings, adj_sim, k=k_neighbors, user_mean=active_user_mean)
    
    # Generate Matplotlib plots
    plot1_b64, plot2_b64, plot3_b64, plot4_b64 = generate_visualization_plots(
        R, adj_sim, raw_sim, active_user_idx, predictions, user_means, target_movie_id=target_movie_id
    )
    
    # Build detailed calculation breakdown for #1 top recommended movie
    top_recommendation_calc = None
    if len(predictions) > 0 and len(predictions[0]['neighbors']) > 0:
        top_rec = predictions[0]
        n_list = top_rec['neighbors']
        numerator_terms = [f"({n['similarity']} \u00d7 {n['user_rating']})" for n in n_list]
        num_str = " + ".join(numerator_terms)
        num_val = sum(n['similarity'] * n['user_rating'] for n in n_list)
        
        denominator_terms = [f"{n['similarity']}" for n in n_list]
        den_str = " + ".join(denominator_terms)
        den_val = sum(n['similarity'] for n in n_list)
        
        top_recommendation_calc = {
            'target_movie': top_rec['movie']['title'],
            'target_id': top_rec['item_id'],
            'k': len(n_list),
            'numerator_expr': num_str,
            'numerator_val': round(num_val, 4),
            'denominator_expr': den_str,
            'denominator_val': round(den_val, 4),
            'computed_rating': top_rec['predicted_rating'],
            'neighbors': n_list
        }

    # Prepare catalog items enriched with active user rating
    catalog_movies = []
    for m in MOVIES:
        m_copy = dict(m)
        m_copy['active_rating'] = int(active_ratings[m['id']])
        catalog_movies.append(m_copy)

    # Pairwise comparison table between focal movie and other key movies
    focal_comparisons = []
    for other_id in range(len(MOVIES)):
        if other_id != target_movie_id:
            focal_comparisons.append({
                'id': other_id,
                'title': MOVIES[other_id]['title'],
                'genres': ", ".join(MOVIES[other_id]['genres']),
                'raw_sim': round(float(raw_sim[target_movie_id, other_id]), 3),
                'adj_sim': round(float(adj_sim[target_movie_id, other_id]), 3),
                'difference': round(float(raw_sim[target_movie_id, other_id] - adj_sim[target_movie_id, other_id]), 3)
            })
    # Sort comparisons by adjusted cosine descending
    focal_comparisons.sort(key=lambda x: x['adj_sim'], reverse=True)

    # Build matrix view data for rendering
    matrix_rows = []
    for u_idx, u in enumerate(USERS):
        row_ratings = []
        for m_idx in range(len(MOVIES)):
            val = R[u_idx, m_idx]
            row_ratings.append(int(val) if val > 0 else '-')
        matrix_rows.append({
            'user_name': u['name'],
            'user_role': u['role'],
            'mean_rating': round(float(user_means[u_idx]), 2),
            'ratings': row_ratings,
            'is_active': (u_idx == active_user_idx)
        })

    return render_template(
        'index.html',
        movies=catalog_movies,
        users=USERS,
        active_user=USERS[active_user_idx],
        active_user_idx=active_user_idx,
        active_user_mean=round(float(active_user_mean), 2),
        k_neighbors=k_neighbors,
        target_movie_id=target_movie_id,
        focal_movie=MOVIES[target_movie_id],
        predictions=predictions,
        top_calc=top_recommendation_calc,
        focal_comparisons=focal_comparisons,
        matrix_rows=matrix_rows,
        plot1_b64=plot1_b64,
        plot2_b64=plot2_b64,
        plot3_b64=plot3_b64,
        plot4_b64=plot4_b64
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5017))
    print(f"Starting Experiment 17 Recommender System Server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
