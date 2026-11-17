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
# 1. MOVIES DATASET (20 Movies across diverse genres)
# ==============================================================================
MOVIES = [
    {
        "id": 0,
        "title": "Inception",
        "year": 2010,
        "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "genres": ["Sci-Fi", "Action", "Thriller"],
        "imdb_rating": 8.8,
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "keywords": ["dream", "heist", "subconscious", "mind-bending", "reality", "time-dilation"],
        "icon": "🌀",
        "color": "#1e3a8a",
        "initials": "INC"
    },
    {
        "id": 1,
        "title": "Interstellar",
        "year": 2014,
        "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "genres": ["Sci-Fi", "Drama", "Adventure"],
        "imdb_rating": 8.7,
        "description": "A team of explorers travels through a wormhole in space in an attempt to ensure humanity's survival as Earth faces catastrophic blight.",
        "keywords": ["space", "wormhole", "black-hole", "time-dilation", "astronaut", "survival"],
        "icon": "🚀",
        "color": "#0f172a",
        "initials": "INT"
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "year": 2008,
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "genres": ["Action", "Crime", "Drama"],
        "imdb_rating": 9.0,
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.",
        "keywords": ["superhero", "joker", "vigilante", "gotham", "justice", "chaos"],
        "icon": "🦇",
        "color": "#1e293b",
        "initials": "TDK"
    },
    {
        "id": 3,
        "title": "Pulp Fiction",
        "year": 1994,
        "director": "Quentin Tarantino",
        "cast": "John Travolta, Uma Thurman, Samuel L. Jackson",
        "genres": ["Crime", "Drama"],
        "imdb_rating": 8.9,
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "keywords": ["mobster", "heist", "nonlinear", "dialogue", "hitman", "los-angeles"],
        "icon": "🕶️",
        "color": "#7f1d1d",
        "initials": "PLF"
    },
    {
        "id": 4,
        "title": "Django Unchained",
        "year": 2012,
        "director": "Quentin Tarantino",
        "cast": "Jamie Foxx, Christoph Waltz, Leonardo DiCaprio",
        "genres": ["Drama", "Western", "Action"],
        "imdb_rating": 8.4,
        "description": "With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner.",
        "keywords": ["bounty-hunter", "revenge", "western", "slavery", "shootout", "plantation"],
        "icon": "🤠",
        "color": "#9a3412",
        "initials": "DJU"
    },
    {
        "id": 5,
        "title": "The Matrix",
        "year": 1999,
        "director": "Lana & Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "genres": ["Sci-Fi", "Action"],
        "imdb_rating": 8.7,
        "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is an elaborate deception.",
        "keywords": ["simulation", "cyberpunk", "AI", "martial-arts", "reality", "rebel"],
        "icon": "💊",
        "color": "#064e3b",
        "initials": "MTX"
    },
    {
        "id": 6,
        "title": "Parasite",
        "year": 2019,
        "director": "Bong Joon-ho",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "genres": ["Drama", "Thriller", "Comedy"],
        "imdb_rating": 8.5,
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "keywords": ["social-inequality", "satire", "class-struggle", "con-artist", "deception", "dark-comedy"],
        "icon": "🏠",
        "color": "#3f3f46",
        "initials": "PAR"
    },
    {
        "id": 7,
        "title": "Superbad",
        "year": 2007,
        "director": "Greg Mottola",
        "cast": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse",
        "genres": ["Comedy"],
        "imdb_rating": 7.6,
        "description": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.",
        "keywords": ["high-school", "teenage", "party", "friendship", "coming-of-age", "fake-id"],
        "icon": "🍺",
        "color": "#b45309",
        "initials": "SPB"
    },
    {
        "id": 8,
        "title": "The Hangover",
        "year": 2009,
        "director": "Todd Phillips",
        "cast": "Bradley Cooper, Ed Helms, Zach Galifianakis",
        "genres": ["Comedy"],
        "imdb_rating": 7.7,
        "description": "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend.",
        "keywords": ["bachelor-party", "las-vegas", "hangover", "wedding", "mystery", "chaos"],
        "icon": "🎰",
        "color": "#d97706",
        "initials": "HNG"
    },
    {
        "id": 9,
        "title": "La La Land",
        "year": 2016,
        "director": "Damien Chazelle",
        "cast": "Ryan Gosling, Emma Stone, John Legend",
        "genres": ["Romance", "Drama", "Comedy"],
        "imdb_rating": 8.0,
        "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        "keywords": ["jazz", "musical", "hollywood", "romance", "ambition", "artists"],
        "icon": "🎷",
        "color": "#4338ca",
        "initials": "LLL"
    },
    {
        "id": 10,
        "title": "Titanic",
        "year": 1997,
        "director": "James Cameron",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
        "genres": ["Romance", "Drama"],
        "imdb_rating": 7.9,
        "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "keywords": ["shipwreck", "luxury-liner", "romance", "tragedy", "ocean", "survival"],
        "icon": "🚢",
        "color": "#1e40af",
        "initials": "TTN"
    },
    {
        "id": 11,
        "title": "The Conjuring",
        "year": 2013,
        "director": "James Wan",
        "cast": "Patrick Wilson, Vera Farmiga, Ron Livingston",
        "genres": ["Horror", "Thriller"],
        "imdb_rating": 7.5,
        "description": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.",
        "keywords": ["paranormal", "haunted-house", "exorcism", "ghost", "supernatural", "demons"],
        "icon": "👻",
        "color": "#18181b",
        "initials": "CNJ"
    },
    {
        "id": 12,
        "title": "A Quiet Place",
        "year": 2018,
        "director": "John Krasinski",
        "cast": "Emily Blunt, John Krasinski, Millicent Simmonds",
        "genres": ["Horror", "Sci-Fi", "Drama"],
        "imdb_rating": 7.5,
        "description": "In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing.",
        "keywords": ["sound-monsters", "post-apocalyptic", "silence", "survival", "family", "alien"],
        "icon": "🤫",
        "color": "#374151",
        "initials": "AQP"
    },
    {
        "id": 13,
        "title": "Avengers: Endgame",
        "year": 2019,
        "director": "Anthony & Joe Russo",
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo",
        "genres": ["Action", "Sci-Fi", "Adventure"],
        "imdb_rating": 8.4,
        "description": "After devastating events, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions.",
        "keywords": ["superhero", "time-heist", "thanos", "marvel", "cosmic", "epic"],
        "icon": "🛡️",
        "color": "#831843",
        "initials": "AVG"
    },
    {
        "id": 14,
        "title": "The Shawshank Redemption",
        "year": 1994,
        "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "genres": ["Drama"],
        "imdb_rating": 9.3,
        "description": "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
        "keywords": ["prison-escape", "wrongful-conviction", "friendship", "hope", "redemption", "corruption"],
        "icon": "⛓️",
        "color": "#475569",
        "initials": "SHA"
    },
    {
        "id": 15,
        "title": "The Godfather",
        "year": 1972,
        "director": "Francis Ford Coppola",
        "cast": "Marlon Brando, Al Pacino, James Caan",
        "genres": ["Crime", "Drama"],
        "imdb_rating": 9.2,
        "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant youngest son.",
        "keywords": ["mafia", "family", "organized-crime", "power", "betrayal", "legacy"],
        "icon": "🍷",
        "color": "#450a0a",
        "initials": "GDF"
    },
    {
        "id": 16,
        "title": "Whiplash",
        "year": 2014,
        "director": "Damien Chazelle",
        "cast": "Miles Teller, J.K. Simmons, Paul Reiser",
        "genres": ["Drama"],
        "imdb_rating": 8.5,
        "description": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing.",
        "keywords": ["drumming", "jazz", "music", "obsession", "perfectionism", "teacher-student"],
        "icon": "🥁",
        "color": "#78350f",
        "initials": "WHP"
    },
    {
        "id": 17,
        "title": "Blade Runner 2049",
        "year": 2017,
        "director": "Denis Villeneuve",
        "cast": "Ryan Gosling, Harrison Ford, Ana de Armas",
        "genres": ["Sci-Fi", "Drama", "Mystery"],
        "imdb_rating": 8.0,
        "description": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.",
        "keywords": ["cyberpunk", "replicant", "identity", "future", "dystopia", "detective"],
        "icon": "🤖",
        "color": "#14532d",
        "initials": "BLR"
    },
    {
        "id": 18,
        "title": "Get Out",
        "year": 2017,
        "director": "Jordan Peele",
        "cast": "Daniel Kaluuya, Allison Williams, Bradley Whitford",
        "genres": ["Horror", "Mystery", "Thriller"],
        "imdb_rating": 7.8,
        "description": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him reaches a boiling point.",
        "keywords": ["psychological", "hypnosis", "racial-tension", "suspense", "thriller", "mind-control"],
        "icon": "👁️",
        "color": "#022c22",
        "initials": "GTO"
    },
    {
        "id": 19,
        "title": "Crazy, Stupid, Love.",
        "year": 2011,
        "director": "Glenn Ficarra & John Requa",
        "cast": "Steve Carell, Ryan Gosling, Julianne Moore",
        "genres": ["Comedy", "Romance"],
        "imdb_rating": 7.4,
        "description": "A middle-aged husband's life changes dramatically when his wife asks him for a divorce. He seeks to rediscover his manhood with help from a newfound friend.",
        "keywords": ["divorce", "dating", "pickup-artist", "marriage", "romance", "family"],
        "icon": "💘",
        "color": "#be185d",
        "initials": "CSL"
    }
]

# Vocabulary of Genres and Keywords
ALL_GENRES = sorted(list(set([g for m in MOVIES for g in m["genres"]])))
ALL_DIRECTORS = sorted(list(set([m["director"] for m in MOVIES])))
ALL_KEYWORDS = sorted(list(set([k for m in MOVIES for k in m["keywords"]])))

# ==============================================================================
# 2. CONTENT-BASED FEATURE MATRIX & COSINE SIMILARITY FROM SCRATCH
# ==============================================================================
def build_content_feature_matrix():
    n_movies = len(MOVIES)
    n_feat = len(ALL_GENRES) + len(ALL_KEYWORDS) + len(ALL_DIRECTORS)
    X = np.zeros((n_movies, n_feat), dtype=np.float64)
    
    for i, m in enumerate(MOVIES):
        # Multi-hot genre encoding (weight = 2.0 for strong genre signal)
        for g in m["genres"]:
            idx = ALL_GENRES.index(g)
            X[i, idx] = 2.0
            
        # Multi-hot keyword encoding (weight = 1.0)
        offset1 = len(ALL_GENRES)
        for k in m["keywords"]:
            idx = offset1 + ALL_KEYWORDS.index(k)
            X[i, idx] = 1.0
            
        # One-hot director encoding (weight = 1.5)
        offset2 = offset1 + len(ALL_KEYWORDS)
        idx = offset2 + ALL_DIRECTORS.index(m["director"])
        X[i, idx] = 1.5
        
    return X

MOVIE_FEATURE_MATRIX = build_content_feature_matrix()

def compute_content_similarity_matrix(X):
    # Cosine Similarity: S_ij = (X_i . X_j) / (||X_i|| * ||X_j||)
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms[norms == 0] = 1e-9
    X_norm = X / norms
    sim_matrix = np.dot(X_norm, X_norm.T)
    # Clip numerical precision to [0, 1]
    return np.clip(sim_matrix, 0.0, 1.0)

CONTENT_SIM_MATRIX = compute_content_similarity_matrix(MOVIE_FEATURE_MATRIX)

# ==============================================================================
# 3. COLLABORATIVE FILTERING: USER-RATINGS MATRIX (8 Benchmarks + 1 Active)
# ==============================================================================
USER_NAMES = [
    "U1: Alex (Sci-Fi / Tech)",
    "U2: Beth (Crime & Drama)",
    "U3: Charlie (Rom-Com)",
    "U4: Diana (Horror/Thriller)",
    "U5: Evan (Nolan Auteur)",
    "U6: Fiona (Action Hits)",
    "U7: George (Indie/Critique)",
    "U8: Hannah (Casual Eclectic)"
]

# 8 Historical Users x 20 Movies Rating Matrix (0 = Unrated)
# Columns correspond to movie IDs 0 through 19
INITIAL_RATINGS = np.array([
    # 0:INC, 1:INT, 2:TDK, 3:PLF, 4:DJU, 5:MTX, 6:PAR, 7:SPB, 8:HNG, 9:LLL, 10:TTN, 11:CNJ, 12:AQP, 13:AVG, 14:SHA, 15:GDF, 16:WHP, 17:BLR, 18:GTO, 19:CSL
    [5, 5, 4, 0, 0, 5, 3, 1, 2, 0, 1, 0, 3, 4, 0, 0, 0, 5, 2, 0],  # U1: Sci-Fi / Tech
    [0, 0, 4, 5, 4, 0, 5, 0, 0, 0, 0, 1, 0, 0, 5, 5, 5, 0, 4, 0],  # U2: Crime & Drama
    [0, 0, 0, 0, 0, 1, 3, 4, 4, 5, 5, 1, 0, 2, 3, 0, 0, 0, 0, 5],  # U3: Rom-Com
    [3, 0, 4, 0, 0, 0, 4, 2, 0, 1, 0, 5, 5, 0, 0, 0, 0, 3, 5, 0],  # U4: Horror/Thriller
    [5, 5, 5, 3, 0, 4, 4, 1, 1, 0, 0, 0, 2, 2, 4, 0, 4, 5, 0, 0],  # U5: Nolan Auteur
    [4, 0, 5, 3, 4, 4, 0, 3, 4, 0, 3, 0, 0, 5, 4, 0, 0, 3, 0, 0],  # U6: Action Hits
    [0, 3, 0, 5, 4, 0, 5, 0, 0, 4, 0, 0, 3, 1, 5, 5, 5, 4, 5, 0],  # U7: Indie/Critique
    [4, 4, 4, 0, 3, 3, 0, 3, 3, 3, 4, 0, 0, 4, 4, 3, 0, 0, 0, 3]   # U8: Casual Eclectic
], dtype=np.float64)

# Default Active User (Monis) ratings: Sci-Fi & Auteur oriented
DEFAULT_ACTIVE_RATINGS = {
    0: 5,   # Inception: 5
    1: 5,   # Interstellar: 5
    2: 4,   # The Dark Knight: 4
    5: 4    # The Matrix: 4
}

# ==============================================================================
# 4. RECOMMENDER ALGORITHM ENGINES (FROM SCRATCH IN NUMPY)
# ==============================================================================
def compute_cbf_scores(active_ratings, sim_matrix):
    """
    Computes Content-Based affinity score for all movies.
    For unrated movies: weighted average similarity to watched movies normalized by rating.
    """
    n_movies = len(MOVIES)
    cbf_scores = np.zeros(n_movies, dtype=np.float64)
    rated_ids = [m_id for m_id, r in active_ratings.items() if r > 0]
    
    if not rated_ids:
        # Default cold-start baseline: normalized popularity/IMDb rating
        for i in range(n_movies):
            cbf_scores[i] = (MOVIES[i]["imdb_rating"] - 7.0) / 3.0
        return np.clip(cbf_scores, 0.05, 0.95)
        
    for i in range(n_movies):
        if i in rated_ids:
            # Already watched: scale known rating directly to [0, 1]
            cbf_scores[i] = (active_ratings[i] - 1.0) / 4.0
        else:
            sim_weights = np.array([sim_matrix[i, j] for j in rated_ids], dtype=np.float64)
            user_ratings = np.array([active_ratings[j] / 5.0 for j in rated_ids], dtype=np.float64)
            denom = np.sum(sim_weights)
            if denom > 1e-6:
                cbf_scores[i] = np.sum(sim_weights * user_ratings) / denom
            else:
                cbf_scores[i] = 0.2  # low fallback
                
    return np.clip(cbf_scores, 0.0, 1.0)


def compute_cf_scores(active_ratings, benchmark_ratings):
    """
    Computes Collaborative Filtering scores using Pearson Correlation
    between Active User and the 8 benchmark users across co-rated items.
    """
    n_movies = len(MOVIES)
    n_users = benchmark_ratings.shape[0]
    
    # Active user rating vector (length 20, 0 = unrated)
    r_active = np.zeros(n_movies, dtype=np.float64)
    for m_id, r in active_ratings.items():
        if r > 0:
            r_active[m_id] = float(r)
            
    rated_mask = r_active > 0
    if not np.any(rated_mask):
        # Cold start fallback: average rating across benchmark users
        avg_ratings = np.zeros(n_movies)
        for i in range(n_movies):
            col = benchmark_ratings[:, i]
            nz = col[col > 0]
            avg_ratings[i] = np.mean(nz) if len(nz) > 0 else 3.0
        cf_norm = (avg_ratings - 1.0) / 4.0
        return cf_norm, np.zeros(n_users), avg_ratings
        
    mean_active = np.mean(r_active[rated_mask])
    
    # Compute similarity between active user and each benchmark user
    user_sims = np.zeros(n_users, dtype=np.float64)
    for u in range(n_users):
        r_u = benchmark_ratings[u]
        co_mask = (r_active > 0) & (r_u > 0)
        co_count = np.sum(co_mask)
        
        if co_count >= 2:
            # Pearson correlation on co-rated items
            u_co = r_u[co_mask]
            a_co = r_active[co_mask]
            u_diff = u_co - np.mean(u_co)
            a_diff = a_co - np.mean(a_co)
            denom = (np.sqrt(np.sum(u_diff**2)) * np.sqrt(np.sum(a_diff**2)))
            if denom > 1e-6:
                user_sims[u] = np.sum(u_diff * a_diff) / denom
            else:
                user_sims[u] = 0.0
        elif co_count == 1:
            # Vector cosine fallback on 1 item
            co_idx = np.where(co_mask)[0][0]
            diff = abs(r_active[co_idx] - r_u[co_idx])
            user_sims[u] = max(0.0, 1.0 - diff / 4.0) * 0.5
        else:
            user_sims[u] = 0.0
            
    # Predict rating for each movie
    pred_ratings = np.zeros(n_movies, dtype=np.float64)
    for i in range(n_movies):
        if r_active[i] > 0:
            pred_ratings[i] = r_active[i]
        else:
            # Consider users who rated movie i and have positive similarity
            candidate_users = [u for u in range(n_users) if benchmark_ratings[u, i] > 0 and user_sims[u] > 0]
            if candidate_users:
                sim_weights = np.array([user_sims[u] for u in candidate_users])
                u_means = np.array([np.mean(benchmark_ratings[u, benchmark_ratings[u] > 0]) for u in candidate_users])
                u_ratings = np.array([benchmark_ratings[u, i] for u in candidate_users])
                weighted_dev = np.sum(sim_weights * (u_ratings - u_means))
                sum_weights = np.sum(sim_weights)
                pred_ratings[i] = mean_active + (weighted_dev / sum_weights)
            else:
                # Fallback to general average of movie i or active mean
                col = benchmark_ratings[:, i]
                nz = col[col > 0]
                pred_ratings[i] = np.mean(nz) if len(nz) > 0 else mean_active
                
    pred_ratings = np.clip(pred_ratings, 1.0, 5.0)
    cf_scores = (pred_ratings - 1.0) / 4.0
    return np.clip(cf_scores, 0.0, 1.0), user_sims, pred_ratings


def compute_hybrid_recommendations(active_ratings, alpha=0.5):
    """
    Combines Content-Based and Collaborative Filtering:
    Final_Score = alpha * CBF_Score + (1 - alpha) * CF_Score
    """
    cbf_scores = compute_cbf_scores(active_ratings, CONTENT_SIM_MATRIX)
    cf_scores, user_sims, cf_pred_ratings = compute_cf_scores(active_ratings, INITIAL_RATINGS)
    
    hybrid_scores = alpha * cbf_scores + (1.0 - alpha) * cf_scores
    hybrid_predicted_ratings = 1.0 + 4.0 * hybrid_scores
    
    rated_ids = set([m_id for m_id, r in active_ratings.items() if r > 0])
    
    # Compile candidate recommendation list
    recommendations = []
    for i in range(len(MOVIES)):
        m = MOVIES[i]
        is_watched = i in rated_ids
        
        # Determine why it was recommended
        reasons = []
        if cbf_scores[i] >= 0.70:
            reasons.append(f"High Content Match ({int(cbf_scores[i]*100)}% thematic/genre overlap)")
        elif cbf_scores[i] >= 0.50:
            reasons.append(f"Moderate Genre Match ({int(cbf_scores[i]*100)}%)")
            
        if cf_scores[i] >= 0.70:
            reasons.append(f"Community Favorite (CF Est: {cf_pred_ratings[i]:.2f}★)")
        elif cf_scores[i] >= 0.50:
            reasons.append(f"Favorable Peer Reviews ({cf_pred_ratings[i]:.2f}★)")
            
        if not reasons:
            reasons.append("Balanced Catalog Suggestion")
            
        recommendations.append({
            "id": i,
            "title": m["title"],
            "year": m["year"],
            "director": m["director"],
            "genres": ", ".join(m["genres"]),
            "imdb_rating": m["imdb_rating"],
            "cbf_score": round(float(cbf_scores[i]), 3),
            "cf_score": round(float(cf_scores[i]), 3),
            "cf_pred_rating": round(float(cf_pred_ratings[i]), 2),
            "cbf_pred_rating": round(float(1.0 + 4.0 * cbf_scores[i]), 2),
            "hybrid_score": round(float(hybrid_scores[i]), 3),
            "hybrid_pred_rating": round(float(hybrid_predicted_ratings[i]), 2),
            "is_watched": is_watched,
            "user_rating": active_ratings.get(i, 0),
            "reason": " • ".join(reasons),
            "icon": m["icon"],
            "color": m["color"],
            "initials": m["initials"]
        })
        
    # Unwatched movies ranked highest by hybrid score
    unwatched_recs = [r for r in recommendations if not r["is_watched"]]
    unwatched_recs.sort(key=lambda x: x["hybrid_score"], reverse=True)
    
    # Add rank
    for rank, item in enumerate(unwatched_recs, start=1):
        item["rank"] = rank
        
    return unwatched_recs, recommendations, user_sims, cbf_scores, cf_scores, hybrid_scores


def compute_alpha_sensitivity(active_ratings, alpha_values=[1.0, 0.75, 0.5, 0.25, 0.0]):
    """
    Computes top-5 recommendations across varying alpha levels to show sensitivity.
    """
    results = {}
    for a in alpha_values:
        unwatched, _, _, _, _, _ = compute_hybrid_recommendations(active_ratings, alpha=a)
        results[f"{a:.2f}"] = unwatched[:5]
    return results


# ==============================================================================
# 5. MATPLOTLIB VISUALIZATION GENERATOR (Base64 PNG)
# ==============================================================================
def generate_algorithm_plots(active_ratings, alpha, user_sims, unwatched_recs):
    fig = plt.figure(figsize=(15.5, 9.8), dpi=120)
    
    # Subplot 1: 20x20 Content Cosine Similarity Heatmap
    ax1 = fig.add_subplot(2, 2, 1)
    im1 = ax1.imshow(CONTENT_SIM_MATRIX, cmap='coolwarm', vmin=0, vmax=1)
    ax1.set_title("1. Content-Based Cosine Similarity Matrix (20 x 20 Movies)", fontsize=10, fontweight='bold', color='#003366')
    ax1.set_xticks(range(20))
    ax1.set_yticks(range(20))
    ax1.set_xticklabels([m["initials"] for m in MOVIES], fontsize=7, rotation=90)
    ax1.set_yticklabels([m["initials"] for m in MOVIES], fontsize=7)
    cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.ax.tick_params(labelsize=8)
    
    # Highlight active user's watched movies with red borders/markers on ticks
    rated_ids = [m_id for m_id, r in active_ratings.items() if r > 0]
    for r_id in rated_ids:
        ax1.get_xticklabels()[r_id].set_color('#b91c1c')
        ax1.get_xticklabels()[r_id].set_weight('bold')
        ax1.get_yticklabels()[r_id].set_color('#b91c1c')
        ax1.get_yticklabels()[r_id].set_weight('bold')

    # Subplot 2: User-User Collaborative Correlation Heatmap (8 Benchmarks + Active)
    ax2 = fig.add_subplot(2, 2, 2)
    # Build complete 9x9 user similarity matrix
    all_users_matrix = np.zeros((9, 20))
    all_users_matrix[:8, :] = INITIAL_RATINGS
    for m_id, r in active_ratings.items():
        if r > 0:
            all_users_matrix[8, m_id] = float(r)
            
    corr_9x9 = np.eye(9)
    for u1 in range(9):
        for u2 in range(u1 + 1, 9):
            mask = (all_users_matrix[u1] > 0) & (all_users_matrix[u2] > 0)
            if np.sum(mask) >= 2:
                v1 = all_users_matrix[u1, mask]
                v2 = all_users_matrix[u2, mask]
                diff1 = v1 - np.mean(v1)
                diff2 = v2 - np.mean(v2)
                d = np.sqrt(np.sum(diff1**2)) * np.sqrt(np.sum(diff2**2))
                val = np.sum(diff1 * diff2) / d if d > 1e-6 else 0.0
            else:
                val = 0.0
            corr_9x9[u1, u2] = val
            corr_9x9[u2, u1] = val
            
    im2 = ax2.imshow(corr_9x9, cmap='YlGnBu', vmin=-0.5, vmax=1.0)
    ax2.set_title("2. Collaborative User-User Correlation Matrix (9 Users)", fontsize=10, fontweight='bold', color='#003366')
    short_user_labels = [f"U{i+1}" for i in range(8)] + ["Active"]
    ax2.set_xticks(range(9))
    ax2.set_yticks(range(9))
    ax2.set_xticklabels(short_user_labels, fontsize=8)
    ax2.set_yticklabels(short_user_labels, fontsize=8)
    ax2.get_xticklabels()[-1].set_color('#b91c1c')
    ax2.get_xticklabels()[-1].set_weight('bold')
    ax2.get_yticklabels()[-1].set_color('#b91c1c')
    ax2.get_yticklabels()[-1].set_weight('bold')
    
    # Annotate values inside cells
    for i in range(9):
        for j in range(9):
            text_col = "white" if abs(corr_9x9[i, j]) > 0.6 else "black"
            ax2.text(j, i, f"{corr_9x9[i, j]:.2f}", ha="center", va="center", color=text_col, fontsize=6.5)
    cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    cbar2.ax.tick_params(labelsize=8)

    # Subplot 3: Hybrid Score Trajectory Curve across Alpha [0, 1] for Top 5 Movies
    ax3 = fig.add_subplot(2, 2, 3)
    alpha_range = np.linspace(0.0, 1.0, 21)
    top_5_items = unwatched_recs[:5] if len(unwatched_recs) >= 5 else unwatched_recs
    
    colors = ['#1d4ed8', '#b91c1c', '#047857', '#7c3aed', '#b45309']
    for idx, item in enumerate(top_5_items):
        m_id = item["id"]
        c_score = item["cbf_score"]
        cf_score = item["cf_score"]
        trajectory = alpha_range * c_score + (1.0 - alpha_range) * cf_score
        ax3.plot(alpha_range, trajectory, marker='o', markersize=3.5, linewidth=2.0,
                 label=f"{item['title']} (CB={c_score:.2f}, CF={cf_score:.2f})", color=colors[idx % len(colors)])
                 
    ax3.axvline(x=alpha, color='#000000', linestyle='--', linewidth=1.8, label=f'Current Alpha = {alpha:.2f}')
    ax3.set_title("3. Sensitivity Trajectory: Hybrid Score vs Alpha (Top 5 Unwatched)", fontsize=10, fontweight='bold', color='#003366')
    ax3.set_xlabel("Alpha Weight (α: Content-Based ←───→ 1-α: Collaborative)", fontsize=8.5)
    ax3.set_ylabel("Hybrid Score S_Hybrid", fontsize=8.5)
    ax3.set_xlim(-0.02, 1.02)
    ax3.set_ylim(0.0, 1.05)
    ax3.grid(True, linestyle=':', alpha=0.6)
    ax3.legend(loc='lower left', fontsize=7.0, framealpha=0.9)

    # Subplot 4: Stacked Score Contribution Breakdown for Top 5
    ax4 = fig.add_subplot(2, 2, 4)
    if top_5_items:
        labels = [item["title"][:12] + ("..." if len(item["title"]) > 12 else "") for item in top_5_items]
        cb_contrib = [alpha * item["cbf_score"] for item in top_5_items]
        cf_contrib = [(1.0 - alpha) * item["cf_score"] for item in top_5_items]
        x_indices = np.arange(len(labels))
        width = 0.45
        
        p1 = ax4.bar(x_indices, cb_contrib, width, label=f'Content Contribution (α={alpha:.2f})', color='#3b82f6', edgecolor='#1e40af')
        p2 = ax4.bar(x_indices, cf_contrib, width, bottom=cb_contrib, label=f'Collab Contribution (1-α={1.0-alpha:.2f})', color='#f97316', edgecolor='#c2410c')
        
        # Add value labels
        for idx in range(len(labels)):
            total = cb_contrib[idx] + cf_contrib[idx]
            ax4.text(idx, total + 0.02, f"{total:.2f}\n({top_5_items[idx]['hybrid_pred_rating']:.1f}★)", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
            
        ax4.set_title("4. Decomposition of Top 5 Recommended Hybrid Scores", fontsize=10, fontweight='bold', color='#003366')
        ax4.set_xticks(x_indices)
        ax4.set_xticklabels(labels, fontsize=8, rotation=15)
        ax4.set_ylabel("Composite Score Value", fontsize=8.5)
        ax4.set_ylim(0.0, 1.15)
        ax4.grid(True, linestyle=':', alpha=0.5, axis='y')
        ax4.legend(loc='upper right', fontsize=7.5)
    else:
        ax4.text(0.5, 0.5, "No unwatched movies remaining", ha='center', va='center')
        
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return plot_base64


# ==============================================================================
# 6. FLASK ROUTE HANDLERS
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    # Active ratings stored as dictionary {movie_id: rating}
    active_ratings = dict(DEFAULT_ACTIVE_RATINGS)
    alpha = 0.50
    selected_movie_id = 0
    active_profile = "default"
    
    if request.method == 'POST':
        action = request.form.get('action', 'update_alpha')
        
        # 1. Read Alpha parameter
        try:
            alpha = float(request.form.get('alpha', 0.50))
            alpha = max(0.0, min(1.0, alpha))
        except (ValueError, TypeError):
            alpha = 0.50
            
        # 2. Selected focus movie
        try:
            selected_movie_id = int(request.form.get('focus_movie_id', 0))
            if selected_movie_id < 0 or selected_movie_id >= len(MOVIES):
                selected_movie_id = 0
        except (ValueError, TypeError):
            selected_movie_id = 0
            
        # 3. Read profile preset if triggered
        profile_preset = request.form.get('profile_preset', '')
        if profile_preset == 'scifi':
            active_ratings = {0: 5, 1: 5, 2: 4, 5: 5, 17: 5}
            active_profile = 'scifi'
        elif profile_preset == 'crime':
            active_ratings = {3: 5, 4: 4, 14: 5, 15: 5}
            active_profile = 'crime'
        elif profile_preset == 'romance':
            active_ratings = {7: 4, 8: 3, 9: 5, 10: 5, 19: 5}
            active_profile = 'romance'
        elif profile_preset == 'horror':
            active_ratings = {11: 5, 12: 5, 18: 5}
            active_profile = 'horror'
        elif profile_preset == 'clear':
            active_ratings = {}
            active_profile = 'clear'
        elif profile_preset == 'default':
            active_ratings = dict(DEFAULT_ACTIVE_RATINGS)
            active_profile = 'default'
        else:
            # Reconstruct ratings from individual movie inputs
            custom_ratings = {}
            for i in range(len(MOVIES)):
                val = request.form.get(f'rating_{i}')
                if val is not None and val != "":
                    try:
                        int_val = int(val)
                        if 1 <= int_val <= 5:
                            custom_ratings[i] = int_val
                    except ValueError:
                        pass
            if custom_ratings or action == 'rate_single':
                active_ratings = custom_ratings
                active_profile = 'custom'
                
            # Direct rating button clicked on a single card
            if action == 'rate_single':
                try:
                    m_id = int(request.form.get('single_movie_id', -1))
                    m_val = int(request.form.get('single_rating_val', 0))
                    if 0 <= m_id < len(MOVIES):
                        if 1 <= m_val <= 5:
                            active_ratings[m_id] = m_val
                        elif m_val == 0 and m_id in active_ratings:
                            del active_ratings[m_id]
                except (ValueError, TypeError):
                    pass

    # Run recommendation pipeline
    unwatched_recs, all_recs, user_sims, cbf_scores, cf_scores, hybrid_scores = compute_hybrid_recommendations(
        active_ratings, alpha=alpha
    )
    
    # Generate alpha sensitivity comparison table
    sensitivity_table = compute_alpha_sensitivity(active_ratings, [1.0, 0.75, 0.50, 0.25, 0.0])
    
    # Generate visualization plots
    plot_url = generate_algorithm_plots(active_ratings, alpha, user_sims, unwatched_recs)
    
    # Benchmark users correlation table
    peer_correlations = []
    for idx, name in enumerate(USER_NAMES):
        peer_correlations.append({
            "name": name,
            "sim": round(float(user_sims[idx]), 3),
            "alignment": "High Affinity" if user_sims[idx] >= 0.5 else ("Moderate" if user_sims[idx] > 0 else "Low / Opposing")
        })
        
    # Top 3 content-similar movies to the currently focused movie
    focus_movie = MOVIES[selected_movie_id]
    focus_sims = []
    for j in range(len(MOVIES)):
        if j != selected_movie_id:
            focus_sims.append({
                "id": j,
                "title": MOVIES[j]["title"],
                "year": MOVIES[j]["year"],
                "sim": round(float(CONTENT_SIM_MATRIX[selected_movie_id, j]), 3),
                "genres": ", ".join(MOVIES[j]["genres"]),
                "director": MOVIES[j]["director"]
            })
    focus_sims.sort(key=lambda x: x["sim"], reverse=True)
    top_focus_similar = focus_sims[:3]
    
    # Build complete user-item rating table with predictions for unrated
    full_matrix_display = []
    for u in range(8):
        row = {"user": USER_NAMES[u], "is_active": False, "ratings": []}
        for m_id in range(len(MOVIES)):
            r = int(INITIAL_RATINGS[u, m_id])
            row["ratings"].append({
                "val": r if r > 0 else "-",
                "is_pred": False,
                "class": f"r-{r}" if r > 0 else "r-0"
            })
        full_matrix_display.append(row)
        
    # Add Active User row with both watched and hybrid predicted ratings
    active_row = {"user": "Monis (Active User)", "is_active": True, "ratings": []}
    for m_id in range(len(MOVIES)):
        if m_id in active_ratings and active_ratings[m_id] > 0:
            active_row["ratings"].append({
                "val": f"{active_ratings[m_id]}★",
                "is_pred": False,
                "class": f"r-{active_ratings[m_id]}"
            })
        else:
            pred_val = round(float(1.0 + 4.0 * hybrid_scores[m_id]), 1)
            active_row["ratings"].append({
                "val": f"{pred_val}",
                "is_pred": True,
                "class": "r-pred"
            })
    full_matrix_display.append(active_row)

    return render_template(
        'index.html',
        movies=MOVIES,
        active_ratings=active_ratings,
        alpha=alpha,
        alpha_pct=int(round(alpha * 100)),
        collab_pct=int(round((1.0 - alpha) * 100)),
        unwatched_recs=unwatched_recs,
        all_recs=all_recs,
        sensitivity_table=sensitivity_table,
        peer_correlations=peer_correlations,
        plot_url=plot_url,
        selected_movie=focus_movie,
        selected_movie_id=selected_movie_id,
        top_focus_similar=top_focus_similar,
        full_matrix_display=full_matrix_display,
        active_profile=active_profile
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5019))
    print(f"Starting Experiment 19 Hybrid Recommender on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
