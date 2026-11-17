import os
import io
import base64
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==============================================================================
# MOVIES DATASET (20 Benchmark Movies Across Multiple Diverse Genres)
# ==============================================================================
MOVIES = [
    {
        "id": 0,
        "title": "Inception",
        "genres": ["Sci-Fi", "Action", "Thriller"],
        "year": 2010,
        "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "rating": 8.8,
        "runtime": "148 min",
        "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        "plot_keywords": ["dream heist", "subconscious", "mind-bending", "totem", "reality distortion"],
        "emoji": "🌀",
        "initials": "INC",
        "bg_color": "#1e3a8a"
    },
    {
        "id": 1,
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "year": 2008,
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "rating": 9.0,
        "runtime": "152 min",
        "description": "When the menace known as the Joker wreaks havoc on Gotham City, Batman must accept one of the greatest tests of his ability to fight injustice.",
        "plot_keywords": ["batman", "joker", "vigilante", "anarchy", "gotham justice"],
        "emoji": "🦇",
        "initials": "TDK",
        "bg_color": "#111827"
    },
    {
        "id": 2,
        "title": "Interstellar",
        "genres": ["Sci-Fi", "Adventure", "Drama"],
        "year": 2014,
        "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "rating": 8.7,
        "runtime": "169 min",
        "description": "When Earth becomes uninhabitable, a team of ex-NASA researchers travels through a wormhole near Saturn in search of a new habitable home.",
        "plot_keywords": ["black hole", "wormhole", "relativity", "space travel", "time dilation"],
        "emoji": "🚀",
        "initials": "INT",
        "bg_color": "#0369a1"
    },
    {
        "id": 3,
        "title": "The Matrix",
        "genres": ["Sci-Fi", "Action"],
        "year": 1999,
        "director": "Lana & Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "rating": 8.7,
        "runtime": "136 min",
        "description": "A computer hacker discovers the shocking reality behind simulated existence and joins a rebel movement fighting sentient machine overlords.",
        "plot_keywords": ["simulated reality", "cyberpunk", "red pill", "machine war", "the one"],
        "emoji": "🕶️",
        "initials": "MTX",
        "bg_color": "#065f46"
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama", "Thriller"],
        "year": 1994,
        "director": "Quentin Tarantino",
        "cast": "John Travolta, Uma Thurman, Samuel L. Jackson",
        "rating": 8.9,
        "runtime": "154 min",
        "description": "The intersecting storylines of mob hitmen, a boxer, a gangster's wife, and diner bandits unfold in a non-linear narrative of violence and humor.",
        "plot_keywords": ["nonlinear crime", "hitmen", "diner robbery", "briefcase", "overdose revival"],
        "emoji": "💼",
        "initials": "PLF",
        "bg_color": "#78350f"
    },
    {
        "id": 5,
        "title": "Fight Club",
        "genres": ["Drama", "Thriller"],
        "year": 1999,
        "director": "David Fincher",
        "cast": "Brad Pitt, Edward Norton, Helena Bonham Carter",
        "rating": 8.8,
        "runtime": "139 min",
        "description": "An insomniac white-collar worker and a charismatic soap salesman create an underground bare-knuckle fight club that escalates into anarchy.",
        "plot_keywords": ["insomnia", "alter ego", "underground fight", "consumerism", "project mayhem"],
        "emoji": "🥊",
        "initials": "FCL",
        "bg_color": "#831843"
    },
    {
        "id": 6,
        "title": "Forrest Gump",
        "genres": ["Drama", "Romance"],
        "year": 1994,
        "director": "Robert Zemeckis",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise",
        "rating": 8.8,
        "runtime": "142 min",
        "description": "A gentle Alabama man with an endearing optimism witnesses and unintentionally influences historical landmark events across several decades.",
        "plot_keywords": ["destiny", "vietnam war", "cross country running", "feather", "unconditional love"],
        "emoji": "🍫",
        "initials": "FGP",
        "bg_color": "#15803d"
    },
    {
        "id": 7,
        "title": "The Shawshank Redemption",
        "genres": ["Drama"],
        "year": 1994,
        "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "rating": 9.3,
        "runtime": "142 min",
        "description": "A banker sentenced to life imprisonment for a crime he did not commit builds an enduring bond of hope with a fellow inmate while planning his escape.",
        "plot_keywords": ["prison escape", "hope", "wrongful conviction", "tunnel", "lifelong friendship"],
        "emoji": "🏛️",
        "initials": "SHW",
        "bg_color": "#334155"
    },
    {
        "id": 8,
        "title": "The Grand Budapest Hotel",
        "genres": ["Comedy", "Adventure", "Drama"],
        "year": 2014,
        "director": "Wes Anderson",
        "cast": "Ralph Fiennes, Tony Revolori, Saoirse Ronan",
        "rating": 8.1,
        "runtime": "99 min",
        "description": "A legendary concierge at a luxurious European ski resort is framed for murder amid the theft of a priceless Renaissance painting.",
        "plot_keywords": ["concierge", "heirloom painting", "symmetry", "lobby boy", "whimsical caper"],
        "emoji": "🏨",
        "initials": "GBH",
        "bg_color": "#be185d"
    },
    {
        "id": 9,
        "title": "Superbad",
        "genres": ["Comedy"],
        "year": 2007,
        "director": "Greg Mottola",
        "cast": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse",
        "rating": 7.6,
        "runtime": "113 min",
        "description": "Two high school best friends embark on a chaotic quest to acquire alcohol for a house party before graduation leads them to separate colleges.",
        "plot_keywords": ["high school", "fake id", "mclovin", "wild party", "separation anxiety"],
        "emoji": "🍺",
        "initials": "SBD",
        "bg_color": "#c2410c"
    },
    {
        "id": 10,
        "title": "The Hangover",
        "genres": ["Comedy"],
        "year": 2009,
        "director": "Todd Phillips",
        "cast": "Bradley Cooper, Ed Helms, Zach Galifianakis",
        "rating": 7.7,
        "runtime": "100 min",
        "description": "Three groomsmen wake up from a riotous Las Vegas bachelor party with raging hangovers, a missing groom, and a Bengal tiger in their suite bathroom.",
        "plot_keywords": ["bachelor party", "las vegas", "tiger", "missing groom", "amnesia mystery"],
        "emoji": "🎰",
        "initials": "HNG",
        "bg_color": "#a16207"
    },
    {
        "id": 11,
        "title": "La La Land",
        "genres": ["Comedy", "Drama", "Romance"],
        "year": 2016,
        "director": "Damien Chazelle",
        "cast": "Ryan Gosling, Emma Stone, John Legend",
        "rating": 8.0,
        "runtime": "128 min",
        "description": "A dedicated jazz pianist and an aspiring actress fall deeply in love in modern-day Los Angeles while reconciling personal artistic ambitions.",
        "plot_keywords": ["jazz pianist", "aspiring actress", "hollywood dream", "musical romance", "bittersweet"],
        "emoji": "🎷",
        "initials": "LLL",
        "bg_color": "#4338ca"
    },
    {
        "id": 12,
        "title": "Titanic",
        "genres": ["Drama", "Romance"],
        "year": 1997,
        "director": "James Cameron",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
        "rating": 7.9,
        "runtime": "194 min",
        "description": "A passionate romance blossoms between aristocratic Rose and free-spirited artist Jack aboard the ill-fated luxury ocean liner Titanic.",
        "plot_keywords": ["shipwreck", "iceberg collision", "forbidden love", "ocean liner", "heart of the ocean"],
        "emoji": "🚢",
        "initials": "TTN",
        "bg_color": "#0e7490"
    },
    {
        "id": 13,
        "title": "The Conjuring",
        "genres": ["Horror", "Mystery", "Thriller"],
        "year": 2013,
        "director": "James Wan",
        "cast": "Patrick Wilson, Vera Farmiga, Ron Livingston",
        "rating": 7.5,
        "runtime": "112 min",
        "description": "Renowned paranormal investigators Ed and Lorraine Warren confront an ominous malevolent demonic presence terrorizing a secluded Rhode Island family farmhouse.",
        "plot_keywords": ["paranormal investigators", "haunted house", "demonic possession", "exorcism", "dark spirit"],
        "emoji": "🕯️",
        "initials": "CNJ",
        "bg_color": "#3f3f46"
    },
    {
        "id": 14,
        "title": "A Quiet Place",
        "genres": ["Drama", "Horror", "Sci-Fi"],
        "year": 2018,
        "director": "John Krasinski",
        "cast": "Emily Blunt, John Krasinski, Millicent Simmonds",
        "rating": 7.5,
        "runtime": "90 min",
        "description": "In a post-apocalyptic world overrun by lethal predatory blind creatures that hunt strictly by sound, a family navigates daily survival in utter silence.",
        "plot_keywords": ["sound hunting monsters", "post apocalyptic", "sign language", "sensory tension", "family survival"],
        "emoji": "🤫",
        "initials": "AQP",
        "bg_color": "#451a03"
    },
    {
        "id": 15,
        "title": "Alien",
        "genres": ["Horror", "Sci-Fi"],
        "year": 1979,
        "director": "Ridley Scott",
        "cast": "Sigourney Weaver, Tom Skerritt, John Hurt",
        "rating": 8.5,
        "runtime": "117 min",
        "description": "The crew of the commercial towing starship Nostromo encounters a deadly extraterrestrial parasitic predator after investigating a derelict spacecraft.",
        "plot_keywords": ["xenomorph", "deep space", "facehugger", "claustrophobic horror", "nostromo"],
        "emoji": "👽",
        "initials": "ALN",
        "bg_color": "#14532d"
    },
    {
        "id": 16,
        "title": "Mad Max: Fury Road",
        "genres": ["Action", "Adventure", "Sci-Fi"],
        "year": 2015,
        "director": "George Miller",
        "cast": "Tom Hardy, Charlize Theron, Nicholas Hoult",
        "rating": 8.1,
        "runtime": "120 min",
        "description": "In a barren apocalyptic wasteland, Imperator Furiosa escapes a tyrannical cult warlord driving a heavily armored War Rig alongside lone drifter Max.",
        "plot_keywords": ["wasteland car chase", "furiosa", "immortan joe", "desert warfare", "high octane"],
        "emoji": "🔥",
        "initials": "MMF",
        "bg_color": "#b45309"
    },
    {
        "id": 17,
        "title": "Gladiator",
        "genres": ["Action", "Adventure", "Drama"],
        "year": 2000,
        "director": "Ridley Scott",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen",
        "rating": 8.5,
        "runtime": "155 min",
        "description": "A betrayed Roman general is forced into the gladiator arena as a slave, battling his way to the Colosseum to avenge his murdered wife and son.",
        "plot_keywords": ["roman empire", "colosseum", "general betrayed", "gladiatorial combat", "vengeance"],
        "emoji": "⚔️",
        "initials": "GLD",
        "bg_color": "#713f12"
    },
    {
        "id": 18,
        "title": "Knives Out",
        "genres": ["Comedy", "Crime", "Mystery"],
        "year": 2019,
        "director": "Rian Johnson",
        "cast": "Daniel Craig, Chris Evans, Ana de Armas",
        "rating": 7.9,
        "runtime": "130 min",
        "description": "Master detective Benoit Blanc investigates the suspicious circumstances surrounding the sudden demise of wealthy crime novelist Harlan Thrombey.",
        "plot_keywords": ["whodunit", "murder mystery", "detective blanc", "eccentric family", "inheritance twists"],
        "emoji": "🔍",
        "initials": "KNO",
        "bg_color": "#365314"
    },
    {
        "id": 19,
        "title": "Get Out",
        "genres": ["Horror", "Mystery", "Thriller"],
        "year": 2017,
        "director": "Jordan Peele",
        "cast": "Daniel Kaluuya, Allison Williams, Bradley Whitford",
        "rating": 7.8,
        "runtime": "104 min",
        "description": "A young African-American photographer uncovers a horrifying sinister secret while visiting his white girlfriend's parents at their secluded country estate.",
        "plot_keywords": ["psychological horror", "sunken place", "hypnosis teacup", "upstate family", "social suspense"],
        "emoji": "☕",
        "initials": "GOT",
        "bg_color": "#312e81"
    }
]

# Quick lookup by ID
MOVIE_DICT = {m["id"]: m for m in MOVIES}
TOTAL_MOVIES = len(MOVIES)

# ==============================================================================
# USER COMMUNITY DATASET (8 Realistic Users with Diverse Genre Profiles)
# ==============================================================================
USERS = [
    {
        "id": 0,
        "name": "Alice (Sci-Fi & Cyberpunk)",
        "pref_desc": "Loves hard science fiction, high-concept space journeys, mind-bending reality, and dystopian thrillers.",
        "watched_movie_ids": [0, 1, 2, 3, 15, 16]
    },
    {
        "id": 1,
        "name": "Bob (Action & Adrenaline)",
        "pref_desc": "Drawn to fast-paced action choreography, intense crime thrillers, gritty combat, and martial grit.",
        "watched_movie_ids": [0, 1, 3, 4, 5, 16, 17, 18]
    },
    {
        "id": 2,
        "name": "Charlie (Comedy & Whimsical)",
        "pref_desc": "Prefers lighthearted entertainment, quirky director styles, slapstick adventures, and modern mystery capers.",
        "watched_movie_ids": [8, 9, 10, 18]
    },
    {
        "id": 3,
        "name": "Dana (Drama & Romantic Epics)",
        "pref_desc": "Passionate about character-driven melodramas, sweeping romantic narratives, and emotional period epics.",
        "watched_movie_ids": [2, 6, 7, 8, 11, 12]
    },
    {
        "id": 4,
        "name": "Evan (Horror & Supernatural)",
        "pref_desc": "Dedicated horror buff seeking psychological tension, paranormal disturbances, and alien thrillers.",
        "watched_movie_ids": [13, 14, 15, 19]
    },
    {
        "id": 5,
        "name": "Fiona (Sci-Fi / Horror Hybrids)",
        "pref_desc": "Enjoys creature features, alien biology, survival suspense, and cerebral mind-bending cinema.",
        "watched_movie_ids": [0, 2, 3, 13, 14, 15, 19]
    },
    {
        "id": 6,
        "name": "George (Classic Drama & Epics)",
        "pref_desc": "Values historical epics, prison redemption dramas, auteur masterpieces, and noir thrillers.",
        "watched_movie_ids": [1, 4, 5, 6, 7, 17]
    },
    {
        "id": 7,
        "name": "Hannah (Eclectic Cinephile)",
        "pref_desc": "Eclectic viewer sampling comedies, musicals, romances, whodunits, and iconic 90s dramas.",
        "watched_movie_ids": [4, 6, 8, 9, 10, 11, 12, 18]
    }
]

# Ground Truth User-Ratings Matrix (Scale 1-5, 0 = Unrated / Unseen)
# Shape: (8 Users, 20 Movies)
RAW_RATINGS = np.array([
    # M0  M1  M2  M3  M4  M5  M6  M7  M8  M9  M10 M11 M12 M13 M14 M15 M16 M17 M18 M19
    [ 5,  4,  5,  5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  4,  0,  0,  0], # Alice
    [ 5,  5,  0,  5,  5,  4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  5,  3,  0], # Bob
    [ 0,  0,  0,  0,  0,  0,  0,  0,  5,  5,  4,  0,  0,  0,  0,  0,  0,  0,  4,  0], # Charlie
    [ 0,  0,  4,  0,  0,  0,  5,  5,  4,  0,  0,  5,  5,  0,  0,  0,  0,  0,  0,  0], # Dana
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  5,  4,  0,  0,  0,  5], # Evan
    [ 4,  0,  4,  4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4,  4,  5,  0,  0,  0,  4], # Fiona
    [ 0,  5,  0,  0,  5,  5,  4,  5,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  0,  0], # George
    [ 0,  0,  0,  0,  3,  0,  4,  0,  4,  4,  5,  4,  4,  0,  0,  0,  0,  0,  4,  0]  # Hannah
], dtype=int)

# Binarization: Seen = 1, Not-Seen = 0
BINARY_MATRIX = (RAW_RATINGS > 0).astype(int)

# ==============================================================================
# ALGORITHM FROM SCRATCH: ITEM-ITEM JACCARD SIMILARITY COMPUTATION (NUMPY)
# ==============================================================================
def compute_jaccard_matrix_from_scratch(B):
    """
    Computes pairwise Jaccard similarity matrix J between items using pure NumPy.
    B: shape (M, N), where M = number of users, N = number of items.
    
    J(i, j) = |U_i ∩ U_j| / |U_i ∪ U_j|
            = (b_i . b_j) / (sum(b_i) + sum(b_j) - (b_i . b_j))
    """
    # Intersection matrix M_11: shape (N, N)
    intersection = np.dot(B.T, B).astype(float)
    
    # Watch count per item: sum along users axis (M,)
    item_sums = np.sum(B, axis=0).astype(float)
    
    # Union matrix: |U_i| + |U_j| - |U_i ∩ U_j|
    union = item_sums[:, None] + item_sums[None, :] - intersection
    
    # Jaccard index: safe vectorized division
    with np.errstate(divide='ignore', invalid='ignore'):
        jaccard = np.where(union > 0, intersection / union, 0.0)
        
    # Diagonal represents identical item similarity: J(i, i) = 1.0
    np.fill_diagonal(jaccard, 1.0)
    
    return jaccard, intersection, union

# Precompute baseline community item-item Jaccard matrix
JACCARD_MATRIX, INTERSECTION_MATRIX, UNION_MATRIX = compute_jaccard_matrix_from_scratch(BINARY_MATRIX)

# ==============================================================================
# ITEM-BASED kNN BINARY RECOMMENDATION ENGINE (FROM SCRATCH)
# ==============================================================================
def recommend_item_knn_binary(active_watched_ids, k=3, top_n=5, jaccard_mat=JACCARD_MATRIX):
    """
    Generates recommendations for an active user with seen items S:
    1. Filter candidates C = Items not in S.
    2. For each unseen item c in C:
       Find its k-nearest neighbors among watched items S based on Jaccard similarity J(c, s).
       Score(c) = (1 / |k-NN(c; S)|) * sum_{s in k-NN(c; S)} J(c, s)
    3. Rank candidate items descending by Score(c).
    """
    active_watched_set = set(active_watched_ids)
    all_item_ids = list(range(TOTAL_MOVIES))
    candidate_ids = [idx for idx in all_item_ids if idx not in active_watched_set]
    
    if not active_watched_ids:
        # Cold start: if active user has watched 0 movies, rank by global popularity and rating
        popularity = np.sum(BINARY_MATRIX, axis=0)
        cold_rankings = []
        for c in candidate_ids:
            pop = int(popularity[c])
            imdb = MOVIES[c]["rating"]
            cold_rankings.append({
                "movie": MOVIES[c],
                "score": round(pop / len(USERS), 3),
                "sum_score": round(pop / len(USERS), 3),
                "k_neighbors": [],
                "primary_reason": f"Popular baseline: watched by {pop} users (IMDb: {imdb})",
                "best_neighbor_title": "N/A (Cold Start)",
                "best_sim": 0.0
            })
        cold_rankings.sort(key=lambda x: (x["score"], x["movie"]["rating"]), reverse=True)
        return cold_rankings[:top_n]
    
    if not candidate_ids:
        # All movies watched
        return []
        
    recommendations = []
    
    for c in candidate_ids:
        # Pairwise similarities between unseen candidate c and all seen items in S
        item_sim_pairs = []
        for s in active_watched_ids:
            sim = float(jaccard_mat[c, s])
            item_sim_pairs.append((s, sim))
            
        # Sort descending by Jaccard similarity
        item_sim_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Select top-k nearest neighbors within watched set S
        eff_k = min(k, len(item_sim_pairs))
        top_k_pairs = item_sim_pairs[:eff_k]
        
        # Compute mean Jaccard score across k nearest watched items
        sim_values = [p[1] for p in top_k_pairs]
        mean_score = float(np.mean(sim_values)) if sim_values else 0.0
        sum_score = float(np.sum(sim_values)) if sim_values else 0.0
        
        # Best single neighbor for intuitive explanation
        best_neighbor_id, best_sim = item_sim_pairs[0]
        best_movie = MOVIES[best_neighbor_id]
        
        k_neighbors_detail = [
            {
                "id": p[0],
                "title": MOVIES[p[0]]["title"],
                "emoji": MOVIES[p[0]]["emoji"],
                "sim": round(p[1], 3)
            }
            for p in top_k_pairs
        ]
        
        recommendations.append({
            "movie": MOVIES[c],
            "score": round(mean_score, 4),
            "sum_score": round(sum_score, 4),
            "k_neighbors": k_neighbors_detail,
            "primary_reason": f"Because you watched '{best_movie['title']}' (Jaccard = {best_sim:.3f})",
            "best_neighbor_title": best_movie["title"],
            "best_sim": round(best_sim, 3)
        })
        
    # Rank candidates by descending recommendation score, break ties with IMDb rating
    recommendations.sort(key=lambda x: (x["score"], x["movie"]["rating"]), reverse=True)
    return recommendations[:top_n]

# ==============================================================================
# MATPLOTLIB MULTI-PANEL VISUALIZATION GENERATOR
# ==============================================================================
def generate_visualizations(active_watched_ids, recommendations, k=3, active_user_name="Active User"):
    """
    Renders 4-panel publication grade plots:
    1. Item-Item Jaccard Similarity Heatmap (20 x 20)
    2. User-Item Binary Seen/Not-Seen Interaction Grid (8 x 20) with active profile marker
    3. Top-k Recommendations Bar Chart (horizontal scores)
    4. Movie Catalog Popularity & Watched Status Histogram
    """
    fig, axes = plt.subplots(2, 2, figsize=(14.2, 11.2), dpi=125)
    plt.subplots_adjust(wspace=0.32, hspace=0.38)
    
    # --------------------------------------------------------------------------
    # PANEL 1: Item-Item Jaccard Similarity Heatmap (20 x 20)
    # --------------------------------------------------------------------------
    ax1 = axes[0, 0]
    initials = [m["initials"] for m in MOVIES]
    im1 = ax1.imshow(JACCARD_MATRIX, cmap="YlGnBu", vmin=0.0, vmax=1.0, aspect="auto")
    
    ax1.set_xticks(range(TOTAL_MOVIES))
    ax1.set_xticklabels(initials, rotation=90, fontsize=7.5, fontweight="bold")
    ax1.set_yticks(range(TOTAL_MOVIES))
    ax1.set_yticklabels(initials, fontsize=7.5, fontweight="bold")
    
    cbar1 = fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.03)
    cbar1.set_label("Jaccard Similarity Index J(i, j)", fontsize=8.5, fontweight="bold")
    cbar1.ax.tick_params(labelsize=8)
    
    ax1.set_title("Panel 1: Item-Item Jaccard Similarity Heatmap (20x20)", fontsize=10.5, fontweight="bold", pad=8, color="#003366")
    ax1.set_xlabel("Item Index j (Candidate / Target Movie)", fontsize=8.5)
    ax1.set_ylabel("Item Index i (Source Movie)", fontsize=8.5)
    
    # --------------------------------------------------------------------------
    # PANEL 2: User-Item Binary Seen/Not-Seen Interaction Grid
    # --------------------------------------------------------------------------
    ax2 = axes[0, 1]
    user_labels = [u["name"].split(" ")[0] for u in USERS]
    
    # Create display matrix: 8 users + 1 virtual Active User row if customized
    display_matrix = BINARY_MATRIX.copy()
    display_users = list(user_labels)
    
    # Show active user vector at bottom
    active_vec = np.zeros(TOTAL_MOVIES, dtype=int)
    for w in active_watched_ids:
        if 0 <= w < TOTAL_MOVIES:
            active_vec[w] = 1
    
    display_matrix = np.vstack([display_matrix, active_vec])
    display_users.append(f"-> {active_user_name.split(' ')[0]}")
    
    im2 = ax2.imshow(display_matrix, cmap="Blues", aspect="auto", vmin=0, vmax=1)
    
    ax2.set_xticks(range(TOTAL_MOVIES))
    ax2.set_xticklabels(initials, rotation=90, fontsize=7.5)
    ax2.set_yticks(range(len(display_users)))
    ax2.set_yticklabels(display_users, fontsize=8, fontweight="bold")
    
    # Highlight the active user row label
    ax2.get_yticklabels()[-1].set_color("#dc2626")
    
    # Grid lines to separate cells
    ax2.set_xticks(np.arange(-0.5, TOTAL_MOVIES, 1), minor=True)
    ax2.set_yticks(np.arange(-0.5, len(display_users), 1), minor=True)
    ax2.grid(which="minor", color="#94a3b8", linestyle="-", linewidth=0.6)
    ax2.tick_params(which="minor", bottom=False, left=False)
    
    cbar2 = fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.03, ticks=[0, 1])
    cbar2.ax.set_yticklabels(["0: Unseen", "1: Seen"], fontsize=8)
    
    ax2.set_title("Panel 2: User-Item Binary Seen Matrix B in {0,1}", fontsize=10.5, fontweight="bold", pad=8, color="#003366")
    ax2.set_xlabel("Movie Catalog Items (20 Movies)", fontsize=8.5)
    ax2.set_ylabel("Users (Alice - Hannah + Active User)", fontsize=8.5)
    
    # --------------------------------------------------------------------------
    # PANEL 3: Top-K Recommendations Ranked Bar Chart
    # --------------------------------------------------------------------------
    ax3 = axes[1, 0]
    if recommendations:
        rec_titles = [r["movie"]["title"] for r in reversed(recommendations)]
        rec_scores = [r["score"] for r in reversed(recommendations)]
        y_pos = np.arange(len(rec_titles))
        
        # Color gradient based on score
        colors = plt.cm.viridis(np.linspace(0.4, 0.9, len(rec_scores)))
        bars = ax3.barh(y_pos, rec_scores, color=colors, edgecolor="#1e293b", height=0.65)
        
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(rec_titles, fontsize=8.5, fontweight="bold")
        ax3.set_xlim(0, max(max(rec_scores) * 1.25, 0.5))
        
        # Score labels on bars
        for bar, score in zip(bars, rec_scores):
            ax3.text(bar.get_width() + 0.015, bar.get_y() + bar.get_height()/2,
                     f"Score: {score:.3f}", va="center", ha="left",
                     fontsize=8, fontweight="bold", color="#0f172a")
                     
        ax3.set_title(f"Panel 3: Top Recommendations by Mean Jaccard Score (k={k})",
                      fontsize=10.5, fontweight="bold", pad=8, color="#003366")
        ax3.set_xlabel(f"kNN Recommendation Score: mean J(c, s) for s in Top-{k} Watched Items", fontsize=8.5)
        ax3.grid(axis="x", linestyle="--", alpha=0.5)
    else:
        ax3.text(0.5, 0.5, "All 20 Movies Watched!\nNo Candidate Unseen Movies Left.",
                 ha="center", va="center", fontsize=11, fontweight="bold", color="#64748b")
        ax3.set_title("Panel 3: Recommendation Scores", fontsize=10.5, fontweight="bold", color="#003366")
        
    # --------------------------------------------------------------------------
    # PANEL 4: Movie Popularity & Active User Watched State
    # --------------------------------------------------------------------------
    ax4 = axes[1, 1]
    watch_counts = np.sum(BINARY_MATRIX, axis=0)
    x_indices = np.arange(TOTAL_MOVIES)
    
    # Differentiate watched by active user vs unseen
    bar_colors = []
    for i in range(TOTAL_MOVIES):
        if i in active_watched_ids:
            bar_colors.append("#f97316") # Orange = Watched by active user
        else:
            bar_colors.append("#2563eb") # Blue = Unseen by active user
            
    bars4 = ax4.bar(x_indices, watch_counts, color=bar_colors, edgecolor="#0f172a", width=0.68)
    
    ax4.set_xticks(x_indices)
    ax4.set_xticklabels(initials, rotation=90, fontsize=7.5, fontweight="bold")
    ax4.set_ylim(0, 8)
    ax4.set_yticks(range(0, 9))
    ax4.set_title("Panel 4: Catalog Watch Counts & Active User Status", fontsize=10.5, fontweight="bold", pad=8, color="#003366")
    ax4.set_xlabel("Movie Catalog Items (20 Movies)", fontsize=8.5)
    ax4.set_ylabel("Total Community View Count (Out of 8 Users)", fontsize=8.5)
    ax4.grid(axis="y", linestyle="--", alpha=0.5)
    
    # Custom Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#f97316", edgecolor="#0f172a", label="Seen by Active User"),
        Patch(facecolor="#2563eb", edgecolor="#0f172a", label="Unseen Candidate Item")
    ]
    ax4.legend(handles=legend_elements, loc="upper right", fontsize=8)
    
    # Convert to base64
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=125)
    buf.seek(0)
    plot_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()
    
    return plot_b64

# ==============================================================================
# FLASK ROUTING
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    # Default initial state: User 0 (Alice)
    selected_user_id = 0
    k_val = 3
    top_n_val = 5
    active_watched_ids = list(USERS[0]["watched_movie_ids"])
    active_user_name = USERS[0]["name"]
    selected_movie_detail = None
    
    if request.method == 'POST':
        # Preset User handling
        preset_raw = request.form.get('user_preset', '0')
        k_val = int(request.form.get('k_neighbors', 3))
        top_n_val = int(request.form.get('top_n', 5))
        
        # Clicked movie detail
        detail_id_raw = request.form.get('detail_movie_id')
        if detail_id_raw is not None and detail_id_raw != "":
            try:
                detail_id = int(detail_id_raw)
                if 0 <= detail_id < TOTAL_MOVIES:
                    selected_movie_detail = MOVIES[detail_id]
            except ValueError:
                pass
                
        # If user selected a preset from the dropdown and hit "Load Preset"
        action = request.form.get('action', 'recommend')
        
        if action == 'load_preset' and preset_raw != 'custom':
            try:
                selected_user_id = int(preset_raw)
                if 0 <= selected_user_id < len(USERS):
                    active_watched_ids = list(USERS[selected_user_id]["watched_movie_ids"])
                    active_user_name = USERS[selected_user_id]["name"]
            except ValueError:
                selected_user_id = 0
                active_watched_ids = list(USERS[0]["watched_movie_ids"])
                active_user_name = USERS[0]["name"]
        else:
            # Custom checkbox selections
            watched_raw = request.form.getlist('watched_movies')
            active_watched_ids = [int(mid) for mid in watched_raw if mid.isdigit() and 0 <= int(mid) < TOTAL_MOVIES]
            
            if preset_raw != 'custom' and preset_raw.isdigit():
                uid = int(preset_raw)
                if 0 <= uid < len(USERS) and set(active_watched_ids) == set(USERS[uid]["watched_movie_ids"]):
                    selected_user_id = uid
                    active_user_name = USERS[uid]["name"]
                else:
                    selected_user_id = -1
                    active_user_name = "Custom User Profile"
            else:
                selected_user_id = -1
                active_user_name = "Custom User Profile"
                
    # Run Item-Based kNN Recommender
    recommendations = recommend_item_knn_binary(
        active_watched_ids=active_watched_ids,
        k=k_val,
        top_n=top_n_val,
        jaccard_mat=JACCARD_MATRIX
    )
    
    # Generate multi-panel Matplotlib dashboard
    plot_b64 = generate_visualizations(
        active_watched_ids=active_watched_ids,
        recommendations=recommendations,
        k=k_val,
        active_user_name=active_user_name
    )
    
    # Prepare numerical tables
    # 1. Binary User-Item Matrix Table
    binary_table_rows = []
    for u_idx, u in enumerate(USERS):
        row = {
            "user_name": u["name"],
            "ratings": BINARY_MATRIX[u_idx].tolist()
        }
        binary_table_rows.append(row)
        
    # Active user row in binary table
    active_row = [1 if i in active_watched_ids else 0 for i in range(TOTAL_MOVIES)]
    
    # 2. Key Jaccard Pairs Table (Selected meaningful pairs)
    sample_jaccard_pairs = [
        (0, 2, "Inception vs Interstellar (Sci-Fi Nolan)"),
        (0, 3, "Inception vs The Matrix (Sci-Fi Action Reality)"),
        (1, 17, "The Dark Knight vs Gladiator (High-Octane Action)"),
        (4, 5, "Pulp Fiction vs Fight Club (Cult Crime/Drama)"),
        (6, 7, "Forrest Gump vs Shawshank Redemption (90s Heartfelt Drama)"),
        (8, 9, "Grand Budapest Hotel vs Superbad (Comedies)"),
        (9, 10, "Superbad vs The Hangover (Party Comedy)"),
        (11, 12, "La La Land vs Titanic (Romantic Drama)"),
        (13, 14, "The Conjuring vs A Quiet Place (Supernatural/Horror)"),
        (14, 15, "A Quiet Place vs Alien (Sci-Fi Monster/Survival)"),
        (15, 19, "Alien vs Get Out (Suspense/Horror)"),
        (0, 9, "Inception vs Superbad (Cross-Genre: SciFi vs Slapstick)")
    ]
    
    jaccard_pairs_data = []
    for id_a, id_b, desc in sample_jaccard_pairs:
        sim = float(JACCARD_MATRIX[id_a, id_b])
        inter = int(INTERSECTION_MATRIX[id_a, id_b])
        uni = int(UNION_MATRIX[id_a, id_b])
        jaccard_pairs_data.append({
            "pair": f"{MOVIES[id_a]['title']} & {MOVIES[id_b]['title']}",
            "emojis": f"{MOVIES[id_a]['emoji']} + {MOVIES[id_b]['emoji']}",
            "desc": desc,
            "intersection": inter,
            "union": uni,
            "jaccard": round(sim, 3)
        })
        
    stats = {
        "total_movies": TOTAL_MOVIES,
        "total_users": len(USERS),
        "total_watched": len(active_watched_ids),
        "total_unseen": TOTAL_MOVIES - len(active_watched_ids),
        "k_val": k_val,
        "top_n_val": top_n_val,
        "active_user_name": active_user_name,
        "matrix_density": round(float(np.mean(BINARY_MATRIX)) * 100, 1),
        "sparsity": round((1.0 - float(np.mean(BINARY_MATRIX))) * 100, 1)
    }
    
    return render_template(
        'index.html',
        movies=MOVIES,
        users=USERS,
        selected_user_id=selected_user_id,
        active_watched_ids=active_watched_ids,
        active_row=active_row,
        recommendations=recommendations,
        plot_b64=plot_b64,
        stats=stats,
        binary_table_rows=binary_table_rows,
        jaccard_pairs_data=jaccard_pairs_data,
        selected_movie_detail=selected_movie_detail
    )

@app.route('/api/movie/<int:movie_id>')
def get_movie_detail_api(movie_id):
    if 0 <= movie_id < TOTAL_MOVIES:
        return jsonify(MOVIES[movie_id])
    return jsonify({"error": "Movie not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5018))
    print(f"Starting Experiment 18 Item-Based kNN Server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
