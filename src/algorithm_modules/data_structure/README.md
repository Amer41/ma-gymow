# **Datenstruktur**

## **Vector3 & Matrix3**
- Die Klassen wurden selbständig erstellt, um Rechengeschwindigkeit zu optimieren.

## **Triangle**
- Diese Klasse repräsentiert die Dreiecke, welche das Polygonnetz bilden.
- Beim erstellen werden die für jedes Dreieck spezifischen Konstanten beim Möller-Trumbore-Algorithmus berechnet und als Attribute gespeichert.
    - Dadurch wird die Rechenzeit beim Berechnen der Schnittpunkte zwischen Stahlen und Dreiecke verringert.

- **Achtung**: Bei der Berechnung wird immer angenommen, dass der Strahl durch den Koordinatenursprung geht.



- Der MT-Algorithmus wurde aus folgender Quelle entnommen und selbständig implementiert:
    - https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/moller-trumbore-ray-triangle-intersection.html

