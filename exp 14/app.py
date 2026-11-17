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
# DATASET DEFINITION: 20 MOVIES ACROSS DIVERSE GENRES + 1 NEW COLD-START ITEM
# ==============================================================================
MOVIES = [
    {
        "id": 1,
        "title": "Inception",
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "year": 2010,
        "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "rating": 4.8,
        "plot_keywords": ["dream", "subconscious", "heist", "reality", "mind-bending"],
        "description": "A skilled thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster_color": "#0f172a",
        "emoji": "🌀",
        "is_new_arrival": False
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "year": 2008,
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "rating": 4.9,
        "plot_keywords": ["batman", "joker", "vigilante", "crime-fighter", "chaos"],
        "description": "When the menace known as the Joker wreaks havoc and chaos on Gotham City, Batman must accept one of the greatest psychological tests of his ability.",
        "poster_color": "#111827",
        "emoji": "🦇",
        "is_new_arrival": False
    },
    {
        "id": 3,
        "title": "Interstellar",
        "genres": ["Sci-Fi", "Adventure", "Drama"],
        "year": 2014,
        "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "rating": 4.7,
        "plot_keywords": ["space", "black-hole", "wormhole", "time-dilation", "future"],
        "description": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot is tasked to pilot a spacecraft along with a team of researchers.",
        "poster_color": "#0c4a6e",
        "emoji": "🚀",
        "is_new_arrival": False
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama", "Thriller"],
        "year": 1994,
        "director": "Quentin Tarantino",
        "cast": "John Travolta, Samuel L. Jackson, Uma Thurman",
        "rating": 4.6,
        "plot_keywords": ["gangster", "non-linear", "dark-comedy", "heist", "redemption"],
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "poster_color": "#78350f",
        "emoji": "🔫",
        "is_new_arrival": False
    },
    {
        "id": 5,
        "title": "The Matrix",
        "genres": ["Sci-Fi", "Action"],
        "year": 1999,
        "director": "Lana Wachowski, Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "rating": 4.7,
        "plot_keywords": ["simulation", "cyberpunk", "martial-arts", "rebellion", "virtual-reality"],
        "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth: his reality is a simulation.",
        "poster_color": "#064e3b",
        "emoji": "🕶️",
        "is_new_arrival": False
    },
    {
        "id": 6,
        "title": "Forrest Gump",
        "genres": ["Drama", "Romance", "Comedy"],
        "year": 1994,
        "director": "Robert Zemeckis",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise",
        "rating": 4.5,
        "plot_keywords": ["inspirational", "historical", "running", "innocence", "destiny"],
        "description": "The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
        "poster_color": "#1e3a5f",
        "emoji": "🏃",
        "is_new_arrival": False
    },
    {
        "id": 7,
        "title": "Parasite",
        "genres": ["Thriller", "Drama", "Comedy"],
        "year": 2019,
        "director": "Bong Joon-ho",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "rating": 4.7,
        "plot_keywords": ["class-struggle", "dark-comedy", "satire", "deception", "suspense"],
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "poster_color": "#1f2937",
        "emoji": "🏠",
        "is_new_arrival": False
    },
    {
        "id": 8,
        "title": "The Godfather",
        "genres": ["Crime", "Drama"],
        "year": 1972,
        "director": "Francis Ford Coppola",
        "cast": "Marlon Brando, Al Pacino, James Caan",
        "rating": 4.9,
        "plot_keywords": ["mafia", "family", "patriarch", "crime-syndicate", "power"],
        "description": "The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son.",
        "poster_color": "#311b92",
        "emoji": "🌹",
        "is_new_arrival": False
    },
    {
        "id": 9,
        "title": "Spirited Away",
        "genres": ["Animation", "Adventure", "Fantasy"],
        "year": 2001,
        "director": "Hayao Miyazaki",
        "cast": "Rumi Hiiragi, Miyu Irino, Mari Natsuki",
        "rating": 4.6,
        "plot_keywords": ["anime", "spirits", "bathhouse", "magical", "curse"],
        "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits where humans are changed into beasts.",
        "poster_color": "#065f46",
        "emoji": "🐉",
        "is_new_arrival": False
    },
    {
        "id": 10,
        "title": "Avengers: Endgame",
        "genres": ["Action", "Sci-Fi", "Adventure"],
        "year": 2019,
        "director": "Anthony Russo, Joe Russo",
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo",
        "rating": 4.4,
        "plot_keywords": ["superhero", "marvel", "time-travel", "thanos", "cosmic"],
        "description": "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions.",
        "poster_color": "#831843",
        "emoji": "🦸",
        "is_new_arrival": False
    },
    {
        "id": 11,
        "title": "La La Land",
        "genres": ["Romance", "Drama", "Comedy"],
        "year": 2016,
        "director": "Damien Chazelle",
        "cast": "Ryan Gosling, Emma Stone, Rosemarie DeWitt",
        "rating": 4.3,
        "plot_keywords": ["jazz", "hollywood", "lovers", "musical", "aspiring-artist"],
        "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        "poster_color": "#9d174d",
        "emoji": "💃",
        "is_new_arrival": False
    },
    {
        "id": 12,
        "title": "Get Out",
        "genres": ["Horror", "Mystery", "Thriller"],
        "year": 2017,
        "director": "Jordan Peele",
        "cast": "Daniel Kaluuya, Allison Williams, Bradley Whitford",
        "rating": 4.4,
        "plot_keywords": ["racism", "hypnosis", "psychological", "thriller", "dread"],
        "description": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception reaches a boiling point.",
        "poster_color": "#3b0764",
        "emoji": "👁️",
        "is_new_arrival": False
    },
    {
        "id": 13,
        "title": "The Shining",
        "genres": ["Horror", "Drama"],
        "year": 1980,
        "director": "Stanley Kubrick",
        "cast": "Jack Nicholson, Shelley Duvall, Danny Lloyd",
        "rating": 4.5,
        "plot_keywords": ["hotel", "cabin-fever", "isolation", "madness", "supernatural"],
        "description": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings.",
        "poster_color": "#450a0a",
        "emoji": "🪓",
        "is_new_arrival": False
    },
    {
        "id": 14,
        "title": "Superbad",
        "genres": ["Comedy"],
        "year": 2007,
        "director": "Greg Mottola",
        "cast": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse",
        "rating": 4.1,
        "plot_keywords": ["high-school", "party", "friendship", "fake-id", "coming-of-age"],
        "description": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.",
        "poster_color": "#854d0e",
        "emoji": "🍻",
        "is_new_arrival": False
    },
    {
        "id": 15,
        "title": "Gladiator",
        "genres": ["Action", "Drama", "Adventure"],
        "year": 2000,
        "director": "Ridley Scott",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen",
        "rating": 4.6,
        "plot_keywords": ["rome", "gladiator", "revenge", "emperor", "arena"],
        "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "poster_color": "#581c87",
        "emoji": "⚔️",
        "is_new_arrival": False
    },
    {
        "id": 16,
        "title": "Titanic",
        "genres": ["Romance", "Drama"],
        "year": 1997,
        "director": "James Cameron",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
        "rating": 4.5,
        "plot_keywords": ["shipwreck", "class-difference", "tragedy", "forbidden-love", "1912"],
        "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "poster_color": "#134e4a",
        "emoji": "🚢",
        "is_new_arrival": False
    },
    {
        "id": 17,
        "title": "Fight Club",
        "genres": ["Drama", "Thriller"],
        "year": 1999,
        "director": "David Fincher",
        "cast": "Brad Pitt, Edward Norton, Helena Bonham Carter",
        "rating": 4.6,
        "plot_keywords": ["anti-consumerism", "alter-ego", "underground", "psychological", "chaos"],
        "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
        "poster_color": "#701a75",
        "emoji": "🥊",
        "is_new_arrival": False
    },
    {
        "id": 18,
        "title": "The Grand Budapest Hotel",
        "genres": ["Comedy", "Adventure", "Drama"],
        "year": 2014,
        "director": "Wes Anderson",
        "cast": "Ralph Fiennes, F. Murray Abraham, Mathieu Amalric",
        "rating": 4.4,
        "plot_keywords": ["hotel", "quirky", "heist", "pastel", "friendship"],
        "description": "A writer encounters the owner of an aging high-class hotel, who tells of his early years serving as a lobby boy in the glorious years of the hotel.",
        "poster_color": "#9a3412",
        "emoji": "🏨",
        "is_new_arrival": False
    },
    {
        "id": 19,
        "title": "Whiplash",
        "genres": ["Drama", "Music"],
        "year": 2014,
        "director": "Damien Chazelle",
        "cast": "Miles Teller, J.K. Simmons, Melissa Benoist",
        "rating": 4.7,
        "plot_keywords": ["drums", "jazz", "obsession", "perfection", "mentorship"],
        "description": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing.",
        "poster_color": "#1e293b",
        "emoji": "🥁",
        "is_new_arrival": False
    },
    {
        "id": 20,
        "title": "Oppenheimer",
        "genres": ["Drama", "History", "Biography"],
        "year": 2023,
        "director": "Christopher Nolan",
        "cast": "Cillian Murphy, Emily Blunt, Matt Damon",
        "rating": 4.7,
        "plot_keywords": ["atomic-bomb", "manhattan-project", "physics", "politics", "guilt"],
        "description": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
        "poster_color": "#374151",
        "emoji": "💣",
        "is_new_arrival": False
    },
    {
        "id": 21,
        "title": "Quantum Odyssey: Multiverse",
        "genres": ["Sci-Fi", "Action", "Thriller"],
        "year": 2026,
        "director": "Christopher Nolan",
        "cast": "Cillian Murphy, Elliot Page, John David Washington",
        "rating": 0.0,
        "plot_keywords": ["quantum", "spacetime", "simulation", "multiverse", "mind-bending"],
        "description": "[NEW UNRATED ARRIVAL - ITEM COLD START BENCHMARK] A theoretical physicist discovers an anomaly in quantum entanglement that allows temporal communication across parallel timelines.",
        "poster_color": "#2e1065",
        "emoji": "🔮",
        "is_new_arrival": True
    }
]

# Map ID to movie dictionary for fast lookup
MOVIE_MAP = {m["id"]: m for m in MOVIES}
ALL_GENRES = sorted(list({g for m in MOVIES for g in m["genres"]}))

# ==============================================================================
# HARDCODED USER-RATINGS MATRIX (USERS 1 TO 7 + USER 8 COLD START)
# ==============================================================================
USERS = [
    {"id": 1, "name": "Monis (User 1 - Sci-Fi / Nolan Buff)", "desc": "Loves high-concept Sci-Fi, mind-bending thrillers, and Nolan films."},
    {"id": 2, "name": "Aisha (User 2 - Romance / Musical / Drama)", "desc": "Prefers artistic romance, musicals, and heartwarming character drama."},
    {"id": 3, "name": "Rohit (User 3 - Action / Superhero / Blockbuster)", "desc": "Enjoys high-octane action, superhero spectacles, and crime sagas."},
    {"id": 4, "name": "Priya (User 4 - Psychological / Horror / Mystery)", "desc": "Loves intense psychological horror, twists, and dark suspense."},
    {"id": 5, "name": "David (User 5 - Classic Crime / Historical Drama)", "desc": "Fan of mafia epics, gritty violence, and historical masterworks."},
    {"id": 6, "name": "Sneha (User 6 - Animation / Whimsical / Comedy)", "desc": "Drawn to animated fantasy, witty comedies, and aesthetic direction."},
    {"id": 7, "name": "Vikram (User 7 - Eclectic Cinephile)", "desc": "High-volume viewer rating across diverse genres."},
    {"id": 8, "name": "Guest / New User (User 8 - Cold Start 0 Ratings)", "desc": "Completely new user with zero prior ratings in the system."}
]

# Baseline ratings matrix: rows=users 1..7, cols=movies 1..20 (scale 1-5, 0=unrated)
# Note: Movie 21 is a brand-new release with 0 collaborative ratings for everyone!
BASE_RATINGS = np.array([
    # M1  M2  M3  M4  M5  M6  M7  M8  M9 M10 M11 M12 M13 M14 M15 M16 M17 M18 M19 M20
    [ 5,  5,  5,  0,  5,  0,  0,  0,  0,  4,  0,  0,  0,  0,  0,  0,  4,  0,  0,  5], # User 1: Monis
    [ 0,  0,  0,  0,  0,  5,  0,  0,  4,  0,  5,  0,  0,  0,  0,  5,  0,  4,  4,  0], # User 2: Aisha
    [ 4,  5,  0,  4,  4,  0,  0,  0,  0,  5,  0,  0,  0,  4,  5,  0,  0,  0,  0,  0], # User 3: Rohit
    [ 4,  0,  0,  4,  0,  0,  5,  0,  0,  0,  0,  5,  5,  0,  0,  0,  5,  0,  0,  0], # User 4: Priya
    [ 0,  4,  0,  5,  0,  0,  0,  5,  0,  0,  0,  0,  4,  0,  4,  0,  4,  0,  0,  5], # User 5: David
    [ 0,  0,  0,  0,  0,  4,  4,  0,  5,  0,  4,  0,  0,  5,  0,  0,  0,  5,  0,  0], # User 6: Sneha
    [ 4,  5,  5,  4,  4,  3,  5,  4,  0,  4,  0,  3,  0,  0,  5,  0,  4,  4,  5,  4], # User 7: Vikram
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]  # User 8: Cold Start
], dtype=float)

# ==============================================================================
# ALGORITHM IMPLEMENTATION FROM SCRATCH (NUMPY ONLY)
# ==============================================================================

def compute_content_similarity_matrix():
    """
    Constructs multi-hot attribute vectors from genres, directors, and plot keywords
    for all 21 movies and calculates pure cosine similarity from scratch.
    """
    # 1. Build attribute vocabulary
    vocab = set()
    for m in MOVIES:
        for g in m["genres"]:
            vocab.add(f"genre:{g}")
        vocab.add(f"dir:{m['director']}")
        for kw in m["plot_keywords"]:
            vocab.add(f"kw:{kw}")
    vocab = sorted(list(vocab))
    vocab_map = {word: i for i, word in enumerate(vocab)}
    
    n_movies = len(MOVIES)
    n_features = len(vocab)
    F = np.zeros((n_movies, n_features), dtype=float)
    
    for i, m in enumerate(MOVIES):
        for g in m["genres"]:
            F[i, vocab_map[f"genre:{g}"]] = 2.0  # Weight genres higher
        F[i, vocab_map[f"dir:{m['director']}"]] = 1.5  # Weight director
        for kw in m["plot_keywords"]:
            F[i, vocab_map[f"kw:{kw}"]] = 1.0
            
    # L2 normalize rows
    norms = np.linalg.norm(F, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    F_norm = F / norms
    
    # Cosine similarity matrix: S = F_norm @ F_norm.T
    sim_matrix = np.dot(F_norm, F_norm.T)
    return sim_matrix, vocab


SIM_MATRIX, VOCAB = compute_content_similarity_matrix()


def calculate_bayesian_popularity(ratings_mat, m_threshold=2.0):
    """
    Computes IMDB / Bayesian Weighted Rating for each movie:
    WR = (v / (v + m)) * R + (m / (v + m)) * C
    v = number of non-zero ratings
    m = minimum rating confidence parameter (threshold)
    R = movie average rating
    C = global mean rating across all observed ratings
    """
    num_users, num_movies = ratings_mat.shape
    v = np.sum(ratings_mat > 0, axis=0)
    
    # Compute movie mean rating R
    R = np.zeros(num_movies)
    for j in range(num_movies):
        rated_entries = ratings_mat[ratings_mat[:, j] > 0, j]
        if len(rated_entries) > 0:
            R[j] = np.mean(rated_entries)
        else:
            R[j] = MOVIES[j]["rating"] if MOVIES[j]["rating"] > 0 else 3.5

    # Global mean C
    all_positive = ratings_mat[ratings_mat > 0]
    C = np.mean(all_positive) if len(all_positive) > 0 else 4.0
    
    # Bayesian weighted ratings
    WR = np.zeros(num_movies)
    for j in range(num_movies):
        if (v[j] + m_threshold) > 0:
            WR[j] = (v[j] / (v[j] + m_threshold)) * R[j] + (m_threshold / (v[j] + m_threshold)) * C
        else:
            WR[j] = C
            
    return WR, v, R, C


def recommend_for_user(user_vector, ratings_mat, selected_genres=None, k_warm_threshold=4.0):
    """
    Comprehensive recommender that dynamically solves the Cold-Start problem:
    - User Cold-Start: If user_vector has few/no ratings (k < k_warm_threshold),
      blends Bayesian Popularity & Genre Onboarding prior with emergent Collaborative Filtering.
    - Blending factor alpha_k = min(1.0, k / k_warm_threshold)
    - Item Cold-Start: For Movie 21 (0 collaborative ratings), projects its rating using
      attribute cosine similarity with existing items.
    """
    n_users, n_catalog_movies = ratings_mat.shape  # 8 users, 20 catalog movies
    k = np.sum(user_vector > 0)  # number of movies user has rated
    
    # Dynamic blending weight: 0.0 for pure new user, 1.0 for warm user (>= 4 ratings)
    alpha = min(1.0, float(k) / float(k_warm_threshold))
    
    # 1. COLD COMPONENT: Bayesian Weighted Rating Popularity
    WR, v_counts, avg_R, C_global = calculate_bayesian_popularity(ratings_mat)
    cold_scores = WR.copy()
    
    # If user selected preferred genres upon onboarding, boost relevant genres
    if selected_genres and len(selected_genres) > 0:
        for j in range(n_catalog_movies):
            movie_genres = set(MOVIES[j]["genres"])
            common = movie_genres.intersection(set(selected_genres))
            if len(common) > 0:
                overlap_ratio = len(common) / len(movie_genres)
                cold_scores[j] *= (1.0 + 0.35 * overlap_ratio)
                
    # 2. WARM COMPONENT: Collaborative + Content Filtering
    warm_scores = np.zeros(n_catalog_movies)
    
    if k > 0:
        # User-based Collaborative Filtering with mean centering
        # Compute user similarity with existing users (excluding self / user 8)
        user_mean = np.mean(user_vector[user_vector > 0]) if k > 0 else C_global
        user_centered = np.zeros_like(user_vector)
        mask = user_vector > 0
        user_centered[mask] = user_vector[mask] - user_mean
        
        cf_preds = np.zeros(n_catalog_movies)
        for j in range(n_catalog_movies):
            if user_vector[j] > 0:
                cf_preds[j] = user_vector[j]
                continue
                
            sim_weights = []
            rating_diffs = []
            
            for u in range(n_users - 1): # compare with known users 0..6
                other_vec = ratings_mat[u]
                other_rated = other_vec > 0
                common_rated = mask & other_rated
                
                if np.sum(common_rated) >= 1:
                    other_mean = np.mean(other_vec[other_rated])
                    # Pearson / Cosine correlation on common items
                    u_c = user_vector[common_rated] - user_mean
                    o_c = other_vec[common_rated] - other_mean
                    denom = (np.linalg.norm(u_c) * np.linalg.norm(o_c)) + 1e-6
                    sim = np.dot(u_c, o_c) / denom if denom > 1e-5 else 0.0
                    
                    if sim > 0 and other_vec[j] > 0:
                        sim_weights.append(sim)
                        rating_diffs.append(other_vec[j] - other_mean)
                        
            if len(sim_weights) > 0 and np.sum(sim_weights) > 0:
                cf_preds[j] = user_mean + (np.sum(np.array(sim_weights) * np.array(rating_diffs)) / np.sum(sim_weights))
            else:
                # Content-based fallback to user's liked movies
                liked_indices = np.where(user_vector >= 4.0)[0]
                if len(liked_indices) > 0:
                    sims_to_liked = [SIM_MATRIX[j, idx] for idx in liked_indices]
                    cf_preds[j] = user_mean + 0.8 * np.mean(sims_to_liked)
                else:
                    cf_preds[j] = WR[j]
                    
        warm_scores = np.clip(cf_preds, 1.0, 5.0)
    else:
        warm_scores = cold_scores.copy()
        
    # 3. HYBRID BLENDED RECOMMENDATION SCORE FOR CATALOG MOVIES
    hybrid_scores = (1.0 - alpha) * cold_scores + alpha * warm_scores
    
    # 4. ITEM COLD-START RESOLUTION (Movie 21: Brand New Unrated Arrival)
    # Movie 21 has zero collaborative ratings. We predict its score by projecting via attribute similarity!
    new_movie_idx = 20  # index of Movie 21
    # Find top 4 attribute-similar catalog movies
    sim_to_catalog = SIM_MATRIX[new_movie_idx, :n_catalog_movies]
    top_neighbor_indices = np.argsort(sim_to_catalog)[::-1][:4]
    
    # Predict rating for new item for current user
    neighbor_sims = sim_to_catalog[top_neighbor_indices]
    
    # If user has rated any neighbors, use user's own ratings
    user_neighbor_ratings = [user_vector[idx] for idx in top_neighbor_indices if user_vector[idx] > 0]
    if len(user_neighbor_ratings) > 0:
        # Weighted combination of user's ratings on similar items
        rated_sims = [sim_to_catalog[idx] for idx in top_neighbor_indices if user_vector[idx] > 0]
        new_item_score = float(np.sum(np.array(rated_sims) * np.array(user_neighbor_ratings)) / (np.sum(rated_sims) + 1e-6))
        new_item_reason = f"Attribute projection from your watched similar movies: {', '.join([MOVIES[idx]['title'] for idx in top_neighbor_indices if user_vector[idx] > 0])}"
    else:
        # Fallback to Bayesian popularity of the nearest neighbor items
        neighbor_wr = [WR[idx] for idx in top_neighbor_indices]
        new_item_score = float(np.sum(neighbor_sims * np.array(neighbor_wr)) / (np.sum(neighbor_sims) + 1e-6))
        new_item_reason = f"Cold Item Attribute Matching: High similarity to {MOVIES[top_neighbor_indices[0]]['title']} (sim={neighbor_sims[0]:.2f}) and {MOVIES[top_neighbor_indices[1]]['title']} (sim={neighbor_sims[1]:.2f})"
        
    new_item_data = {
        "movie": MOVIES[new_movie_idx],
        "predicted_score": round(new_item_score, 2),
        "neighbors": [
            {
                "title": MOVIES[idx]["title"],
                "similarity": round(float(sim_to_catalog[idx]), 3),
                "user_rating": int(user_vector[idx]) if user_vector[idx] > 0 else "Unrated",
                "wr_popularity": round(float(WR[idx]), 2)
            }
            for idx in top_neighbor_indices
        ],
        "reason": new_item_reason
    }
    
    # Build complete recommendation list
    recs = []
    for j in range(n_catalog_movies):
        # Exclude movies already rated by user if interactive, or display with status
        is_already_rated = (user_vector[j] > 0)
        
        # Decide recommendation rationale label
        if k == 0:
            rec_mode = "Cold-Start Popularity Prior"
            if selected_genres and any(g in selected_genres for g in MOVIES[j]["genres"]):
                reason = f"Top Bayesian popularity weighted by your onboarding genre preference ({', '.join(set(selected_genres).intersection(MOVIES[j]['genres']))})"
            else:
                reason = f"High global consensus (v={int(v_counts[j])} ratings, Bayesian WR={WR[j]:.2f})"
        elif k < k_warm_threshold:
            rec_mode = f"Cold-to-Warm Hybrid Transition (α={alpha:.2f})"
            reason = f"Blended {int((1-alpha)*100)}% cold popularity prior + {int(alpha*100)}% personalized similarity"
        else:
            rec_mode = "Warm Personalized Collaborative"
            reason = "High personalized peer similarity and content affinity to your ratings"
            
        recs.append({
            "movie": MOVIES[j],
            "score": round(float(hybrid_scores[j]), 2),
            "cold_component": round(float(cold_scores[j]), 2),
            "warm_component": round(float(warm_scores[j]), 2),
            "alpha": round(alpha, 2),
            "rec_mode": rec_mode,
            "reason": reason,
            "is_rated": is_already_rated,
            "user_rating": int(user_vector[j]) if is_already_rated else None
        })
        
    # Sort unrated recommendations first, descending by hybrid score
    unrated_recs = [r for r in recs if not r["is_rated"]]
    rated_recs = [r for r in recs if r["is_rated"]]
    unrated_recs.sort(key=lambda x: x["score"], reverse=True)
    rated_recs.sort(key=lambda x: x["score"], reverse=True)
    
    final_recommendations = unrated_recs + rated_recs
    
    stats = {
        "k_rated": int(k),
        "alpha": round(alpha, 3),
        "cold_weight_pct": round((1.0 - alpha) * 100, 1),
        "warm_weight_pct": round(alpha * 100, 1),
        "global_mean_C": round(float(C_global), 2),
        "total_catalog_movies": n_catalog_movies,
        "active_mode": "New User Cold Start" if k == 0 else ("Cold-to-Warm Transition" if k < k_warm_threshold else "Warm Collaborative")
    }
    
    return final_recommendations, new_item_data, stats, WR, cold_scores, warm_scores, hybrid_scores


def generate_visualization(user_vector, ratings_mat, recs, new_item_data, stats):
    """
    Generates a 3-panel publication-grade figure:
    1. Cold-to-Warm Transition curve showing dynamic weight alpha_k vs number of rated movies.
    2. Recommendation Score Decomposition (Cold Prior vs Personalized Warm) for top movies.
    3. Item Attribute Cosine Similarity Heatmap showcasing New Item Cold Start projection.
    """
    k_curr = stats["k_rated"]
    alpha_curr = stats["alpha"]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5.2), dpi=120)
    
    # --------------------------------------------------------------------------
    # PANEL 1: Dynamic Cold-to-Warm Transition Curves
    # --------------------------------------------------------------------------
    k_vals = np.linspace(0, 7, 100)
    alpha_vals = np.minimum(1.0, k_vals / 4.0)
    cold_weights = 1.0 - alpha_vals
    
    ax1.plot(k_vals, cold_weights, color='#dc2626', linewidth=2.5, linestyle='--', label='Cold Prior Weight (1 - αₖ)')
    ax1.plot(k_vals, alpha_vals, color='#2563eb', linewidth=2.5, linestyle='-', label='Warm Personalized Weight (αₖ)')
    ax1.axvline(4.0, color='#6b7280', linestyle=':', label='Warm Saturation Threshold (K=4)')
    
    # Current user operating point
    ax1.scatter([k_curr], [1.0 - alpha_curr], color='#dc2626', s=100, zorder=5, edgecolors='black')
    ax1.scatter([k_curr], [alpha_curr], color='#2563eb', s=100, zorder=5, edgecolors='black')
    ax1.annotate(f'Active User: k={k_curr}\nα={alpha_curr:.2f}', 
                 xy=(k_curr, alpha_curr), 
                 xytext=(k_curr + 0.35, alpha_curr - 0.15 if alpha_curr > 0.5 else alpha_curr + 0.15),
                 bbox=dict(boxstyle='round,pad=0.3', fc='#fef3c7', ec='#d97706', lw=1.2),
                 fontsize=8.5, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#b45309'))
    
    ax1.set_title('Panel 1: Cold-to-Warm Dynamic Blending Factor', fontsize=10.5, fontweight='bold', color='#003366')
    ax1.set_xlabel('Number of Movies Rated by User (k)', fontsize=9.5)
    ax1.set_ylabel('Component Weight in Final Score', fontsize=9.5)
    ax1.set_ylim(-0.05, 1.08)
    ax1.set_xlim(-0.2, 7.2)
    ax1.grid(True, linestyle='--', alpha=0.45)
    ax1.legend(loc='center right', fontsize=8)
    
    # --------------------------------------------------------------------------
    # PANEL 2: Top-6 Recommendation Score Decomposition
    # --------------------------------------------------------------------------
    top_recs = [r for r in recs if not r["is_rated"]][:6]
    if len(top_recs) == 0:
        top_recs = recs[:6]
        
    titles = [r["movie"]["title"][:14] for r in top_recs][::-1]
    cold_parts = [(1.0 - alpha_curr) * r["cold_component"] for r in top_recs][::-1]
    warm_parts = [alpha_curr * r["warm_component"] for r in top_recs][::-1]
    y_pos = np.arange(len(titles))
    
    ax2.barh(y_pos, cold_parts, color='#f87171', edgecolor='#991b1b', height=0.55, label='Cold Popularity Prior')
    ax2.barh(y_pos, warm_parts, left=cold_parts, color='#60a5fa', edgecolor='#1e40af', height=0.55, label='Personalized Collaborative')
    
    for i, (cp, wp) in enumerate(zip(cold_parts, warm_parts)):
        total = cp + wp
        ax2.text(total + 0.08, i, f"{total:.2f}★", va='center', fontsize=8.5, fontweight='bold', color='#111827')
        
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(titles, fontsize=9)
    ax2.set_title('Panel 2: Top Recommendations Score Breakdown', fontsize=10.5, fontweight='bold', color='#003366')
    ax2.set_xlabel('Blended Recommendation Score (1 - 5 Stars)', fontsize=9.5)
    ax2.set_xlim(0, 5.5)
    ax2.grid(True, linestyle='--', alpha=0.45, axis='x')
    ax2.legend(loc='lower right', fontsize=8)
    
    # --------------------------------------------------------------------------
    # PANEL 3: Attribute Cosine Similarity Heatmap (with New Item Cold Start)
    # --------------------------------------------------------------------------
    # Focus on key representative movies + Movie 21 (New Arrival)
    sample_indices = [0, 1, 2, 4, 6, 7, 9, 10, 11, 20] # Inception, Dark Knight, Interstellar, Matrix, Parasite, Godfather, Endgame, La La Land, Get Out, Quantum Odyssey
    sub_sim = SIM_MATRIX[np.ix_(sample_indices, sample_indices)]
    sample_labels = [MOVIES[i]["title"][:10] for i in sample_indices]
    sample_labels[-1] = "★ NEW: Quantum" # Highlight new item
    
    im = ax3.imshow(sub_sim, cmap='YlGnBu', vmin=0.0, vmax=1.0)
    ax3.set_xticks(np.arange(len(sample_labels)))
    ax3.set_yticks(np.arange(len(sample_labels)))
    ax3.set_xticklabels(sample_labels, rotation=45, ha='right', fontsize=7.5)
    ax3.set_yticklabels(sample_labels, fontsize=7.5)
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(sample_labels)):
        for j in range(len(sample_labels)):
            val = sub_sim[i, j]
            color = "white" if val > 0.55 else "black"
            if i == len(sample_labels) - 1 or j == len(sample_labels) - 1:
                # Highlight new item row/column
                ax3.text(j, i, f"{val:.2f}", ha="center", va="center", color="#b91c1c" if val > 0.4 else color, fontsize=7, fontweight='bold')
            else:
                ax3.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=6.8)
                
    ax3.set_title('Panel 3: Attribute Cosine Matrix & Item Cold Start', fontsize=10.5, fontweight='bold', color='#003366')
    cbar = fig.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=8)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return plot_url


# ==============================================================================
# FLASK WEB APPLICATION CONTROLLER / ROUTES
# ==============================================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    # 1. Determine active user and mode
    user_id = int(request.values.get('user_id', 8))  # default User 8 (Cold Start)
    mode = request.values.get('mode', 'new_user')
    selected_movie_id = int(request.values.get('detail_id', 1))
    
    # Retrieve user ratings vector
    # We maintain a session/interactive array for User 8 or override for users 1-7
    user_vector = BASE_RATINGS[user_id - 1].copy()
    
    # Process onboarding genres if provided
    selected_genres = request.values.getlist('selected_genres')
    if not selected_genres and mode == 'new_user':
        # Default starter onboarding tags if none selected
        selected_genres = ["Action", "Sci-Fi"]
        
    # Check if a movie rating was submitted
    rate_movie_id = request.values.get('rate_movie_id')
    rate_score = request.values.get('rate_score')
    
    # Parse interactive custom ratings passed from form
    for m in MOVIES:
        param_name = f"rating_{m['id']}"
        if param_name in request.values:
            try:
                val = float(request.values.get(param_name))
                if 0 <= val <= 5:
                    user_vector[m['id'] - 1] = val
            except (ValueError, TypeError):
                pass
                
    if rate_movie_id and rate_score:
        try:
            mid = int(rate_movie_id)
            score = float(rate_score)
            if 1 <= mid <= 20 and 1 <= score <= 5:
                user_vector[mid - 1] = score
                mode = 'interactive'
        except (ValueError, TypeError):
            pass
            
    # Reset ratings button handler
    if request.values.get('action') == 'reset_ratings':
        user_vector = np.zeros(20, dtype=float)
        mode = 'new_user'
        user_id = 8
        selected_genres = ["Action", "Sci-Fi"]
        
    # 2. Run Recommender Engine with Cold Start Solutions
    ratings_mat = BASE_RATINGS.copy()
    ratings_mat[user_id - 1] = user_vector
    
    recs, new_item_data, stats, WR, cold_scores, warm_scores, hybrid_scores = recommend_for_user(
        user_vector=user_vector,
        ratings_mat=ratings_mat,
        selected_genres=selected_genres
    )
    
    # 3. Generate Visualizations
    plot_url = generate_visualization(user_vector, ratings_mat, recs, new_item_data, stats)
    
    # 4. Prepare data for template
    selected_movie = MOVIE_MAP.get(selected_movie_id, MOVIES[0])
    
    # Top 3 similar movies to selected movie
    sel_sims = SIM_MATRIX[selected_movie_id - 1]
    sim_indices = np.argsort(sel_sims)[::-1]
    similar_to_selected = [
        {
            "movie": MOVIES[idx],
            "similarity": round(float(sel_sims[idx]), 3)
        }
        for idx in sim_indices if idx != (selected_movie_id - 1)
    ][:4]
    
    return render_template(
        'index.html',
        movies=MOVIES,
        users=USERS,
        active_user_id=user_id,
        user_vector=user_vector.tolist(),
        selected_genres=selected_genres,
        all_genres=ALL_GENRES,
        mode=mode,
        recs=recs,
        new_item_data=new_item_data,
        stats=stats,
        plot_url=plot_url,
        selected_movie=selected_movie,
        similar_to_selected=similar_to_selected,
        ratings_mat=ratings_mat.tolist()
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5014))
    print(f"Starting Experiment 14 Cold Start Recommender Server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
