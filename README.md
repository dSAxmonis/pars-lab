# Pattern Analysis & Recognition Systems (PARS) Lab

Comprehensive practical solutions, implementations, datasets, and laboratory reports for the PARS Lab course.

---

## Laboratory Experiments Directory

### 1. [Experiment 2: Web-Based Dataset Extraction, Storage, Feature Analysis, and Performance Visualization](./exp%202/)
- **Description:** Flask web application to extract and persist CIFAR-10 (Image) and Iris (Tabular) datasets, inspect feature descriptions, and plot evaluation performance curves and confusion matrices.
- **Code:** [`exp 2/app.py`](./exp%202/app.py) &amp; [`exp 2/templates/index.html`](./exp%202/templates/index.html)
- **Manual Report:** [`LAB_PRACTICAL_FILE.md`](./LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_2_Lab_Practical.pdf`](./Experiment_2_Lab_Practical.pdf)

### 2. [Experiment 3: Multimodal Feature Extraction from Audio Across Multiple Timestamps](./exp%203/)
- **Description:** Informative Flask web application extracting 3 key features (RMS Energy, Zero Crossing Rate, and Spectral Centroid) across 10 temporal timestamps from an embedded playable audio file, justifying real-world engineering objectives.
- **Code:** [`exp 3/app.py`](./exp%203/app.py) &amp; [`exp 3/templates/index.html`](./exp%203/templates/index.html)
- **Manual Report:** [`exp 3/LAB_PRACTICAL_FILE.md`](./exp%203/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_3_Lab_Practical.pdf`](./Experiment_3_Lab_Practical.pdf)

### 3. [Experiment 4: Bayesian Classification for Single Feature & Multiple Features Multiple Class](./exp%204/)
- **Description:** Interactive Flask web application implementing Bayesian pattern classification under univariate and multivariate Gaussian models, calculating prior, likelihood, and posterior probabilities with real-time decision plots.
- **Code:** [`exp 4/app.py`](./exp%204/app.py) &amp; [`exp 4/templates/index.html`](./exp%204/templates/index.html)
- **Manual Report:** [`exp 4/LAB_PRACTICAL_FILE.md`](./exp%204/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_4_Lab_Practical.pdf`](./Experiment_4_Lab_Practical.pdf)

### 4. [Experiment 5: NLP Text Paragraph Preprocessing & Bayesian Classification](./exp%205/)
- **Description:** Interactive Flask web application performing sentence segmentation, lexical tokenization, stop words removal, Porter stemming, WordNet lemmatization, and domain classification via Multinomial Naive Bayes.
- **Code:** [`exp 5/app.py`](./exp%205/app.py) &amp; [`exp 5/templates/index.html`](./exp%205/templates/index.html)
- **Manual Report:** [`exp 5/LAB_PRACTICAL_FILE.md`](./exp%205/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_5_Lab_Practical.pdf`](./Experiment_5_Lab_Practical.pdf)

### 5. [Experiment 6: Bayesian Risk Minimization for Three Classes and Three Actions](./exp%206/)
- **Description:** Interactive Flask web application evaluating Bayesian conditional risks $R(\alpha_i | \mathbf{x}) = \sum \lambda_{ij} P(\omega_j | \mathbf{x})$ given an asymmetric loss matrix, dynamically triggering and reflecting operational consequences (Clearance, Review, Lockout) on the page.
- **Code:** [`exp 6/app.py`](./exp%206/app.py) &amp; [`exp 6/templates/index.html`](./exp%206/templates/index.html)
- **Manual Report:** [`exp 6/LAB_PRACTICAL_FILE.md`](./exp%206/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_6_Lab_Practical.pdf`](./Experiment_6_Lab_Practical.pdf)

### 6. [Experiment 7: Linear Regression from Scratch Using Gradient Descent](./exp%207/)
- **Description:** Pure Python/NumPy Linear Regression implementation (no inbuilt estimators) optimizing weight $w$ and bias $b$ via gradient descent on housing prices with live Gradient Descent MSE cost decay curve plotting.
- **Code:** [`exp 7/app.py`](./exp%207/app.py) &amp; [`exp 7/templates/index.html`](./exp%207/templates/index.html)
- **Manual Report:** [`exp 7/LAB_PRACTICAL_FILE.md`](./exp%207/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_7_Lab_Practical.pdf`](./Experiment_7_Lab_Practical.pdf)

### 7. [Experiment 8: Logistic Regression (Binary & Multiclass from Scratch)](./exp%208/)
- **Description:** Pure Python/NumPy Logistic Regression implementation (no inbuilt estimators) providing Sigmoid binary classification and Softmax multiclass classification with Gradient Descent cross-entropy curves and decision boundary plots.
- **Code:** [`exp 8/app.py`](./exp%208/app.py) &amp; [`exp 8/templates/index.html`](./exp%208/templates/index.html)
- **Manual Report:** [`exp 8/LAB_PRACTICAL_FILE.md`](./exp%208/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_8_Lab_Practical.pdf`](./Experiment_8_Lab_Practical.pdf)

### 8. [Experiment 9: Implementation of Regularization (L1 & L2)](./exp%209/)
- **Description:** Flask web application demonstrating L1 (Lasso) and L2 (Ridge) regularization on polynomial features, comparing decision boundaries before vs after regularization, and plotting performance accuracy and loss.
- **Code:** [`exp 9/app.py`](./exp%209/app.py) &amp; [`exp 9/templates/index.html`](./exp%209/templates/index.html)
- **Manual Report:** [`exp 9/LAB_PRACTICAL_FILE.md`](./exp%209/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_9_Lab_Practical.pdf`](./Experiment_9_Lab_Practical.pdf)

### 9. [Experiment 10: Principal Component Analysis (PCA) with Testing](./exp%2010/)
- **Description:** Pure Python/NumPy PCA implementation projecting bivariate sensor data onto the 1st principal component line, mapping reduced 1D features along the line, and testing unseen candidate vectors with reconstruction error analysis.
- **Code:** [`exp 10/app.py`](./exp%2010/app.py) &amp; [`exp 10/templates/index.html`](./exp%2010/templates/index.html)
- **Manual Report:** [`exp 10/LAB_PRACTICAL_FILE.md`](./exp%2010/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_10_Lab_Practical.pdf`](./Experiment_10_Lab_Practical.pdf)

### 10. [Experiment 11: Linear Discriminant Analysis (LDA) with Testing](./exp%2011/)
- **Description:** Pure Python/NumPy Fisher's Linear Discriminant Analysis implementation maximizing between-class to within-class scatter, visualizing the optimal projected line with mapped class points, and testing classification with decision threshold.
- **Code:** [`exp 11/app.py`](./exp%2011/app.py) &amp; [`exp 11/templates/index.html`](./exp%2011/templates/index.html)
- **Manual Report:** [`exp 11/LAB_PRACTICAL_FILE.md`](./exp%2011/LAB_PRACTICAL_FILE.md)
- **Print-Ready PDF:** [`Experiment_11_Lab_Practical.pdf`](./Experiment_11_Lab_Practical.pdf)
