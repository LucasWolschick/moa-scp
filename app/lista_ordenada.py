import bisect


def contem(lista: list, x):
    """Retorna o índice de *x* em *lista* ou False se *x* não estiver em *lista*."""
    i = bisect.bisect_left(lista, x)
    return i != len(lista) and lista[i] == x and i


def insere(lista: list, x):
    """Insere *x* em *lista*."""
    i = bisect.bisect(lista, x)
    lista.insert(i, x)


def remove(lista: list, x):
    """Remove *x* de *lista*, se ele está na lista."""
    if i := contem(lista, x):
        lista.pop(i)


def uniao(lhs: list, rhs: list):
    """Retorna a união de *lhs* e *rhs*."""
    res = []
    il = 0
    ir = 0
    while il < len(lhs) and ir < len(rhs):
        l = lhs[il]
        r = rhs[ir]
        if l == r:
            res.append(l)
            il += 1
            ir += 1
        elif l < r:
            res.append(l)
            il += 1
        elif l > r:
            res.append(r)
            ir += 1
    if il < len(lhs):
        res += lhs[il:]
    elif ir < len(rhs):
        res += rhs[ir:]
    return res


def inter(lhs: list, rhs: list):
    """Retorna a interseção de *lhs* e *rhs*."""
    res = []
    il = 0
    ir = 0
    while il < len(lhs) and ir < len(rhs):
        l = lhs[il]
        r = rhs[ir]
        if l == r:
            res.append(l)
            il += 1
            ir += 1
        elif l < r:
            il += 1
        elif l > r:
            ir += 1
    return res


def sub(lhs: list, rhs: list):
    res = []
    il = 0
    ir = 0
    while il < len(lhs) and ir < len(rhs):
        l = lhs[il]
        r = rhs[ir]
        if l == r:
            il += 1
            ir += 1
        elif l < r:
            res.append(l)
            il += 1
        elif l > r:
            ir += 1
    if il < len(lhs):
        res += lhs[il:]
    return res
