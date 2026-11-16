from pathlib import Path
import json
p=Path('/mnt/data')
faces=(p/'maquete_geometry.json').read_text()
html=r'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Maquete 3D | Sistema Ferroviário de Cargas</title>
<style>
:root{color-scheme:dark;--bg:#080e1b;--panel:#111b2d;--line:#26344b;--text:#eaf3fb;--muted:#9aaec2;--cyan:#2ad3de;--yellow:#ffcf58}
*{box-sizing:border-box}body{margin:0;min-height:100vh;background:var(--bg);color:var(--text);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
header{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:19px clamp(18px,4.5vw,74px);border-bottom:1px solid #1b2a41;background:#0d1727}
.brand{display:flex;align-items:center;gap:14px}.brand-icon{display:grid;place-items:center;width:48px;height:48px;border:1px solid #2b8ca1;border-radius:13px;background:#143444;color:#56e6ef}
.eyebrow{font-size:11px;letter-spacing:2.2px;text-transform:uppercase;font-weight:750;color:var(--cyan)}h1{font-size:clamp(18px,2.1vw,27px);letter-spacing:-.7px;margin:4px 0 1px;line-height:1.25}.subheader{color:var(--muted);font-size:12px;margin-top:4px}
.header-status{font-size:12px;color:#c7d6e6;border:1px solid #344358;border-radius:999px;padding:9px 13px;white-space:nowrap}.header-status b{color:#8af5d0}
main{display:grid;grid-template-columns:minmax(0,1fr) 314px;gap:20px;padding:22px clamp(18px,4.5vw,74px);max-width:1840px;margin:0 auto}
.viewer-shell{border:1px solid #26364b;background:#0e1d30;border-radius:18px;min-width:0;overflow:hidden;box-shadow:0 22px 72px #03060e60}
.viewer-top{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;padding:15px 18px;border-bottom:1px solid #233149;background:#111f34}.viewer-heading{font-size:14px;font-weight:750}.viewer-caption{font-size:12px;color:var(--muted);margin-top:2px}
.view-actions{display:flex;gap:6px;align-items:center;flex-wrap:wrap}button,.download{border:1px solid #354860;border-radius:9px;background:#192b43;color:#d7e5f1;padding:9px 11px;font:600 12px inherit;cursor:pointer;transition:background .15s,border-color .15s}button{font-family:inherit;font-size:12px;font-weight:650}button:hover,.download:hover{background:#24405e;border-color:#55b0c4}button.active{background:#14596b;border-color:#3fb6c7;color:#e3fdff}
#stage{height:clamp(440px,57vw,690px);position:relative;overflow:hidden;background:radial-gradient(ellipse at 45% 35%,#213d57 0%,#152b43 38%,#0d1a2d 85%);cursor:grab;touch-action:none}#stage.dragging{cursor:grabbing}
#world{display:block;width:100%;height:100%}.stage-hint{pointer-events:none;position:absolute;bottom:17px;left:18px;border:1px solid #ffffff1f;background:#0d1b2acb;backdrop-filter:blur(7px);border-radius:11px;padding:9px 12px;color:#ccdae7;font-size:11px}.stage-hint span{color:#78e6e5}
.marker{position:absolute;pointer-events:none;transform:translate(-50%,-50%);min-width:30px;height:30px;border-radius:50%;border:2px solid #e8fafe;background:#186c86;box-shadow:0 0 0 4px #0b273a9e,0 6px 18px #001322;display:grid;place-items:center;font-size:13px;font-weight:900;color:white;transition:background .18s;z-index:2}
.marker.selected{background:#efae32;color:#1d2633;border-color:#fff7cf;box-shadow:0 0 0 5px #dba43a42,0 0 19px #ffc35266}.stage-gradient{position:absolute;inset:0;pointer-events:none;background:linear-gradient(to top,#0b142c49,transparent 28%)}
.bottom{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;padding:13px 18px;background:#101e31;border-top:1px solid #25364e;font-size:11px;color:#aabed0}.key{display:flex;gap:13px;flex-wrap:wrap}.swatch{display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:5px}
aside{display:flex;flex-direction:column;gap:16px;min-width:0}.side-card{background:#111b2d;border:1px solid #26364b;border-radius:16px;padding:18px}.side-top{font-size:11px;letter-spacing:1.5px;color:var(--cyan);font-weight:800;text-transform:uppercase}.side-title{font-size:19px;margin:5px 0 8px;font-weight:800;letter-spacing:-.3px}.side-text{font-size:12.5px;color:var(--muted);line-height:1.65;margin:0 0 13px}
.flow-list{display:grid;gap:8px}.step{width:100%;display:flex;gap:12px;text-align:left;padding:12px;background:#18253a;border:1px solid #304159;border-radius:11px}.step:hover{background:#22334b}.step.active{background:#173b47;border-color:#3ecbd6}.step-num{display:grid;place-items:center;flex:0 0 30px;height:30px;background:#2c4c64;color:#a8eff4;font-size:13px;border-radius:9px}.step.active .step-num{background:#2ed0da;color:#073244}.step-title{font-size:12.5px;font-weight:750;line-height:1.3}.step-info{font-size:11px;color:#9fb2c9;margin-top:5px;line-height:1.45}
.action-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.download{display:block;text-decoration:none;text-align:center;font-size:11.5px;padding:12px 6px}
.note{font-size:11px;color:#91a5b7;line-height:1.6;margin:10px 0 0}footer{text-align:center;font-size:11px;color:#8194a9;padding:8px 20px 22px}
@media(max-width:1100px){main{grid-template-columns:1fr}aside{display:grid;grid-template-columns:1.5fr 1fr}.side-card:nth-child(1){grid-row:span 2}}@media(max-width:650px){header{align-items:flex-start}.header-status{display:none}main{padding:12px;gap:12px}aside{display:flex}#stage{height:430px}.viewer-top{padding:12px}.view-actions{justify-content:flex-start}.brand-icon{width:40px;height:40px}.bottom{padding:10px 12px}}
</style>
</head>
<body>
<header>
 <div class="brand"><div class="brand-icon" aria-hidden="true"><svg width="28" height="28" viewBox="0 0 32 32" fill="none"><path d="M8 3v26M24 3v26M8 8h16M8 16h16M8 24h16" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/></svg></div><div><div class="eyebrow">Projeto TCC • Maquete tridimensional</div><h1>Sistema Ferroviário de Cargas</h1><div class="subheader">Transporte, armazenagem e distribuição logística integrada</div></div></div>
 <div class="header-status"><b>●</b> Modelo 3D interativo · Funciona offline</div>
</header>
<main>
 <section class="viewer-shell" aria-label="Visualizador de maquete tridimensional">
  <div class="viewer-top"><div><div class="viewer-heading">Visão geral do terminal ferroviário</div><div class="viewer-caption">Explore livremente: rotacione, amplie e observe cada etapa.</div></div><div class="view-actions"><button id="iso" class="active">◈ Isométrica</button><button id="top">▦ Vista superior</button><button id="flow">▶ Animar fluxo</button><button id="reset">↺ Reiniciar</button></div></div>
  <div id="stage"><canvas id="world" aria-label="Maquete 3D giratória do sistema ferroviário"></canvas><div class="stage-gradient"></div>
   <div class="marker" id="m1">1</div><div class="marker" id="m2">2</div><div class="marker" id="m3">3</div><div class="marker" id="m4">4</div><div class="marker" id="m5">5</div>
   <div class="stage-hint"><span>Arrastar</span> para girar &nbsp;·&nbsp; <span>Roda do mouse</span> para ampliar</div>
  </div>
  <div class="bottom"><div class="key"><span><i class="swatch" style="background:#f6c94d"></i>Guindaste</span><span><i class="swatch" style="background:#2588d4"></i>Ferrovia</span><span><i class="swatch" style="background:#ed9444"></i>Contêineres</span><span><i class="swatch" style="background:#59a58a"></i>Armazenagem</span></div><span id="zoomText">Zoom: 100%</span></div>
 </section>
 <aside>
  <div class="side-card"><div class="side-top">Cadeia logística</div><h2 class="side-title">5 etapas do sistema</h2><p class="side-text">Uma maquete didática que demonstra como a ferrovia se conecta ao armazenamento e ao transporte rodoviário.</p>
   <div class="flow-list">
    <button class="step active" data-step="1"><span class="step-num">01</span><span><div class="step-title">Origem das mercadorias</div><div class="step-info">Silos e unidades de armazenamento recebem a produção.</div></span></button>
    <button class="step" data-step="2"><span class="step-num">02</span><span><div class="step-title">Centro de distribuição</div><div class="step-info">Estoque, conferência e preparação para despacho.</div></span></button>
    <button class="step" data-step="3"><span class="step-num">03</span><span><div class="step-title">Terminal intermodal</div><div class="step-info">Guindaste transfere contêineres entre áreas de carga e vagões.</div></span></button>
    <button class="step" data-step="4"><span class="step-num">04</span><span><div class="step-title">Transporte ferroviário</div><div class="step-info">Locomotiva, vagões, trilhos, desvios e sinalização.</div></span></button>
    <button class="step" data-step="5"><span class="step-num">05</span><span><div class="step-title">Distribuição rodoviária</div><div class="step-info">Caminhões e vans completam a entrega ao destino.</div></span></button>
   </div>
  </div>
  <div class="side-card"><div class="side-top">Arquivos do projeto</div><h2 class="side-title" style="font-size:16px">Use a maquete no TCC</h2><p class="side-text">Os arquivos do modelo 3D podem ser abertos em programas como Blender e outros visualizadores 3D.</p>
   <div class="action-grid"><a class="download" href="maquete_sistema_ferroviario.glb" download>↓ Modelo .GLB</a><a class="download" href="maquete_sistema_ferroviario.obj" download>↓ Modelo .OBJ</a></div>
   <p class="note">Os botões de download funcionam quando o HTML e os arquivos 3D estão na mesma pasta. Modelo conceitual, sem escala de engenharia.</p>
  </div>
 </aside>
</main>
<footer>Projeto demonstrativo de logística ferroviária para apresentação acadêmica • Geometria original gerada especialmente para esta maquete</footer>
<script>
'use strict';
const faces=__GEOMETRY__;
const canvas=document.getElementById('world'), stage=document.getElementById('stage');
const ctx=canvas.getContext('2d',{alpha:true}),buffer=document.createElement('canvas'),g=buffer.getContext('2d',{alpha:true});
const marks=[null,[-55,31,24],[-5,31,15],[-8,-21,23],[22,-22.5,14],[59,26,13]];
let yaw=-.86,elev=.80,zoom=1,selected=1,isFlow=false,lastFrame=0,drag=false,lx=0,ly=0,w=1000,h=680,dpr=1,dirty=true;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function camera(){const a=Math.cos(elev),b=Math.sin(elev),cy=Math.cos(yaw),sy=Math.sin(yaw);return {cx:a*cy,cy:a*sy,cz:b,rx:-sy,ry:cy,ux:-b*cy,uy:-b*sy,uz:a,sc:Math.min(w/187,h/128)*zoom}}
function project(x,y,z,c){const dz=z-4;return [w*.50+(x*c.rx+y*c.ry)*c.sc,h*.54-(x*c.ux+y*c.uy+dz*c.uz)*c.sc]}
function resize(){const r=stage.getBoundingClientRect();w=Math.max(300,Math.round(r.width));h=Math.max(300,Math.round(r.height));dpr=1;canvas.width=buffer.width=Math.round(w*dpr);canvas.height=buffer.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);g.setTransform(dpr,0,0,dpr,0,0);dirty=true;requestDraw()}
let pending=false;
function requestDraw(){if(pending)return;pending=true;requestAnimationFrame(draw)}
function drawStatic(c){
 // Software z-buffer: real visibility per pixel, no reliance on painter-order,
 // so it also works in browsers where hardware WebGL is disabled.
 g.setTransform(1,0,0,1,0,0);
 const img=g.createImageData(w,h), pixels=img.data;
 const depth=new Float32Array(w*h);depth.fill(-1e6);
 const light=[.38,-.49,.78];
 for(let j=0;j<faces.length;j++){
  const f=faces[j];
  const abx=f[3]-f[0],aby=f[4]-f[1],abz=f[5]-f[2],acx=f[6]-f[0],acy=f[7]-f[1],acz=f[8]-f[2];
  const nx=aby*acz-abz*acy,ny=abz*acx-abx*acz,nz=abx*acy-aby*acx;
  if(nx*c.cx+ny*c.cy+nz*c.cz<=.0001)continue;
  const p1=project(f[0],f[1],f[2],c),p2=project(f[3],f[4],f[5],c),p3=project(f[6],f[7],f[8],c);
  const x1=p1[0],y1=p1[1],x2=p2[0],y2=p2[1],x3=p3[0],y3=p3[1];
  const minx=Math.max(0,Math.floor(Math.min(x1,x2,x3))),maxx=Math.min(w-1,Math.ceil(Math.max(x1,x2,x3)));
  const miny=Math.max(0,Math.floor(Math.min(y1,y2,y3))),maxy=Math.min(h-1,Math.ceil(Math.max(y1,y2,y3)));
  if(minx>maxx||miny>maxy)continue;
  const den=(y2-y3)*(x1-x3)+(x3-x2)*(y1-y3);
  if(Math.abs(den)<.000001)continue;
  const inv=1/den;
  const waX=(y2-y3)*inv,waY=(x3-x2)*inv;
  const wbX=(y3-y1)*inv,wbY=(x1-x3)*inv;
  const da=f[0]*c.cx+f[1]*c.cy+f[2]*c.cz;
  const db=f[3]*c.cx+f[4]*c.cy+f[5]*c.cz;
  const dc=f[6]*c.cx+f[7]*c.cy+f[8]*c.cz;
  const norm=Math.sqrt(nx*nx+ny*ny+nz*nz)||1;
  const shade=clamp(.77+.23*(nx*light[0]+ny*light[1]+nz*light[2])/norm,.56,1.08);
  const red=Math.min(255,Math.round(f[9]*shade)),green=Math.min(255,Math.round(f[10]*shade)),blue=Math.min(255,Math.round(f[11]*shade));
  const px0=minx+.5,py0=miny+.5;
  let rowA=((y2-y3)*(px0-x3)+(x3-x2)*(py0-y3))*inv;
  let rowB=((y3-y1)*(px0-x3)+(x1-x3)*(py0-y3))*inv;
  for(let py=miny;py<=maxy;py++){
    let aa=rowA,bb=rowB;let idx=py*w+minx;
    for(let px=minx;px<=maxx;px++,idx++){
     if(aa>=-.00001&&bb>=-.00001&&aa+bb<=1.00001){
       const dep=dc+(da-dc)*aa+(db-dc)*bb;
       if(dep>depth[idx]+.0001){
        depth[idx]=dep;const o=idx*4;pixels[o]=red;pixels[o+1]=green;pixels[o+2]=blue;pixels[o+3]=255;
       }
     }
     aa+=waX;bb+=wbX;
    }
    rowA+=waY;rowB+=wbY;
  }
 }
 g.putImageData(img,0,0);
}
function overlay(c,t){
 const p=project(...marks[selected],c);const pulse=1+.10*Math.sin(t/280);
 ctx.save();ctx.strokeStyle='rgba(255,204,75,.9)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(p[0],p[1],20*pulse,0,Math.PI*2);ctx.stroke();ctx.restore();
 if(isFlow){
  const routes=[{x1:-61,x2:67,y:-22.5,z:12.5,col:'#fed169',reverse:false},{x1:62,x2:-63,y:11,z:2.1,col:'#2adee0',reverse:false}];
  routes.forEach((r)=>{for(let k=0;k<6;k++){
   let frac=((t*.000055+k/6)%1);let xx=r.x1+(r.x2-r.x1)*frac;const q=project(xx,r.y,r.z,c);
   ctx.beginPath();ctx.arc(q[0],q[1],Math.max(2,3.4*zoom),0,Math.PI*2);ctx.fillStyle=r.col;ctx.shadowColor=r.col;ctx.shadowBlur=11;ctx.fill();ctx.shadowBlur=0;
  }});
 }
}
function updateMarkers(c){for(let i=1;i<=5;i++){
 const p=project(...marks[i],c);const el=document.getElementById('m'+i);el.style.left=p[0]+'px';el.style.top=p[1]+'px';el.classList.toggle('selected',i===selected);
}}
function draw(t=0){pending=false;const c=camera();if(dirty){drawStatic(c);dirty=false;updateMarkers(c)}ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);ctx.drawImage(buffer,0,0,w,h);overlay(c,t);if(isFlow||selected) {if(isFlow)requestAnimationFrame(draw);}}
function redraw(){dirty=true;requestDraw()}
function setSelected(n){selected=n;document.querySelectorAll('.step').forEach(el=>el.classList.toggle('active',+el.dataset.step===n));requestDraw()}
document.querySelectorAll('.step').forEach(b=>b.addEventListener('click',()=>setSelected(+b.dataset.step)));
function mode(which){const top=which==='top';yaw=top?-Math.PI/2:-.86;elev=top?1.55:.80;document.getElementById('iso').classList.toggle('active',!top);document.getElementById('top').classList.toggle('active',top);redraw()}
document.getElementById('iso').onclick=()=>mode('iso');document.getElementById('top').onclick=()=>mode('top');
document.getElementById('reset').onclick=()=>{zoom=1;document.getElementById('zoomText').textContent='Zoom: 100%';setSelected(1);mode('iso')};
document.getElementById('flow').onclick=function(){isFlow=!isFlow;this.classList.toggle('active',isFlow);this.textContent=isFlow?'Ⅱ Pausar fluxo':'▶ Animar fluxo';requestDraw()};
stage.addEventListener('pointerdown',e=>{if(e.target!==canvas&&e.target!==stage)return;drag=true;lx=e.clientX;ly=e.clientY;stage.classList.add('dragging');stage.setPointerCapture(e.pointerId)});
stage.addEventListener('pointermove',e=>{if(!drag)return;let dx=e.clientX-lx,dy=e.clientY-ly;lx=e.clientX;ly=e.clientY;yaw+=dx*.006;elev=clamp(elev+dy*.005,.13,1.56);redraw()});
function release(){drag=false;stage.classList.remove('dragging')}stage.addEventListener('pointerup',release);stage.addEventListener('pointercancel',release);
stage.addEventListener('wheel',e=>{e.preventDefault();zoom=clamp(zoom*(e.deltaY>0?.90:1.10),.6,2.2);document.getElementById('zoomText').textContent='Zoom: '+Math.round(zoom*100)+'%';redraw()},{passive:false});
window.addEventListener('resize',resize);
resize();
</script>
</body></html>'''
html=html.replace('__GEOMETRY__',faces)
(p/'maquete_ferroviaria_interativa.html').write_text(html,encoding='utf-8')
print('HTML file MB',round((p/'maquete_ferroviaria_interativa.html').stat().st_size/1e6,2))
