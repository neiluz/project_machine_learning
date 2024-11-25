import streamlit as st
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.stats.mstats import winsorize

# --- Definiciones necesarias para el pipeline ---

def winsorize_transform(X):
    return np.apply_along_axis(lambda col: winsorize(col, limits=[0.05, 0.05]), axis=0, arr=X)

# Función para transformación logarítmica
def log_transform(X):
    X = np.where(X <= 0, X + np.abs(X.min(axis=0)) + 1, X)  # Ajusta valores negativos o ceros
    return np.log1p(X)

# Clase para agrupar categorías de baja frecuencia
class LowFrequencyGrouper(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=0.05):
        self.threshold = threshold
        self.low_freq_categories_ = None

    def fit(self, X, y=None):
        self.low_freq_categories_ = []
        for col in range(X.shape[1]):
            unique, counts = np.unique(X[:, col], return_counts=True)
            freq = counts / len(X)
            low_freq_categories = unique[freq < self.threshold]
            self.low_freq_categories_.append(low_freq_categories)
        return self

    def transform(self, X):
        X_transformed = X.copy()
        for col in range(X.shape[1]):
            low_freq_categories = self.low_freq_categories_[col]
            X_transformed[:, col] = np.where(
                np.isin(X_transformed[:, col], low_freq_categories), 'Otros', X_transformed[:, col]
            )
        return X_transformed