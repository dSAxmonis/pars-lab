import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ==============================================================================
# EXPERIMENT 16: ITEM-BASED k-NEAREST NEIGHBORS (kNN) RECOMMENDER SYSTEM
# Domain: Movies Recommendation System
# Netaji Subhas University of Technology (NSUT)
# Student: Monis | Roll No: 2023UIT3027 | Instructor: Dr. Vishal Maheshkar
# ==============================================================================

# 1. MOVIES DATASET (20 Movies across 7 Genres)
MOVIES = [
    {
        "id": 0, "code": "M01", "title": "Inception", "year": 2010,
        "genres": ["Sci-Fi", "Action", "Thriller"], "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page", "imdb": 8.8,
        "initials": "INC", "emoji": "🌀", "color": "#1a365d",
        "plot": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        "id": 1, "code": "M02", "title": "The Dark Knight", "year": 2008,
        "genres": ["Action", "Crime", "Drama"], "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart", "imdb": 9.0,
        "initials": "TDK", "emoji": "🦇", "color": "#2d3748",
        "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        "id": 2, "code": "M03", "title": "Interstellar", "year": 2014,
        "genres": ["Sci-Fi", "Drama", "Adventure"], "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain", "imdb": 8.7,
        "initials": "INT", "emoji": "🚀", "color": "#2b6cb0",
        "plot": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft along with a team of researchers to find a new planet for humans."
    },
    {
        "id": 3, "code": "M04", "title": "The Matrix", "year": 1999,
        "genres": ["Sci-Fi", "Action"], "director": "Lana & Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", "imdb": 8.7,
        "initials": "MTX", "emoji": "🕶️", "color": "#22543d",
        "plot": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence."
    },
    {
        "id": 4, "code": "M05", "title": "Pulp Fiction", "year": 1994,
        "genres": ["Crime", "Drama", "Thriller"], "director": "Quentin Tarantino",
        "cast": "John Travolta, Uma Thurman, Samuel L. Jackson", "imdb": 8.9,
        "initials": "PF", "emoji": "🔫", "color": "#742a2a",
        "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
    },
    {
        "id": 5, "code": "M06", "title": "The Godfather", "year": 1972,
        "genres": ["Crime", "Drama"], "director": "Francis Ford Coppola",
        "cast": "Marlon Brando, Al Pacino, James Caan", "imdb": 9.2,
        "initials": "GF", "emoji": "🌹", "color": "#4a5568",
        "plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    },
    {
        "id": 6, "code": "M07", "title": "Fight Club", "year": 1999,
        "genres": ["Drama", "Thriller"], "director": "David Fincher",
        "cast": "Brad Pitt, Edward Norton, Helena Bonham Carter", "imdb": 8.8,
        "initials": "FC", "emoji": "🥊", "color": "#9b2c2c",
        "plot": "An insomniac office worker looking for a way to change his life crosses paths with a devil-may-care soap maker and forms an underground fight club that evolves into something much more."
    },
    {
        "id": 7, "code": "M08", "title": "Forrest Gump", "year": 1994,
        "genres": ["Drama", "Romance", "Comedy"], "director": "Robert Zemeckis",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise", "imdb": 8.8,
        "initials": "FG", "emoji": "🏃", "color": "#2c5282",
        "plot": "The history of the United States from the 1950s to the '70s unfolds from the perspective of an Alabama man with an IQ of 75 who yearns to be reunited with his childhood sweetheart."
    },
    {
        "id": 8, "code": "M09", "title": "The Shawshank Redemption", "year": 1994,
        "genres": ["Drama", "Crime"], "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton", "imdb": 9.3,
        "initials": "SR", "emoji": "🗝️", "color": "#319795",
        "plot": "A banker convicted of uxoricide forms a friendship over a quarter of a century with a hardened convict, while maintaining his innocence and trying to remain hopeful through simple compassion."
    },
    {
        "id": 9, "code": "M10", "title": "Titanic", "year": 1997,
        "genres": ["Romance", "Drama"], "director": "James Cameron",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane", "imdb": 7.9,
        "initials": "TTN", "emoji": "🚢", "color": "#2c7a7b",
        "plot": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."
    },
    {
        "id": 10, "code": "M11", "title": "La La Land", "year": 2016,
        "genres": ["Romance", "Comedy", "Drama"], "director": "Damien Chazelle",
        "cast": "Ryan Gosling, Emma Stone, John Legend", "imdb": 8.0,
        "initials": "LLL", "emoji": "🎹", "color": "#6b46c1",
        "plot": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future."
    },
    {
        "id": 11, "code": "M12", "title": "The Hangover", "year": 2009,
        "genres": ["Comedy"], "director": "Todd Phillips",
        "cast": "Bradley Cooper, Ed Helms, Zach Galifianakis", "imdb": 7.7,
        "initials": "HNG", "emoji": "🍻", "color": "#b7791f",
        "plot": "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend."
    },
    {
        "id": 12, "code": "M13", "title": "Superbad", "year": 2007,
        "genres": ["Comedy"], "director": "Greg Mottola",
        "cast": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse", "imdb": 7.6,
        "initials": "SBD", "emoji": "🎒", "color": "#c05621",
        "plot": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry."
    },
    {
        "id": 13, "code": "M14", "title": "The Conjuring", "year": 2013,
        "genres": ["Horror", "Thriller"], "director": "James Wan",
        "cast": "Patrick Wilson, Vera Farmiga, Ron Livingston", "imdb": 7.5,
        "initials": "CNJ", "emoji": "👻", "color": "#553c9a",
        "plot": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse."
    },
    {
        "id": 14, "code": "M15", "title": "A Quiet Place", "year": 2018,
        "genres": ["Horror", "Sci-Fi", "Drama"], "director": "John Krasinski",
        "cast": "Emily Blunt, John Krasinski, Millicent Simmonds", "imdb": 7.5,
        "initials": "AQP", "emoji": "🤫", "color": "#4c51bf",
        "plot": "A family struggles for survival in a world where most humans have been killed by blind but noise-sensitive creatures. They are forced to communicate in sign language."
    },
    {
        "id": 15, "code": "M16", "title": "Get Out", "year": 2017,
        "genres": ["Horror", "Mystery", "Thriller"], "director": "Jordan Peele",
        "cast": "Daniel Kaluuya, Allison Williams, Bradley Whitford", "imdb": 7.8,
        "initials": "GOT", "emoji": "👁️", "color": "#1a202c",
        "plot": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point."
    },
    {
        "id": 16, "code": "M17", "title": "Gladiator", "year": 2000,
        "genres": ["Action", "Drama", "Adventure"], "director": "Ridley Scott",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen", "imdb": 8.5,
        "initials": "GLD", "emoji": "⚔️", "color": "#7b341e",
        "plot": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery."
    },
    {
        "id": 17, "code": "M18", "title": "Avengers: Endgame", "year": 2019,
        "genres": ["Action", "Sci-Fi", "Adventure"], "director": "Anthony & Joe Russo",
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo", "imdb": 8.4,
        "initials": "AVG", "emoji": "🛡️", "color": "#805ad5",
        "plot": "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions."
    },
    {
        "id": 18, "code": "M19", "title": "Crazy Rich Asians", "year": 2018,
        "genres": ["Romance", "Comedy"], "director": "Jon M. Chu",
        "cast": "Constance Wu, Henry Golding, Michelle Yeoh", "imdb": 6.9,
        "initials": "CRA", "emoji": "💎", "color": "#97266d",
        "plot": "This contemporary romantic comedy follows native New Yorker Rachel Chu to Singapore to meet her boyfriend's family, discovering they are wildly wealthy."
    },
    {
        "id": 19, "code": "M20", "title": "Whiplash", "year": 2014,
        "genres": ["Drama", "Music"], "director": "Damien Chazelle",
        "cast": "Miles Teller, J.K. Simmons, Paul Reiser", "imdb": 8.5,
        "initials": "WPL", "emoji": "🥁", "color": "#9c4221",
        "plot": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential."
    }
]

# 2. USERS METADATA (8 Users)
USERS = [
    {"id": 0, "name": "User 1 (Alice)", "persona": "Sci-Fi & Action Fan"},
    {"id": 1, "name": "User 2 (Bob)", "persona": "Classic Crime & Drama Buff"},
    {"id": 2, "name": "User 3 (Charlie)", "persona": "Rom-Com & Comedy Enthusiast"},
    {"id": 3, "name": "User 4 (Diana)", "persona": "Horror & Suspense Fanatic"},
    {"id": 4, "name": "User 5 (Ethan)", "persona": "Blockbuster & Action Lover"},
    {"id": 5, "name": "User 6 (Fiona)", "persona": "Drama & Romance Connoisseur"},
    {"id": 6, "name": "User 7 (George)", "persona": "Indie & Psychological Cinema"},
    {"id": 7, "name": "User 8 (Monis - Active)", "persona": "Custom / Interactive Student Profile"}
]

# 3. INITIAL RATINGS MATRIX (8 Users x 20 Movies, 1-5 scale, 0 = Unrated)
DEFAULT_RATINGS = np.array([
    # U1 (Alice - Sci-Fi / Action)
    [5, 5, 5, 5, 4, 3, 4, 0, 0, 1, 1, 2, 1, 2, 3, 0, 4, 5, 1, 3],
    # U2 (Bob - Crime / Drama)
    [3, 4, 0, 0, 5, 5, 5, 4, 5, 2, 0, 0, 1, 2, 0, 4, 4, 2, 1, 5],
    # U3 (Charlie - Rom-Com / Comedy)
    [2, 2, 1, 1, 2, 1, 1, 5, 4, 5, 5, 5, 5, 1, 1, 2, 2, 3, 5, 3],
    # U4 (Diana - Horror / Suspense)
    [4, 4, 3, 3, 4, 2, 4, 2, 3, 1, 1, 2, 1, 5, 5, 5, 3, 2, 1, 4],
    # U5 (Ethan - Blockbuster / Action)
    [5, 5, 4, 5, 4, 3, 4, 3, 0, 1, 2, 3, 4, 2, 3, 2, 5, 5, 2, 0],
    # U6 (Fiona - Drama & Romance)
    [3, 0, 4, 2, 3, 4, 2, 5, 5, 5, 4, 3, 2, 1, 2, 3, 3, 2, 4, 4],
    # U7 (George - Indie / Thriller)
    [4, 3, 4, 0, 5, 5, 5, 3, 5, 1, 4, 1, 0, 3, 4, 5, 2, 1, 0, 5],
    # U8 (Monis - Interactive Current User)
    [5, 5, 0, 5, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 4, 0, 0, 0]
], dtype=float)

# In-memory working ratings copy
active_ratings = DEFAULT_RATINGS.copy()

# ==============================================================================
# ITEM-BASED COLLABORATIVE FILTERING MATHEMATICAL ROUTINES (FROM SCRATCH NUMPY)
# ==============================================================================

def compute_item_similarity_matrix(R_mat, metric='adj_cos'):
    """
    Computes pairwise item similarity matrix S in R^{n x n} from rating matrix R in R^{m x n}.
    - metric='adj_cos': Adjusted Cosine Similarity (subtracts user mean rating)
    - metric='cosine': Standard Cosine Similarity over co-rated observations
    """
    m, n = R_mat.shape
    S = np.zeros((n, n), dtype=float)
    
    # Calculate user mean ratings across non-zero ratings
    user_means = np.zeros(m, dtype=float)
    for u in range(m):
        rated_mask = R_mat[u] > 0
        if np.sum(rated_mask) > 0:
            user_means[u] = np.mean(R_mat[u, rated_mask])
            
    for i in range(n):
        for j in range(n):
            if i == j:
                S[i, j] = 1.0
                continue
            # Users who rated BOTH item i and item j
            co_rated = (R_mat[:, i] > 0) & (R_mat[:, j] > 0)
            count = np.sum(co_rated)
            
            if count >= 2:
                if metric == 'adj_cos':
                    u_sub = np.where(co_rated)[0]
                    diff_i = R_mat[u_sub, i] - user_means[u_sub]
                    diff_j = R_mat[u_sub, j] - user_means[u_sub]
                    denom = np.sqrt(np.sum(diff_i**2)) * np.sqrt(np.sum(diff_j**2))
                    if denom > 1e-9:
                        S[i, j] = np.sum(diff_i * diff_j) / denom
                    else:
                        S[i, j] = 0.0
                else:  # Standard Cosine
                    vec_i = R_mat[co_rated, i]
                    vec_j = R_mat[co_rated, j]
                    denom = np.sqrt(np.sum(vec_i**2)) * np.sqrt(np.sum(vec_j**2))
                    S[i, j] = np.sum(vec_i * vec_j) / denom if denom > 1e-9 else 0.0
            elif count == 1:
                # Single co-rater fallback (weighted lower)
                vec_i = R_mat[co_rated, i]
                vec_j = R_mat[co_rated, j]
                denom = np.sqrt(np.sum(vec_i**2)) * np.sqrt(np.sum(vec_j**2))
                S[i, j] = 0.5 * (np.sum(vec_i * vec_j) / denom) if denom > 1e-9 else 0.0
            else:
                S[i, j] = 0.0
                
    return S


def predict_user_ratings(R_mat, u_idx, S, k=3):
    r"""
    Predicts ratings for all unrated movies of user u_idx using weighted sum of k nearest items:
    \hat{R}_{u, i} = \frac{\sum_{j \in S^k(i; u)} sim(i, j) \cdot R_{u, j}}{\sum_{j \in S^k(i; u)} |sim(i, j)|}
    """
    m, n = R_mat.shape
    user_ratings = R_mat[u_idx]
    rated_items = np.where(user_ratings > 0)[0]
    
    predictions = []
    
    for i in range(n):
        if user_ratings[i] > 0:
            # Already rated by user
            continue
            
        # Candidate neighbors rated by user
        # We consider items j in rated_items with positive similarity sim(i, j) > 0
        cand = []
        for j in rated_items:
            sim_val = float(S[i, j])
            if sim_val > 0.001:
                cand.append({
                    "neighbor_id": int(j),
                    "movie": MOVIES[j]["title"],
                    "code": MOVIES[j]["code"],
                    "similarity": round(sim_val, 4),
                    "user_rating": float(user_ratings[j])
                })
                
        # Sort candidates by similarity descending
        cand.sort(key=lambda x: x["similarity"], reverse=True)
        top_k = cand[:k]
        
        if top_k:
            numerator = sum(item["similarity"] * item["user_rating"] for item in top_k)
            denominator = sum(item["similarity"] for item in top_k)
            pred_rating = numerator / denominator if denominator > 1e-9 else 3.0
            pred_rating = max(1.0, min(5.0, pred_rating))  # clamp to [1, 5]
            
            # Formulate step-by-step mathematical breakdown
            terms = [f"({item['similarity']:.3f} × {item['user_rating']:.1f})" for item in top_k]
            sim_terms = [f"{item['similarity']:.3f}" for item in top_k]
            math_formula = f"[{' + '.join(terms)}] / [{' + '.join(sim_terms)}] = {numerator:.3f} / {denominator:.3f} = {pred_rating:.2f}"
            has_neighbors = True
        else:
            # Fallback when no positive neighbors rated
            # Use global average rating for movie i across other users
            other_ratings = R_mat[:, i][R_mat[:, i] > 0]
            fallback_val = float(np.mean(other_ratings)) if len(other_ratings) > 0 else 3.0
            pred_rating = round(fallback_val, 2)
            math_formula = f"Global Catalog Mean for Movie {MOVIES[i]['code']} = {pred_rating:.2f} (No positive rated neighbors)"
            has_neighbors = False

        predictions.append({
            "movie_id": i,
            "code": MOVIES[i]["code"],
            "title": MOVIES[i]["title"],
            "year": MOVIES[i]["year"],
            "genres": ", ".join(MOVIES[i]["genres"]),
            "director": MOVIES[i]["director"],
            "imdb": MOVIES[i]["imdb"],
            "emoji": MOVIES[i]["emoji"],
            "color": MOVIES[i]["color"],
            "pred_rating": round(pred_rating, 2),
            "top_k_neighbors": top_k,
            "math_formula": math_formula,
            "has_neighbors": has_neighbors
        })
        
    # Rank by predicted rating descending
    predictions.sort(key=lambda x: x["pred_rating"], reverse=True)
    return predictions


def get_movie_nearest_neighbors(movie_id, S, top_n=5):
    """
    Finds the top N most similar items to movie_id in the entire catalog.
    """
    n = S.shape[0]
    scores = []
    for j in range(n):
        if j != movie_id:
            scores.append({
                "movie_id": j,
                "code": MOVIES[j]["code"],
                "title": MOVIES[j]["title"],
                "year": MOVIES[j]["year"],
                "genres": ", ".join(MOVIES[j]["genres"]),
                "director": MOVIES[j]["director"],
                "imdb": MOVIES[j]["imdb"],
                "emoji": MOVIES[j]["emoji"],
                "color": MOVIES[j]["color"],
                "similarity": round(float(S[movie_id, j]), 4),
                "sim_percent": round(float(S[movie_id, j]) * 100, 1)
            })
    scores.sort(key=lambda x: x["similarity"], reverse=True)
    return scores[:top_n]


def generate_visualizations(S, selected_movie_id, u_idx, predictions, R_mat):
    """
    Generates three matplotlib plots converted to base64 PNG images:
    1. 20x20 Item-Item Similarity Matrix Heatmap
    2. Top Nearest Neighbors Bar Chart for Selected Movie
    3. Top Predicted Ratings & Rating Distribution Comparison
    """
    plots = {}
    
    # -------------------------------------------------------------
    # PLOT 1: Item-Item Similarity Matrix Heatmap (20x20)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.8, 7.2), dpi=120)
    cax = ax.imshow(S, cmap='coolwarm', vmin=-1.0 if np.min(S) < 0 else 0.0, vmax=1.0)
    cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Similarity Score s(i, j)', fontsize=10, fontweight='bold', color='#003366')
    
    movie_labels = [m["code"] for m in MOVIES]
    ax.set_xticks(np.arange(len(MOVIES)))
    ax.set_yticks(np.arange(len(MOVIES)))
    ax.set_xticklabels(movie_labels, rotation=90, fontsize=8.5, fontweight='bold')
    ax.set_yticklabels(movie_labels, fontsize=8.5, fontweight='bold')
    ax.set_title("Item-Item Similarity Matrix Heatmap (20 × 20)", fontsize=13, fontweight='bold', color='#003366', pad=12)
    ax.set_xlabel("Movie Item j", fontsize=10, fontweight='bold', color='#003366')
    ax.set_ylabel("Movie Item i", fontsize=10, fontweight='bold', color='#003366')
    
    # Add subtle grid
    ax.set_xticks(np.arange(-.5, len(MOVIES), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(MOVIES), 1), minor=True)
    ax.grid(which='minor', color='#ffffff', linestyle='-', linewidth=0.5, alpha=0.6)
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    plots['heatmap'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # -------------------------------------------------------------
    # PLOT 2: Top Similar Neighbors Bar Chart for Selected Movie
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=120)
    sel_movie = MOVIES[selected_movie_id]
    top_neighbors = get_movie_nearest_neighbors(selected_movie_id, S, top_n=6)
    
    nbr_titles = [f"{n['code']} - {n['title']}" for n in reversed(top_neighbors)]
    nbr_sims = [n['similarity'] for n in reversed(top_neighbors)]
    colors = ['#1a365d' if s > 0.7 else ('#2b6cb0' if s > 0.4 else '#4a5568') for s in nbr_sims]
    
    bars = ax.barh(nbr_titles, nbr_sims, color=colors, edgecolor='#003366', height=0.6)
    ax.set_xlim(min(0, min(nbr_sims) - 0.1), max(1.0, max(nbr_sims) + 0.1))
    ax.set_xlabel("Similarity Score s(i, j)", fontsize=10, fontweight='bold', color='#003366')
    ax.set_title(f"Top Nearest Neighbor Items for: [{sel_movie['code']}] {sel_movie['title']}", 
                 fontsize=12, fontweight='bold', color='#003366', pad=10)
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    
    # Annotate value on bars
    for bar, val in zip(bars, nbr_sims):
        x_pos = val + 0.02 if val >= 0 else val - 0.08
        ax.text(x_pos, bar.get_y() + bar.get_height()/2, f"{val:.3f}", 
                va='center', fontsize=9, fontweight='bold', color='#111111')
        
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    plots['neighbors_bar'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # -------------------------------------------------------------
    # PLOT 3: Active User Predictions vs Catalog Ratings
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=120)
    
    # Left subplot: Top 5 Predicted Ratings for Active User
    top_preds = predictions[:6]
    p_titles = [p['code'] for p in top_preds]
    p_scores = [p['pred_rating'] for p in top_preds]
    
    bars1 = ax1.bar(p_titles, p_scores, color='#004d40', edgecolor='#00251a', width=0.55)
    ax1.set_ylim(0, 5.5)
    ax1.set_ylabel("Predicted Rating R̂ (1 to 5)", fontsize=9.5, fontweight='bold', color='#003366')
    ax1.set_title(f"Top Predicted Movies for {USERS[u_idx]['name'].split(' ')[0]}", 
                  fontsize=11, fontweight='bold', color='#003366')
    ax1.axhline(4.0, color='#d9534f', linestyle='--', linewidth=1.2, label='Recommended Threshold (≥4.0)')
    ax1.legend(loc='lower right', fontsize=8)
    
    for bar, score in zip(bars1, p_scores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f"{score:.2f}★", 
                 ha='center', fontsize=8.5, fontweight='bold', color='#004d40')
        
    # Right subplot: Active User's Rating Distribution vs Dataset Profile
    user_ratings = R_mat[u_idx][R_mat[u_idx] > 0]
    all_ratings = R_mat[R_mat > 0]
    
    bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    counts_user, _ = np.histogram(user_ratings, bins=bins)
    counts_all, _ = np.histogram(all_ratings, bins=bins)
    
    x_stars = np.array([1, 2, 3, 4, 5])
    width = 0.35
    ax2.bar(x_stars - width/2, counts_user, width=width, color='#3182ce', label='Active User Ratings')
    ax2.bar(x_stars + width/2, counts_all / len(USERS), width=width, color='#a0aec0', label='Avg User Ratings')
    ax2.set_xlabel("Star Rating (1 to 5)", fontsize=9.5, fontweight='bold', color='#003366')
    ax2.set_ylabel("Frequency", fontsize=9.5, fontweight='bold', color='#003366')
    ax2.set_title("Rating Distribution Comparison", fontsize=11, fontweight='bold', color='#003366')
    ax2.set_xticks(x_stars)
    ax2.legend(loc='upper left', fontsize=8)
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    plots['predictions_dist'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return plots


# ==============================================================================
# FLASK WEB APPLICATION ROUTES
# ==============================================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    global active_ratings
    
    # State parameters with defaults
    selected_user_id = 7  # Default to User 8 (Monis)
    selected_movie_id = 0  # Default to Inception
    k_neighbors = 3        # Default k
    similarity_metric = 'adj_cos'  # 'adj_cos' or 'cosine'
    top_n_rec = 5          # Default Top-N
    user_action_msg = ""
    
    if request.method == 'POST':
        action = request.form.get('action', '')
        
        # Parse common form settings
        if 'user_id' in request.form:
            try:
                selected_user_id = int(request.form.get('user_id', 7))
            except ValueError:
                selected_user_id = 7
                
        if 'selected_movie_id' in request.form:
            try:
                selected_movie_id = int(request.form.get('selected_movie_id', 0))
            except ValueError:
                selected_movie_id = 0
                
        if 'k_neighbors' in request.form:
            try:
                k_neighbors = int(request.form.get('k_neighbors', 3))
            except ValueError:
                k_neighbors = 3
                
        if 'metric' in request.form:
            similarity_metric = request.form.get('metric', 'adj_cos')
            
        if 'top_n' in request.form:
            try:
                top_n_rec = int(request.form.get('top_n', 5))
            except ValueError:
                top_n_rec = 5

        # Handle specific button actions
        if action == 'select_movie':
            target_mid = int(request.form.get('target_movie_id', selected_movie_id))
            selected_movie_id = target_mid
            user_action_msg = f"Inspecting details & nearest neighbors for: [{MOVIES[selected_movie_id]['code']}] {MOVIES[selected_movie_id]['title']}."

        elif action == 'rate_movie':
            target_mid = int(request.form.get('target_movie_id', selected_movie_id))
            new_rating = float(request.form.get('rating_value', 5.0))
            active_ratings[selected_user_id, target_mid] = new_rating
            selected_movie_id = target_mid
            user_action_msg = f"Successfully updated rating for [{MOVIES[target_mid]['code']}] {MOVIES[target_mid]['title']} to {new_rating:.1f} ★ for {USERS[selected_user_id]['name']}!"

        elif action == 'unrate_movie':
            target_mid = int(request.form.get('target_movie_id', selected_movie_id))
            active_ratings[selected_user_id, target_mid] = 0.0
            selected_movie_id = target_mid
            user_action_msg = f"Cleared rating for [{MOVIES[target_mid]['code']}] {MOVIES[target_mid]['title']} (marked as unrated/candidate for recommendation)."

        elif action == 'reset_ratings':
            active_ratings = DEFAULT_RATINGS.copy()
            user_action_msg = "Reset all rating values across all users to benchmark defaults."

        elif action == 'apply_settings':
            user_action_msg = f"Updated settings: metric={similarity_metric}, k={k_neighbors}, Top-N={top_n_rec}."

    # Compute item-item similarity matrix S
    S = compute_item_similarity_matrix(active_ratings, metric=similarity_metric)
    
    # Compute rating predictions for all unrated movies for selected_user_id
    all_predictions = predict_user_ratings(active_ratings, selected_user_id, S, k=k_neighbors)
    top_recommendations = all_predictions[:top_n_rec]
    
    # Nearest neighbors for the selected movie
    movie_neighbors = get_movie_nearest_neighbors(selected_movie_id, S, top_n=6)
    
    # Generate matplotlib internal visualizations (Base64)
    plots = generate_visualizations(S, selected_movie_id, selected_user_id, all_predictions, active_ratings)
    
    # Build movie catalog status array for template display
    catalog_items = []
    user_ratings_vector = active_ratings[selected_user_id]
    for m in MOVIES:
        m_id = m["id"]
        cur_rating = float(user_ratings_vector[m_id])
        catalog_items.append({
            "id": m_id,
            "code": m["code"],
            "title": m["title"],
            "year": m["year"],
            "genres": ", ".join(m["genres"]),
            "director": m["director"],
            "cast": m["cast"],
            "imdb": m["imdb"],
            "initials": m["initials"],
            "emoji": m["emoji"],
            "color": m["color"],
            "plot": m["plot"],
            "user_rating": cur_rating,
            "is_rated": cur_rating > 0,
            "is_selected": (m_id == selected_movie_id)
        })
        
    # Prepare Item Similarity Matrix Table Data (subset or full)
    sim_matrix_display = {
        "headers": [m["code"] for m in MOVIES],
        "rows": []
    }
    for i in range(len(MOVIES)):
        row_vals = [round(float(S[i, j]), 2) for j in range(len(MOVIES))]
        sim_matrix_display["rows"].append({
            "code": MOVIES[i]["code"],
            "title": MOVIES[i]["title"],
            "sim_values": row_vals
        })
        
    return render_template(
        'index.html',
        movies=catalog_items,
        users=USERS,
        selected_user=USERS[selected_user_id],
        selected_user_id=selected_user_id,
        selected_movie=MOVIES[selected_movie_id],
        selected_movie_id=selected_movie_id,
        movie_neighbors=movie_neighbors,
        recommendations=top_recommendations,
        all_predictions=all_predictions,
        k_neighbors=k_neighbors,
        similarity_metric=similarity_metric,
        top_n_rec=top_n_rec,
        user_action_msg=user_action_msg,
        plots=plots,
        sim_matrix=sim_matrix_display,
        total_movies=len(MOVIES),
        total_users=len(USERS),
        rated_count=int(np.sum(user_ratings_vector > 0)),
        unrated_count=int(np.sum(user_ratings_vector == 0))
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5016))
    print(f"Starting PARS Lab Experiment 16 on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
