def __search_nearest_layer(bands, wl):
    b, e, idx = 0, len(bands) - 1, 0    # Begin, end

    while True:
        m = floor((b + e) / 2.0)  # Middle 

        if b == e or bands[m] <= wl < bands[m + 1]:
            idx = m
            break
        elif wl < bands[m]:
            e = m - 1
        else:
            b = m + 1

    if idx == (len(bands) - 1):
        return idx
    else:
        if abs(wl - bands[idx]) < abs(wl - bands[idx + 1]):
            return idx
        else:
            return idx + 1