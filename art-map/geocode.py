import json, re, time, urllib.parse, urllib.request, pathlib, random
html=pathlib.Path("art-map/index.html").read_text(encoding="utf-8")
m=re.search(r"const spaces=(\[.*?\]);const map=",html)
if not m: raise RuntimeError("Could not read gallery data")
spaces=json.loads(m.group(1))
out=pathlib.Path("art-map/coordinates.json")
existing=json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
for s in spaces:
    addr=s.get("address","").strip()
    if not addr or addr in existing: continue
    q=urllib.parse.urlencode({"q":addr,"format":"json","limit":1,"countrycodes":"kr"})
    req=urllib.request.Request("https://nominatim.openstreetmap.org/search?"+q,headers={"User-Agent":"SeoulArtArchiveMap/1.0 (https://github.com/chaeyunlee0612/leechaeyun)","Accept":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=18) as resp: data=json.load(resp)
        if data: existing[addr]={"lat":float(data[0]["lat"]),"lon":float(data[0]["lon"])}
        else: print("No results:",s["name"],addr)
    except Exception as e: print("Geocoding failed:",s["name"],repr(e))
    out.write_text(json.dumps(existing,ensure_ascii=False,indent=2),encoding="utf-8")
    time.sleep(1.2)
print("Locations saved:",len(existing),"of",len([s for s in spaces if s.get("address")]))
