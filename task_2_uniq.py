def unique(items):
    res = []
    i = 0
    while i < len(items):
        if len(res) == 0 or res[-1] != items[i]:
            res = res + [items[i]]
        i = i + 1
    return res
