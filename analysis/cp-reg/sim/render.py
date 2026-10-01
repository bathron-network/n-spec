#!/usr/bin/env python3
"""Static, reproducible SVG/PNG charts and complete Markdown tables.

No browser, network, or extra package installation. Pillow is used for
the preview raster; SVG is the portable, lossless master.
"""
import csv
from html import escape
import json
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE/'results'
COLORS = {1.:'#2455a4',.7:'#00816e',.4:'#d58400',.2:'#b22a49'}


class Canvas:
    def __init__(self,w,h):
        self.w,self.h = w,h
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
                      '<rect width="100%" height="100%" fill="white"/>']
        self.im = Image.new('RGB',(w,h),'white')
        self.draw = ImageDraw.Draw(self.im)
    def line(self,pts,color,width=2,dashed=False):
        encoded = ' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)
        dash = ' stroke-dasharray="5 4"' if dashed else ''
        self.parts.append(f'<polyline points="{encoded}" fill="none" stroke="{color}" stroke-width="{width}"{dash}/>')
        if len(pts)>1:
            self.draw.line(pts,fill=color,width=width)
    def text(self,x,y,value,size=15,color='#253047'):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,sans-serif" font-size="{size}">{escape(str(value))}</text>')
        try:
            font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',size)
        except OSError:
            font = ImageFont.load_default()
        self.draw.text((x,y-size),str(value),fill=color,font=font)
    def circle(self,x,y,color,r=3):
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>')
        self.draw.ellipse((x-r,y-r,x+r,y+r),fill=color)
    def save(self,name):
        (OUT/f'{name}.svg').write_text('\n'.join(self.parts+['</svg>'])+'\n')
        self.im.save(OUT/f'{name}.png')


def panel(canvas,col,row,title,series,ymin=1e-4):
    left,top = 65+col*400,130+row*315
    width,height = 330,225
    xmin,xmax = math.log2(4),math.log2(7200)
    def xy(k,p):
        return (left+(math.log2(k)-xmin)/(xmax-xmin)*width,
                top+height*(math.log10(max(ymin,min(1.,p)))/math.log10(ymin)))
    canvas.text(left,top-16,title,17)
    for power in range(0,int(-math.log10(ymin))+1):
        y = xy(4,10**(-power))[1]
        canvas.line([(left,y),(left+width,y)],'#e1e5ec',1)
        canvas.text(left-44,y+5,f'1e-{power}',12)
    for k in (4,32,256,2048,7200):
        x = xy(k,1)[0]
        canvas.line([(x,top),(x,top+height)],'#edf0f5',1)
        canvas.text(x-10,top+height+20,str(k),12)
    for color,rows,dashed in series:
        pts = [xy(float(r['k']),float(r['estimate'])) for r in rows if float(r['estimate'])>0]
        canvas.line(pts,color,2,dashed)
        for r in rows:
            k,p = float(r['k']),float(r['estimate'])
            lo,hi = float(r['ci95_low']),float(r['ci95_high'])
            x,y = xy(k,p if p else float(r.get('zero_events_exact_upper95') or hi))
            if p:
                canvas.line([xy(k,lo),xy(k,hi)],color,1)
                canvas.circle(x,y,color,2)
            else:
                # Down arrow at the one-sided exact 95% upper limit.
                canvas.line([(x,y-4),(x,y+4),(x-3,y+1),(x,y+4),(x+3,y+1)],color,1)
    canvas.text(left+100,top+height+43,'K (créneaux, échelle log)',12)


def main():
    curves = list(csv.DictReader((OUT/'mc-curves.csv').open()))
    beta_grid=(.1,.2,.25,.3)
    delays=(0.,.5,1.,2.)
    for kind,title,name in (
        ('constructive_age','Attaque constructive : P[âge maximal de divergence ≥ K]','epsilon-attack'),
        ('envelope_gap','Enveloppe : P[intervalle maximal sans barrière ≥ K]','epsilon-envelope')):
        c = Canvas(1660,1450)
        c.text(35,35,title,26)
        c.text(35,62,'4 096 essais / case ; horizon 14 400 ; IC Wilson 95 % ponctuels ; flèche : zéro événement, borne exacte unilatérale.',15)
        for i,(u,color) in enumerate(COLORS.items()):
            c.text(80+300*i,88,f'u = {u:g}',17,color)
        for ri,beta in enumerate(beta_grid):
            for ci,delay in enumerate(delays):
                series=[]
                for u,color in COLORS.items():
                    rows=[r for r in curves if r['kind']==kind and float(r['beta'])==beta and
                          float(r['delay'])==delay and float(r['u'])==u]
                    series.append((color,rows,False))
                panel(c,ci,ri,f'β={beta:g} ; Δ/τ={delay:g}',series)
        c.text(35,1420,'Ces fréquences ne sont pas des bornes de sécurité N. Les cases Δ/τ=0 et 0,5 utilisent les mêmes calendriers.',15)
        c.save(name)
    if (OUT/'closure-calibration.csv').exists():
        closure=list(csv.DictReader((OUT/'closure-calibration.csv').open()))
        c=Canvas(1660,470)
        c.text(35,35,'Divergence de D_e par abstention calibrée et fermeture tardive (scénario conditionnel)',24)
        c.text(35,62,'1 000 000 essais / (β,u) ; b=2 880 ; maturité à start(e)−1 ; livraison instantanée autorisée pour les quatre Δ.',15)
        for i,(u,color) in enumerate(COLORS.items()):
            c.text(80+300*i,88,f'u = {u:g}',17,color)
        for ci,beta in enumerate(beta_grid):
            series=[(color,[r for r in closure if float(r['beta'])==beta and float(r['u'])==u],False)
                    for u,color in COLORS.items()]
            panel(c,ci,0,f'β={beta:g}',series,1e-6)
        c.text(35,457,'La probabilité de ce scénario Bitcoin et de son histoire initiale n’est pas incluse. Aucun risque inconditionnel de N n’est déduit.',15)
        c.save('epsilon-closure')
    derivation=list(csv.DictReader((OUT/'derivation.csv').open()))
    lines=['# Table complète — auteur 1','',
           'Valeurs **conditionnelles**, Q=1, horizon observé 14 400 ; horizon total augmenté du recul calculé. N v0.6 : UNKNOWN dans toutes les cases.',
           '', 'Chaque cellule : **K_reg en créneaux / b en blocs**. K utilise la marge historique candidate G=6 000 créneaux (τ=6 s). Le CSV donne aussi G=0, le temps, le risque recomposé et Q=256.',
           '', '| β | u | h=(1−β)u | Δ/τ | ε=10⁻⁶ | ε=10⁻⁹ | ε=10⁻¹² |',
           '|---:|---:|---:|---:|---:|---:|---:|']
    for beta in beta_grid:
        for u in COLORS:
            for delay in delays:
                vals=[]
                for eps in (1e-6,1e-9,1e-12):
                    r=next(r for r in derivation if float(r['beta'])==beta and float(r['u'])==u and
                           float(r['delay'])==delay and float(r['epsilon'])==eps and r['q_paths']=='1')
                    if r['conditional_status']=='CONDITIONAL':
                        vals.append(f"{int(r['K_reg_slots_guard6000']):,} / {int(r['registry_min_blocks_conditional']):,}".replace(',',' '))
                    else:
                        vals.append('NC-dérive' if r['reason']=='NO_HONEST_DRIFT' else 'NC-délai')
                lines.append(f'| {beta:g} | {u:g} | {(1-beta)*u:g} | {delay:g} | '+ ' | '.join(vals)+' |')
    lines += ['', 'NC-dérive : h≤β ; la course privée ne possède plus de dérive honnête positive. NC-délai : cette réduction conservatrice échoue ; cela ne prouve pas une attaque contre toutes les exécutions. Aucun « ∞ » de protocole n’est inféré de la seule absence de certificat.',
              '', 'La croissance convertit les créneaux en blocs avec une probabilité propre. K_reg×densité observée n’est pas une conversion garantie.']
    (OUT/'TABLE-DERIVATION.md').write_text('\n'.join(lines)+'\n')
    campaign=json.loads((OUT/'campaign.json').read_text())
    lines=['# Monte-Carlo — 64 cases','',
           'Quantiles empiriques ; les IC ponctuels des probabilités se trouvent dans mc-curves.csv. q99 n’est pas une garantie à 99 % hors modèle.',
           '', '| β | u | Δ/τ | croissance publique / créneau | âge q99 | déconnexions q99 | déconnexions max |',
           '|---:|---:|---:|---:|---:|---:|---:|']
    for r in campaign['summaries']:
        p=r['parameters']
        lines.append(f"| {p['beta']:g} | {p['u']:g} | {p['delay']:g} | {r['mean_public_growth']:.4f} | {r['max_age_quantiles'][3]:.2f} | {r['max_blocks_quantiles'][3]:.2f} | {r['max_blocks_quantiles'][4]:.0f} |")
    (OUT/'TABLE-MONTE-CARLO.md').write_text('\n'.join(lines)+'\n')
    # XML and row coverage are part of generation, not a visual substitute.
    import xml.etree.ElementTree as ET
    for path in OUT.glob('*.svg'):
        ET.parse(path)
    assert len(derivation)==384 and len(campaign['summaries'])==64
    print('Rendered charts and complete tables.')


if __name__=='__main__':
    main()
