import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay,accuracy_score
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from joblib import dump

# Load and preprocess data
df = pd.read_csv('notes_with_outcomes.csv')
df = df[['note_text', 'trial_outcome']].drop_duplicates().dropna()



def map_outcome(outcome):
    outcome = outcome.strip().lower()
    if outcome == 'worsened':
        return 'Negative'
    elif outcome == 'improved':
        return 'Positive'
    elif outcome == 'stable':
        return 'Neutral'
    return None

df['expected'] = df['trial_outcome'].apply(map_outcome)
df = df[df['expected'].notna()]

# Encode labels
le = LabelEncoder()
y = le.fit_transform(df['expected'])

# Load ClinicalBERT
tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
model = AutoModel.from_pretrained("medicalai/ClinicalBERT")
model.eval()

# Get embeddings
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

print("Generating embeddings...")
embeddings = np.array([get_embedding(text) for text in tqdm(df['note_text'].tolist())])

# Find optimal PCA components
print("\nFinding optimal PCA components...")
explained = PCA().fit(embeddings).explained_variance_ratio_
cumulative = np.cumsum(explained)

# Plot cumulative variance
plt.plot(cumulative, marker='o')
plt.axhline(y=0.90, color='r', linestyle='--', label='90% variance')
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')
plt.title('Explained Variance vs. Components')
plt.grid(True)
plt.legend()
plt.show()

# Test performance from 10 to 100 components
best_n = 10
best_acc = 0
components_to_test = range(10, 51, 10)
acc_results = []

for n in components_to_test:
    pca = PCA(n_components=n)
    X_pca = pca.fit_transform(embeddings)

    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    acc = []

    for train_idx, test_idx in skf.split(X_pca, y):
        X_train, X_test = X_pca[train_idx], X_pca[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        clf = LogisticRegression(max_iter=1000)
        clf.fit(X_train, y_train)
        acc.append(clf.score(X_test, y_test))

    avg = np.mean(acc)
    acc_results.append(avg)

    if avg > best_acc:
        best_acc = avg
        best_n = n

# Plot accuracy
plt.plot(components_to_test, acc_results, marker='o')
plt.xlabel('n_components')
plt.ylabel('Cross-validated Accuracy (LogReg)')
plt.title('LogReg Accuracy vs. PCA Components')
plt.grid(True)
plt.show()

print(f"\n✅ Best n_components = {best_n} with Accuracy = {best_acc:.4f}")
best_n=10
# Apply best PCA
pca = PCA(n_components=best_n)
X_pca = pca.fit_transform(embeddings)


def evaluate_model(model, name):
    print(f"\n--- Evaluating {name} ---")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    all_true, all_pred = [], []

    for train_idx, test_idx in skf.split(X_pca, y):
        X_train, X_test = X_pca[train_idx], X_pca[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        all_true.extend(y_test)
        all_pred.extend(preds)

    y_true_labels = le.inverse_transform(all_true)
    y_pred_labels = le.inverse_transform(all_pred)

    print("Classification Report:")
    print(classification_report(y_true_labels, y_pred_labels, digits=3))

    # Adjusted accuracy
    def is_correct(pred, true):
        if true == 'Neutral':
            return pred in ['Neutral', 'Positive']
        return pred == true

    true_acc = accuracy_score(y_true_labels, y_pred_labels)
    adjusted_acc = np.mean([is_correct(p, t) for p, t in zip(y_pred_labels, y_true_labels)])
    print(f"True Accuracy: {true_acc:.4f} || Adjusted Accuracy: {adjusted_acc:.4f}")

    # Confusion Matrix
    cm = confusion_matrix(y_true_labels, y_pred_labels, labels=le.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
    disp.plot(cmap='Blues', values_format='d')
    plt.title(f"Confusion Matrix - {name}")
    plt.show()

# Unified evaluation
evaluate_model(LogisticRegression(max_iter=100, C=0.5), "Logistic Regression")
evaluate_model(SVC(kernel='linear', C=1.0), "SVM (Linear Kernel)")
evaluate_model(RandomForestClassifier(n_estimators=80, max_depth=10, random_state=42), "Random Forest")

# Placeholder for accuracy results
n_estimators_range = range(10, 201, 10)
rf_n_estimators_results = []

# Evaluate Random Forest with varying n_estimators, fixed max_depth=10
for n in n_estimators_range:
    print(f"\nRandom Forest with n_estimators={n}, max_depth=10")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    acc_list = []

    for train_idx, test_idx in skf.split(X_pca, y):
        X_train, X_test = X_pca[train_idx], X_pca[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model = RandomForestClassifier(n_estimators=n, max_depth=10, random_state=42)
        model.fit(X_train, y_train)
        acc_list.append(model.score(X_test, y_test))

    avg_acc = np.mean(acc_list)
    rf_n_estimators_results.append((n, avg_acc))
    print(f"Avg Accuracy: {avg_acc:.4f}")

# Plot: n_estimators vs Accuracy
n_values, accuracies = zip(*rf_n_estimators_results)
plt.plot(n_values, accuracies, marker='o')
plt.xlabel("n_estimators")
plt.ylabel("Accuracy")
plt.title("Random Forest (max_depth=10): n_estimators vs Accuracy")
plt.grid(True)
plt.show()
evaluate_model(DecisionTreeClassifier(max_depth=8, random_state=42), "Decision Tree")


# Store results for plotting
logreg_results = []
svc_results = []
rf_results = []
dt_results = []

# Evaluate Logistic Regression with varying iterations
for iter in range(50, 501, 50):
    print(f"\nLogistic Regression with max_iter={iter}")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    acc_list = []

    for train_idx, test_idx in skf.split(X_pca, y):
        X_train, X_test = X_pca[train_idx], X_pca[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model = LogisticRegression(max_iter=iter, C=0.5)
        model.fit(X_train, y_train)
        acc_list.append(model.score(X_test, y_test))

    avg_acc = np.mean(acc_list)
    logreg_results.append((iter, avg_acc))
    print(f"Avg Accuracy: {avg_acc:.4f}")

# Plot Logistic Regression: max_iter vs accuracy
iters, accs = zip(*logreg_results)
plt.plot(iters, accs, marker='o')
plt.xlabel("max_iter")
plt.ylabel("Accuracy")
plt.title("Logistic Regression: max_iter vs Accuracy")
plt.grid(True)
plt.show()

# Evaluate SVC with varying C
c = 0.1
while c <= 1.0:
    print(f"\nSVM with C={c:.1f}")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    acc_list = []

    for train_idx, test_idx in skf.split(X_pca, y):
        X_train, X_test = X_pca[train_idx], X_pca[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model = SVC(kernel='linear', C=c)
        model.fit(X_train, y_train)
        acc_list.append(model.score(X_test, y_test))

    avg_acc = np.mean(acc_list)
    svc_results.append((round(c, 1), avg_acc))
    print(f"Avg Accuracy: {avg_acc:.4f}")
    c += 0.1

# Plot SVC: C vs accuracy
cs, accs = zip(*svc_results)
plt.plot(cs, accs, marker='o')
plt.xlabel("C")
plt.ylabel("Accuracy")
plt.title("SVM (linear kernel): C vs Accuracy")
plt.grid(True)
plt.show()

# Evaluate Random Forest with varying max_depth
for depth in range(5, 11):
    print(f"\nRandom Forest with max_depth={depth}")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    acc_list = []

    for train_idx, test_idx in skf.split(X_pca, y):
        X_train, X_test = X_pca[train_idx], X_pca[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model = RandomForestClassifier(n_estimators=100, max_depth=depth, random_state=42)
        model.fit(X_train, y_train)
        acc_list.append(model.score(X_test, y_test))

    avg_acc = np.mean(acc_list)
    rf_results.append((depth, avg_acc))
    print(f"Avg Accuracy: {avg_acc:.4f}")

# Plot Random Forest: max_depth vs accuracy
depths, accs = zip(*rf_results)
plt.plot(depths, accs, marker='o')
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.title("Random Forest: max_depth vs Accuracy")
plt.grid(True)
plt.show()

# Evaluate Decision Tree with varying max_depth
for depth in range(5, 11):
    print(f"\nDecision Tree with max_depth={depth}")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    acc_list = []

    for train_idx, test_idx in skf.split(X_pca, y):
        X_train, X_test = X_pca[train_idx], X_pca[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model = DecisionTreeClassifier(max_depth=depth, random_state=42)
        model.fit(X_train, y_train)
        acc_list.append(model.score(X_test, y_test))

    avg_acc = np.mean(acc_list)
    dt_results.append((depth, avg_acc))
    print(f"Avg Accuracy: {avg_acc:.4f}")

# Plot Decision Tree: max_depth vs accuracy
depths, accs = zip(*dt_results)
plt.plot(depths, accs, marker='o')
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.title("Decision Tree: max_depth vs Accuracy")
plt.grid(True)
plt.show()

# Train on the entire PCA-transformed dataset
final_rf = RandomForestClassifier(n_estimators=80, max_depth=10, random_state=42)
final_rf.fit(X_pca, y)

# Save the model
dump(final_rf, r'.\models\best_random_forest_model.joblib')
print("✅ Random Forest model saved as 'best_random_forest_model.joblib'")
dump(pca, r'.\models\pca_transformer.joblib')
dump(le, r'.\models\label_encoder.joblib')

