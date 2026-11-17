import os
import io
import base64
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ==========================================
# 1. HARDCODED MOVIES DATASET (20 MOVIES)
# ==========================================
MOVIES = [
    {
        "id": 0,
        "title": "Inception",
        "genres": ["Sci-Fi", "Action", "Thriller"],
        "year": 2010,
        "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "imdb_rating": 8.8,
        "plot_keywords": "Dream infiltration, subconscious heist, spinning totem, reality distortion",
        "poster_color": "#0284c7",
        "poster_emoji": "🌀",
        "tagline": "Your mind is the scene of the crime."
    },
    {
        "id": 1,
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Thriller"],
        "year": 2008,
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "imdb_rating": 9.0,
        "plot_keywords": "Gotham city vigilante, Joker psychological warfare, moral dilemma",
        "poster_color": "#1e293b",
        "poster_emoji": "🦇",
        "tagline": "Why so serious?"
    },
    {
        "id": 2,
        "title": "Interstellar",
        "genres": ["Sci-Fi", "Drama", "Adventure"],
        "year": 2014,
        "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "imdb_rating": 8.7,
        "plot_keywords": "Wormhole expedition, relativistic time dilation, black hole Gargantua",
        "poster_color": "#4338ca",
        "poster_emoji": "🚀",
        "tagline": "Mankind was born on Earth. It was never meant to die here."
    },
    {
        "id": 3,
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama", "Thriller"],
        "year": 1994,
        "director": "Quentin Tarantino",
        "cast": "John Travolta, Samuel L. Jackson, Uma Thurman",
        "imdb_rating": 8.9,
        "plot_keywords": "Non-linear mob chronicle, mysterious glowing briefcase, Los Angeles diner",
        "poster_color": "#b45309",
        "poster_emoji": "🔫",
        "tagline": "You won't know the facts until you've seen the fiction."
    },
    {
        "id": 4,
        "title": "The Shawshank Redemption",
        "genres": ["Drama"],
        "year": 1994,
        "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "imdb_rating": 9.3,
        "plot_keywords": "Wrongful conviction, endurance, geological hammer tunnel, Pacific freedom",
        "poster_color": "#475569",
        "poster_emoji": "🗝️",
        "tagline": "Fear can hold you prisoner. Hope can set you free."
    },
    {
        "id": 5,
        "title": "The Matrix",
        "genres": ["Sci-Fi", "Action"],
        "year": 1999,
        "director": "Lana & Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "imdb_rating": 8.7,
        "plot_keywords": "Simulated reality matrix, red pill rebellion, cybernetic dystopia, bullet time",
        "poster_color": "#047857",
        "poster_emoji": "🕶️",
        "tagline": "Welcome to the Real World."
    },
    {
        "id": 6,
        "title": "Forrest Gump",
        "genres": ["Drama", "Romance", "Comedy"],
        "year": 1994,
        "director": "Robert Zemeckis",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise",
        "imdb_rating": 8.8,
        "plot_keywords": "Life is like a box of chocolates, cross-country run, Vietnam valor, Jenny",
        "poster_color": "#be123c",
        "poster_emoji": "🏃",
        "tagline": "The world will never be the same once you've seen it through Forrest Gump."
    },
    {
        "id": 7,
        "title": "The Godfather",
        "genres": ["Crime", "Drama"],
        "year": 1972,
        "director": "Francis Ford Coppola",
        "cast": "Marlon Brando, Al Pacino, James Caan",
        "imdb_rating": 9.2,
        "plot_keywords": "Corleone mafia dynasty, family honor, succession of power, Sicilian code",
        "poster_color": "#7f1d1d",
        "poster_emoji": "🎩",
        "tagline": "An offer you can't refuse."
    },
    {
        "id": 8,
        "title": "Superbad",
        "genres": ["Comedy"],
        "year": 2007,
        "director": "Greg Mottola",
        "cast": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse",
        "imdb_rating": 7.6,
        "plot_keywords": "McLovin fake ID, high school party, alcohol smuggling adventure",
        "poster_color": "#c2410c",
        "poster_emoji": "🍺",
        "tagline": "It's not just a party, it's a mission."
    },
    {
        "id": 9,
        "title": "The Hangover",
        "genres": ["Comedy"],
        "year": 2009,
        "director": "Todd Phillips",
        "cast": "Bradley Cooper, Ed Helms, Zach Galifianakis",
        "imdb_rating": 7.7,
        "plot_keywords": "Las Vegas stag party blackout, tiger in the bathroom, missing groom",
        "poster_color": "#a16207",
        "poster_emoji": "🎰",
        "tagline": "Some guys just can't handle Vegas."
    },
    {
        "id": 10,
        "title": "Gladiator",
        "genres": ["Action", "Drama", "Adventure"],
        "year": 2000,
        "director": "Ridley Scott",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen",
        "imdb_rating": 8.5,
        "plot_keywords": "Roman general enslaved, gladiatorial vengeance, Colosseum combat",
        "poster_color": "#991b1b",
        "poster_emoji": "⚔️",
        "tagline": "What we do in life echoes in eternity."
    },
    {
        "id": 11,
        "title": "Alien",
        "genres": ["Horror", "Sci-Fi"],
        "year": 1979,
        "director": "Ridley Scott",
        "cast": "Sigourney Weaver, Tom Skerritt, John Hurt",
        "imdb_rating": 8.5,
        "plot_keywords": "Nostromo freighter, predatory extraterrestrial xenomorph, claustrophobic terror",
        "poster_color": "#15803d",
        "poster_emoji": "👽",
        "tagline": "In space no one can hear you scream."
    },
    {
        "id": 12,
        "title": "The Conjuring",
        "genres": ["Horror", "Thriller"],
        "year": 2013,
        "director": "James Wan",
        "cast": "Vera Farmiga, Patrick Wilson, Lili Taylor",
        "imdb_rating": 7.5,
        "plot_keywords": "Paranormal investigators Ed & Lorraine Warren, haunted farmhouse, occult",
        "poster_color": "#312e81",
        "poster_emoji": "👻",
        "tagline": "Based on the true case files of the Warrens."
    },
    {
        "id": 13,
        "title": "Titanic",
        "genres": ["Romance", "Drama"],
        "year": 1997,
        "director": "James Cameron",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
        "imdb_rating": 7.9,
        "plot_keywords": "Transatlantic maiden voyage, Jack and Rose class romance, fateful iceberg",
        "poster_color": "#0f766e",
        "poster_emoji": "🚢",
        "tagline": "Nothing on Earth could come between them."
    },
    {
        "id": 14,
        "title": "La La Land",
        "genres": ["Romance", "Comedy", "Drama"],
        "year": 2016,
        "director": "Damien Chazelle",
        "cast": "Ryan Gosling, Emma Stone, John Legend",
        "imdb_rating": 8.0,
        "plot_keywords": "Aspiring jazz pianist and actress, modern Los Angeles romance, audition dreams",
        "poster_color": "#7e22ce",
        "poster_emoji": "🎹",
        "tagline": "Here's to the fools who dream."
    },
    {
        "id": 15,
        "title": "Avengers: Endgame",
        "genres": ["Action", "Sci-Fi", "Adventure"],
        "year": 2019,
        "director": "Anthony & Joe Russo",
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo",
        "imdb_rating": 8.4,
        "plot_keywords": "Quantum realm time travel, reverse Thanos universal snap, infinity stones",
        "poster_color": "#1d4ed8",
        "poster_emoji": "🛡️",
        "tagline": "Part of the journey is the end."
    },
    {
        "id": 16,
        "title": "Parasite",
        "genres": ["Thriller", "Drama", "Comedy"],
        "year": 2019,
        "director": "Bong Joon-ho",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "imdb_rating": 8.5,
        "plot_keywords": "Kim family socioeconomic deception, wealthy Park residence, class struggle",
        "poster_color": "#134e4a",
        "poster_emoji": "🍑",
        "tagline": "Act like you own the place."
    },
    {
        "id": 17,
        "title": "The Shining",
        "genres": ["Horror", "Drama"],
        "year": 1980,
        "director": "Stanley Kubrick",
        "cast": "Jack Nicholson, Shelley Duvall, Danny Lloyd",
        "imdb_rating": 8.4,
        "plot_keywords": "Overlook Hotel winter solitude, psychic shining, cabin fever, axe rampage",
        "poster_color": "#881337",
        "poster_emoji": "🪓",
        "tagline": "A masterpiece of modern horror."
    },
    {
        "id": 18,
        "title": "Spider-Man: Into the Spider-Verse",
        "genres": ["Action", "Sci-Fi", "Animation"],
        "year": 2018,
        "director": "Bob Persichetti, Peter Ramsey",
        "cast": "Shameik Moore, Jake Johnson, Hailee Steinfeld",
        "imdb_rating": 8.4,
        "plot_keywords": "Miles Morales Brooklyn spider origin, parallel multiverse heroes, leap of faith",
        "poster_color": "#a21caf",
        "poster_emoji": "🕸️",
        "tagline": "More than one wears the mask."
    },
    {
        "id": 19,
        "title": "Crazy Rich Asians",
        "genres": ["Comedy", "Romance"],
        "year": 2018,
        "director": "Jon M. Chu",
        "cast": "Constance Wu, Henry Golding, Michelle Yeoh",
        "imdb_rating": 6.9,
        "plot_keywords": "Opulent Singapore dynasty, intimidating matriarch Eleanor, cultural family clash",
        "poster_color": "#854d0e",
        "poster_emoji": "💍",
        "tagline": "The only thing crazier than love is family."
    }
]

# Map movie ID to movie metadata
MOVIE_DICT = {m["id"]: m for m in MOVIES}

# ==========================================
# 2. REFERENCE USER RATINGS MATRIX (8 USERS x 20 MOVIES)
# Scale: 1 to 5 stars, 0 = Unrated / Missing
# ==========================================
USERS = [
    {"id": 0, "name": "Alice Miller", "persona": "Sci-Fi & Action buff"},
    {"id": 1, "name": "Bob Kelly", "persona": "Blockbuster & Tech-Thriller fan"},
    {"id": 2, "name": "Charlie Davis", "persona": "Classic Crime & Prestige Drama fan"},
    {"id": 3, "name": "Diana Prince", "persona": "Romance & Light Comedy lover"},
    {"id": 4, "name": "Ethan Ross", "persona": "Horror & Psychological Thriller fanatic"},
    {"id": 5, "name": "Fiona Scott", "persona": "Arthouse Cinephile & Dark Drama critic"},
    {"id": 6, "name": "George Brown", "persona": "Action Comedy & Popcorn Movie enthusiast"},
    {"id": 7, "name": "Hannah Turner", "persona": "Emotional Romance & Period Drama lover"}
]

# 8 rows x 20 columns
# Movies:
# 0:Inception, 1:Dark Knight, 2:Interstellar, 3:Pulp Fiction, 4:Shawshank,
# 5:Matrix, 6:Forrest Gump, 7:Godfather, 8:Superbad, 9:Hangover,
# 10:Gladiator, 11:Alien, 12:Conjuring, 13:Titanic, 14:La La Land,
# 15:Endgame, 16:Parasite, 17:Shining, 18:Spider-Verse, 19:Crazy Rich Asians
RATINGS_MATRIX = np.array([
    # Alice (Sci-Fi / Action lover)
    [5, 5, 5, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 1, 2, 4, 0, 0, 5, 0],
    # Bob (Action / Sci-Fi enthusiast)
    [5, 5, 4, 0, 0, 4, 0, 0, 0, 0, 5, 0, 0, 2, 0, 5, 3, 0, 4, 0],
    # Charlie (Crime & Drama)
    [0, 4, 0, 5, 5, 0, 4, 5, 1, 2, 0, 0, 0, 0, 0, 0, 5, 4, 0, 0],
    # Diana (Romance & Comedy)
    [0, 0, 0, 0, 4, 0, 5, 0, 4, 4, 0, 1, 1, 5, 5, 0, 0, 1, 0, 5],
    # Ethan (Horror & Thriller)
    [0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 1, 0, 5, 5, 0, 1],
    # Fiona (Cinephile / Arthouse)
    [4, 0, 0, 5, 5, 0, 0, 4, 0, 0, 0, 4, 0, 0, 4, 0, 5, 4, 5, 0],
    # George (Comedy & Blockbusters)
    [3, 4, 0, 0, 0, 3, 0, 0, 5, 5, 4, 0, 0, 0, 0, 5, 0, 0, 4, 3],
    # Hannah (Romance & Drama)
    [0, 0, 4, 0, 5, 0, 5, 4, 0, 0, 0, 0, 0, 5, 4, 0, 4, 0, 0, 4]
], dtype=float)

# ==========================================
# 3. ACTIVE USER PRESETS
# ==========================================
PRESETS = {
    "scifi": {
        "name": "Preset A: Sci-Fi & Action Explorer",
        "description": "Loves high-concept sci-fi (Inception, Interstellar, Dark Knight, Matrix); dislikes pure romance (Titanic).",
        "ratings": {0: 5.0, 1: 5.0, 2: 5.0, 5: 4.0, 13: 1.0}
    },
    "romcom": {
        "name": "Preset B: Romance & Comedy Lover",
        "description": "Loves romantic dramas and comedies (La La Land, Titanic, Crazy Rich Asians, Superbad); dislikes horror (Alien).",
        "ratings": {6: 5.0, 8: 4.0, 11: 1.0, 13: 5.0, 14: 5.0, 19: 5.0}
    },
    "horror": {
        "name": "Preset C: Horror & Dark Thriller Fan",
        "description": "Loves eerie terror and visceral suspense (The Shining, The Conjuring, Alien, Parasite); avoids musicals (La La Land).",
        "ratings": {11: 5.0, 12: 5.0, 14: 1.0, 16: 5.0, 17: 5.0}
    },
    "drama": {
        "name": "Preset D: Prestige Drama & Crime Connoisseur",
        "description": "Values profound narratives and crime epics (Shawshank, Godfather, Pulp Fiction, Parasite); dislikes crude comedy (Superbad).",
        "ratings": {3: 5.0, 4: 5.0, 7: 5.0, 8: 1.0, 16: 5.0}
    },
    "custom": {
        "name": "Custom User Profile",
        "description": "Interactive ratings specified by you on the movie catalog grid below.",
        "ratings": {}
    }
}

# ==========================================
# 4. USER-BASED kNN ALGORITHM (FROM SCRATCH VIA NUMPY)
# ==========================================
def compute_user_knn_recommendations(active_ratings_dict, k=3, metric="pearson"):
    """
    Computes User-based k-Nearest Neighbor collaborative filtering recommendations from scratch.
    
    Parameters:
        active_ratings_dict: dict mapping movie_id (int) -> rating (float, 1-5)
        k: number of nearest neighbors to aggregate (int, 1-5)
        metric: 'pearson' for Pearson Correlation Coefficient or 'cosine' for Cosine Similarity
        
    Returns:
        similarity_results: list of dicts with reference user similarity metrics
        top_recommendations: list of recommended unrated movies with predicted scores
        top_explanation: detailed step-by-step breakdown of top recommendation
        sim_matrix_full: (9, 9) similarity matrix among all users including active user
        active_vector: (20,) active user ratings array
    """
    num_movies = len(MOVIES)
    num_ref_users = RATINGS_MATRIX.shape[0]
    
    active_vector = np.zeros(num_movies, dtype=float)
    for m_id, r in active_ratings_dict.items():
        if 0 <= m_id < num_movies and r > 0:
            active_vector[m_id] = float(r)
            
    rated_indices_active = np.where(active_vector > 0)[0]
    has_active_ratings = len(rated_indices_active) > 0
    active_mean = float(np.mean(active_vector[rated_indices_active])) if has_active_ratings else 3.0
    
    # Precompute reference user means on their rated items
    ref_user_means = np.zeros(num_ref_users, dtype=float)
    for u in range(num_ref_users):
        rated_u = np.where(RATINGS_MATRIX[u] > 0)[0]
        ref_user_means[u] = float(np.mean(RATINGS_MATRIX[u, rated_u])) if len(rated_u) > 0 else 3.0

    # 1. Compute Pairwise Similarities between Active User and Each Reference User
    similarities = np.zeros(num_ref_users, dtype=float)
    co_rated_counts = np.zeros(num_ref_users, dtype=int)
    co_rated_titles = [[] for _ in range(num_ref_users)]
    
    for u in range(num_ref_users):
        co_rated = np.where((active_vector > 0) & (RATINGS_MATRIX[u] > 0))[0]
        co_rated_counts[u] = len(co_rated)
        co_rated_titles[u] = [MOVIES[idx]["title"] for idx in co_rated]
        
        if len(co_rated) == 0:
            similarities[u] = 0.0
            continue
            
        r_a_co = active_vector[co_rated]
        r_u_co = RATINGS_MATRIX[u, co_rated]
        
        if metric == "pearson":
            # Pearson Correlation Coefficient using user overall mean-centering
            diff_a = r_a_co - active_mean
            diff_u = r_u_co - ref_user_means[u]
            
            numer = np.sum(diff_a * diff_u)
            denom = np.sqrt(np.sum(diff_a ** 2)) * np.sqrt(np.sum(diff_u ** 2))
            
            if denom > 1e-9:
                sim = numer / denom
            else:
                # If variance in co-rated sample is zero, fall back to cosine
                norm_a = np.sqrt(np.sum(r_a_co ** 2))
                norm_u = np.sqrt(np.sum(r_u_co ** 2))
                sim = np.sum(r_a_co * r_u_co) / (norm_a * norm_u + 1e-9) if (norm_a * norm_u) > 1e-9 else 0.0
            similarities[u] = float(np.clip(sim, -1.0, 1.0))
        else:
            # Vector Cosine Similarity
            numer = np.sum(r_a_co * r_u_co)
            denom = np.sqrt(np.sum(r_a_co ** 2)) * np.sqrt(np.sum(r_u_co ** 2))
            similarities[u] = float(numer / denom) if denom > 1e-9 else 0.0

    # 2. Select k Nearest Neighbors (Sorted descending by similarity score)
    ranked_user_indices = np.argsort(-similarities)
    
    similarity_results = []
    chosen_neighbors_indices = []
    
    for rank, u_idx in enumerate(ranked_user_indices):
        sim_val = round(float(similarities[u_idx]), 4)
        is_chosen = (rank < k) and (sim_val > -0.99)
        if is_chosen:
            chosen_neighbors_indices.append(u_idx)
            
        similarity_results.append({
            "rank": rank + 1,
            "user_id": int(u_idx),
            "name": USERS[u_idx]["name"],
            "persona": USERS[u_idx]["persona"],
            "similarity": sim_val,
            "similarity_pct": round(sim_val * 100, 1),
            "co_rated_count": int(co_rated_counts[u_idx]),
            "co_rated_movies": ", ".join(co_rated_titles[u_idx]) if co_rated_titles[u_idx] else "None",
            "mean_rating": round(float(ref_user_means[u_idx]), 2),
            "is_neighbor": is_chosen
        })

    # 3. Predict Ratings for All Unrated Movies
    unrated_indices = [i for i in range(num_movies) if active_vector[i] == 0]
    recommendations_list = []
    
    for m_id in unrated_indices:
        movie = MOVIES[m_id]
        
        # Find neighbors among top k who have rated this movie
        neighbor_ratings = []
        for n_idx in chosen_neighbors_indices:
            r_val = RATINGS_MATRIX[n_idx, m_id]
            if r_val > 0:
                neighbor_ratings.append({
                    "user_id": n_idx,
                    "name": USERS[n_idx]["name"],
                    "similarity": float(similarities[n_idx]),
                    "rating": float(r_val),
                    "user_mean": float(ref_user_means[n_idx])
                })
                
        # Mean-centered deviation formula:
        # r_hat = active_mean + sum(sim_u * (r_u_i - mean_u)) / sum(|sim_u|)
        if len(neighbor_ratings) > 0:
            numer_sum = 0.0
            denom_sum = 0.0
            for nr in neighbor_ratings:
                # Use positive weights for neighbors to avoid negative inverse votes pushing ratings unexpectedly
                weight = max(0.001, nr["similarity"]) if metric == "cosine" else nr["similarity"]
                dev = nr["rating"] - nr["user_mean"]
                numer_sum += weight * dev
                denom_sum += abs(weight)
                
            if denom_sum > 1e-9:
                pred_rating = active_mean + (numer_sum / denom_sum)
            else:
                pred_rating = np.mean([nr["rating"] for nr in neighbor_ratings])
            method = "User kNN Aggregation"
        else:
            # Fallback: Global movie average among all reference users who rated it
            rated_by_all = RATINGS_MATRIX[:, m_id][RATINGS_MATRIX[:, m_id] > 0]
            if len(rated_by_all) > 0:
                pred_rating = float(np.mean(rated_by_all))
            else:
                pred_rating = float(movie["imdb_rating"]) / 2.0  # Scale 10 to 5
            method = "Global Baseline (No Neighbor Rated)"
            
        pred_rating = float(np.clip(pred_rating, 1.0, 5.0))
        
        recommendations_list.append({
            "id": m_id,
            "title": movie["title"],
            "genres": movie["genres"],
            "year": movie["year"],
            "director": movie["director"],
            "cast": movie["cast"],
            "imdb_rating": movie["imdb_rating"],
            "plot_keywords": movie["plot_keywords"],
            "poster_color": movie["poster_color"],
            "poster_emoji": movie["poster_emoji"],
            "predicted_rating": round(pred_rating, 2),
            "stars_display": "★" * int(round(pred_rating)) + "☆" * (5 - int(round(pred_rating))),
            "neighbor_contributors": neighbor_ratings,
            "num_contributors": len(neighbor_ratings),
            "method": method
        })
        
    # Sort unrated movies by predicted rating descending
    recommendations_list.sort(key=lambda x: x["predicted_rating"], reverse=True)
    
    # 4. Detailed Calculation Walkthrough for Top Recommendation
    top_explanation = None
    if len(recommendations_list) > 0:
        top_rec = recommendations_list[0]
        top_m_id = top_rec["id"]
        
        step_rows = []
        numer_sum = 0.0
        denom_sum = 0.0
        
        for n_idx in chosen_neighbors_indices:
            r_val = RATINGS_MATRIX[n_idx, top_m_id]
            s_val = float(similarities[n_idx])
            u_mean = float(ref_user_means[n_idx])
            if r_val > 0:
                dev = r_val - u_mean
                prod = s_val * dev
                numer_sum += prod
                denom_sum += abs(s_val)
                step_rows.append({
                    "neighbor_name": USERS[n_idx]["name"],
                    "similarity": round(s_val, 4),
                    "rating": round(r_val, 1),
                    "user_mean": round(u_mean, 2),
                    "deviation": round(dev, 2),
                    "weighted_dev": round(prod, 4)
                })
            else:
                step_rows.append({
                    "neighbor_name": USERS[n_idx]["name"],
                    "similarity": round(s_val, 4),
                    "rating": "Not Rated",
                    "user_mean": round(u_mean, 2),
                    "deviation": "-",
                    "weighted_dev": "0.0000"
                })
                
        adj_dev = round(numer_sum / denom_sum, 4) if denom_sum > 1e-9 else 0.0
        
        top_explanation = {
            "movie_title": top_rec["title"],
            "movie_id": top_m_id,
            "active_mean": round(active_mean, 2),
            "steps": step_rows,
            "numer_sum": round(numer_sum, 4),
            "denom_sum": round(denom_sum, 4),
            "adjusted_deviation": adj_dev,
            "raw_prediction": round(active_mean + adj_dev, 2),
            "final_predicted_rating": top_rec["predicted_rating"]
        }

    # 5. Build Full (9x9) User Similarity Matrix (Active User at index 0, Reference Users 1..8)
    all_users_matrix = np.vstack([active_vector, RATINGS_MATRIX])
    sim_matrix_full = np.zeros((9, 9), dtype=float)
    
    for i in range(9):
        for j in range(9):
            if i == j:
                sim_matrix_full[i, j] = 1.0
                continue
            v_i = all_users_matrix[i]
            v_j = all_users_matrix[j]
            co_idx = np.where((v_i > 0) & (v_j > 0))[0]
            if len(co_idx) == 0:
                sim_matrix_full[i, j] = 0.0
                continue
            r_i = v_i[co_idx]
            r_j = v_j[co_idx]
            
            m_i = np.mean(v_i[v_i > 0]) if np.any(v_i > 0) else 3.0
            m_j = np.mean(v_j[v_j > 0]) if np.any(v_j > 0) else 3.0
            
            if metric == "pearson":
                d_i = r_i - m_i
                d_j = r_j - m_j
                den = np.sqrt(np.sum(d_i ** 2)) * np.sqrt(np.sum(d_j ** 2))
                sim_matrix_full[i, j] = np.sum(d_i * d_j) / den if den > 1e-9 else 0.0
            else:
                den = np.sqrt(np.sum(r_i ** 2)) * np.sqrt(np.sum(r_j ** 2))
                sim_matrix_full[i, j] = np.sum(r_i * r_j) / den if den > 1e-9 else 0.0
                
    return similarity_results, recommendations_list, top_explanation, sim_matrix_full, active_vector, active_mean


# ==========================================
# 5. MATPLOTLIB VISUALIZATIONS GENERATOR
# ==========================================
def generate_recommender_plots(sim_matrix_full, similarity_results, recommendations_list, active_mean, k=3, metric="pearson"):
    """
    Renders base64 encoded matplotlib plots showing:
    1) User-User Similarity Matrix Heatmap (9x9)
    2) Dual-Panel Diagnostics: Neighbor Similarities Ranking + Top-5 Recommendations Bar Chart
    """
    labels = ["Active User (You)"] + [u["name"].split()[0] for u in USERS]
    
    # ----------------------------------------------------
    # PLOT 1: 9x9 USER SIMILARITY HEATMAP
    # ----------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(8.5, 6.2), dpi=120)
    cmap = plt.cm.coolwarm if metric == "pearson" else plt.cm.Blues
    vmin, vmax = (-1.0, 1.0) if metric == "pearson" else (0.0, 1.0)
    
    cax = ax1.imshow(sim_matrix_full, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')
    cbar = fig1.colorbar(cax, ax=ax1, fraction=0.046, pad=0.04)
    cbar.set_label(f"Similarity Score ({metric.capitalize()})", fontsize=10, fontweight='bold')
    
    ax1.set_xticks(range(9))
    ax1.set_yticks(range(9))
    ax1.set_xticklabels(labels, rotation=35, ha='right', fontsize=9, fontweight='bold')
    ax1.set_yticklabels(labels, fontsize=9, fontweight='bold')
    
    # Text annotations in each cell
    for i in range(9):
        for j in range(9):
            val = sim_matrix_full[i, j]
            color = "white" if abs(val) > 0.6 else "black"
            ax1.text(j, i, f"{val:+.2f}" if metric == "pearson" else f"{val:.2f}",
                     ha="center", va="center", color=color, fontsize=8.5, fontweight='bold')
            
    ax1.set_title(f"User-User Pairwise Similarity Matrix ({metric.upper()} Metric)\nShowing Active User ('You') and 8 Reference Users",
                  fontsize=12, fontweight='bold', pad=12, color='#003366')
    plt.tight_layout()
    
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', bbox_inches='tight')
    buf1.seek(0)
    plot_heatmap_url = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)

    # ----------------------------------------------------
    # PLOT 2: DUAL-PANEL RECOMMENDER DIAGNOSTICS
    # (Left: Neighbor Similarities; Right: Top 5 Recommendations)
    # ----------------------------------------------------
    fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(13.0, 5.2), dpi=120)
    
    # Subplot A: Reference Users Similarity Ranking
    user_names = [r["name"].split()[0] for r in similarity_results]
    user_sims = [r["similarity"] for r in similarity_results]
    user_colors = ['#16a34a' if r["is_neighbor"] else '#64748b' for r in similarity_results]
    
    y_pos = np.arange(len(user_names))
    bars2 = ax2.barh(y_pos, user_sims, color=user_colors, edgecolor='black', linewidth=0.8, height=0.6)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(user_names, fontsize=9.5, fontweight='bold')
    ax2.invert_yaxis()  # Top user at the top
    ax2.axvline(0, color='black', linewidth=1.0, linestyle='-')
    ax2.set_xlim(-1.05 if metric == "pearson" else 0.0, 1.05)
    ax2.set_xlabel(f"Similarity Score ({metric.capitalize()})", fontsize=10, fontweight='bold')
    ax2.set_title(f"Neighbor Selection (k = {k} Nearest Neighbors in Green)", fontsize=11, fontweight='bold', color='#003366')
    ax2.grid(True, linestyle='--', alpha=0.5, axis='x')
    
    # Value annotations on bars
    for bar in bars2:
        w = bar.get_width()
        x_text = w + (0.04 if w >= 0 else -0.14)
        ax2.text(x_text, bar.get_y() + bar.get_height()/2, f"{w:+.2f}" if metric == "pearson" else f"{w:.2f}",
                 va='center', fontsize=8.5, fontweight='bold', color='#1e293b')
        
    # Subplot B: Top Recommended Movies Predicted Ratings
    top_5 = recommendations_list[:5]
    if len(top_5) > 0:
        top_titles = [m["title"] for m in top_5]
        top_scores = [m["predicted_rating"] for m in top_5]
        top_colors = [m["poster_color"] for m in top_5]
        
        y_pos3 = np.arange(len(top_titles))
        bars3 = ax3.barh(y_pos3, top_scores, color=top_colors, edgecolor='black', linewidth=0.8, height=0.6)
        ax3.set_yticks(y_pos3)
        ax3.set_yticklabels(top_titles, fontsize=9.5, fontweight='bold')
        ax3.invert_yaxis()
        ax3.set_xlim(0, 5.5)
        ax3.set_xlabel("Predicted Rating (Scale: 1 to 5 Stars)", fontsize=10, fontweight='bold')
        ax3.set_title(f"Top-{len(top_5)} Movie Recommendations for Active User", fontsize=11, fontweight='bold', color='#003366')
        ax3.grid(True, linestyle='--', alpha=0.5, axis='x')
        
        # User mean benchmark line
        ax3.axvline(active_mean, color='#b91c1c', linestyle='--', linewidth=2.0, label=f'Your Mean Rating: {active_mean:.2f}')
        ax3.legend(loc='lower right', fontsize=8.5)
        
        for bar in bars3:
            w = bar.get_width()
            ax3.text(w + 0.08, bar.get_y() + bar.get_height()/2, f"★ {w:.2f}",
                     va='center', fontsize=9, fontweight='bold', color='#003366')
    else:
        ax3.text(0.5, 0.5, "All Movies Rated! No unrated candidates.", ha='center', va='center', fontsize=12)
        ax3.set_axis_off()

    plt.tight_layout()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', bbox_inches='tight')
    buf2.seek(0)
    plot_diagnostics_url = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)

    return plot_heatmap_url, plot_diagnostics_url


# ==========================================
# 6. FLASK ROUTING CONTROLLERS
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    # Read controls from form submission or defaults
    preset_key = request.form.get('preset_key', 'scifi')
    similarity_metric = request.form.get('metric', 'pearson')
    try:
        k_neighbors = int(request.form.get('k', 3))
    except (ValueError, TypeError):
        k_neighbors = 3
    k_neighbors = max(1, min(5, k_neighbors))
    
    # Active ratings reconstruction
    active_ratings = {}
    
    # Check if a preset was explicitly loaded
    action = request.form.get('action', 'recommend')
    
    if action == 'load_preset' and preset_key in PRESETS:
        active_ratings = PRESETS[preset_key]["ratings"].copy()
    elif action == 'clear_all':
        active_ratings = {}
        preset_key = 'custom'
    else:
        # Check if individual movie ratings were submitted via the form
        for m in MOVIES:
            field_name = f"rating_{m['id']}"
            r_str = request.form.get(field_name, '')
            if r_str:
                try:
                    r_val = float(r_str)
                    if 1.0 <= r_val <= 5.0:
                        active_ratings[m['id']] = r_val
                except ValueError:
                    pass
                    
        # If no ratings provided on first GET request, initialize with default scifi preset
        if request.method == 'GET' and len(active_ratings) == 0:
            preset_key = 'scifi'
            active_ratings = PRESETS['scifi']['ratings'].copy()

    # Run Pure NumPy User-based kNN
    sim_results, recs, explanation, sim_matrix, active_vector, active_mean = compute_user_knn_recommendations(
        active_ratings, k=k_neighbors, metric=similarity_metric
    )
    
    # Generate Matplotlib Visualizations
    plot_heatmap_url, plot_diagnostics_url = generate_recommender_plots(
        sim_matrix, sim_results, recs, active_mean, k=k_neighbors, metric=similarity_metric
    )
    
    # Prepare complete ratings matrix view (Users 1-8 + Active User) for template table
    matrix_rows = []
    # Row for active user
    matrix_rows.append({
        "name": "You (Active User)",
        "persona": "Current Session Ratings",
        "mean": round(active_mean, 2),
        "is_active": True,
        "ratings": [round(active_vector[m["id"]], 1) if active_vector[m["id"]] > 0 else 0 for m in MOVIES]
    })
    for u in range(len(USERS)):
        matrix_rows.append({
            "name": USERS[u]["name"],
            "persona": USERS[u]["persona"],
            "mean": round(float(np.mean(RATINGS_MATRIX[u, RATINGS_MATRIX[u] > 0])), 2),
            "is_active": False,
            "ratings": [int(RATINGS_MATRIX[u, m["id"]]) for m in MOVIES]
        })

    # Prepare catalog items enriched with active user rating
    catalog_movies = []
    for m in MOVIES:
        m_copy = dict(m)
        m_copy["user_rating"] = active_ratings.get(m["id"], 0)
        m_copy["is_rated"] = m["id"] in active_ratings and active_ratings[m["id"]] > 0
        catalog_movies.append(m_copy)

    return render_template(
        'index.html',
        movies=catalog_movies,
        active_ratings=active_ratings,
        preset_key=preset_key,
        presets=PRESETS,
        metric=similarity_metric,
        k=k_neighbors,
        similarity_results=sim_results,
        recommendations=recs,
        top_recommendations=recs[:5],
        explanation=explanation,
        plot_heatmap_url=plot_heatmap_url,
        plot_diagnostics_url=plot_diagnostics_url,
        matrix_rows=matrix_rows,
        active_mean=round(active_mean, 2),
        rated_count=len(active_ratings)
    )


@app.route('/api/movie/<int:movie_id>')
def api_movie(movie_id):
    """API endpoint to retrieve detailed metadata for an individual movie"""
    movie = MOVIE_DICT.get(movie_id)
    if not movie:
        return {"error": "Movie not found"}, 404
    return movie


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5015))
    print(f"Starting Experiment 15 (User-Based kNN Recommender) on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
