# **3D model descriptor**

Die untermodule in diesem Modul Definieren die Funktionen welche zur Extrahierung des Merkmalsvektors von 3D-Modelle eingesetzt werden. <br><br>
Der Algorithmus wurde aus dem folgenden Paper entnommen und selbstängig implementiert:
<p align="center">
*E. Ait Lmaati et al., «A 3-D Search engine based on Fourier series,» in Computer Vision and Image Understanding, 2010, pp. 1-7, Band: 114.*
</p>

## **continuous Principle Component Analysis (cPCA)**

- auf deutsch: kontinuierliche Hauptkomponentenanalyse.

- Der Algorithmus für die Hauptkomponentenanalyse wurde aus folgender Quelle entnommen und selbständig implementiert*:
    - D. V. Vranic et al., «Pose Estimation,» in 3D Model Retrieval, 2003, pp. 61-76 <br><br>
    - *Die einzige Ausnahme ist die "compute_scaling_factor"-Funtion. Diese wurde eins zu eins von einem Pseudo-Code in der Quelle übernommen.

## **mt_intersection_algorithm**
- Möller-Trumbore-Algorithmus (siehe triangle.py).
- Berechnung der Schnittpunkte zwischen Strahen und Dreiecken

## **curve**
- Definition der Spirale
- Spannung einer zur Spirale homöomorphenen 3D-Kurve um ein 3D-Objekt
- Zur Berechnung:
    - Um die Rechenzeit zu reduzieren, werden die Dreiecke des Polygonnetzes in 8 Teilmengen aufgeteil.
    - Sollten mehrere Schnittpunkte gefunden werden, wird nur der Punkt gezählt, welche am weitesten vom Ursprung liegt.
    - Wenn keine Schnittpunkte gefunden werden, wird der Schnittpunkt in den Ursprung gesetzt. 

## **fourier**
- Da können die Fourier-Koeffizienten von einem beliebigen Signal berechent.
- Der Algorithmus wurde aus dem folgendem Video übernommen:
    - https://www.youtube.com/watch?v=r6sGWTCMz2k


## **feature_vector**
- Extrahierung der Merkmalsvektor
- Definition der Distanzfunktion zwischen zwei Merkmalsvektoren
