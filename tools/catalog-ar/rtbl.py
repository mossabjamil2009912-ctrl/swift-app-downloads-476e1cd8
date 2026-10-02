"""RTL flip of a spec table: label column moves to the right edge, value clusters mirrored per text line.
flip(src, dst, pno, y0, y1, lab=(lx0,lx1), val=(vx0,vx1), extra=[((x0,y0,x1,y1), dest_x0), ...])"""
import pymupdf, numpy as np

Z = 4


def _runs(v, gap):
    out = []; i = 0; n = len(v)
    while i < n:
        if v[i]:
            j = i
            while j < n and v[j]: j += 1
            if out and i - out[-1][1] < gap: out[-1] = (out[-1][0], j)
            else: out.append((i, j))
            i = j
        else: i += 1
    return out


def flip(src, dst, pno, y0, y1, lab, val, extra=(), thr=200, colgap=6.0, doc=None):
    s = pymupdf.open(src); d = doc or pymupdf.open(src)
    sp = s[pno]; page = d[pno]
    lx0, lx1 = lab; vx0, vx1 = val
    new_l = vx1 - (lx1 - lx0)
    new_v0 = lx0
    pm = sp.get_pixmap(clip=pymupdf.Rect(lx0, y0, vx1, y1), matrix=pymupdf.Matrix(Z, Z))
    rgb = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, pm.n)[:, :, :3]
    ink = rgb.mean(2) < thr
    fills, copies = [], []
    for a, b in _runs(ink.any(1), 1):
        ya, yb = y0 + a / Z - 0.3, y0 + b / Z + 0.3
        bg = tuple(float(c) / 255 for c in rgb[max(a - 1, 0), int((vx0 - lx0 + 2) * Z)])
        fills.append((pymupdf.Rect(lx0, ya, vx1, yb), bg))
        copies.append((pymupdf.Rect(lx0, ya, lx1, yb), new_l))
        vi0 = int((vx0 - lx0) * Z)
        for c0, c1 in _runs(ink[a:b, vi0:].any(0), int(colgap * Z)):
            x0 = vx0 + c0 / Z - 0.6; x1 = vx0 + c1 / Z + 0.6
            copies.append((pymupdf.Rect(x0, ya, x1, yb), new_v0 + (vx1 - x1)))
    for r, dx in extra:
        fills.insert(0, (pymupdf.Rect(*r), (1, 1, 1)))
        copies.append((pymupdf.Rect(*r), dx))
    for r, c in fills:
        page.draw_rect(r, color=None, fill=c, overlay=True)
    for r, dx in copies:
        page.show_pdf_page(pymupdf.Rect(dx, r.y0, dx + r.width, r.y1), s, pno, clip=r, overlay=True)
    if doc is None:
        d.save(dst, garbage=4, deflate=True)
    return d
