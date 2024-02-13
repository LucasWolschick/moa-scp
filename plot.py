# plots a nice time series using matplotlib using data:
data = """
0	87296
1.65200209617615	76777
3.67500042915344	74903
4.48899960517883	72801
5.3860023021698	71533
8.18500328063965	71218
13.389003276825	70864
18.0300006866455	68499
975.448002099991	68490
1581.4080016613	68084
1599.3580019474	67536
2255.09700250626	67242
3572.89900183678	67096
4196.59400224686	65073
4226.92781710625	64586
7735.90942144394	64427
7934.78743171692	64423
8085.06441950798	64396
9104.10956716538	63754
9148.58056139946	63483
9166.74556851387	63087
9568.71233296394	63025
9602.54432439804	62950
9611.41228103638	62732
10671.8165464401	62340
11396.671459198	61703
11401.7354609966	61332
11401.9404592514	61319
11672.5964615345	61319


""".strip().split(
    "\n"
)


def flatten(lst):
    if not lst:
        return []
    if isinstance(lst[0], list):
        return flatten(lst[0]) + flatten(lst[1:])
    return lst[:1] + flatten(lst[1:])


data = flatten([list(map(float, line.split())) for line in data])
x = data[0::2]
y = data[1::2]

import matplotlib.pyplot as plt

# show grid and dots
plt.grid()
plt.scatter(x, y, None, "black")
# show line
# red
plt.plot(x, y, "black")
# draw value for each point
xrange = max(x) - min(x)
yrange = max(y) - min(y)
for i in range(len(x)):
    plt.text(
        x[i] + xrange * 0.02,
        y[i] + yrange * 0.01,
        f"{y[i]}",
    )
# draw label for x and y axis
plt.xlabel("t (s)")
plt.ylabel("custo")

plt.show()
