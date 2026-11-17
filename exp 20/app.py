import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# =========================================================================
# 1. HARDCODED MOVIES KNOWLEDGE BASE (20 DIVERSE MOVIES)
# Criteria: acting, visuals, story, pace (rated 1.0 - 10.0 scale)
# =========================================================================
MOVIES_DATABASE = [
    {
        "id": 1,
        "title": "Inception",
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "year": 2010,
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
        "rating": 8.8,
        "description": "A thief who steals corporate secrets through dream-sharing technology is tasked with planting an idea into the mind of a C.E.O.",
        "plot_keywords": ["dream heist", "subconscious", "reality", "totem", "time dilation"],
        "poster_color": "#1e3a8a",
        "poster_emoji": "🌀",
        "acting": 8.8,
        "visuals": 9.7,
        "story": 9.2,
        "pace": 8.6
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "year": 2008,
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "rating": 9.0,
        "description": "When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological tests of his ability to fight injustice.",
        "plot_keywords": ["vigilante", "Joker", "chaos", "Gotham", "moral dilemma"],
        "poster_color": "#0f172a",
        "poster_emoji": "🦇",
        "acting": 9.6,
        "visuals": 9.1,
        "story": 9.5,
        "pace": 9.2
    },
    {
        "id": 3,
        "title": "Interstellar",
        "genres": ["Sci-Fi", "Drama", "Adventure"],
        "year": 2014,
        "director": "Christopher Nolan",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "rating": 8.7,
        "description": "When Earth becomes uninhabitable, a team of explorers travels through a wormhole across the galaxy to find humanity a new home.",
        "plot_keywords": ["wormhole", "black hole", "space exploration", "relativity", "love"],
        "poster_color": "#172554",
        "poster_emoji": "🚀",
        "acting": 9.1,
        "visuals": 9.9,
        "story": 9.3,
        "pace": 7.9
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama"],
        "year": 1994,
        "director": "Quentin Tarantino",
        "cast": ["John Travolta", "Samuel L. Jackson", "Uma Thurman"],
        "rating": 8.9,
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "plot_keywords": ["nonlinear narrative", "hitmen", "dialogue", "Los Angeles", "black comedy"],
        "poster_color": "#78350f",
        "poster_emoji": "💼",
        "acting": 9.6,
        "visuals": 8.3,
        "story": 9.6,
        "pace": 8.8
    },
    {
        "id": 5,
        "title": "The Shawshank Redemption",
        "genres": ["Drama"],
        "year": 1994,
        "director": "Frank Darabont",
        "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
        "rating": 9.3,
        "description": "A banker convicted of a crime he did not commit bonds with a fellow inmate over decades while retaining hope and preparing an escape.",
        "plot_keywords": ["prison escape", "hope", "friendship", "wrongful conviction", "redemption"],
        "poster_color": "#1e293b",
        "poster_emoji": "🏛️",
        "acting": 9.8,
        "visuals": 8.1,
        "story": 9.9,
        "pace": 8.1
    },
    {
        "id": 6,
        "title": "Forrest Gump",
        "genres": ["Drama", "Romance", "Comedy"],
        "year": 1994,
        "director": "Robert Zemeckis",
        "cast": ["Tom Hanks", "Robin Wright", "Gary Sinise"],
        "rating": 8.8,
        "description": "The history of the United States from the 1950s to the '70s unfolds through the perspective of an Alabama man with an IQ of 75.",
        "plot_keywords": ["historical events", "running", "chocolates", "innocence", "enduring love"],
        "poster_color": "#065f46",
        "poster_emoji": "🍫",
        "acting": 9.7,
        "visuals": 8.5,
        "story": 9.4,
        "pace": 8.5
    },
    {
        "id": 7,
        "title": "The Matrix",
        "genres": ["Action", "Sci-Fi"],
        "year": 1999,
        "director": "The Wachowskis",
        "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
        "rating": 8.7,
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "plot_keywords": ["simulated reality", "red pill", "bullet time", "cyberpunk", "chosen one"],
        "poster_color": "#052e16",
        "poster_emoji": "🕶️",
        "acting": 8.4,
        "visuals": 9.6,
        "story": 9.3,
        "pace": 9.3
    },
    {
        "id": 8,
        "title": "Parasite",
        "genres": ["Drama", "Thriller", "Comedy"],
        "year": 2019,
        "director": "Bong Joon-ho",
        "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
        "rating": 8.5,
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "plot_keywords": ["class struggle", "social satire", "subterfuge", "basement", "architecture"],
        "poster_color": "#365314",
        "poster_emoji": "🏠",
        "acting": 9.5,
        "visuals": 9.3,
        "story": 9.8,
        "pace": 9.1
    },
    {
        "id": 9,
        "title": "Spirited Away",
        "genres": ["Animation", "Adventure", "Fantasy"],
        "year": 2001,
        "director": "Hayao Miyazaki",
        "cast": ["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki"],
        "rating": 8.6,
        "description": "During her family's move to the suburbs, a 10-year-old girl wanders into a world ruled by gods, witches, and spirits where humans are changed into beasts.",
        "plot_keywords": ["bathhouse", "spirits", "Ghibli", "folklore", "courage"],
        "poster_color": "#831843",
        "poster_emoji": "🐉",
        "acting": 8.9,
        "visuals": 9.9,
        "story": 9.5,
        "pace": 8.2
    },
    {
        "id": 10,
        "title": "Gladiator",
        "genres": ["Action", "Adventure", "Drama"],
        "year": 2000,
        "director": "Ridley Scott",
        "cast": ["Russell Crowe", "Joaquin Phoenix", "Connie Nielsen"],
        "rating": 8.5,
        "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "plot_keywords": ["ancient Rome", "colosseum", "gladiator", "revenge", "honor"],
        "poster_color": "#7c2d12",
        "poster_emoji": "⚔️",
        "acting": 9.3,
        "visuals": 9.4,
        "story": 8.9,
        "pace": 8.9
    },
    {
        "id": 11,
        "title": "The Grand Budapest Hotel",
        "genres": ["Comedy", "Adventure", "Drama"],
        "year": 2014,
        "director": "Wes Anderson",
        "cast": ["Ralph Fiennes", "Tony Revolori", "Saoirse Ronan"],
        "rating": 8.1,
        "description": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy under an exceptional concierge.",
        "plot_keywords": ["pastel aesthetic", "heist", "quirky humor", "concierge", "friendship"],
        "poster_color": "#831843",
        "poster_emoji": "🏨",
        "acting": 9.2,
        "visuals": 9.8,
        "story": 8.7,
        "pace": 9.0
    },
    {
        "id": 12,
        "title": "Whiplash",
        "genres": ["Drama", "Music"],
        "year": 2014,
        "director": "Damien Chazelle",
        "cast": ["Miles Teller", "J.K. Simmons", "Paul Reiser"],
        "rating": 8.5,
        "description": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing.",
        "plot_keywords": ["jazz drumming", "obsession", "ruthless mentor", "perfectionism", "rivalry"],
        "poster_color": "#451a03",
        "poster_emoji": "🥁",
        "acting": 9.9,
        "visuals": 8.7,
        "story": 9.5,
        "pace": 9.8
    },
    {
        "id": 13,
        "title": "Avengers: Endgame",
        "genres": ["Action", "Adventure", "Sci-Fi"],
        "year": 2019,
        "director": "Anthony & Joe Russo",
        "cast": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"],
        "rating": 8.4,
        "description": "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions.",
        "plot_keywords": ["superheroes", "infinity stones", "time heist", "epic finale", "cosmic battle"],
        "poster_color": "#4c1d95",
        "poster_emoji": "🛡️",
        "acting": 8.6,
        "visuals": 9.6,
        "story": 8.5,
        "pace": 8.9
    },
    {
        "id": 14,
        "title": "The Shining",
        "genres": ["Horror", "Drama"],
        "year": 1980,
        "director": "Stanley Kubrick",
        "cast": ["Jack Nicholson", "Shelley Duvall", "Danny Lloyd"],
        "rating": 8.4,
        "description": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings.",
        "plot_keywords": ["isolated hotel", "cabin fever", "psychic vision", "madness", "maze"],
        "poster_color": "#701a75",
        "poster_emoji": "🪓",
        "acting": 9.6,
        "visuals": 9.5,
        "story": 9.0,
        "pace": 7.8
    },
    {
        "id": 15,
        "title": "La La Land",
        "genres": ["Comedy", "Drama", "Music", "Romance"],
        "year": 2016,
        "director": "Damien Chazelle",
        "cast": ["Ryan Gosling", "Emma Stone", "John Legend"],
        "rating": 8.0,
        "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        "plot_keywords": ["Hollywood", "jazz piano", "musical romance", "bittersweet dreams", "audition"],
        "poster_color": "#1e1b4b",
        "poster_emoji": "🎹",
        "acting": 9.3,
        "visuals": 9.7,
        "story": 8.6,
        "pace": 8.4
    },
    {
        "id": 16,
        "title": "Alien",
        "genres": ["Horror", "Sci-Fi"],
        "year": 1979,
        "director": "Ridley Scott",
        "cast": ["Sigourney Weaver", "Tom Skerritt", "John Hurt"],
        "rating": 8.5,
        "description": "The crew of a commercial spacecraft encounters a deadly lifeform after investigating a mysterious transmission of unknown origin on an uncharted moon.",
        "plot_keywords": ["xenomorph", "spaceship Nostromo", "chestburster", "claustrophobia", "survival"],
        "poster_color": "#064e3b",
        "poster_emoji": "👽",
        "acting": 9.1,
        "visuals": 9.5,
        "story": 9.2,
        "pace": 8.3
    },
    {
        "id": 17,
        "title": "Get Out",
        "genres": ["Horror", "Mystery", "Thriller"],
        "year": 2017,
        "director": "Jordan Peele",
        "cast": ["Daniel Kaluuya", "Allison Williams", "Bradley Whitford"],
        "rating": 7.8,
        "description": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception reaches a boiling point.",
        "plot_keywords": ["hypnosis", "sunken place", "social commentary", "suburban secret", "suspense"],
        "poster_color": "#18181b",
        "poster_emoji": "☕",
        "acting": 9.1,
        "visuals": 8.5,
        "story": 9.4,
        "pace": 9.2
    },
    {
        "id": 18,
        "title": "Toy Story",
        "genres": ["Animation", "Adventure", "Comedy"],
        "year": 1995,
        "director": "John Lasseter",
        "cast": ["Tom Hanks", "Tim Allen", "Don Rickles"],
        "rating": 8.3,
        "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.",
        "plot_keywords": ["living toys", "friendship", "jealousy", "Pixar", "childhood nostalgia"],
        "poster_color": "#1e3a5f",
        "poster_emoji": "🤠",
        "acting": 9.0,
        "visuals": 9.2,
        "story": 9.3,
        "pace": 9.1
    },
    {
        "id": 19,
        "title": "The Prestige",
        "genres": ["Drama", "Mystery", "Sci-Fi", "Thriller"],
        "year": 2006,
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Hugh Jackman", "Scarlett Johansson"],
        "rating": 8.5,
        "description": "After a tragic accident, two stage magicians in 1890s London engage in a battle to create the ultimate illusion while sacrificing everything to outwit each other.",
        "plot_keywords": ["rival magicians", "obsession", "teleportation", "Nikola Tesla", "twist ending"],
        "poster_color": "#3b0764",
        "poster_emoji": "🎩",
        "acting": 9.5,
        "visuals": 9.0,
        "story": 9.7,
        "pace": 8.9
    },
    {
        "id": 20,
        "title": "Titanic",
        "genres": ["Drama", "Romance"],
        "year": 1997,
        "director": "James Cameron",
        "cast": ["Leonardo DiCaprio", "Kate Winslet", "Billy Zane"],
        "rating": 7.9,
        "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "plot_keywords": ["shipwreck", "forbidden love", "iceberg", "ocean liner", "disaster spectacle"],
        "poster_color": "#0c4a6e",
        "poster_emoji": "🚢",
        "acting": 9.1,
        "visuals": 9.8,
        "story": 8.8,
        "pace": 8.1
    }
]

# Attribute names list
ATTRIBUTES = ["acting", "visuals", "story", "pace"]

# Precompute the Attribute Matrix A of shape (20, 4) using NumPy
ATTRIBUTE_MATRIX = np.array([
    [m["acting"], m["visuals"], m["story"], m["pace"]] for m in MOVIES_DATABASE
], dtype=np.float64)

# =========================================================================
# 2. HARDCODED USER-RATINGS MATRIX (7 USERS x 20 MOVIES)
# Scale: 1 to 5, 0 denotes unrated/unknown
# =========================================================================
BENCHMARK_USERS = [
    {"id": 1, "name": "Dr. Alice (Film Scholar)", "bias": "Story & Acting Prioritizer"},
    {"id": 2, "name": "Bob (Action Enthusiast)", "bias": "Pace & Visuals Prioritizer"},
    {"id": 3, "name": "Clara (VFX & Cinematography Artist)", "bias": "Visuals Prioritizer"},
    {"id": 4, "name": "David (Indie & Drama Critic)", "bias": "Acting & Deep Plot Critic"},
    {"id": 5, "name": "Elena (Casual Moviegoer)", "bias": "Popular Blockbuster Viewer"},
    {"id": 6, "name": "Farhan (Sci-Fi Theorist)", "bias": "Sci-Fi & Narrative Complexity"},
    {"id": 7, "name": "Grace (Thriller & Horror Fan)", "bias": "Pace & Suspense Lover"}
]

# Rows = 7 Users, Columns = 20 Movies
USER_RATINGS_MATRIX = np.array([
    # M1  M2  M3  M4  M5  M6  M7  M8  M9 M10 M11 M12 M13 M14 M15 M16 M17 M18 M19 M20
    [  4,  5,  4,  5,  5,  4,  0,  5,  5,  4,  5,  5,  0,  4,  4,  4,  4,  0,  5,  3], # Dr. Alice
    [  5,  5,  4,  4,  0,  3,  5,  3,  0,  5,  0,  4,  5,  3,  0,  4,  3,  4,  4,  2], # Bob
    [  5,  4,  5,  3,  4,  4,  5,  4,  5,  5,  5,  4,  5,  5,  5,  5,  3,  4,  4,  5], # Clara
    [  4,  5,  4,  5,  5,  5,  3,  5,  4,  4,  5,  5,  2,  5,  4,  4,  4,  3,  5,  4], # David
    [  4,  5,  4,  3,  4,  5,  4,  3,  4,  4,  3,  0,  5,  0,  4,  0,  3,  5,  3,  5], # Elena
    [  5,  4,  5,  4,  4,  3,  5,  4,  4,  3,  3,  4,  5,  3,  3,  5,  4,  3,  5,  3], # Farhan
    [  4,  5,  3,  5,  4,  0,  4,  5,  0,  4,  0,  5,  3,  5,  2,  5,  5,  0,  5,  2]  # Grace
], dtype=np.int32)


# =========================================================================
# 3. KNOWLEDGE-BASED ALGORITHM FROM SCRATCH (PURE NUMPY)
# =========================================================================
def compute_knowledge_scores(weights, genre_filter, min_year, min_rating):
    """
    Computes Multi-Attribute Utility Theory (MAUT) scores and evaluates
    constraint satisfaction for all 20 movies using pure NumPy.
    """
    w_vec = np.array([
        weights.get("acting", 8.0),
        weights.get("visuals", 9.0),
        weights.get("story", 9.0),
        weights.get("pace", 7.0)
    ], dtype=np.float64)

    sum_w = float(np.sum(w_vec))
    if sum_w == 0.0:
        w_vec = np.array([1.0, 1.0, 1.0, 1.0])
        sum_w = 4.0

    # 1. Multi-Attribute Utility Score via dot product: raw_score_i = sum(w_j * attr_{i,j})
    raw_scores = np.dot(ATTRIBUTE_MATRIX, w_vec)  # Shape (20,)

    # 2. Normalized Utility Score (0.0 to 10.0 scale) and percentage (0 - 100%)
    norm_scores_10 = raw_scores / sum_w
    norm_scores_pct = (norm_scores_10 / 10.0) * 100.0

    # 3. Predicted 5-star rating: mapped linearly from [0, 10] -> [1.0, 5.0]
    predicted_ratings = 1.0 + (norm_scores_10 / 10.0) * 4.0

    # 4. Constraint Evaluation
    all_results = []
    passed_items = []
    filtered_items = []

    for i, m in enumerate(MOVIES_DATABASE):
        reasons_failed = []

        # Constraint A: Genre match
        if genre_filter != "All" and genre_filter not in m["genres"]:
            reasons_failed.append(f"Genre does not include '{genre_filter}' (Has: {', '.join(m['genres'])})")

        # Constraint B: Minimum Release Year
        if m["year"] < min_year:
            reasons_failed.append(f"Release year {m['year']} < required min year {min_year}")

        # Constraint C: Minimum IMDb Rating
        if m["rating"] < min_rating:
            reasons_failed.append(f"IMDb rating {m['rating']:.1f} < required min rating {min_rating:.1f}")

        is_passed = len(reasons_failed) == 0

        # Criterion weighted contributions
        contributions = {
            "acting": float(round(w_vec[0] * m["acting"], 2)),
            "visuals": float(round(w_vec[1] * m["visuals"], 2)),
            "story": float(round(w_vec[2] * m["story"], 2)),
            "pace": float(round(w_vec[3] * m["pace"], 2))
        }

        # Determine dominant attribute justifying recommendation
        highest_attr = max(contributions, key=contributions.get)
        attr_titles = {"acting": "Exceptional Acting", "visuals": "Stunning Visuals", "story": "Masterful Storytelling", "pace": "Thrilling Pace"}
        justification = (
            f"High match driven by {attr_titles[highest_attr]} (Score: {m[highest_attr]:.1f}/10, contributing +{contributions[highest_attr]:.1f} pts) "
            f"aligning with your preference weight {weights[highest_attr]}."
        )

        item_data = {
            "id": m["id"],
            "title": m["title"],
            "genres": m["genres"],
            "year": m["year"],
            "director": m["director"],
            "cast": m["cast"],
            "rating": m["rating"],
            "description": m["description"],
            "plot_keywords": m["plot_keywords"],
            "poster_color": m["poster_color"],
            "poster_emoji": m["poster_emoji"],
            "acting": m["acting"],
            "visuals": m["visuals"],
            "story": m["story"],
            "pace": m["pace"],
            "raw_score": round(float(raw_scores[i]), 2),
            "norm_score_10": round(float(norm_scores_10[i]), 2),
            "match_pct": round(float(norm_scores_pct[i]), 1),
            "pred_rating": round(float(predicted_ratings[i]), 2),
            "contributions": contributions,
            "justification": justification,
            "passed": is_passed,
            "filter_reasons": reasons_failed
        }

        all_results.append(item_data)
        if is_passed:
            passed_items.append(item_data)
        else:
            filtered_items.append(item_data)

    # Sort passed items in descending order of utility score
    passed_items.sort(key=lambda x: x["norm_score_10"], reverse=True)
    for rank, item in enumerate(passed_items, 1):
        item["rank"] = rank

    return all_results, passed_items, filtered_items, w_vec


def compute_pairwise_cosine_similarity():
    """
    Computes pairwise Cosine Similarity between all 20 movies using pure NumPy
    over the 4-dimensional knowledge attribute matrix.
    Formula: Sim(a, b) = (a . b) / (||a|| * ||b||)
    """
    norms = np.linalg.norm(ATTRIBUTE_MATRIX, axis=1, keepdims=True)
    norm_A = ATTRIBUTE_MATRIX / norms
    sim_matrix = np.dot(norm_A, norm_A.T)
    return sim_matrix


# Compute static 20x20 attribute cosine similarity matrix
SIMILARITY_MATRIX = compute_pairwise_cosine_similarity()


# =========================================================================
# 4. MATPLOTLIB VISUALIZATION GENERATORS (BASE64 PNG OUTPUTS)
# =========================================================================
def generate_visualizations(w_vec, top_passed_movies):
    """
    Generates two publication-grade figures displaying algorithm internals:
    Figure 1: User Weights vs Top Recommended Movie Profiles & Stacked Points Breakdown.
    Figure 2: 20-Movie Multi-Attribute Matrix Heatmap & 20x20 Cosine Similarity Heatmap.
    """
    # -------------------------------------------------------------
    # FIGURE 1: Preference Weights Alignment & Top Scores Breakdown
    # -------------------------------------------------------------
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.0), dpi=130)

    # SUBPLOT 1: Grouped Bar Chart comparing User Weights vs #1 & #2 Movies
    labels = ["Acting", "Visuals", "Story", "Pace"]
    x = np.arange(len(labels))
    width = 0.26

    # Normalize user weights to 10 for comparison
    w_normalized = (w_vec / np.max(w_vec)) * 10.0 if np.max(w_vec) > 0 else w_vec

    ax1.bar(x - width, w_normalized, width, label='Your Normalized Weights (Max=10)', color='#f59e0b', edgecolor='#b45309')
    
    if len(top_passed_movies) > 0:
        top1 = top_passed_movies[0]
        top1_vals = [top1["acting"], top1["visuals"], top1["story"], top1["pace"]]
        ax1.bar(x, top1_vals, width, label=f'#1: {top1["title"]}', color='#2563eb', edgecolor='#1e40af')

    if len(top_passed_movies) > 1:
        top2 = top_passed_movies[1]
        top2_vals = [top2["acting"], top2["visuals"], top2["story"], top2["pace"]]
        ax1.bar(x + width, top2_vals, width, label=f'#2: {top2["title"]}', color='#10b981', edgecolor='#047857')

    ax1.set_title("User Criteria Preference Weights vs. Top Movie Profiles", fontsize=11, fontweight='bold', color='#003366')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontweight='bold')
    ax1.set_ylabel("Score / Weight (Scale 0 - 10)")
    ax1.set_ylim(0, 11.5)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right', fontsize=8.5)

    # SUBPLOT 2: Stacked Bar Chart for Top 5 Recommended Movies
    top_n = min(5, len(top_passed_movies))
    if top_n > 0:
        top_candidates = top_passed_movies[:top_n]
        titles = [item["title"] for item in top_candidates]
        y_pos = np.arange(top_n)

        acting_pts = np.array([w_vec[0] * item["acting"] for item in top_candidates])
        visuals_pts = np.array([w_vec[1] * item["visuals"] for item in top_candidates])
        story_pts = np.array([w_vec[2] * item["story"] for item in top_candidates])
        pace_pts = np.array([w_vec[3] * item["pace"] for item in top_candidates])

        p1 = ax2.barh(y_pos, acting_pts, label=f'Acting (w={w_vec[0]:.1f})', color='#3b82f6')
        p2 = ax2.barh(y_pos, visuals_pts, left=acting_pts, label=f'Visuals (w={w_vec[1]:.1f})', color='#8b5cf6')
        p3 = ax2.barh(y_pos, story_pts, left=acting_pts + visuals_pts, label=f'Story (w={w_vec[2]:.1f})', color='#ec4899')
        p4 = ax2.barh(y_pos, pace_pts, left=acting_pts + visuals_pts + story_pts, label=f'Pace (w={w_vec[3]:.1f})', color='#14b8a6')

        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(titles, fontweight='bold')
        ax2.invert_yaxis()
        ax2.set_xlabel("Weighted Utility Sum: Score(m) = Σ (w_i × s_{m,i})")
        ax2.set_title("Multi-Criteria Utility Breakdown (Top Ranked Candidates)", fontsize=11, fontweight='bold', color='#003366')
        ax2.legend(loc='lower right', fontsize=8.5)
        ax2.grid(axis='x', linestyle='--', alpha=0.5)
    else:
        ax2.text(0.5, 0.5, "No movies passed active constraint filters", horizontalalignment='center', verticalalignment='center')
        ax2.set_title("Multi-Criteria Utility Breakdown", fontsize=11, fontweight='bold')

    plt.tight_layout()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', bbox_inches='tight')
    buf1.seek(0)
    plot_b64_1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)

    # -------------------------------------------------------------
    # FIGURE 2: 20-Movie Criteria Matrix & 20x20 Similarity Heatmap
    # -------------------------------------------------------------
    fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14.0, 6.2), dpi=130)

    # SUBPLOT 3: Knowledge Attributes Heatmap for all 20 Movies
    movie_short_titles = [f"M{m['id']}: {m['title'][:14]}" for m in MOVIES_DATABASE]
    im1 = ax3.imshow(ATTRIBUTE_MATRIX, cmap='YlGnBu', aspect='auto', vmin=7.0, vmax=10.0)
    ax3.set_xticks(np.arange(4))
    ax3.set_xticklabels(["Acting", "Visuals", "Story", "Pace"], fontweight='bold')
    ax3.set_yticks(np.arange(len(MOVIES_DATABASE)))
    ax3.set_yticklabels(movie_short_titles, fontsize=7.5)
    ax3.set_title("20-Movie Multi-Attribute Knowledge Space Matrix", fontsize=11, fontweight='bold', color='#003366')
    plt.colorbar(im1, ax=ax3, fraction=0.046, pad=0.04, label="Attribute Score (1-10)")

    # Overlay numeric annotations
    for i in range(len(MOVIES_DATABASE)):
        for j in range(4):
            val = ATTRIBUTE_MATRIX[i, j]
            ax3.text(j, i, f"{val:.1f}", ha="center", va="center", color="black" if val < 9.3 else "white", fontsize=6.8)

    # SUBPLOT 4: 20x20 Pairwise Cosine Similarity Matrix
    im2 = ax4.imshow(SIMILARITY_MATRIX, cmap='magma', vmin=0.95, vmax=1.0)
    ax4.set_xticks(np.arange(20))
    ax4.set_xticklabels([f"M{i+1}" for i in range(20)], fontsize=6.5, rotation=90)
    ax4.set_yticks(np.arange(20))
    ax4.set_yticklabels([f"M{i+1}: {MOVIES_DATABASE[i]['title'][:10]}" for i in range(20)], fontsize=7.0)
    ax4.set_title("Pairwise Movie Attribute Cosine Similarity Matrix (20×20)", fontsize=11, fontweight='bold', color='#003366')
    plt.colorbar(im2, ax=ax4, fraction=0.046, pad=0.04, label="Cosine Similarity")

    plt.tight_layout()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', bbox_inches='tight')
    buf2.seek(0)
    plot_b64_2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)

    return plot_b64_1, plot_b64_2


# =========================================================================
# 5. FLASK ROUTING CONTROLLER
# =========================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    # Default preference weights
    weights = {
        "acting": 8.0,
        "visuals": 9.0,
        "story": 9.0,
        "pace": 7.0
    }
    genre_filter = "All"
    min_year = 1970
    min_rating = 8.0
    selected_movie_id = 1
    feedback_msg = None

    if request.method == 'POST':
        action = request.form.get('action', 'recommend')

        # Preset weight application
        preset = request.form.get('preset')
        if preset == 'cinephile':
            weights = {"acting": 10.0, "visuals": 7.0, "story": 10.0, "pace": 6.0}
            feedback_msg = "Applied Preset: Cinephile Critic (Prioritizing Story & Acting Depth)"
        elif preset == 'blockbuster':
            weights = {"acting": 6.0, "visuals": 10.0, "story": 7.0, "pace": 10.0}
            feedback_msg = "Applied Preset: Blockbuster Thrill (Prioritizing High Visuals & Fast Pace)"
        elif preset == 'visualist':
            weights = {"acting": 7.0, "visuals": 10.0, "story": 8.0, "pace": 6.0}
            feedback_msg = "Applied Preset: Visualist & Cinematography (Prioritizing Aesthetics)"
        elif preset == 'balanced':
            weights = {"acting": 8.0, "visuals": 8.0, "story": 8.0, "pace": 8.0}
            feedback_msg = "Applied Preset: Balanced Equal Weights (8.0 across all criteria)"
        else:
            try:
                weights["acting"] = float(request.form.get('w_acting', 8.0))
                weights["visuals"] = float(request.form.get('w_visuals', 9.0))
                weights["story"] = float(request.form.get('w_story', 9.0))
                weights["pace"] = float(request.form.get('w_pace', 7.0))
            except (ValueError, TypeError):
                weights = {"acting": 8.0, "visuals": 9.0, "story": 9.0, "pace": 7.0}

        # Constraint parameters
        genre_filter = request.form.get('genre_filter', 'All')
        try:
            min_year = int(request.form.get('min_year', 1970))
        except (ValueError, TypeError):
            min_year = 1970
        try:
            min_rating = float(request.form.get('min_rating', 8.0))
        except (ValueError, TypeError):
            min_rating = 8.0

        # Selected movie inspect
        try:
            selected_movie_id = int(request.form.get('selected_movie_id', 1))
        except (ValueError, TypeError):
            selected_movie_id = 1

        if action == 'inspect':
            feedback_msg = f"Inspecting Knowledge Profile & Attribute Similarities for Movie #{selected_movie_id}"
        elif action == 'rate':
            rate_val = request.form.get('user_rating_val', '5')
            feedback_msg = f"Logged your rating of {rate_val}★ for Movie #{selected_movie_id} into User Profile"

    # Compute recommendations and constraints
    all_movies, passed_movies, filtered_movies, w_vec = compute_knowledge_scores(
        weights, genre_filter, min_year, min_rating
    )

    # Retrieve selected movie details and top-3 attribute-similar movies
    selected_movie = next((m for m in all_movies if m["id"] == selected_movie_id), all_movies[0])
    selected_idx = selected_movie["id"] - 1
    sim_scores = SIMILARITY_MATRIX[selected_idx]
    
    # Sort by similarity, exclude self
    similar_indices = np.argsort(sim_scores)[::-1]
    similar_indices = [idx for idx in similar_indices if idx != selected_idx][:3]
    top_similar_movies = []
    for idx in similar_indices:
        top_similar_movies.append({
            "id": MOVIES_DATABASE[idx]["id"],
            "title": MOVIES_DATABASE[idx]["title"],
            "genres": MOVIES_DATABASE[idx]["genres"],
            "rating": MOVIES_DATABASE[idx]["rating"],
            "poster_emoji": MOVIES_DATABASE[idx]["poster_emoji"],
            "poster_color": MOVIES_DATABASE[idx]["poster_color"],
            "sim_pct": round(float(sim_scores[idx]) * 100.0, 2)
        })

    # Generate Matplotlib Base64 plots
    plot_b64_1, plot_b64_2 = generate_visualizations(w_vec, passed_movies)

    # Compute benchmark user ratings statistics
    rated_mask = USER_RATINGS_MATRIX > 0
    total_ratings_count = int(np.sum(rated_mask))
    sparsity_pct = round((1.0 - (total_ratings_count / (7 * 20))) * 100.0, 1)
    movie_mean_ratings = []
    for col in range(20):
        col_ratings = USER_RATINGS_MATRIX[:, col]
        col_rated = col_ratings[col_ratings > 0]
        mean_val = round(float(np.mean(col_rated)), 2) if len(col_rated) > 0 else 0.0
        movie_mean_ratings.append(mean_val)

    # Format benchmark users with their rating row list
    users_with_ratings = []
    for i, u in enumerate(BENCHMARK_USERS):
        u_copy = dict(u)
        u_copy["ratings"] = USER_RATINGS_MATRIX[i].tolist()
        users_with_ratings.append(u_copy)

    # Distinct genres list for filter dropdown
    all_genres = sorted(list(set(g for m in MOVIES_DATABASE for g in m["genres"])))

    return render_template(
        'index.html',
        movies=all_movies,
        passed_movies=passed_movies,
        filtered_movies=filtered_movies,
        weights=weights,
        genre_filter=genre_filter,
        min_year=min_year,
        min_rating=min_rating,
        selected_movie=selected_movie,
        top_similar_movies=top_similar_movies,
        plot_b64_1=plot_b64_1,
        plot_b64_2=plot_b64_2,
        all_genres=all_genres,
        feedback_msg=feedback_msg,
        benchmark_users=users_with_ratings,
        user_ratings_matrix=USER_RATINGS_MATRIX,
        movie_mean_ratings=movie_mean_ratings,
        sparsity_pct=sparsity_pct,
        total_ratings_count=total_ratings_count
    )


@app.route('/api/movie/<int:movie_id>')
def api_movie(movie_id):
    movie = next((m for m in MOVIES_DATABASE if m["id"] == movie_id), None)
    if movie is None:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(movie)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5020))
    print(f"============================================================")
    print(f" PARS LAB EXPERIMENT 20: KNOWLEDGE-BASED RECOMMENDER SYSTEM ")
    print(f" Server active on: http://127.0.0.1:{port}")
    print(f"============================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
