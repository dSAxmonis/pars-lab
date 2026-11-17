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
# 1. MOVIES DATASET (20 Diverse Movies Across Major Genres)
# ==============================================================================
MOVIES_DATABASE = [
    {
        "id": 1,
        "title": "Inception",
        "genres": ["Action", "Sci-Fi", "Thriller"],
        "year": 2010,
        "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "rating": 8.8,
        "plot_keywords": "dream heist, subconscious, architecture, reality distortion",
        "description": "A skilled thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        "icon": "🌌",
        "initials": "INC",
        "color": "#1e3a8a"
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "year": 2008,
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "rating": 9.0,
        "plot_keywords": "gotham, joker, chaos, moral dilemma, vigilante",
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological tests of his ability to fight injustice.",
        "icon": "🦇",
        "initials": "TDK",
        "color": "#0f172a"
    },
    {
        "id": 3,
        "title": "Interstellar",
        "genres": ["Sci-Fi", "Drama", "Adventure"],
        "year": 2014,
        "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "rating": 8.7,
        "plot_keywords": "wormhole, black hole, time dilation, relativity, space exploration",
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival as Earth faces catastrophic ecological collapse.",
        "icon": "🪐",
        "initials": "INT",
        "color": "#312e81"
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama", "Thriller"],
        "year": 1994,
        "director": "Quentin Tarantino",
        "cast": "John Travolta, Uma Thurman, Samuel L. Jackson",
        "rating": 8.9,
        "plot_keywords": "mob hitmen, briefcase, nonlinear narrative, diner robbery",
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption in Los Angeles.",
        "icon": "💼",
        "initials": "PF",
        "color": "#78350f"
    },
    {
        "id": 5,
        "title": "The Shawshank Redemption",
        "genres": ["Drama"],
        "year": 1994,
        "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "rating": 9.3,
        "plot_keywords": "prison escape, hope, resilience, friendship, wrongful conviction",
        "description": "Over the course of several decades, two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "icon": "⛓️",
        "initials": "TSR",
        "color": "#374151"
    },
    {
        "id": 6,
        "title": "Forrest Gump",
        "genres": ["Drama", "Romance", "Comedy"],
        "year": 1994,
        "director": "Robert Zemeckis",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise",
        "rating": 8.8,
        "plot_keywords": "destiny, vietnam war, running, feather, chocolate box",
        "description": "The history of the United States from the 1950s to the 1970s unfolds through the eyes of an Alabama man with an IQ of 75, who yearns to be reunited with his childhood sweetheart.",
        "icon": "🏃",
        "initials": "FG",
        "color": "#065f46"
    },
    {
        "id": 7,
        "title": "The Matrix",
        "genres": ["Action", "Sci-Fi"],
        "year": 1999,
        "director": "Lana & Lilly Wachowski",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "rating": 8.7,
        "plot_keywords": "simulation, red pill, bullet time, cybernetics, rebellion",
        "description": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.",
        "icon": "🕶️",
        "initials": "MTX",
        "color": "#064e3b"
    },
    {
        "id": 8,
        "title": "Parasite",
        "genres": ["Drama", "Thriller", "Comedy"],
        "year": 2019,
        "director": "Bong Joon Ho",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "rating": 8.5,
        "plot_keywords": "class disparity, deception, basement, architecture, social satire",
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "icon": "🏠",
        "initials": "PAR",
        "color": "#713f12"
    },
    {
        "id": 9,
        "title": "Spirited Away",
        "genres": ["Animation", "Adventure", "Family"],
        "year": 2001,
        "director": "Hayao Miyazaki",
        "cast": "Rumi Hiiragi, Miyu Irino, Mari Natsuki",
        "rating": 8.6,
        "plot_keywords": "bathhouse, spirits, enchanted, dragon, coming of age",
        "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, where humans are changed into beasts.",
        "icon": "🐉",
        "initials": "SA",
        "color": "#831843"
    },
    {
        "id": 10,
        "title": "Avengers: Endgame",
        "genres": ["Action", "Adventure", "Sci-Fi"],
        "year": 2019,
        "director": "Anthony & Joe Russo",
        "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo",
        "rating": 8.4,
        "plot_keywords": "infinity stones, time heist, cosmic battle, sacrifice, superheroes",
        "description": "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions.",
        "icon": "🛡️",
        "initials": "AVG",
        "color": "#881337"
    },
    {
        "id": 11,
        "title": "The Grand Budapest Hotel",
        "genres": ["Comedy", "Adventure", "Crime"],
        "year": 2014,
        "director": "Wes Anderson",
        "cast": "Ralph Fiennes, Tony Revolori, Adrien Brody",
        "rating": 8.1,
        "plot_keywords": "concierge, painting theft, pastel symmetry, alpine republic",
        "description": "A writer encounters the owner of an aging high-class hotel, who tells of his early years serving as a lobby boy during the hotel's glorious years under an exceptional concierge.",
        "icon": "🏨",
        "initials": "GBH",
        "color": "#9d174d"
    },
    {
        "id": 12,
        "title": "Whiplash",
        "genres": ["Drama", "Psychological"],
        "year": 2014,
        "director": "Damien Chazelle",
        "cast": "Miles Teller, J.K. Simmons, Paul Reiser",
        "rating": 8.5,
        "plot_keywords": "jazz drumming, perfectionism, ruthless mentor, blood on cymbals",
        "description": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are ruthlessly mentored by an instructor who will stop at nothing.",
        "icon": "🥁",
        "initials": "WHP",
        "color": "#451a03"
    },
    {
        "id": 13,
        "title": "La La Land",
        "genres": ["Comedy", "Drama", "Romance"],
        "year": 2016,
        "director": "Damien Chazelle",
        "cast": "Ryan Gosling, Emma Stone, John Legend",
        "rating": 8.0,
        "plot_keywords": "los angeles, jazz pianist, audition, sunset dance, ambitions",
        "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        "icon": "🎹",
        "initials": "LLL",
        "color": "#4c1d95"
    },
    {
        "id": 14,
        "title": "Get Out",
        "genres": ["Horror", "Mystery", "Thriller"],
        "year": 2017,
        "director": "Jordan Peele",
        "cast": "Daniel Kaluuya, Allison Williams, Bradley Whitford",
        "rating": 7.8,
        "plot_keywords": "sunken place, hypnosis, country estate, paranoia, social horror",
        "description": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception reaches a boiling point.",
        "icon": "👁️",
        "initials": "GO",
        "color": "#18181b"
    },
    {
        "id": 15,
        "title": "The Shining",
        "genres": ["Horror", "Drama"],
        "year": 1980,
        "director": "Stanley Kubrick",
        "cast": "Jack Nicholson, Shelley Duvall, Danny Lloyd",
        "rating": 8.4,
        "plot_keywords": "overlook hotel, isolation, typewriter, cabin fever, hedge maze",
        "description": "A family heads to an isolated hotel for the winter where an ominous psychic presence influences the father into violent madness while his psychic son sees terrifying omens.",
        "icon": "🪓",
        "initials": "SHN",
        "color": "#581c87"
    },
    {
        "id": 16,
        "title": "Superbad",
        "genres": ["Comedy"],
        "year": 2007,
        "director": "Greg Mottola",
        "cast": "Jonah Hill, Michael Cera, Christopher Mintz-Plasse",
        "rating": 7.6,
        "plot_keywords": "fake id, mclovin, high school graduation, party quest, teenage friendship",
        "description": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes hilariously awry.",
        "icon": "🍺",
        "initials": "SB",
        "color": "#b45309"
    },
    {
        "id": 17,
        "title": "Gladiator",
        "genres": ["Action", "Adventure", "Drama"],
        "year": 2000,
        "director": "Ridley Scott",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen",
        "rating": 8.5,
        "plot_keywords": "colosseum, roman empire, revenge, honor, general turned gladiator",
        "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "icon": "⚔️",
        "initials": "GLD",
        "color": "#92400e"
    },
    {
        "id": 18,
        "title": "Titanic",
        "genres": ["Drama", "Romance"],
        "year": 1997,
        "director": "James Cameron",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
        "rating": 7.9,
        "plot_keywords": "shipwreck, iceberg, romance across social classes, heart of the ocean",
        "description": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "icon": "🚢",
        "initials": "TTN",
        "color": "#1e3a5f"
    },
    {
        "id": 19,
        "title": "Alien",
        "genres": ["Horror", "Sci-Fi"],
        "year": 1979,
        "director": "Ridley Scott",
        "cast": "Sigourney Weaver, Tom Skerritt, John Hurt",
        "rating": 8.5,
        "plot_keywords": "nostromo, xenomorph, facehugger, claustrophobia, deep space",
        "description": "The crew of a commercial spacecraft encounters a deadly lifeform after investigating an unknown transmission on a desolate extraterrestrial moon.",
        "icon": "👽",
        "initials": "ALN",
        "color": "#14532d"
    },
    {
        "id": 20,
        "title": "Her",
        "genres": ["Drama", "Romance", "Sci-Fi"],
        "year": 2013,
        "director": "Spike Jonze",
        "cast": "Joaquin Phoenix, Scarlett Johansson, Amy Adams",
        "rating": 8.0,
        "plot_keywords": "artificial intelligence, future os, loneliness, emotional connection",
        "description": "In a near future, a lonely writer develops an unlikely relationship with an advanced operating system designed to meet his every intellectual and emotional need.",
        "icon": "💌",
        "initials": "HER",
        "color": "#be123c"
    }
]

# Lookup dictionary for movies by ID
MOVIES_DICT = {m['id']: m for m in MOVIES_DATABASE}
MOVIE_TITLES = [m['title'] for m in MOVIES_DATABASE]
NUM_MOVIES = len(MOVIES_DATABASE)

# ==============================================================================
# 2. USER DATABASE & RATINGS MATRIX
# Users 1-8 are community benchmark users with defined genre tastes
# User 9 is the Active Student User (Monis), with customizable ratings
# Scale: 1.0 to 5.0 (0.0 denotes unrated / unwatched item)
# ==============================================================================
USER_PROFILES = [
    {"id": 0, "name": "Alice", "persona": "Sci-Fi & Action Purist", "avatar": "👩‍🚀"},
    {"id": 1, "name": "Bob", "persona": "Classic Drama & Romance Admirer", "avatar": "🎩"},
    {"id": 2, "name": "Charlie", "persona": "Dark Thriller & Horror Buff", "avatar": "🕵️"},
    {"id": 3, "name": "David", "persona": "Blockbuster & Action Fan", "avatar": "⚡"},
    {"id": 4, "name": "Emma", "persona": "Feel-Good Comedy & Musicals", "avatar": "✨"},
    {"id": 5, "name": "Frank", "persona": "Arthouse Cinephile & Drama Critic", "avatar": "📽️"},
    {"id": 6, "name": "Grace", "persona": "Pop Culture & Teen Comedy Lover", "avatar": "🍿"},
    {"id": 7, "name": "Henry", "persona": "Mind-Bending Sci-Fi & Psychological", "avatar": "🧩"},
    {"id": 8, "name": "Monis (Active User)", "persona": "Curated Tech & Cinema Explorer", "avatar": "👨‍💻"}
]

# Baseline ratings matrix (9 users x 20 movies)
# Columns correspond to movie IDs 1 through 20
BASE_RATINGS = np.array([
    # Alice: Loves Sci-Fi & Action (Inception, Dark Knight, Interstellar, Matrix, Alien)
    # Movies: [1:Inc, 2:TDK, 3:Int, 4:PF, 5:TSR, 6:FG, 7:Mtx, 8:Par, 9:SA, 10:Avg, 11:GBH, 12:Whp, 13:LLL, 14:GO, 15:Shn, 16:SB, 17:Gld, 18:Ttn, 19:Aln, 20:Her]
    [5.0, 4.5, 5.0, 3.5, 0.0, 2.0, 5.0, 4.0, 0.0, 4.5, 0.0, 3.5, 1.5, 2.5, 3.0, 2.0, 4.5, 1.0, 5.0, 3.5],
    
    # Bob: Loves Dramas & Romance (Shawshank, Forrest Gump, Titanic, La La Land, Gladiator)
    [2.5, 3.0, 3.0, 4.0, 5.0, 5.0, 2.0, 4.0, 3.5, 2.5, 4.0, 4.5, 5.0, 2.0, 1.5, 3.0, 4.5, 5.0, 1.5, 4.5],
    
    # Charlie: Dark Thriller & Horror Buff (The Shining, Get Out, Alien, Pulp Fiction, Parasite)
    [4.0, 4.5, 3.5, 5.0, 4.0, 2.0, 4.0, 5.0, 3.0, 2.0, 3.0, 4.5, 1.0, 5.0, 5.0, 2.5, 3.5, 1.0, 5.0, 3.0],
    
    # David: Blockbuster Action & Adventure (Dark Knight, Gladiator, Avengers, Matrix, Inception)
    [5.0, 5.0, 4.5, 3.5, 3.5, 3.0, 5.0, 3.0, 2.0, 5.0, 2.5, 3.0, 2.0, 2.5, 2.0, 3.5, 5.0, 2.0, 4.0, 2.5],
    
    # Emma: Comedy, Romance & Musicals (La La Land, Superbad, Grand Budapest Hotel, Forrest Gump, Titanic)
    [2.0, 2.5, 2.5, 1.5, 4.5, 5.0, 1.5, 3.5, 4.5, 3.0, 5.0, 3.5, 5.0, 1.5, 1.0, 4.5, 2.5, 5.0, 1.0, 4.5],
    
    # Frank: Arthouse & Intense Dramas (Parasite, Whiplash, Shawshank, Grand Budapest, Pulp Fiction, Her)
    [4.5, 4.0, 4.0, 5.0, 5.0, 3.5, 3.5, 5.0, 4.5, 1.5, 5.0, 5.0, 4.0, 4.0, 4.5, 2.0, 3.5, 3.0, 3.5, 5.0],
    
    # Grace: Pop Culture, Comedies, Teen Films (Superbad, Grand Budapest, Avengers, Forrest Gump)
    [3.0, 4.0, 2.5, 2.0, 3.5, 4.5, 3.0, 2.5, 4.0, 5.0, 4.5, 2.5, 4.0, 2.0, 1.5, 5.0, 3.0, 4.0, 1.5, 2.5],
    
    # Henry: Mind-Bending Sci-Fi & Psychological (Inception, Interstellar, Her, Get Out, Matrix, The Shining)
    [5.0, 4.0, 5.0, 4.5, 4.0, 2.5, 4.5, 4.5, 3.5, 3.5, 3.5, 4.5, 2.5, 4.5, 4.5, 1.5, 3.5, 2.0, 4.5, 5.0],
    
    # Active User: Monis (Default Seed: High on Nolan Sci-Fi & Thrillers, Unrated items ready for CF recommendation)
    [5.0, 4.5, 5.0, 0.0, 0.0, 0.0, 4.5, 4.0, 0.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 3.5, 0.0, 0.0, 0.0, 0.0]
], dtype=float)

# In-memory storage for active session ratings
CURRENT_RATINGS = np.copy(BASE_RATINGS)


# ==============================================================================
# 3. PURE NUMPY COLLABORATIVE FILTERING ENGINE (FROM FIRST PRINCIPLES)
# ==============================================================================

def compute_pearson_similarity_matrix(R):
    r"""
    Computes User-User Pearson Correlation Matrix from scratch using NumPy.
    r_{u, v} = \frac{\sum_{i \in I_{u, v}} (R_{u, i} - \bar{R}_u)(R_{v, i} - \bar{R}_v)}
                   {\sqrt{\sum_{i \in I_{u, v}} (R_{u, i} - \bar{R}_u)^2} \sqrt{\sum_{i \in I_{u, v}} (R_{v, i} - \bar{R}_v)^2}}
    """
    n_users = R.shape[0]
    similarity_matrix = np.eye(n_users, dtype=float)
    
    for u in range(n_users):
        for v in range(u + 1, n_users):
            # Find co-rated items (both rated > 0)
            co_rated = (R[u] > 0) & (R[v] > 0)
            num_co = np.sum(co_rated)
            
            if num_co < 2:
                # Need at least 2 co-rated items for standard Pearson variance
                sim = 0.0
            else:
                r_u = R[u, co_rated]
                r_v = R[v, co_rated]
                
                mean_u = np.mean(r_u)
                mean_v = np.mean(r_v)
                
                diff_u = r_u - mean_u
                diff_v = r_v - mean_v
                
                numerator = np.sum(diff_u * diff_v)
                denom = np.sqrt(np.sum(diff_u ** 2)) * np.sqrt(np.sum(diff_v ** 2))
                
                if denom < 1e-9:
                    sim = 0.0
                else:
                    sim = numerator / denom
                    sim = float(np.clip(sim, -1.0, 1.0))
                    
            similarity_matrix[u, v] = sim
            similarity_matrix[v, u] = sim
            
    return similarity_matrix


def predict_user_item_ratings(active_user_idx, R, S, k_neighbors=3):
    r"""
    Predicts ratings for all items using Resnick's mean-centered weighted average collaborative filtering:
    \hat{R}_{a, i} = \bar{R}_a + \frac{\sum_{v \in TopK} S(a, v) \cdot (R_{v, i} - \bar{R}_v)}
                                      {\sum_{v \in TopK} |S(a, v)|}
    """
    n_users, n_items = R.shape
    active_ratings = R[active_user_idx]
    
    # Active user's overall rated mean
    active_rated_mask = active_ratings > 0
    if np.sum(active_rated_mask) > 0:
        active_mean = np.mean(active_ratings[active_rated_mask])
    else:
        active_mean = 3.0
        
    predictions = {}
    neighbor_details = {}
    
    for item_idx in range(n_items):
        # Eligible neighbors: other users who rated this item with positive similarity
        candidate_neighbors = []
        for other_u in range(n_users):
            if other_u != active_user_idx and R[other_u, item_idx] > 0:
                sim = S[active_user_idx, other_u]
                if sim > 0:  # Positively correlated neighbors
                    candidate_neighbors.append((other_u, sim))
                    
        # Sort candidate neighbors by similarity descending
        candidate_neighbors.sort(key=lambda x: x[1], reverse=True)
        top_k = candidate_neighbors[:k_neighbors]
        
        if not top_k:
            # Fallback: item average or active user mean
            rated_other = [R[u, item_idx] for u in range(n_users) if u != active_user_idx and R[u, item_idx] > 0]
            if rated_other:
                pred_rating = float(np.mean(rated_other))
            else:
                pred_rating = active_mean
            weighted_avg = pred_rating
            explanation = "Defaulted to community mean rating (no positively correlated neighbor rated this item)."
            contributors = []
        else:
            num = 0.0
            den = 0.0
            simple_num = 0.0
            simple_den = 0.0
            contributors = []
            
            for u_idx, sim in top_k:
                u_ratings = R[u_idx]
                u_mean = np.mean(u_ratings[u_ratings > 0])
                rating_val = R[u_idx, item_idx]
                
                num += sim * (rating_val - u_mean)
                den += abs(sim)
                
                simple_num += sim * rating_val
                simple_den += sim
                
                contributors.append({
                    "user_id": u_idx,
                    "user_name": USER_PROFILES[u_idx]["name"],
                    "similarity": round(sim, 3),
                    "rated_val": rating_val,
                    "user_mean": round(u_mean, 2)
                })
                
            if den > 0:
                pred_rating = active_mean + (num / den)
            else:
                pred_rating = active_mean
                
            weighted_avg = simple_num / simple_den if simple_den > 0 else active_mean
            pred_rating = float(np.clip(pred_rating, 1.0, 5.0))
            weighted_avg = float(np.clip(weighted_avg, 1.0, 5.0))
            
            # Format readable explanation
            top_names = [f"{c['user_name']} (r={c['similarity']}, rated {c['rated_val']}★)" for c in contributors]
            explanation = f"Inferred via Top-{len(contributors)} similar peer(s): " + ", ".join(top_names)
            
        predictions[item_idx] = {
            "movie_id": item_idx + 1,
            "predicted_rating": round(pred_rating, 2),
            "weighted_average": round(weighted_avg, 2),
            "explanation": explanation,
            "contributors": contributors
        }
        
    return predictions, active_mean


def evaluate_predicted_vs_actual(active_user_idx, R, S, k_neighbors=3):
    """
    Evaluates Collaborative Filtering performance on items the active user has already rated.
    Performs leave-one-out prediction to compare Actual Rating vs Predicted Rating.
    Computes MAE and RMSE.
    """
    active_ratings = R[active_user_idx]
    rated_indices = np.where(active_ratings > 0)[0]
    
    eval_records = []
    errors = []
    
    for idx in rated_indices:
        actual_val = active_ratings[idx]
        movie = MOVIES_DATABASE[idx]
        
        # Candidate neighbors who rated this item
        candidate_neighbors = []
        for other_u in range(R.shape[0]):
            if other_u != active_user_idx and R[other_u, idx] > 0:
                sim = S[active_user_idx, other_u]
                if sim > 0:
                    candidate_neighbors.append((other_u, sim))
                    
        candidate_neighbors.sort(key=lambda x: x[1], reverse=True)
        top_k = candidate_neighbors[:k_neighbors]
        
        # User mean without current item
        other_rated = active_ratings[active_ratings > 0]
        active_mean = np.mean(other_rated)
        
        if top_k:
            num = 0.0
            den = 0.0
            for u_idx, sim in top_k:
                u_ratings = R[u_idx]
                u_mean = np.mean(u_ratings[u_ratings > 0])
                num += sim * (R[u_idx, idx] - u_mean)
                den += abs(sim)
            predicted_val = active_mean + (num / den) if den > 0 else active_mean
        else:
            other_u_ratings = [R[u, idx] for u in range(R.shape[0]) if u != active_user_idx and R[u, idx] > 0]
            predicted_val = np.mean(other_u_ratings) if other_u_ratings else active_mean
            
        predicted_val = float(np.clip(predicted_val, 1.0, 5.0))
        err = actual_val - predicted_val
        abs_err = abs(err)
        sq_err = err ** 2
        errors.append((abs_err, sq_err))
        
        eval_records.append({
            "movie_id": movie["id"],
            "title": movie["title"],
            "genres": ", ".join(movie["genres"]),
            "actual": round(actual_val, 1),
            "predicted": round(predicted_val, 2),
            "error": round(err, 2),
            "abs_error": round(abs_err, 2),
            "sq_error": round(sq_err, 3)
        })
        
    if errors:
        mae = float(np.mean([e[0] for e in errors]))
        rmse = float(np.sqrt(np.mean([e[1] for e in errors])))
    else:
        mae, rmse = 0.0, 0.0
        
    metrics = {
        "rated_count": len(rated_indices),
        "mae": round(mae, 3),
        "rmse": round(rmse, 3)
    }
    
    return eval_records, metrics


# ==============================================================================
# 4. MATPLOTLIB VISUALIZATIONS GENERATOR
# ==============================================================================

def generate_collaborative_filtering_plots(active_user_idx, R, S, predictions, eval_records, k_neighbors=3):
    """
    Generates two base64-encoded diagnostic visualization figures:
    Plot 1: User-User Similarity Matrix Heatmap & Top Neighbor Similarity Bar Chart.
    Plot 2: Actual vs Predicted Ratings with Error Residuals & Top Recommended Items.
    """
    user_names = [u["name"].split()[0] for u in USER_PROFILES]
    active_name = USER_PROFILES[active_user_idx]["name"]
    
    # --------------------------------------------------------------------------
    # FIGURE 1: Algorithm Internals (Similarity Heatmap + Neighbor Strengths)
    # --------------------------------------------------------------------------
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.0), dpi=120)
    
    # Heatmap of User-User Similarity Matrix
    cax = ax1.imshow(S, cmap='coolwarm', vmin=-1.0, vmax=1.0)
    fig1.colorbar(cax, ax=ax1, fraction=0.046, pad=0.04, label="Pearson Correlation r(u, v)")
    
    ax1.set_xticks(range(len(user_names)))
    ax1.set_yticks(range(len(user_names)))
    ax1.set_xticklabels(user_names, rotation=45, ha='right', fontsize=8.5, fontweight='bold')
    ax1.set_yticklabels(user_names, fontsize=8.5, fontweight='bold')
    
    # Annotate values inside cells
    for i in range(len(user_names)):
        for j in range(len(user_names)):
            val = S[i, j]
            text_color = "white" if abs(val) > 0.55 else "black"
            ax1.text(j, i, f"{val:.2f}", ha="center", va="center", color=text_color, fontsize=7.5)
            
    ax1.set_title("User-User Pearson Similarity Matrix (All 9 Users)", fontsize=10.5, fontweight='bold', pad=8)
    
    # Neighbor Similarity Ranking for Active User
    other_users = [i for i in range(len(user_names)) if i != active_user_idx]
    other_names = [user_names[i] for i in other_users]
    sim_scores = [S[active_user_idx, i] for i in other_users]
    
    # Determine top K neighbors
    sorted_pairs = sorted(zip(other_names, sim_scores), key=lambda x: x[1], reverse=True)
    sorted_names = [p[0] for p in sorted_pairs]
    sorted_sims = [p[1] for p in sorted_pairs]
    
    bar_colors = ['#16a34a' if i < k_neighbors and sorted_sims[i] > 0 else '#2563eb' if sorted_sims[i] > 0 else '#dc2626'
                  for i in range(len(sorted_names))]
    
    bars = ax2.barh(sorted_names[::-1], sorted_sims[::-1], color=bar_colors[::-1], edgecolor='black', height=0.6)
    ax2.axvline(0, color='black', linewidth=1.0)
    ax2.set_xlim(-1.05, 1.05)
    ax2.set_xlabel("Pearson Correlation r with Active User", fontsize=9.0)
    ax2.set_title(f"Similarity of Peers to {active_name} (Top {k_neighbors} in Green)", fontsize=10.5, fontweight='bold', pad=8)
    ax2.grid(axis='x', linestyle='--', alpha=0.5)
    
    for bar in bars:
        width = bar.get_width()
        offset = 0.03 if width >= 0 else -0.15
        ax2.text(width + offset, bar.get_y() + bar.get_height()/2, f"{width:.2f}",
                 va='center', fontsize=8.5, fontweight='bold')
        
    plt.tight_layout()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', bbox_inches='tight')
    buf1.seek(0)
    plot1_base64 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)
    
    # --------------------------------------------------------------------------
    # FIGURE 2: Predicted vs Actual Evaluation & Top Recommendations
    # --------------------------------------------------------------------------
    fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(12.5, 5.0), dpi=120)
    
    # Subplot 1: Predicted vs Actual Ratings for Active User's Rated Movies
    if eval_records:
        titles_eval = [r["title"][:14] + ".." if len(r["title"]) > 15 else r["title"] for r in eval_records]
        actuals = [r["actual"] for r in eval_records]
        predicts = [r["predicted"] for r in eval_records]
        x_indices = np.arange(len(titles_eval))
        width = 0.36
        
        ax3.bar(x_indices - width/2, actuals, width, label='Actual Rating', color='#1d4ed8', edgecolor='black')
        ax3.bar(x_indices + width/2, predicts, width, label='Predicted (CF)', color='#f97316', edgecolor='black')
        
        # Display error values above bars
        for idx in range(len(titles_eval)):
            err = actuals[idx] - predicts[idx]
            ax3.text(x_indices[idx], max(actuals[idx], predicts[idx]) + 0.15,
                     f"Δ={abs(err):.2f}", ha='center', fontsize=7.5, color='#b91c1c' if abs(err) > 0.8 else '#15803d')
            
        ax3.set_xticks(x_indices)
        ax3.set_xticklabels(titles_eval, rotation=35, ha='right', fontsize=8)
        ax3.set_ylim(0, 5.8)
        ax3.set_ylabel("Rating (Stars 1-5)", fontsize=9.0)
        ax3.set_title("Validation: Predicted vs Actual Ratings on Known Movies", fontsize=10.5, fontweight='bold', pad=8)
        ax3.legend(loc='upper right', fontsize=8.5)
        ax3.grid(axis='y', linestyle='--', alpha=0.5)
    else:
        ax3.text(0.5, 0.5, "No movies currently rated by active user", ha='center', va='center', fontsize=10)
        ax3.set_title("Validation: Predicted vs Actual Ratings", fontsize=10.5, fontweight='bold')
        
    # Subplot 2: Top Recommended Unrated Movies
    active_ratings = R[active_user_idx]
    unrated_indices = np.where(active_ratings == 0)[0]
    unrated_recs = []
    for idx in unrated_indices:
        pred_obj = predictions[idx]
        movie = MOVIES_DATABASE[idx]
        unrated_recs.append({
            "title": movie["title"],
            "pred": pred_obj["predicted_rating"],
            "genre": movie["genres"][0]
        })
    unrated_recs.sort(key=lambda x: x["pred"], reverse=True)
    top_display = unrated_recs[:7]
    
    if top_display:
        rec_titles = [m["title"][:16] for m in top_display][::-1]
        rec_scores = [m["pred"] for m in top_display][::-1]
        
        bar_colors_rec = ['#8b5cf6' if s >= 4.0 else '#3b82f6' for s in rec_scores]
        bars2 = ax4.barh(rec_titles, rec_scores, color=bar_colors_rec, edgecolor='black', height=0.55)
        ax4.set_xlim(0, 5.5)
        ax4.set_xlabel("Predicted Rating (Stars)", fontsize=9.0)
        ax4.set_title(f"Top Recommended Movies for {active_name}", fontsize=10.5, fontweight='bold', pad=8)
        ax4.grid(axis='x', linestyle='--', alpha=0.5)
        
        for bar in bars2:
            w = bar.get_width()
            ax4.text(w + 0.08, bar.get_y() + bar.get_height()/2, f"{w:.2f} ★",
                     va='center', fontsize=8.5, fontweight='bold')
    else:
        ax4.text(0.5, 0.5, "All catalog movies have already been rated!", ha='center', va='center')
        ax4.set_title("Top Recommended Movies", fontsize=10.5, fontweight='bold')
        
    plt.tight_layout()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', bbox_inches='tight')
    buf2.seek(0)
    plot2_base64 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)
    
    return plot1_base64, plot2_base64


# ==============================================================================
# 5. FLASK WEB ROUTES & CONTROLLER
# ==============================================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    global CURRENT_RATINGS
    
    # Handle user switching and rating modifications
    active_user_idx = int(request.form.get('active_user_idx', 8))
    k_neighbors = int(request.form.get('k_neighbors', 3))
    genre_filter = request.form.get('genre_filter', 'ALL')
    selected_movie_id = request.form.get('selected_movie_id', None)
    action = request.form.get('action', '')
    
    # Action Handlers
    if action == 'rate_movie':
        movie_id = int(request.form.get('movie_id', 1))
        new_rating = float(request.form.get('new_rating', 0.0))
        CURRENT_RATINGS[active_user_idx, movie_id - 1] = new_rating
        selected_movie_id = str(movie_id)
        
    elif action == 'reset_defaults':
        CURRENT_RATINGS = np.copy(BASE_RATINGS)
        selected_movie_id = None
        
    elif action == 'preset_scifi':
        # Preset Active User as Heavy Sci-Fi & Action enthusiast
        CURRENT_RATINGS[active_user_idx] = 0.0
        CURRENT_RATINGS[active_user_idx, 0] = 5.0  # Inception
        CURRENT_RATINGS[active_user_idx, 1] = 4.5  # Dark Knight
        CURRENT_RATINGS[active_user_idx, 2] = 5.0  # Interstellar
        CURRENT_RATINGS[active_user_idx, 6] = 5.0  # Matrix
        CURRENT_RATINGS[active_user_idx, 9] = 4.5  # Avengers
        CURRENT_RATINGS[active_user_idx, 18] = 4.5 # Alien
        
    elif action == 'preset_romance':
        # Preset Active User as Romance & Feel-Good lover
        CURRENT_RATINGS[active_user_idx] = 0.0
        CURRENT_RATINGS[active_user_idx, 4] = 4.5  # Shawshank
        CURRENT_RATINGS[active_user_idx, 5] = 5.0  # Forrest Gump
        CURRENT_RATINGS[active_user_idx, 10] = 4.0 # Grand Budapest
        CURRENT_RATINGS[active_user_idx, 12] = 5.0 # La La Land
        CURRENT_RATINGS[active_user_idx, 17] = 5.0 # Titanic
        CURRENT_RATINGS[active_user_idx, 19] = 4.5 # Her
        
    elif action == 'preset_horror':
        # Preset Active User as Horror & Dark Thriller buff
        CURRENT_RATINGS[active_user_idx] = 0.0
        CURRENT_RATINGS[active_user_idx, 3] = 5.0  # Pulp Fiction
        CURRENT_RATINGS[active_user_idx, 7] = 4.5  # Parasite
        CURRENT_RATINGS[active_user_idx, 13] = 5.0 # Get Out
        CURRENT_RATINGS[active_user_idx, 14] = 5.0 # The Shining
        CURRENT_RATINGS[active_user_idx, 18] = 4.5 # Alien
        
    # Execute Collaborative Filtering Pipeline from Scratch
    similarity_matrix = compute_pearson_similarity_matrix(CURRENT_RATINGS)
    predictions, active_mean = predict_user_item_ratings(active_user_idx, CURRENT_RATINGS, similarity_matrix, k_neighbors)
    eval_records, eval_metrics = evaluate_predicted_vs_actual(active_user_idx, CURRENT_RATINGS, similarity_matrix, k_neighbors)
    
    # Generate Plots
    plot1_base64, plot2_base64 = generate_collaborative_filtering_plots(
        active_user_idx, CURRENT_RATINGS, similarity_matrix, predictions, eval_records, k_neighbors
    )
    
    # Build Movie Catalog View Model with Active User Ratings and Predictions
    active_ratings = CURRENT_RATINGS[active_user_idx]
    catalog = []
    
    for idx, movie in enumerate(MOVIES_DATABASE):
        user_rating = active_ratings[idx]
        pred_info = predictions[idx]
        
        matches_genre = True
        if genre_filter != 'ALL' and genre_filter not in movie['genres']:
            matches_genre = False
            
        catalog.append({
            "id": movie["id"],
            "title": movie["title"],
            "genres": movie["genres"],
            "genres_str": ", ".join(movie["genres"]),
            "year": movie["year"],
            "director": movie["director"],
            "cast": movie["cast"],
            "imdb_rating": movie["rating"],
            "plot_keywords": movie["plot_keywords"],
            "description": movie["description"],
            "icon": movie["icon"],
            "initials": movie["initials"],
            "color": movie["color"],
            "user_rating": user_rating,
            "has_rated": user_rating > 0,
            "pred_rating": pred_info["predicted_rating"],
            "explanation": pred_info["explanation"],
            "contributors": pred_info["contributors"],
            "matches_genre": matches_genre
        })
        
    # Filtered recommendations (only unwatched/unrated movies)
    unwatched_recommendations = [m for m in catalog if not m["has_rated"]]
    if genre_filter != 'ALL':
        unwatched_recommendations = [m for m in unwatched_recommendations if genre_filter in m["genres"]]
    unwatched_recommendations.sort(key=lambda x: x["pred_rating"], reverse=True)
    
    # Watched / Rated movies list
    watched_movies = [m for m in catalog if m["has_rated"]]
    
    # Selected movie for detailed modal / preview drawer
    selected_movie = None
    if selected_movie_id:
        try:
            m_id = int(selected_movie_id)
            if m_id in MOVIES_DICT:
                selected_movie = MOVIES_DICT[m_id]
                selected_movie["user_rating"] = active_ratings[m_id - 1]
                selected_movie["pred_rating"] = predictions[m_id - 1]["predicted_rating"]
                selected_movie["explanation"] = predictions[m_id - 1]["explanation"]
                selected_movie["contributors"] = predictions[m_id - 1]["contributors"]
        except (ValueError, TypeError):
            pass
            
    # Format similarity matrix for clean table rendering
    sim_table_header = [u["name"].split()[0] for u in USER_PROFILES]
    sim_table_rows = []
    for i, u_obj in enumerate(USER_PROFILES):
        row_vals = [round(float(similarity_matrix[i, j]), 2) for j in range(len(USER_PROFILES))]
        sim_table_rows.append({
            "name": u_obj["name"],
            "avatar": u_obj["avatar"],
            "scores": row_vals,
            "is_active": i == active_user_idx
        })
        
    # Format full ratings matrix for table rendering
    ratings_table_rows = []
    for i, u_obj in enumerate(USER_PROFILES):
        r_vals = [round(float(CURRENT_RATINGS[i, j]), 1) if CURRENT_RATINGS[i, j] > 0 else "-" for j in range(NUM_MOVIES)]
        ratings_table_rows.append({
            "name": u_obj["name"],
            "avatar": u_obj["avatar"],
            "ratings": r_vals,
            "is_active": i == active_user_idx
        })
        
    return render_template(
        'index.html',
        movies_database=MOVIES_DATABASE,
        catalog=catalog,
        unwatched_recommendations=unwatched_recommendations,
        watched_movies=watched_movies,
        selected_movie=selected_movie,
        user_profiles=USER_PROFILES,
        active_user_idx=active_user_idx,
        active_user_name=USER_PROFILES[active_user_idx]["name"],
        active_user_avatar=USER_PROFILES[active_user_idx]["avatar"],
        active_user_persona=USER_PROFILES[active_user_idx]["persona"],
        active_mean=round(active_mean, 2),
        k_neighbors=k_neighbors,
        genre_filter=genre_filter,
        eval_records=eval_records,
        eval_metrics=eval_metrics,
        plot1_base64=plot1_base64,
        plot2_base64=plot2_base64,
        sim_table_header=sim_table_header,
        sim_table_rows=sim_table_rows,
        ratings_table_rows=ratings_table_rows
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5013))
    print(f"Starting Experiment 13 Collaborative Filtering Server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
