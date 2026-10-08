from sklearn.preprocessing import StandardScaler
# preprocessing
# This is a section/module inside scikit-learn containing tools for preparing data before machine learning.

def fit_scaler(X_train):
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler


def transform_features(scaler, X):
    return scaler.transform(X)