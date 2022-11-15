# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import requests
import pandas as pd
import os
import sys

QNAME = sys.argv[1]

CURRENT_PATH = os.path.dirname(__file__) + '/'

if not os.path.exists(CURRENT_PATH + "results/"):
    os.mkdir(CURRENT_PATH + "results/")

QRELS_FILE = CURRENT_PATH + f"qrels/{QNAME}_qrels"
Q_FILE = CURRENT_PATH + f"querries/{QNAME}_q"
TUNED_QUERY_URL = open(Q_FILE).readline()

# Read qrels to extract relevant documents
relevant = list(map(lambda el: int(el.strip()), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
# Query URL format: http://localhost:8983/solr/{}/select?q={QUERY}&q.op={OPERATOR}&indent=true&wt=json
tuned_results = requests.get(TUNED_QUERY_URL.format(
    "games_tuned")).json()['response']['docs']
simple_results = requests.get(TUNED_QUERY_URL.format(
    "games_simple")).json()['response']['docs']

# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
def metric(f): return metrics.setdefault(f.__name__, f)


@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = [
        len([
            doc
            for doc in results[:idx]
            if doc['ResponseID'] in relevant
        ]) / idx
        for idx in range(1, len(results))
    ]
    return sum(precision_values)/len(precision_values)


@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['ResponseID'] in relevant])/n


@metric
def r10(results, relevant, n=10):
    """Recall at N"""
    return len([doc for doc in results[:n] if doc['ResponseID'] in relevant])/len(relevant)


@metric
def f10(results, relevant, n=10):
    """F1-score at N"""
    precision_at_10 = len(
        [doc for doc in results[:n] if doc['ResponseID'] in relevant])/n
    recall_at_10 = len([doc for doc in results[:n] if
                        doc['ResponseID'] in relevant])/len(relevant)
    return 2 * (precision_at_10 * recall_at_10) / (precision_at_10 + recall_at_10)


def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)


# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p10': 'Precision at 10 (P@10)',
    'r10': 'Recall at 10 (R@10)',
    'f10': 'F1-Score at 10 (F@10)'
}

# Calculate all metrics and export results as LaTeX table
df = pd.DataFrame([['Metric', 'Value']] +
                  [
    [evaluation_metrics[m], calculate_metric(m, tuned_results, relevant)]
    for m in evaluation_metrics
]
)

with open(CURRENT_PATH + f'results/{QNAME}_metrics_table.tex', 'w') as tf:
    tf.write(df.style.to_latex())


def calculate_precision_recall_curve(results, relevant, schematype):
    "Calculate precision and recall values as we move down the ranked list"
    precision_values = [
        len([
            doc
            for doc in results[:idx]
            if (doc['ResponseID'] if schematype == "tuned" else doc['ResponseID'][0]) in relevant
        ]) / idx
        for idx, _ in enumerate(results, start=1)
    ]

    recall_values = [
        len([
            doc for doc in results[:idx]
            if (doc['ResponseID'] if schematype == "tuned" else doc['ResponseID'][0]) in relevant
        ]) / len(relevant)
        for idx, _ in enumerate(results, start=1)
    ]

    precision_recall_match = {k: v for k,
                              v in zip(recall_values, precision_values)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(
        0.1, 1.1, 0.1) if step not in recall_values])
    recall_values = sorted(set(recall_values))

    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            if recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

    disp = PrecisionRecallDisplay(
        [precision_recall_match.get(r) for r in recall_values], recall_values)
    disp.plot()
    plt.savefig(CURRENT_PATH +
                f'results/{QNAME}_precision_recall_graph_{schematype}.pdf')


calculate_precision_recall_curve(simple_results, relevant, "simple")
calculate_precision_recall_curve(tuned_results, relevant, "tuned")
