# 1D Subd Tool

Набор инструментов в Blender для управления подразделениями.

Функционал
-
**Store Subd**

Для всех выделенных объектов у модификатора Subdivision Surface выполняется перенос значения View в Render.

Если у объекта нет модификатора Subdivision Surface, он добавляется со значениями View = 0, Render = 0

**Review Subd**

Для всех выделенных объектов у модификатора Subdivision Surface выполняется перенос значения Render в View.

Если у объекта нет модификатора Subdivision Surface, он добавляется со значениями View = 0, Render = 0

**Select Subd**

Выбирает все объекты, у которых в модификаторе Subdivision Surface значение Render равно значению Render у активного объекта.

Если у активного объекта нет модификатора Subdivision Surface выбираются все объекты без этого модификатора.

Версия Blender
-
2.79

