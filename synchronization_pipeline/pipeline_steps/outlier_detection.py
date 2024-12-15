# event_detection/outlier_detection.py
from sklearn.neighbors import LocalOutlierFactor

def detect_outliers(data, signal_column, n_neighbors=200):
    X = data[signal_column].values.reshape(-1, 1)
    lof = LocalOutlierFactor(n_neighbors=n_neighbors)
    outliers = lof.fit_predict(X)
    return outliers == -1  # Convert outlier flags: -1 means outlier
