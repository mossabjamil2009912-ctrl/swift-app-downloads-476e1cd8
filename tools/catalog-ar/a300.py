"""Optimus A300-HY page 2: RTL flip of the spec table, navy section bands handled separately."""
import sys; sys.path.insert(0, '/dev-server/tools/catalog-ar')
import pymupdf, numpy as np
from rtbl import flip, _runs
S = '/dev-server/public/catalogs/official-ar/pylontech-optimus-a300-hy.pdf'
OUT = '/tmp/cat/a300-r.pdf'
L, M, R = 75, 300, 541
NAVY = (0.1389, 0.1684, 0.3090)
bands = [(65.3, 79.0), (269.6, 283.2), (405.2, 418.8), (541.7, 555.3)]
segs = [(79.4, 269.3), (283.5, 404.9), (419.1, 541.4), (555.6, 602)]
d = None
for y0, y1 in segs:
    d = flip(S, OUT, 1, y0, y1, (L, M), (M, R), doc=d, ralign=True, center=True)
s = pymupdf.open(S); page = d[1]; Z = 4
for y0, y1 in bands:
    pm = s[1].get_pixmap(clip=pymupdf.Rect(40, y0, R, y1), matrix=pymupdf.Matrix(Z, Z))
    rgb = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, pm.n)[:, :, :3]
    lite = rgb.mean(2) > 150
    cols = lite.any(0)
    runs = _runs(cols, int(12 * Z))
    page.draw_rect(pymupdf.Rect(L, y0, R, y1), color=None, fill=NAVY, overlay=True)
    for c0, c1 in runs:
        x0 = 40 + c0 / Z - 0.6; x1 = 40 + c1 / Z + 0.6
        r = pymupdf.Rect(max(x0, L + 0.5), y0, min(x1, R - 0.5), y1)
        if x0 < M:   # label -> flush right
            nx = R - 4 - r.width
        else:        # value -> centred in left value column
            nx = L + ((R - M) - r.width) / 2
        page.show_pdf_page(pymupdf.Rect(nx, y0, nx + r.width, y1), s, 1, clip=r, overlay=True)
d.save(OUT, garbage=4, deflate=True)
pymupdf.open(OUT)[1].get_pixmap(dpi=80).save('/tmp/cat/a300.png')
