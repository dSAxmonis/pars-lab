# PATTERN ANALYSIS AND RECOGNITION SYSTEMS (PARS) LAB MANUAL

---

## EXPERIMENT 7

### PRACTICAL NAME:
**Implementation of Linear Regression from Scratch Using Gradient Descent and Cost Curve Analysis in Python**

---

### AIM:
To implement Linear Regression in Python from scratch without using any inbuilt machine learning library functions (such as `scikit-learn`), optimize parameters (weight $w$ and bias $b$) via Gradient Descent for a real-world predictive application (Real Estate Price Prediction), and plot the Gradient Descent convergence cost curve alongside the fitted regression line.

---

### THEORY:

#### 1. Linear Regression Model Representation
Linear Regression models the relationship between a dependent target scalar variable $y$ and an explanatory feature vector $\mathbf{x}$. For a univariate feature $x$, the hypothesis function is expressed as:
$$\hat{y}^{(i)} = w x^{(i)} + b$$
where $w$ is the slope weight parameter, and $b$ is the intercept bias parameter.

#### 2. Loss Function (Mean Squared Error)
The quality of parameter estimates is quantified by the Mean Squared Error (MSE) objective function:
$$J(w, b) = \frac{1}{2m} \sum_{i=1}^{m} \left(\hat{y}^{(i)} - y^{(i)}\right)^2 = \frac{1}{2m} \sum_{i=1}^{m} \left(w x^{(i)} + b - y^{(i)}\right)^2$$
The constant $\frac{1}{2}$ is introduced to cancel during partial differentiation.

#### 3. Gradient Descent Optimization
To find the parameters minimizing $J(w, b)$, parameters are initialized arbitrarily ($w_0 = 0, b_0 = 0$) and iteratively adjusted opposite the direction of the gradient:

- **Partial Derivative with respect to $w$:**
  $$\frac{\partial J}{\partial w} = \frac{1}{m} \sum_{i=1}^{m} \left(\hat{y}^{(i)} - y^{(i)}\right) x^{(i)}$$

- **Partial Derivative with respect to $b$:**
  $$\frac{\partial J}{\partial b} = \frac{1}{m} \sum_{i=1}^{m} \left(\hat{y}^{(i)} - y^{(i)}\right)$$

- **Simultaneous Parameter Update Rule:**
  $$w := w - \alpha \frac{\partial J}{\partial w}$$
  $$b := b - \alpha \frac{\partial J}{\partial b}$$
  where $\alpha > 0$ represents the learning rate hyperparameter.

#### 4. Gradient Descent Convergence Curve
At each iteration $t$, the cost $J_t(w, b)$ is tracked. A properly configured learning rate ensures monotonic convergence towards the global minimum:
$$\lim_{t \to \infty} \nabla J(w_t, b_t) = \mathbf{0}$$

---

### STEPS:

1. **Step 1: Environment & Mathematical Engine Setup**
   - Create directory `exp 7/` with Flask web server and NumPy array processing routines.
   - Prohibit external regression packages (`sklearn.linear_model`).
   - > **[ATTACH FULL PAGE SCREENSHOT: Step 1 - Environment & Implementation Structure]**

2. **Step 2: Mathematical Gradient & Cost Implementation**
   - Code `compute_cost(X, y, w, b)` and `compute_gradients(X, y, w, b)` strictly using vectorized arithmetic.
   - Implement optimization loop tracking cost per epoch.
   - > **[ATTACH FULL PAGE SCREENSHOT: Step 2 - Gradient Descent Routine]**

3. **Step 3: Web Server Deployment & Visualization**
   - Run Flask server on port 5009 (`python3 "exp 7/app.py"`).
   - Display dual plots: Gradient Descent MSE decay curve and Fitted Regression Line against actual housing points.
   - > **[ATTACH FULL PAGE SCREENSHOT: Step 3 - Dashboard Active on Port 5009]**

---

### CODE FILES & REPOSITORY:

- **GitHub Repository Link (Clickable):**  
  [![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github)](https://github.com/dSAxmonis/pars-lab)  
  [https://github.com/dSAxmonis/pars-lab](https://github.com/dSAxmonis/pars-lab)

- **Source Code Links:**
  - [Flask Server (`exp 7/app.py`)](https://github.com/dSAxmonis/pars-lab/blob/main/exp%207/app.py)
  - [HTML Template (`exp 7/templates/index.html`)](https://github.com/dSAxmonis/pars-lab/blob/main/exp%207/templates/index.html)
  - [Dependencies (`exp 7/requirements.txt`)](https://github.com/dSAxmonis/pars-lab/blob/main/exp%207/requirements.txt)
  - [Full Page Screenshot (`exp 7/screenshots/full_page.png`)](https://github.com/dSAxmonis/pars-lab/blob/main/exp%207/screenshots/full_page.png)

---

### OUTPUT / SCREENSHOTS:

> **Full Page Application Screenshot Saved At:** `exp 7/screenshots/full_page.png`  
> **[ATTACH FULL PAGE SCREENSHOT HERE]**

---

### CONCLUSION:
In this experiment, Linear Regression was implemented completely from scratch in Python without relying on pre-built machine learning libraries. Utilizing analytical gradient descent equations, optimal weights ($w^*$) and bias ($b^*$) were iteratively discovered for housing valuation data. The resulting Gradient Descent curve demonstrated stable monotonic cost convergence, and the fitted regression model reliably generalized predictions on unseen feature samples.
