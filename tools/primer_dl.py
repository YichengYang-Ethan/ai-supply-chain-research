#!/usr/bin/env python3
"""Download institutional images referenced by primer_XX.json into figs_primer/.
Enforces: NO semianalysis.com / substackcdn.com URLs (site+repo disclaimer promise).
Returns {url: relpath} map. Normalizes to JPEG via sips."""
import os, json, hashlib, subprocess, glob

BASE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(BASE, "figs_primer")
BANNED = ("semianalysis.com", "substackcdn.com")

def _clean(u): return str(u or "").strip().strip("()").rstrip("\\").strip()

def download_module_images(mod):
    os.makedirs(FIGDIR, exist_ok=True)
    m = {}
    for im in mod.get("images", []) or []:
        u = _clean(im.get("url"))
        if not u.startswith("http"): continue
        if any(b in u for b in BANNED):
            print(f"  REJECTED (banned domain): {u[:80]}"); continue
        h = hashlib.md5(u.encode()).hexdigest()[:10]
        path = os.path.join(FIGDIR, f"inst_{mod['module_id']}_{h}.jpg")
        rel = f"figs_primer/inst_{mod['module_id']}_{h}.jpg"
        if not os.path.exists(path):
            subprocess.run(["curl","-sL","--max-time","40","-A","Mozilla/5.0","-o",path,u], capture_output=True)
            if os.path.exists(path) and os.path.getsize(path) > 8000:
                r = subprocess.run(["sips","-s","format","jpeg",path,"--out",path], capture_output=True)
                if r.returncode != 0:
                    os.remove(path); continue
            elif os.path.exists(path):
                os.remove(path); continue
        if os.path.exists(path) and os.path.getsize(path) > 8000:
            m[u] = rel
    return m

def load_modules():
    mods = []
    for f in sorted(glob.glob(os.path.join(BASE, "primer_*.json"))):
        try: mods.append(json.load(open(f)))
        except Exception as e: print("BAD", f, e)
    return mods

if __name__ == "__main__":
    total = ok = 0
    for mod in load_modules():
        m = download_module_images(mod)
        n = len(mod.get("images", []) or [])
        total += n; ok += len(m)
        print(f"pm{mod['module_id']}: {len(m)}/{n} images downloaded")
    print(f"TOTAL {ok}/{total}")
