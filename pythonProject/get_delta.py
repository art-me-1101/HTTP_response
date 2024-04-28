def get_delta(toponym):
    d = toponym['boundedBy']['Envelope']
    a = list(map(float, d['lowerCorner'].split()))
    b = list(map(float, d['upperCorner'].split()))
    c = abs(a[0] - b[0])
    d = abs(a[1] - b[1])
    return [str(c), str(d)]