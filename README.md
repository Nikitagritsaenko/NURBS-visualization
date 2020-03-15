# NURBS-visualization
NURBS - Non-uniform rational B-spline visualization

### Пояснение
Средствами PyQt и c помощью de Boor's алгоритма создан простой визуализатор NURBS сплайнов. Алгоритм создан для обычных B-сплайнов, однако для перехода к NURBS достаточно:
1. Перевести контрольные точки в пространство большей размерности (положить новую координату равной 1)
2. Умножить компоненты контрольных точек на веса
3. Применить алгоритм для B-сплайна
4. Разделить компоненты получившейся точки на последнюю компоненту

Здесь этот процесс описан подробнее: https://www.researchgate.net/publication/221538041_If_you_know_b-splines_well_you_also_nnow_NURBS

### Примечания:
- Контрольные точки и веса задаются в коде
- Пользователь имеет возможность перестаскивать контрольные точки мышью. При этом происходит перестроение сплайна

### Примеры

#### Обычный B-spline
![](https://github.com/Nikitagritsaenko/NURBS-visualization/blob/master/screenshots/b_spline.JPG)

#### NURBS
![](https://github.com/Nikitagritsaenko/NURBS-visualization/blob/master/screenshots/nurbs.JPG)
