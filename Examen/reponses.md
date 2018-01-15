# R�cup�rer les images et les sauvegarder
---

```
classify_pages.py --images-list classes.csv --save-features saved
```

Seulement 9153 images r�cup�r�es (probleme de path)


# Tester avec un knn de 1
---

```
classify_pages.py --load-features saved --nearest-neighbors 1
```

R�sultat : 0.74877


# Tester avec un knn de 1 � 10
---

```
classify_pages.py --load-features saved --knn
```

![Best KNN](C:/Users/Th�o/Images/knn.png, "Best KNN")
