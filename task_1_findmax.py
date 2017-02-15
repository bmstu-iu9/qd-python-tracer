def findmax(items):
    if len(items) == 0:
        return None
    m = items[0]
    i = 1
    while i < len(items):
        if m < items[i]:
            m = items[i]
    return m
