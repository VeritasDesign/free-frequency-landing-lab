#!/usr/bin/env python3
"""Build the approved Astra static landing from the original publication package.
Never changes production or the original Floot project."""
import hashlib
import os
import pathlib
import urllib.request
import zipfile

ROOT=pathlib.Path("site")
ROOT.mkdir(exist_ok=True)
BASE="https://free-frequency-astra-landing.floot.app/_cdn/static/"
ZIP=BASE+"8d41a65a-92fe-4d25-bb56-6e1f5f8ed235-Free_Frequency_Landing_Publication_Candidate.zip"
HARDWARE=BASE+"5b4d9c29-78b8-43e1-ba8c-a0d16d2007d1-df914650a705bf9a53497250984f59795b5051ee126a2291d9f116b94e672469.png"
BETA_SHOWCASE="https://free-frequency-astra-landing.floot.app/_cdn/static/d36f4a25-dd28-414b-84ab-efe3e8bf4eda-listing-agent-beta-showcase.webp"
PREFIX="Free_Frequency_Landing_Refinement_02/prototype/"
EXPECTED={"free-frequency-mark.svg":1288,"frequency-approved.svg":13768,"frequency-material.webp":86108,"pirate-wall.webp":454784,"workshop-original.webp":30820,"workshop-wall.webp":473876}
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"FreeFrequency-Landing-Liberation/1.0"})
    with urllib.request.urlopen(req,timeout=75) as r:return r.read()
package=fetch(ZIP)
(pathlib.Path("source-package.sha256")).write_text(hashlib.sha256(package).hexdigest()+"  original-publication.zip\n")
with zipfile.ZipFile(__import__("io").BytesIO(package)) as z:
    for name,size in EXPECTED.items():
        data=z.read(PREFIX+name)
        if len(data)!=size:raise RuntimeError(f"Original asset mismatch {name}: {len(data)} != {size}")
        (ROOT/name).write_bytes(data)
    html=z.read(PREFIX+"index.html").decode("utf-8")
# Apply the same approved changes visible in the Astra project's current wrapper.
hardware=fetch(HARDWARE)
if len(hardware)!=2516329:raise RuntimeError("Approved hardware artwork size mismatch")
(ROOT/"frequency-hardware-approved.png").write_bytes(hardware)
beta_showcase=fetch(BETA_SHOWCASE)
if len(beta_showcase)!=48182:raise RuntimeError("Listing Agent beta showcase size mismatch")
(ROOT/"listing-agent-beta-showcase.webp").write_bytes(beta_showcase)
old="frequency:['frequency-material.webp','Unbranded graphite and brushed metal architectural material study']"
new="frequency:['frequency-hardware-approved.png','Brushed-metal FREQUENCY hardware with illuminated status light']"
if html.count(old)!=1:raise RuntimeError("Expected original frequency scene not found")
html=html.replace(old,new)
desktop='''/* AIR-REAL-002 desktop Frequency hero correction */
@media(min-width:761px){
 body[data-skin="frequency"] .heroArt #hero-scene{object-fit:contain;object-position:center;transform:none}
}'''
mobile='''/* Approved FREQ phone-only correction */\n@media(max-width:760px){\n body[data-skin="frequency"] nav{position:relative;top:auto;z-index:20;background:#111519}\n body[data-skin="frequency"] .heroGrid{min-height:0;display:flex;flex-direction:column}\n body[data-skin="frequency"] .heroCopy{width:100%;padding:42px 0 22px}\n body[data-skin="frequency"] .heroArt{position:relative;inset:auto;width:100%;height:auto;min-height:0;overflow:visible;display:block}\n body[data-skin="frequency"] .heroArt #hero-scene{display:block;width:100%;height:auto;max-width:100%;aspect-ratio:1536 / 1024;object-fit:contain;object-position:center;opacity:1;filter:none}\n body[data-skin="frequency"] .heroArt:after{background:none}\n body[data-skin="frequency"] .artIndex{bottom:8px;right:8px}\n}'''
beta_css='''/* Listing Agent private-beta feature */
.betaFeature{margin:0 0 28px;border:1px solid var(--line);background:var(--card);display:grid;grid-template-columns:minmax(0,.92fr) minmax(320px,1.08fr);overflow:hidden}
.betaFeatureCopy{padding:34px;display:flex;flex-direction:column;justify-content:center}
.betaFeature .betaBadge{display:inline-flex;align-self:flex-start;padding:7px 10px;border:1px solid var(--accent);color:var(--accent);font:700 10px/1 monospace;letter-spacing:.12em;text-transform:uppercase;margin-bottom:18px}
.betaFeature h3{font-size:clamp(30px,4vw,54px);line-height:.98;margin:0 0 16px}
.betaFeature p{max-width:620px}
.betaFeatureMedia{background:#eef2ef;min-height:430px;display:flex;align-items:center;justify-content:center;padding:22px}
.betaFeatureMedia img{display:block;width:100%;height:auto;max-height:620px;object-fit:contain;filter:none}
.betaFeature .betaNote{font-size:12px;color:var(--muted);margin-top:14px}
@media(max-width:760px){.betaFeature{grid-template-columns:1fr}.betaFeatureCopy{padding:26px 22px}.betaFeatureMedia{min-height:0;padding:12px}.betaFeatureMedia img{max-height:none}}
'''
if html.count("</style>")!=1:raise RuntimeError("Unexpected style boundaries")
html=html.replace("</style>",beta_css+desktop+mobile+"</style>")
import re
html,n=re.subn(r'<img\s+class="heroApprovedMark"[^>]*>',"",html)
if n<1:raise RuntimeError("Oversized hero logo selector missing")
html=html.replace('href="/field-record.html"','href="https://shannon-bishop-basket.vercel.app/field-record.html"')
beta_feature='''<article class="betaFeature" aria-labelledby="listing-agent-beta-title"><div class="betaFeatureCopy"><div class="betaBadge">Private beta · now live</div><h3 id="listing-agent-beta-title">Listing Agent</h3><p><b>From photos to a listing you control.</b></p><p>Photograph what you are selling. Listing Agent identifies and groups items, helps organize the details, researches current asking prices, and walks you through review and preparation before anything goes live.</p><p>Built for the repetitive part of selling—photo organization, item details, price research and listing preparation—while keeping the seller in control of the final result.</p><div class="actions"><a class="btn primary" href="mailto:beta@frequencyengine.com?subject=Listing%20Agent%20Beta%20Access" aria-label="Request Listing Agent private beta access by email">REQUEST BETA ACCESS ↗</a></div><div class="betaNote">Private beta is now open to a small number of testers. Requests go to beta@frequencyengine.com.</div></div><div class="betaFeatureMedia"><img src="listing-agent-beta-showcase.webp" alt="Listing Agent private beta screens showing photo intake, item grouping, seller workspace and comparable-price research" width="900" height="1160"></div></article>'''
marker='<div class="grid toolGrid">'
if html.count(marker)!=1:raise RuntimeError("Public tools grid anchor missing")
html=html.replace(marker,beta_feature+marker)

old="document.querySelectorAll('.skinPicker button').forEach(button=>button.addEventListener('click',()=>{const skin=button.dataset.skin;"
new="try{const saved=localStorage.getItem('ff-landing-skin');if(saved&&identityScenes[saved]){document.body.dataset.skin=saved;const hero=document.getElementById('hero-scene');hero.src=identityScenes[saved][0];hero.alt=identityScenes[saved][1];document.querySelectorAll('.skinPicker button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.skin===saved)));}}catch(e){}document.querySelectorAll('.skinPicker button').forEach(button=>button.addEventListener('click',()=>{const skin=button.dataset.skin;try{localStorage.setItem('ff-landing-skin',skin)}catch(e){}"
if html.count(old)!=1:raise RuntimeError("Original identity switcher not found")
html=html.replace(old,new)
(ROOT/"index.html").write_text(html,encoding="utf-8")
for label in ("workshop","frequency","pirate"):
    if f"data-skin=\"{label}\"" not in html and f"{label}:[" not in html:raise RuntimeError("Missing identity "+label)
for name in list(EXPECTED)+["frequency-hardware-approved.png","listing-agent-beta-showcase.webp"]:
    if name not in html and name not in ("frequency-material.webp","workshop-original.webp"):raise RuntimeError("Asset not referenced: "+name)
print("PASS: eight image assets, Listing Agent private-beta feature, three identities, mobile patch, Field Record and saved identity")
for p in sorted(ROOT.iterdir()):print(p.name,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
