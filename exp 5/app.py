import os
import io
import re
import math
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize NLTK NLP tools
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words_set = set(stopwords.words('english'))

# -------------------------------------------------------------
# 1. TRAINING CORPUS FOR MULTINOMIAL NAIVE BAYES
# -------------------------------------------------------------
training_corpus = {
    'Technology': [
        "Artificial intelligence and deep neural networks are transforming computer software and algorithms.",
        "Cloud computing servers deploy scalable database systems and automated machine learning models.",
        "Robotics, cybersecurity frameworks, and modern processor hardware drive computational technology innovation.",
        "Software developers program code using python, neural networks, and modern data structures.",
        "Microchips, internet networks, operating systems, and automated algorithm pipelines power computer technology."
    ],
    'Sports': [
        "The football tournament championship match concluded with thrilling goals from athletic players.",
        "Basketball athletes scored record points in the stadium during the competitive national league playoffs.",
        "The coach designed tactical defensive strategies for the team before the final soccer championship tournament.",
        "Runners, sprinters, and marathon athletes train vigorously to win Olympic medals and running titles.",
        "Tennis players competed fiercely in the grand slam tournament championship final on the center court."
    ],
    'Health / Medical': [
        "Doctors diagnose patients with clinical illnesses and prescribe effective therapeutic medicine treatments.",
        "Hospital physicians evaluate patient blood symptoms, surgical therapies, and biological health conditions.",
        "Clinical medical research discovers novel vaccine treatments to prevent contagious virus diseases.",
        "Healthcare nurses monitor patient heart rate, clinical recovery, and pharmaceutical medication dosages.",
        "Nutritional diet, hospital surgery, therapy medications, and medical diagnosis promote patient health recovery."
    ]
}

# -------------------------------------------------------------
# 2. NLP PREPROCESSING PIPELINE
# -------------------------------------------------------------
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    clean_tokens = [t for t in tokens if re.match(r'^[a-zA-Z]+$', t)]
    filtered_tokens = [t for t in clean_tokens if t not in stop_words_set]
    lemmatized = [lemmatizer.lemmatize(t) for t in filtered_tokens]
    return lemmatized

# Build Vocabulary & Word Frequencies for Naive Bayes
vocab = set()
class_word_counts = {}
class_total_words = {}
class_priors = {}
total_docs = sum(len(docs) for docs in training_corpus.values())

for category, docs in training_corpus.items():
    class_priors[category] = len(docs) / total_docs
    class_word_counts[category] = {}
    total_words = 0
    for doc in docs:
        words = preprocess_text(doc)
        for w in words:
            vocab.add(w)
            class_word_counts[category][w] = class_word_counts[category].get(w, 0) + 1
            total_words += 1
    class_total_words[category] = total_words

vocab_size = len(vocab)

# -------------------------------------------------------------
# 3. SENTENCE-BY-SENTENCE PIPELINE FOR INPUT PARAGRAPH
# -------------------------------------------------------------
def process_paragraph_sentences(paragraph):
    raw_sentences = sent_tokenize(paragraph)
    sentence_records = []
    all_final_tokens = []
    
    for idx, sent in enumerate(raw_sentences):
        tokens = word_tokenize(sent)
        clean_words = [w.lower() for w in tokens if re.match(r'^[a-zA-Z]+$', w)]
        removed_stops = [w for w in clean_words if w in stop_words_set]
        kept_tokens = [w for w in clean_words if w not in stop_words_set]
        stemmed = [stemmer.stem(w) for w in kept_tokens]
        lemmatized = [lemmatizer.lemmatize(w) for w in kept_tokens]
        all_final_tokens.extend(lemmatized)
        
        sentence_records.append({
            'sentence_num': idx + 1,
            'original_sentence': sent,
            'clean_tokens': clean_words,
            'removed_stop_words': removed_stops,
            'kept_tokens': kept_tokens,
            'stemmed_tokens': stemmed,
            'lemmatized_tokens': lemmatized
        })
        
    return sentence_records, all_final_tokens

# -------------------------------------------------------------
# 4. MULTINOMIAL NAIVE BAYES CLASSIFICATION
# -------------------------------------------------------------
def classify_text_bayesian(tokens):
    log_posteriors = {}
    word_likelihood_contributions = {cat: {} for cat in training_corpus}
    
    for category in training_corpus:
        # Prior log probability: log P(c)
        log_prob = math.log(class_priors[category])
        denom = class_total_words[category] + vocab_size  # Laplace smoothing denominator
        
        for w in tokens:
            count = class_word_counts[category].get(w, 0)
            # Laplace Smoothed Likelihood: P(w|c) = (count + 1) / (total_words + |V|)
            p_w_c = (count + 1) / denom
            log_prob += math.log(p_w_c)
            if w in vocab:
                word_likelihood_contributions[category][w] = p_w_c
                
        log_posteriors[category] = log_prob
        
    # Convert log-probabilities to normalized posterior probabilities via softmax
    max_log = max(log_posteriors.values())
    exp_probs = {cat: math.exp(val - max_log) for cat, val in log_posteriors.items()}
    sum_exp = sum(exp_probs.values())
    posteriors = {cat: exp_probs[cat] / sum_exp for cat in exp_probs}
    
    predicted_category = max(posteriors, key=posteriors.get)
    confidence = posteriors[predicted_category] * 100
    
    results = []
    for cat in training_corpus:
        results.append({
            'category': cat,
            'prior': round(class_priors[cat], 4),
            'log_score': round(log_posteriors[cat], 4),
            'posterior_prob': round(posteriors[cat], 4),
            'percentage': round(posteriors[cat] * 100, 2),
            'is_winner': (cat == predicted_category)
        })
        
    results.sort(key=lambda x: x['posterior_prob'], reverse=True)
    return results, predicted_category, confidence, word_likelihood_contributions

# -------------------------------------------------------------
# 5. GENERATE VISUALIZATION PLOT
# -------------------------------------------------------------
def generate_nlp_plot(bayes_results, tokens):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # 1. Posterior Probabilities Bar Chart
    cats = [r['category'] for r in bayes_results]
    probs = [r['posterior_prob'] for r in bayes_results]
    colors = ['#1b5e20' if r['is_winner'] else '#455a64' for r in bayes_results]
    
    bars = axes[0].bar(cats, probs, color=colors, width=0.45, edgecolor='black')
    axes[0].set_ylim(0, 1.15)
    axes[0].set_ylabel('Posterior Probability P(c|d)', fontsize=10, fontweight='bold')
    axes[0].set_title('Bayesian Classification Posterior Probabilities', fontsize=11, fontweight='bold')
    axes[0].grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}\n({h*100:.1f}%)",
                     ha='center', va='bottom', fontsize=9, fontweight='bold')
                     
    # 2. Informative Words Frequency in Input
    unique_tokens, counts = np.unique(tokens, return_counts=True)
    top_indices = np.argsort(counts)[-8:]  # Top 8 tokens
    top_words = unique_tokens[top_indices]
    top_counts = counts[top_indices]
    
    axes[1].barh(top_words, top_counts, color='#0277bd', edgecolor='black', height=0.5)
    axes[1].set_xlabel('Token Frequency in Sample', fontsize=10, fontweight='bold')
    axes[1].set_title('Preprocessed Salient Keywords in Test Sample', fontsize=11, fontweight='bold')
    axes[1].grid(axis='x', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# -------------------------------------------------------------
# FLASK ROUTE
# -------------------------------------------------------------
DEFAULT_PARAGRAPH = (
    "Artificial intelligence algorithms are rapidly transforming modern computer software and neural network systems. "
    "Software engineers develop automated cloud database applications to process complex data structures. "
    "Deep learning models enable autonomous machines to solve computational computing challenges."
)

PRESETS = [
    {
        'title': 'Preset 1: Technology & AI Domain',
        'text': (
            "Artificial intelligence algorithms are rapidly transforming modern computer software and neural network systems. "
            "Software engineers develop automated cloud database applications to process complex data structures. "
            "Deep learning models enable autonomous machines to solve computational computing challenges."
        )
    },
    {
        'title': 'Preset 2: Sports & Championship Tournament',
        'text': (
            "The football championship concluded with impressive goals from athletic players in the packed stadium. "
            "The coach implemented tactical strategies that guided the team to a stunning victory. "
            "Competitive athletes train continuously to achieve gold medals in the international league."
        )
    },
    {
        'title': 'Preset 3: Healthcare & Medical Diagnosis',
        'text': (
            "Doctors prescribe clinical medications to diagnose patients suffering from infectious virus illnesses. "
            "Hospital physicians monitor therapeutic treatments and medical healthcare symptoms closely. "
            "Novel pharmaceutical vaccine research provides effective therapies for patient recovery."
        )
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    paragraph = DEFAULT_PARAGRAPH
    
    if request.method == 'POST':
        paragraph = request.form.get('paragraph', DEFAULT_PARAGRAPH).strip()
        if not paragraph:
            paragraph = DEFAULT_PARAGRAPH
            
    # Execute NLP pipeline
    sentence_records, all_tokens = process_paragraph_sentences(paragraph)
    
    # Execute Bayesian classification
    bayes_results, predicted_category, confidence, word_contrib = classify_text_bayesian(all_tokens)
    
    # Generate visualization plot
    plot_b64 = generate_nlp_plot(bayes_results, all_tokens)
    
    return render_template(
        'index.html',
        paragraph=paragraph,
        sentence_records=sentence_records,
        total_sentences=len(sentence_records),
        total_tokens=len(all_tokens),
        unique_tokens=len(set(all_tokens)),
        bayes_results=bayes_results,
        predicted_category=predicted_category,
        confidence=confidence,
        plot_b64=plot_b64,
        presets=PRESETS,
        vocab_size=vocab_size
    )

if __name__ == '__main__':
    print("Starting Experiment 5 NLP Bayesian Server on http://127.0.0.1:5007")
    app.run(host='127.0.0.1', port=5007, debug=True)
