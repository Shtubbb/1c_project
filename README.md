# Задача 214

Найдем сгустки точек пересечения, для этого возьмем и бросим в разлиных направлениях лучи (для каждого луча в одну и в обратную сторону). Если по этому лучу в обе стороны можно далеко дойти по графу(константу и бросаемые лучи можно улучшать для лучше работы), значит точка лежит на ребре. Если точка лежи на нескольких ребрах, то значи она лежит на пересечении ребер. В конце обьединим точки лежащие рядом и посчитаем ответ.
