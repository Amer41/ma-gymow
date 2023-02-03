# **3D model descriptor**

Die Formbeschreibung und die Extrahierung des Merkmalsvektor erfoglt gemäss dem Algorithmus, welcher in
<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;"E. Ait Lmaati et al., «A 3-D Search engine based on Fourier series,» in Computer Vision and Image Understanding, 2010, pp. 1-7, Band: 114." 
<br><br>
beschrieben wurde.

## **continuous Principle Component Analysis (cPCA)**

- auf deutsch: kontinuierliche Hauptkomponentenanalyse.

- In diesem Schritt werden die Modelle normalisiert ...
    1. ... zentriert (verschiebung)
    2. ... entlang der x-achse ausgerichtet (rotation/reflexion)
    3. ... auf eine Standardgrösse skaliert

- Der Algorithmus wurde aus folgender Quelle entnommen und selbständig implementiert*:
    - D. V. Vranic et al., «Pose Estimation,» in 3D Model Retrieval, 2003, pp. 61-76
    - *Die einzige Ausnahme ist die "compute_scaling_factor"-Funtion. Diese wurde eins zu eins von einem Pseudo-Code in der Quelle übernommen.

## **curve**
- Hier wird eine 3D-Kurve um das Model gespannt:
    1. Es wird eine kugelförmige Spirale definiert.
    2. Danach werden die Schnittpunkte zwischen den Strahlen, welche vom Koordinatenurprung ausgehen und auf die Spirale zeigen, und dem Model berechent
        - Dazu wird der  Möller-Trumbore-Algorithmus eingesetzt (siehe triangle.py)
    3. Zum Schluss
- Um die Rechenzeit zu reduzieren, werden die Dreiecke des Polygonnetzes in 8 Teilmengen aufgeteil.
- Sollten mehrere Schnittpunkte gefunden werden, wird nur der Punkt gezählt, welche am weitesten vom Ursprung liegt.
- Wenn keine Schnittpunkte gefunden werden, wird der Schnittpunkt in den Ursprung gesetzt.

## **fourier**
- Da können die Fourier-Koeffizienten von einem beliebigen Signal berechent.
- Der Algorithmus wurde aus dem folgendem Video übernommen:
    - https://www.youtube.com/watch?v=r6sGWTCMz2k


## **feature_vector**
- Extrahierung der Merkmalsvektor
- Die Distanzfunktionen zwischen zwei Merkmalsvektoren
