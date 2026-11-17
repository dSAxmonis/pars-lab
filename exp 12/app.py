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
# MOVIES DATASET (20 Benchmark Movies Across Multiple Genres)
# ==============================================================================
MOVIES = [
    {
        "id": 0,
        "title": "Inception",
        "genres": ["Sci-Fi", "Action", "Thriller"],
        "year": 2010,
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
        "rating": 8.8,
        "plot_keywords": ["dreams", "subconscious", "heist", "mind-bending", "reality", "architecture", "espionage"],
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        "color": "#0f172a",
        "emoji": "🌀"
    },
    {
        "id": 1,
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "year": 2008,
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "rating": 9.0,
        "plot_keywords": ["superhero", "vigilante", "joker", "crime", "corruption", "gotham", "justice", "chaos"],
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "color": "#1e293b",
        "emoji": "🦇"
    },
    {
        "id": 2,
        "title": "Interstellar",
        "genres": ["Sci-Fi", "Drama", "Adventure"],
        "year": 2014,
        "director": "Christopher Nolan",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "rating": 8.7,
        "plot_keywords": ["space", "wormhole", "black-hole", "time-dilation", "astronaut", "father-daughter", "survival"],
        "description": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.",
        "color": "#03254c",
        "emoji": "🚀"
    },
    {
        "id": 3,
        "title": "The Matrix",
        "genres": ["Sci-Fi", "Action"],
        "year": 1999,
        "director": "Lana Wachowski",
        "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
        "rating": 8.7,
        "plot_keywords": ["simulated-reality", "cyberpunk", "rebellion", "ai", "chosen-one", "martial-arts", "virtual-world"],
        "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.",
        "color": "#064e3b",
        "emoji": "🕶️"
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama", "Thriller"],
        "year": 1994,
        "director": "Quentin Tarantino",
        "cast": ["John Travolta", "Samuel L. Jackson", "Uma Thurman"],
        "rating": 8.9,
        "plot_keywords": ["hitmen", "diner", "briefcase", "mobsters", "non-linear", "dialogue", "dark-comedy", "crime"],
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "color": "#7f1d1d",
        "emoji": "🔫"
    },
    {
        "id": 5,
        "title": "The Godfather",
        "genres": ["Crime", "Drama"],
        "year": 1972,
        "director": "Francis Ford Coppola",
        "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
        "rating": 9.2,
        "plot_keywords": ["mafia", "family", "organized-crime", "power", "betrayal", "legacy", "succession", "loyalty"],
        "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "color": "#3b0764",
        "emoji": "🎩"
    },
    {
        "id": 6,
        "title": "Titanic",
        "genres": ["Romance", "Drama"],
        "year": 1997,
        "director": "James Cameron",
        "cast": ["Leonardo DiCaprio", "Kate Winslet", "Billy Zane"],
        "rating": 7.9,
        "plot_keywords": ["shipwreck", "luxury-liner", "tragic-romance", "class-divide", "iceberg", "love", "survival"],
        "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "color": "#1e3a8a",
        "emoji": "🚢"
    },
    {
        "id": 7,
        "title": "La La Land",
        "genres": ["Romance", "Comedy", "Drama"],
        "year": 2016,
        "director": "Damien Chazelle",
        "cast": ["Ryan Gosling", "Emma Stone", "John Legend"],
        "rating": 8.0,
        "plot_keywords": ["jazz", "music", "musical", "hollywood", "ambition", "heartbreak", "romance", "passion"],
        "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        "color": "#831843",
        "emoji": "🎷"
    },
    {
        "id": 8,
        "title": "Superbad",
        "genres": ["Comedy"],
        "year": 2007,
        "director": "Greg Mottola",
        "cast": ["Jonah Hill", "Michael Cera", "Christopher Mintz-Plasse"],
        "rating": 7.6,
        "plot_keywords": ["high-school", "friendship", "fake-id", "party", "alcohol", "teenage", "coming-of-age", "hilarity"],
        "description": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.",
        "color": "#b45309",
        "emoji": "🍻"
    },
    {
        "id": 9,
        "title": "The Hangover",
        "genres": ["Comedy"],
        "year": 2009,
        "director": "Todd Phillips",
        "cast": ["Bradley Cooper", "Ed Helms", "Zach Galifianakis"],
        "rating": 7.7,
        "plot_keywords": ["bachelor-party", "las-vegas", "wedding", "comedy", "memory-loss", "tiger", "chaos"],
        "description": "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing.",
        "color": "#d97706",
        "emoji": "🎰"
    },
    {
        "id": 10,
        "title": "The Conjuring",
        "genres": ["Horror", "Thriller"],
        "year": 2013,
        "director": "James Wan",
        "cast": ["Vera Farmiga", "Patrick Wilson", "Lili Taylor"],
        "rating": 7.5,
        "plot_keywords": ["haunted-house", "paranormal", "demon", "possession", "ghost-hunters", "farmhouse", "evil"],
        "description": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.",
        "color": "#374151",
        "emoji": "👻"
    },
    {
        "id": 11,
        "title": "Hereditary",
        "genres": ["Horror", "Drama", "Thriller"],
        "year": 2018,
        "director": "Ari Aster",
        "cast": ["Toni Collette", "Alex Wolff", "Milly Shapiro"],
        "rating": 7.3,
        "plot_keywords": ["family-curse", "occult", "grief", "psychological", "demon-king", "trauma", "dread", "seance"],
        "description": "A grieving family is haunted by tragic and disturbing occurrences after the death of their secretive grandmother.",
        "color": "#450a0a",
        "emoji": "🕯️"
    },
    {
        "id": 12,
        "title": "Parasite",
        "genres": ["Thriller", "Drama", "Comedy"],
        "year": 2019,
        "director": "Bong Joon-ho",
        "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
        "rating": 8.5,
        "plot_keywords": ["class-divide", "social-inequality", "deception", "basement", "infiltration", "satire", "dark-comedy"],
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "color": "#14532d",
        "emoji": "🪱"
    },
    {
        "id": 13,
        "title": "Se7en",
        "genres": ["Thriller", "Crime", "Drama"],
        "year": 1995,
        "director": "David Fincher",
        "cast": ["Brad Pitt", "Morgan Freeman", "Kevin Spacey"],
        "rating": 8.6,
        "plot_keywords": ["serial-killer", "seven-deadly-sins", "detective", "rain", "box", "dark", "investigation"],
        "description": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.",
        "color": "#262626",
        "emoji": "📦"
    },
    {
        "id": 14,
        "title": "Avengers: Endgame",
        "genres": ["Action", "Sci-Fi", "Adventure"],
        "year": 2019,
        "director": "Anthony Russo",
        "cast": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"],
        "rating": 8.4,
        "plot_keywords": ["superheroes", "time-travel", "marvel", "infinity-stones", "sacrifice", "epic", "battle"],
        "description": "After the devastating events of Infinity War, the Avengers assemble once more to reverse Thanos' actions.",
        "color": "#4338ca",
        "emoji": "🛡️"
    },
    {
        "id": 15,
        "title": "Gladiator",
        "genres": ["Action", "Drama", "Adventure"],
        "year": 2000,
        "director": "Ridley Scott",
        "cast": ["Russell Crowe", "Joaquin Phoenix", "Connie Nielsen"],
        "rating": 8.5,
        "plot_keywords": ["roman-empire", "colosseum", "vengeance", "general", "emperor", "betrayal", "combat", "honor"],
        "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "color": "#78350f",
        "emoji": "⚔️"
    },
    {
        "id": 16,
        "title": "Forgetting Sarah Marshall",
        "genres": ["Comedy", "Romance"],
        "year": 2008,
        "director": "Nicholas Stoller",
        "cast": ["Jason Segel", "Kristen Bell", "Mila Kunis"],
        "rating": 7.1,
        "plot_keywords": ["break-up", "hawaii", "resort", "ex-girlfriend", "vacation", "comedy", "heartbreak", "music"],
        "description": "Devastated Peter takes a Hawaiian vacation in order to deal with recent break-up with his TV star girlfriend, only to find that she is staying at the same resort.",
        "color": "#be185d",
        "emoji": "💔"
    },
    {
        "id": 17,
        "title": "A Quiet Place",
        "genres": ["Horror", "Sci-Fi", "Thriller"],
        "year": 2018,
        "director": "John Krasinski",
        "cast": ["Emily Blunt", "John Krasinski", "Millicent Simmonds"],
        "rating": 7.5,
        "plot_keywords": ["silence", "monsters", "sound-hunting", "post-apocalyptic", "family", "survival", "sign-language"],
        "description": "In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing.",
        "color": "#111827",
        "emoji": "🤫"
    },
    {
        "id": 18,
        "title": "The Shawshank Redemption",
        "genres": ["Drama", "Crime"],
        "year": 1994,
        "director": "Frank Darabont",
        "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
        "rating": 9.3,
        "plot_keywords": ["prison", "hope", "friendship", "wrongful-conviction", "escape", "resilience", "redemption"],
        "description": "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
        "color": "#1f2937",
        "emoji": "🏛️"
    },
    {
        "id": 19,
        "title": "Blade Runner 2049",
        "genres": ["Sci-Fi", "Mystery", "Thriller"],
        "year": 2017,
        "director": "Denis Villeneuve",
        "cast": ["Ryan Gosling", "Harrison Ford", "Ana de Armas"],
        "rating": 8.0,
        "plot_keywords": ["replicant", "cyberpunk", "dystopian", "memory", "future", "detective", "ai", "neon"],
        "description": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.",
        "color": "#1e1b4b",
        "emoji": "🤖"
    }
]

M = len(MOVIES)

# ==============================================================================
# HARDCODED USER RATINGS MATRIX (8 Users x 20 Movies, Scale 1 to 5, 0 = Unrated)
# ==============================================================================
USERS = [
    {
        "id": 0,
        "name": "Alice Sharma",
        "archetype": "Sci-Fi & Cyberpunk Buff",
        "description": "Passionate about mind-bending physics, space-travel, and futuristic AI.",
        "ratings": {0: 5, 2: 5, 3: 5, 14: 4, 17: 4, 19: 5} # Inception, Interstellar, Matrix, Endgame, Quiet Place, Blade Runner 2049
    },
    {
        "id": 1,
        "name": "Bob Anderson",
        "archetype": "Crime & Noir Connoisseur",
        "description": "Loves classic mafia drama, gritty detectives, and dark neo-noir thrillers.",
        "ratings": {1: 4, 4: 5, 5: 5, 13: 5, 18: 5} # Dark Knight, Pulp Fiction, Godfather, Se7en, Shawshank
    },
    {
        "id": 2,
        "name": "Charlie Miller",
        "archetype": "Comedy & Lighthearted Fan",
        "description": "Enjoys hilarious comedies, coming-of-age laughs, and musical rom-coms.",
        "ratings": {7: 4, 8: 5, 9: 5, 12: 3, 16: 4} # La La Land, Superbad, Hangover, Parasite, Sarah Marshall
    },
    {
        "id": 3,
        "name": "Diana Prince",
        "archetype": "Horror & Psychological Dread",
        "description": "Thrives on paranormal terror, haunted tension, and occult thrillers.",
        "ratings": {0: 3, 10: 5, 11: 5, 13: 4, 17: 5} # Inception, Conjuring, Hereditary, Se7en, Quiet Place
    },
    {
        "id": 4,
        "name": "Evan Wright",
        "archetype": "Romance & Melodrama Critic",
        "description": "Drawn to emotional storytelling, tragic love, jazz music, and human drama.",
        "ratings": {6: 5, 7: 5, 15: 3, 16: 4, 18: 4} # Titanic, La La Land, Gladiator, Sarah Marshall, Shawshank
    },
    {
        "id": 5,
        "name": "Fiona Gallagher",
        "archetype": "Action & Epic Blockbusters",
        "description": "Loves high-octane stunts, superhero sagas, gladiatorial combat, and spectacles.",
        "ratings": {0: 4, 1: 5, 3: 5, 14: 5, 15: 5} # Inception, Dark Knight, Matrix, Endgame, Gladiator
    },
    {
        "id": 6,
        "name": "George Lucas",
        "archetype": "Suspense & Mystery Sleuth",
        "description": "Fascinated by plot twists, serial murder cases, and social satire.",
        "ratings": {0: 4, 11: 4, 12: 5, 13: 5, 17: 4, 19: 4} # Inception, Hereditary, Parasite, Se7en, Quiet Place, Blade Runner
    },
    {
        "id": 7,
        "name": "Hannah Abbott",
        "archetype": "Eclectic Cinephile",
        "description": "Values artistic cinematography, deep scripts, and acclaimed masterpieces.",
        "ratings": {1: 4, 5: 5, 7: 4, 12: 5, 18: 5} # Dark Knight, Godfather, La La Land, Parasite, Shawshank
    }
]

# Build User Ratings Matrix (8, 20)
R_matrix = np.zeros((len(USERS), M), dtype=float)
for u in USERS:
    for m_id, r_val in u["ratings"].items():
        if m_id < M:
            R_matrix[u["id"], m_id] = float(r_val)


# ==============================================================================
# ALGORITHM FROM SCRATCH: TF-IDF FEATURE EXTRACTION & COSINE SIMILARITY (NUMPY)
# ==============================================================================
def normalize_token(t):
    return t.strip().lower().replace(" ", "_").replace("-", "_")

def build_content_feature_matrix():
    """
    Builds TF-IDF feature matrix X (M x K) and Cosine Similarity matrix S (M x M)
    entirely from scratch using NumPy.
    """
    movie_docs = []
    for m in MOVIES:
        tokens = []
        # Genres (double weighted for genre emphasis)
        for g in m["genres"]:
            tg = "genre_" + normalize_token(g)
            tokens.extend([tg, tg])
        # Director
        tokens.append("dir_" + normalize_token(m["director"]))
        # Cast members
        for c in m["cast"]:
            tokens.append("cast_" + normalize_token(c))
        # Plot keywords
        for k in m["plot_keywords"]:
            tokens.append("kw_" + normalize_token(k))
        movie_docs.append(tokens)

    # 1. Unique Vocabulary
    vocab_set = set()
    for doc in movie_docs:
        vocab_set.update(doc)
    vocab = sorted(list(vocab_set))
    word2idx = {w: i for i, w in enumerate(vocab)}
    K = len(vocab)

    # 2. Term Frequency (TF) matrix
    TF = np.zeros((M, K), dtype=float)
    for i, doc in enumerate(movie_docs):
        doc_len = max(len(doc), 1)
        for w in doc:
            j = word2idx[w]
            TF[i, j] += 1.0
        TF[i, :] /= doc_len  # Normalize by document token count

    # 3. Document Frequency (DF) & Inverse Document Frequency (IDF)
    # Smooth IDF: ln((1 + M) / (1 + DF)) + 1
    DF = np.zeros(K, dtype=float)
    for j in range(K):
        # Count movies where term j appears at least once
        DF[j] = np.sum(TF[:, j] > 0)
    
    IDF = np.log((1.0 + M) / (1.0 + DF)) + 1.0

    # 4. TF-IDF Matrix X
    X_tfidf = TF * IDF

    # 5. Row-wise L2 Normalization (Euclidean norm)
    row_norms = np.linalg.norm(X_tfidf, axis=1, keepdims=True)
    row_norms[row_norms == 0] = 1.0
    X_norm = X_tfidf / row_norms

    # 6. Pairwise Cosine Similarity Matrix S = X_norm * X_norm^T
    S_matrix = np.dot(X_norm, X_norm.T)

    # Clip numerical precision artifacts to [0.0, 1.0]
    S_matrix = np.clip(S_matrix, 0.0, 1.0)
    # Ensure exact 1.0 on diagonal
    np.fill_diagonal(S_matrix, 1.0)

    return movie_docs, vocab, word2idx, X_norm, S_matrix, TF, IDF

# Precompute content vectors
MOVIE_DOCS, VOCAB, WORD2IDX, X_NORM, S_MATRIX, TF_MATRIX, IDF_VECTOR = build_content_feature_matrix()


def get_item_recommendations(movie_idx, top_n=5):
    """
    Retrieves top_n most similar movies to movie_idx using content-based cosine similarity.
    """
    sim_scores = S_MATRIX[movie_idx].copy()
    
    # Sort indices in descending order of similarity
    ranked_indices = np.argsort(-sim_scores)
    
    recommendations = []
    source_movie = MOVIES[movie_idx]
    source_tokens = set(MOVIE_DOCS[movie_idx])

    for idx in ranked_indices:
        if idx == movie_idx:
            continue  # Exclude self
        
        target_movie = MOVIES[idx]
        target_tokens = set(MOVIE_DOCS[idx])
        shared_tokens = source_tokens.intersection(target_tokens)
        
        # Clean explanations
        shared_readable = []
        for t in shared_tokens:
            if t.startswith("genre_"):
                shared_readable.append(f"Genre: {t[6:].replace('_', ' ').title()}")
            elif t.startswith("dir_"):
                shared_readable.append(f"Director: {t[4:].replace('_', ' ').title()}")
            elif t.startswith("cast_"):
                shared_readable.append(f"Cast: {t[5:].replace('_', ' ').title()}")
            elif t.startswith("kw_"):
                shared_readable.append(f"Keyword: {t[3:].replace('_', '-')}")
                
        sim_val = float(sim_scores[idx])
        recommendations.append({
            "movie": target_movie,
            "similarity": round(sim_val, 4),
            "sim_percent": round(sim_val * 100.0, 1),
            "reasons": shared_readable[:4],
            "common_count": len(shared_tokens)
        })
        
        if len(recommendations) >= top_n:
            break

    return recommendations


def get_user_personalized_recommendations(user_idx, top_n=5, active_ratings=None):
    """
    Constructs user content preference profile vector and predicts affinities
    for unrated movies.
    """
    if active_ratings is not None:
        user_ratings = active_ratings
    else:
        user_ratings = R_matrix[user_idx].copy()

    rated_indices = np.where(user_ratings > 0)[0]
    
    if len(rated_indices) == 0:
        # Default fallback
        user_mean = 3.5
        user_profile = np.mean(X_NORM, axis=0)
    else:
        user_mean = float(np.mean(user_ratings[rated_indices]))
        # Weighted preference vector centered around baseline
        weights = user_ratings[rated_indices] - (user_mean - 1.0)
        profile_accum = np.zeros(X_NORM.shape[1], dtype=float)
        for i, idx in enumerate(rated_indices):
            profile_accum += weights[i] * X_NORM[idx]
        p_norm = np.linalg.norm(profile_accum)
        user_profile = profile_accum / (p_norm if p_norm > 0 else 1.0)

    # Predicted cosine affinity
    affinities = np.dot(X_NORM, user_profile)
    
    # Predict rating on scale 1 to 5: mean + scaled affinity
    predicted_ratings = np.clip(user_mean + 2.4 * (affinities - 0.2), 1.0, 5.0)

    # Rank unrated movies
    candidate_indices = np.where(user_ratings == 0)[0]
    if len(candidate_indices) == 0:
        candidate_indices = np.arange(M)

    ranked_candidates = candidate_indices[np.argsort(-affinities[candidate_indices])]
    
    recommendations = []
    for idx in ranked_candidates[:top_n]:
        aff = float(affinities[idx])
        pred_r = float(predicted_ratings[idx])
        recommendations.append({
            "movie": MOVIES[idx],
            "affinity": round(aff, 4),
            "affinity_percent": round(max(aff, 0.0) * 100.0, 1),
            "predicted_rating": round(pred_r, 1),
            "stars": "★" * int(round(pred_r)) + "☆" * (5 - int(round(pred_r)))
        })

    # Summary of rated movies
    rated_summary = []
    for idx in rated_indices:
        rated_summary.append({
            "movie": MOVIES[idx],
            "rating": int(user_ratings[idx])
        })

    return recommendations, rated_summary, round(user_mean, 2)


# ==============================================================================
# MATPLOTLIB VISUALIZATION ENGINE (4-PANEL ALGORITHM HEATMAP & METRICS)
# ==============================================================================
def generate_recommender_plots(selected_movie_idx, selected_user_idx):
    """
    Generates a 4-panel visual dashboard illustrating:
    1. 20x20 Movie-to-Movie Cosine Similarity Heatmap with active movie highlighted.
    2. Horizontal bar chart of top similar movies.
    3. Top TF-IDF keyword weights for the selected movie.
    4. User-Item rating matrix sparsity and profile matching.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 11), dpi=120)
    plt.subplots_adjust(wspace=0.32, hspace=0.38)
    
    short_titles = [m["title"][:11] for m in MOVIES]

    # --------------------------------------------------------------------------
    # PANEL 1: Cosine Similarity Matrix Heatmap
    # --------------------------------------------------------------------------
    ax1 = axes[0, 0]
    im1 = ax1.imshow(S_MATRIX, cmap="YlGnBu", interpolation="nearest", vmin=0.0, vmax=1.0)
    ax1.set_title(f"20x20 Movie Cosine Similarity Matrix\n(Active: #{selected_movie_idx} {MOVIES[selected_movie_idx]['title']})",
                  fontsize=11, fontweight="bold", color="#003366")
    
    ax1.set_xticks(range(M))
    ax1.set_yticks(range(M))
    ax1.set_xticklabels(short_titles, rotation=90, fontsize=7.5)
    ax1.set_yticklabels(short_titles, fontsize=7.5)
    
    # Highlight the selected movie row and column
    ax1.axhline(selected_movie_idx, color="#d97706", linewidth=2.0, linestyle="--")
    ax1.axvline(selected_movie_idx, color="#d97706", linewidth=2.0, linestyle="--")
    
    cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label("Cosine Similarity S(i, j)", fontsize=8.5)

    # --------------------------------------------------------------------------
    # PANEL 2: Top-6 Similar Movies Bar Chart
    # --------------------------------------------------------------------------
    ax2 = axes[0, 1]
    top_sims = get_item_recommendations(selected_movie_idx, top_n=6)
    rec_names = [r["movie"]["title"] for r in reversed(top_sims)]
    rec_scores = [r["similarity"] for r in reversed(top_sims)]
    
    colors = plt.cm.viridis(np.linspace(0.4, 0.9, len(rec_scores)))
    bars = ax2.barh(range(len(rec_names)), rec_scores, color=colors, edgecolor="#1e293b", height=0.6)
    ax2.set_yticks(range(len(rec_names)))
    ax2.set_yticklabels(rec_names, fontsize=8.5, fontweight="bold")
    ax2.set_xlim(0.0, 1.05)
    ax2.set_xlabel("Cosine Similarity Score", fontsize=9, fontweight="bold")
    ax2.set_title(f"Top Content Matches for '{MOVIES[selected_movie_idx]['title']}'",
                  fontsize=11, fontweight="bold", color="#003366")
    ax2.grid(axis='x', linestyle=':', alpha=0.6)

    # Annotate bar values
    for bar, score in zip(bars, rec_scores):
        width = bar.get_width()
        ax2.text(width + 0.02, bar.get_y() + bar.get_height()/2.0,
                 f"{score:.3f} ({score*100:.1f}%)",
                 va='center', ha='left', fontsize=8, color="#1e3a8a", fontweight="bold")

    # --------------------------------------------------------------------------
    # PANEL 3: Top TF-IDF Feature Weights for Selected Movie
    # --------------------------------------------------------------------------
    ax3 = axes[1, 0]
    movie_vector = X_NORM[selected_movie_idx]
    top_term_indices = np.argsort(-movie_vector)[:10]
    top_term_indices = [idx for idx in top_term_indices if movie_vector[idx] > 0]
    
    if len(top_term_indices) == 0:
        top_term_indices = range(5)
    
    term_labels = [VOCAB[idx].replace("genre_", "genre: ").replace("kw_", "tag: ").replace("dir_", "dir: ").replace("cast_", "cast: ") for idx in reversed(top_term_indices)]
    term_weights = [movie_vector[idx] for idx in reversed(top_term_indices)]

    bars3 = ax3.barh(range(len(term_labels)), term_weights, color="#3b82f6", edgecolor="#1d4ed8", height=0.6)
    ax3.set_yticks(range(len(term_labels)))
    ax3.set_yticklabels(term_labels, fontsize=8.5)
    ax3.set_xlabel("Normalized TF-IDF Feature Weight", fontsize=9, fontweight="bold")
    ax3.set_title(f"Dominant TF-IDF Features: '{MOVIES[selected_movie_idx]['title']}'",
                  fontsize=11, fontweight="bold", color="#003366")
    ax3.grid(axis='x', linestyle=':', alpha=0.6)

    for bar, weight in zip(bars3, term_weights):
        width = bar.get_width()
        ax3.text(width + 0.01, bar.get_y() + bar.get_height()/2.0,
                 f"{weight:.3f}",
                 va='center', ha='left', fontsize=8, color="#1e293b")

    # --------------------------------------------------------------------------
    # PANEL 4: User Ratings Matrix Sparsity Heatmap
    # --------------------------------------------------------------------------
    ax4 = axes[1, 1]
    masked_R = np.ma.masked_where(R_matrix == 0, R_matrix)
    cmap_ratings = plt.colormaps['YlOrRd'].resampled(5)
    cmap_ratings.set_bad(color="#e2e8f0")
    
    im4 = ax4.imshow(masked_R, cmap=cmap_ratings, vmin=1, vmax=5, aspect="auto")
    user_names = [f"U{u['id']}: {u['name'].split()[0]}" for u in USERS]
    ax4.set_yticks(range(len(USERS)))
    ax4.set_yticklabels(user_names, fontsize=8.5)
    ax4.set_xticks(range(M))
    ax4.set_xticklabels(short_titles, rotation=90, fontsize=7.5)
    ax4.set_title(f"User Ratings Matrix Sparsity & Ratings\n(Active: {USERS[selected_user_idx]['name']} highlighted)",
                  fontsize=11, fontweight="bold", color="#003366")
    
    # Highlight selected user row
    ax4.axhline(selected_user_idx, color="#2563eb", linewidth=2.5, linestyle="-")
    
    cbar4 = plt.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04, ticks=[1, 2, 3, 4, 5])
    cbar4.set_label("Observed Star Rating (1-5)", fontsize=8.5)

    # Save to Base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return plot_base64


# ==============================================================================
# FLASK WEB CONTROLLER & ROUTES
# ==============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    selected_movie_id = 0
    selected_user_id = 0
    active_genre_filter = "All"
    user_feedback_msg = None

    if request.method == 'POST':
        action = request.form.get("action", "select_movie")
        
        # Parse selected movie
        try:
            selected_movie_id = int(request.form.get("movie_id", 0))
        except (ValueError, TypeError):
            selected_movie_id = 0
            
        # Parse selected user
        try:
            selected_user_id = int(request.form.get("user_id", 0))
        except (ValueError, TypeError):
            selected_user_id = 0

        # Genre filter
        active_genre_filter = request.form.get("genre_filter", "All")

        # Custom rating interaction
        if action == "rate_movie":
            try:
                rate_movie_id = int(request.form.get("rate_movie_id"))
                star_rating = int(request.form.get("star_rating"))
                if 0 <= rate_movie_id < M and 1 <= star_rating <= 5:
                    R_matrix[selected_user_id, rate_movie_id] = float(star_rating)
                    USERS[selected_user_id]["ratings"][rate_movie_id] = star_rating
                    user_feedback_msg = f"Successfully recorded rating of {star_rating}★ for '{MOVIES[rate_movie_id]['title']}' by {USERS[selected_user_id]['name']}!"
                    selected_movie_id = rate_movie_id
            except Exception as e:
                user_feedback_msg = f"Rating error: {str(e)}"

    else:
        # GET request query parameters
        try:
            selected_movie_id = int(request.args.get("movie_id", 0))
        except (ValueError, TypeError):
            selected_movie_id = 0
        try:
            selected_user_id = int(request.args.get("user_id", 0))
        except (ValueError, TypeError):
            selected_user_id = 0
        active_genre_filter = request.args.get("genre_filter", "All")

    # Safety bounds
    selected_movie_id = max(0, min(M - 1, selected_movie_id))
    selected_user_id = max(0, min(len(USERS) - 1, selected_user_id))

    # Compute Recommendations
    item_recommendations = get_item_recommendations(selected_movie_id, top_n=5)
    user_recommendations, rated_summary, user_mean = get_user_personalized_recommendations(selected_user_id, top_n=5)

    # Filter movie catalog if requested
    filtered_movies = []
    for m in MOVIES:
        if active_genre_filter == "All" or active_genre_filter in m["genres"]:
            filtered_movies.append(m)

    # Generate Algorithm Internals Visualization Plot
    plot_url = generate_recommender_plots(selected_movie_id, selected_user_id)

    # Extract Top TF-IDF keywords for the selected movie to show in UI
    selected_movie_vec = X_NORM[selected_movie_id]
    top_indices = np.argsort(-selected_movie_vec)[:8]
    selected_movie_keywords = [
        {"term": VOCAB[idx].replace("genre_", "Genre: ").replace("kw_", "Keyword: ").replace("dir_", "Director: ").replace("cast_", "Cast: "),
         "weight": round(float(selected_movie_vec[idx]), 3)}
        for idx in top_indices if selected_movie_vec[idx] > 0
    ]

    # Full Cosine Similarity Matrix Row for the selected movie
    sim_row_data = []
    for j in range(M):
        sim_row_data.append({
            "id": j,
            "title": MOVIES[j]["title"],
            "score": round(float(S_MATRIX[selected_movie_id, j]), 4),
            "is_selected": (j == selected_movie_id)
        })

    all_genres = ["All", "Action", "Adventure", "Comedy", "Crime", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller"]

    return render_template(
        'index.html',
        movies=MOVIES,
        filtered_movies=filtered_movies,
        selected_movie=MOVIES[selected_movie_id],
        selected_movie_id=selected_movie_id,
        selected_user=USERS[selected_user_id],
        selected_user_id=selected_user_id,
        users=USERS,
        item_recommendations=item_recommendations,
        user_recommendations=user_recommendations,
        rated_summary=rated_summary,
        user_mean=user_mean,
        plot_url=plot_url,
        selected_movie_keywords=selected_movie_keywords,
        sim_row_data=sim_row_data,
        all_genres=all_genres,
        active_genre_filter=active_genre_filter,
        user_feedback_msg=user_feedback_msg,
        total_movies=M,
        vocab_size=len(VOCAB)
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5012))
    print(f"=================================================================")
    print(f"🎬 PARS LAB - EXPERIMENT 12: CONTENT-BASED RECOMMENDER SYSTEM")
    print(f"🚀 Running on http://127.0.0.1:{port}")
    print(f"=================================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
