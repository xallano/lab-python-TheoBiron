# Récupérer les images et les sauvegarder
---

```
classify_pages.py --images-list classes.csv --save-features saved
```

Seulement 9153 images récupérées (probleme de path)


# Tester avec un knn de 1
---

```
classify_pages.py --load-features saved --nearest-neighbors 1
```

Résultat : 0.74877


# Tester avec un knn de 1 à 10
---

```
classify_pages.py --load-features saved --knn
```

![Best KNN](C:/Users/Théo/Images/knn.png, "Best KNN")
