# ============================================================
# ANÁLISIS DE SENTIMIENTOS CON NLP
# ============================================================
# Objetivo: clasificar reseñas de películas como positivas
# o negativas usando técnicas de procesamiento de lenguaje natural.
#
# Dataset: movie_reviews (NLTK) — 2000 reseñas etiquetadas
#
# Flujo del proyecto:
#   1. Carga y limpieza de texto (tokenización + stopwords)
#   2. Vectorización con TF-IDF (texto → números)
#   3. Entrenamiento con Regresión Logística
#   4. Evaluación con accuracy y F1-score
#   5. Predicción sobre texto nuevo
#
# Librerías: nltk, scikit-learn
# Resultado esperado: ~85% de accuracy
# ============================================================



# ============================================================

## CELDA 1 ##

import nltk
nltk.download('movie_reviews')
nltk.download('stopwords')

from nltk.corpus import movie_reviews
import random

# Cargar reseñas con su etiqueta (pos / neg)
documentos = [(list(movie_reviews.words(fileid)), categoria)
              for categoria in movie_reviews.categories()
              for fileid in movie_reviews.fileids(categoria)]

random.shuffle(documentos)
print(f"Total de reseñas: {len(documentos)}")

# ============================================================

## CELDA 2 ##

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

stop_words = stopwords.words('english')

# Unir palabras en oraciones limpias
textos = [" ".join(w.lower() for w in doc
          if w.isalpha() and w.lower() not in stop_words)
          for doc, _ in documentos]

etiquetas = [1 if cat == 'pos' else 0
             for _, cat in documentos]

# Vectorización TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(textos)

print(f"Matriz de features: {X.shape}")

# ============================================================

## CELDA 3 ##


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(
    X, etiquetas, test_size=0.2, random_state=42)

modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred,
      target_names=['Negativa', 'Positiva']))


# ============================================================

## CELDA 4 ##

def predecir_sentimiento(texto):
    limpio = " ".join(w.lower() for w in texto.split()
                      if w.isalpha() and w.lower()
                      not in stop_words)
    vec = vectorizer.transform([limpio])
    pred = modelo.predict(vec)[0]
    prob = modelo.predict_proba(vec)[0]
    etiqueta = "Positiva 😊" if pred == 1 else "Negativa 😞"
    print(f"Sentimiento: {etiqueta}")
    print(f"Confianza: {max(prob):.1%}")

# Probalo con cualquier reseña en inglés
predecir_sentimiento("This movie was absolutely fantastic!")
predecir_sentimiento("Boring and too long, I hated it.")
	  
	  
# ============================================================
