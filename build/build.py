import base64, json, os, sys
template, outdir = sys.argv[1], sys.argv[2]
home=os.path.expanduser("~"); root=os.path.join(home,"Code/MikeyChess")
with open(template,"r",encoding="utf-8") as f: html=f.read()
def b64file(p):
    with open(p,"rb") as f: return base64.b64encode(f.read()).decode("ascii")
chess_b64=b64file(os.path.join(root,"build/chess.min.js"))
sf_b64   =b64file(os.path.join(root,"build/stockfish.asm.js"))
# piece sets -> {set:{code:dataURL}}
pieces={}
pdir=os.path.join(root,"build/pieces")
for st in sorted(os.listdir(pdir)):
    sp=os.path.join(pdir,st)
    if not os.path.isdir(sp): continue
    pieces[st]={}
    for fn in os.listdir(sp):
        if not fn.endswith(".svg"): continue
        code=fn[:-4]
        pieces[st][code]="data:image/svg+xml;base64,"+b64file(os.path.join(sp,fn))
pieces_b64=base64.b64encode(json.dumps(pieces,separators=(",",":")).encode("utf-8")).decode("ascii")
html=html.replace("/*__CHESS_JS_B64__*/", chess_b64, 1)
html=html.replace("/*__SF_ASM_B64__*/", sf_b64, 1)
html=html.replace("/*__PIECES_JSON__*/", pieces_b64, 1)
for marker in ("/*__CHESS_JS_B64__*/","/*__SF_ASM_B64__*/","/*__PIECES_JSON__*/"):
    assert marker not in html, "unreplaced: "+marker
assert "cdnjs" not in html and "jsdelivr" not in html and "raw.githubusercontent" not in html, "stray network ref"
for p in (os.path.join(root,"chess.html"), os.path.join(outdir,"chess.offline.html")):
    with open(p,"w",encoding="utf-8") as f: f.write(html)
print("built OK; sets:", list(pieces.keys()), "counts:", {k:len(v) for k,v in pieces.items()})
print("size bytes:", len(html.encode("utf-8")))
