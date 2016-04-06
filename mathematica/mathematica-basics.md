Note: `Shift-Enter` to "Evaluate"

- version
~~~
$Version
Print[$Version]
Quit[]
~~~

- other

```
Solve[x^2 + 2 x - 7 == 0, x]

Plot[Sin[x], {x, 0, 6 Pi}]
Plot3D[Sin[x + y^2], {x, -3, 3}, {y, -2, 2}]

r1 = {x - 2 y == 7, x^2 + 4 y^2 == 37}
Solve[r1, {x, y}]
Plot3D[r1, {x, 0, 7}, {y, -4, 1}]
```

