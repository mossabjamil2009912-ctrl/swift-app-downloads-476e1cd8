import pymupdf
S='/dev-server/public/catalogs/official-ar/pylontech-optimus-a300-hy.pdf'
s=pymupdf.open(S); d=pymupdf.open(S); p=d[1]
L,M,R,y0,y1=72,300,598,66,590
lab=pymupdf.Rect(L,y0,M,y1); val=pymupdf.Rect(M,y0,R,y1)
p.draw_rect(pymupdf.Rect(L,y0,R,y1),color=None,fill=(1,1,1),overlay=True)
p.show_pdf_page(pymupdf.Rect(R-lab.width,y0,R,y1),s,1,clip=lab,overlay=True)
p.show_pdf_page(pymupdf.Rect(L,y0,L+val.width,y1),s,1,clip=val,overlay=True)
d.save('/tmp/cat/a300-r.pdf',garbage=4,deflate=True)
pymupdf.open('/tmp/cat/a300-r.pdf')[1].get_pixmap(dpi=80).save('/tmp/cat/a300.png')
