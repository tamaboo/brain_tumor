import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote
from navbar.kamus_bahasa import t

# =====================================================================
# Palet: putih + biru royal (#2F6BFF). Bentuk: sudut membulat, lingkaran,
# kotak miring, pola heksagon, angka outline besar.
# =====================================================================
def _h(s: str) -> str:
    return " ".join(line.strip() for line in s.strip().splitlines())


def html(s: str):
    st.markdown(_h(s), unsafe_allow_html=True)


def _hex_uri(opacity=0.10):
    hx = lambda x, y: (f"M{x+26} {y}L{x+52} {y+15}L{x+52} {y+45}L{x+26} {y+60}L{x} {y+45}L{x} {y+15}Z")
    d = " ".join([hx(0, 0), hx(26, 45), hx(-26, 45)])
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='52' height='90'><path d='{d}' fill='none' "
           f"stroke='#2F6BFF' stroke-opacity='{opacity}' stroke-width='1.2'/></svg>")
    return "data:image/svg+xml;utf8," + quote(svg)


HEX_BG, HEX_PANEL = _hex_uri(0.09), _hex_uri(0.16)


def inject_aos():
    """Tidak lagi memakai library AOS / JavaScript. Animasi muncul memakai CSS murni (lihat inject_css),
    sehingga konten tidak pernah tersembunyi walau komponen/iframe dibuat ulang."""
    return


def inject_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
    :root{--pri:#2F6BFF;--pri-d:#1F4FD6;--pri-l:#EAF0FF;--ink:#0B1B3A;--mute:#5E6C84;--line:#DCE5FA;--red:#D92D2D;
      --fx:'Plus Jakarta Sans',system-ui,sans-serif}
    .stApp{background:linear-gradient(180deg,rgba(47,107,255,.10),rgba(47,107,255,0) 480px),url("__HEX_BG__") #F1F5FF}
    [data-aos]{opacity:1;animation:nsRise .7s cubic-bezier(.2,.7,.2,1) both}
    [data-aos="zoom-in"]{animation-name:nsZoom}
    [data-aos-delay="100"]{animation-delay:.1s}[data-aos-delay="120"]{animation-delay:.12s}[data-aos-delay="200"]{animation-delay:.2s}[data-aos-delay="240"]{animation-delay:.24s}[data-aos-delay="300"]{animation-delay:.3s}
    @keyframes nsRise{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
    @keyframes nsZoom{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}
    @supports (animation-timeline:view()){[data-aos]{animation:nsRise linear both;animation-timeline:view();animation-range:entry 0% entry 40%}[data-aos="zoom-in"]{animation-name:nsZoom}}
    /* ---------- hero ---------- */
    .st-key-hero{position:relative;overflow:hidden;background:#fff;border-radius:32px;padding:2.2rem;
      border:1px solid #fff;box-shadow:0 24px 54px -26px rgba(47,107,255,.45)}
    .st-key-hero::before{content:"";position:absolute;left:-100px;top:-100px;width:300px;height:300px;border-radius:50%;
      background:radial-gradient(circle,rgba(47,107,255,.16),transparent 70%)}
    .st-key-hero::after{content:"";position:absolute;left:44%;bottom:-80px;width:210px;height:210px;border-radius:50%;
      border:28px solid rgba(47,107,255,.06)}
    .pill{display:inline-flex;align-items:center;gap:.5rem;padding:.35rem .9rem;border-radius:999px;background:var(--pri-l);
      color:var(--pri-d);font-size:.8rem;font-weight:700;margin-bottom:1.1rem}
    .pill::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--pri)}
    .hero-title{font:800 clamp(2.1rem,3.9vw,3.2rem)/1.1 var(--fx);letter-spacing:-.02em;color:var(--ink);margin:0 0 1rem}
    .hero-title .hl{color:var(--pri)}
    .hero-sub{font-size:1.05rem;color:var(--mute);line-height:1.75;max-width:32rem;margin:0}
    .chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.4rem}
    .chips span{padding:.4rem .9rem;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--ink);
      font-size:.82rem;font-weight:600;box-shadow:0 4px 10px -6px rgba(47,107,255,.35)}
    /* ---------- fakta ---------- */
    .facts{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.4rem 0 0}
    .fact{background:#fff;border-radius:22px;padding:1.2rem 1.3rem;border:1px solid var(--line);
      box-shadow:0 12px 30px -22px rgba(47,107,255,.5)}
    .fact .ic{width:46px;height:46px;border-radius:14px;background:var(--pri-l);display:flex;align-items:center;
      justify-content:center;margin-bottom:.8rem}
    .fact svg,.card .ic svg{width:22px;height:22px;stroke:var(--pri);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
    .fact b{display:block;font:800 1.3rem var(--fx);color:var(--pri);margin-bottom:.15rem}
    .fact span{color:var(--mute);font-size:.86rem;line-height:1.45}
    @media(max-width:900px){.facts{grid-template-columns:1fr 1fr}}
    /* ---------- panel heksagon ---------- */
    .panel{position:relative;overflow:hidden;margin-top:2.6rem;background:#fff url("__HEX_PANEL__");border-radius:32px;
      padding:3rem 2rem;text-align:center;border:1px solid var(--line);box-shadow:0 18px 44px -28px rgba(47,107,255,.5)}
    .panel .big{font:500 clamp(1.25rem,2.3vw,1.8rem)/1.55 var(--fx);color:var(--ink);max-width:48rem;margin:.9rem auto 0}
    .panel .big b{font-weight:800;color:var(--pri)}
    .eyebrow{display:inline-block;padding:.3rem .85rem;border-radius:999px;background:var(--pri-l);color:var(--pri-d);
      font-size:.78rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
    /* ---------- judul seksi ---------- */
    .sec{margin:3.2rem 0 1.3rem;display:flex;justify-content:space-between;align-items:flex-end;gap:2rem;flex-wrap:wrap}
    .sec .h2{font:800 clamp(1.6rem,2.6vw,2.1rem)/1.15 var(--fx);color:var(--ink);letter-spacing:-.01em}
    .sec .h2 small{font:600 .85rem var(--fx);color:var(--pri);margin-left:.4rem}
    .sec p{color:var(--mute);line-height:1.7;max-width:26rem;margin:0;font-size:.95rem}
    /* ---------- kartu ---------- */
    .card{position:relative;overflow:hidden;height:100%;background:#fff;border:1px solid var(--line);border-radius:24px;
      padding:1.5rem;box-shadow:0 12px 32px -22px rgba(47,107,255,.55);transition:transform .25s,box-shadow .25s,border-color .25s}
    .card:hover{transform:translateY(-6px);border-color:#BFD0FF;box-shadow:0 22px 44px -22px rgba(47,107,255,.6)}
    .card .big-no{position:absolute;right:18px;top:4px;font:800 4.4rem/1 var(--fx);color:transparent;
      -webkit-text-stroke:1.5px rgba(47,107,255,.22);pointer-events:none}
    .card .ic{width:46px;height:46px;border-radius:14px;background:var(--pri-l);display:flex;align-items:center;
      justify-content:center;margin-bottom:1rem}
    .card .tagp{display:inline-block;font-size:.72rem;font-weight:700;color:var(--pri-d);background:var(--pri-l);
      padding:.2rem .65rem;border-radius:999px;margin-bottom:.6rem}
    .card .h3{font:700 1.25rem var(--fx);color:var(--ink);margin:0 0 .5rem}
    .card p{margin:0;color:var(--mute);line-height:1.7;font-size:.95rem}
    /* ---------- panel biru XAI ---------- */
    .st-key-xai{position:relative;overflow:hidden;margin-top:3rem;background:linear-gradient(135deg,#2F6BFF 0%,#1F4FD6 100%);
      border-radius:32px;padding:2.4rem 2.2rem;box-shadow:0 28px 56px -26px rgba(31,79,214,.8)}
    .st-key-xai::before{content:"";position:absolute;right:-80px;top:-80px;width:280px;height:280px;border-radius:50%;
      border:36px solid rgba(255,255,255,.08)}
    .st-key-xai::after{content:"";position:absolute;left:-30px;bottom:-30px;width:130px;height:130px;border-radius:34px;
      background:rgba(255,255,255,.08);transform:rotate(20deg)}
    .xai-h .eyebrow{background:rgba(255,255,255,.18);color:#fff}
    .xai-h .h2{font:800 clamp(1.6rem,2.6vw,2.1rem)/1.15 var(--fx);color:#fff;margin:.8rem 0 .6rem}
    .xai-h p{color:rgba(255,255,255,.88);line-height:1.75;max-width:44rem;margin:0 0 1.4rem}
    .xai-h b{color:#fff}
    .legend{height:10px;border-radius:99px;margin:1.4rem 0 .35rem;max-width:32rem;
      background:linear-gradient(90deg,#2a5db0,#3aa6c8,#8fd16a,#f4d03f,#f08a2b,#d62828);box-shadow:0 0 0 3px rgba(255,255,255,.35)}
    .legend-l{display:flex;justify-content:space-between;max-width:32rem;color:rgba(255,255,255,.88);font-size:.8rem}
    /* ---------- catatan ---------- */
    .callout{display:flex;gap:1rem;align-items:flex-start;margin-top:2.4rem;padding:1.2rem 1.4rem;background:#fff;
      border:1px solid var(--line);border-radius:22px;color:var(--ink);line-height:1.7;font-size:.95rem;
      box-shadow:0 12px 30px -22px rgba(47,107,255,.5)}
    .callout .ic{flex:none;width:42px;height:42px;border-radius:13px;background:var(--pri);display:flex;align-items:center;justify-content:center}
    .callout svg{width:22px;height:22px;stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
    /* ---------- panduan ---------- */
    .banner{position:relative;overflow:hidden;background:linear-gradient(135deg,#2F6BFF,#1F4FD6);border-radius:32px;
      padding:2.8rem 2.4rem;margin-bottom:2.2rem;box-shadow:0 28px 56px -26px rgba(31,79,214,.8)}
    .banner::before{content:"";position:absolute;right:-70px;top:-70px;width:270px;height:270px;border-radius:50%;
      border:36px solid rgba(255,255,255,.09)}
    .banner::after{content:"";position:absolute;right:170px;bottom:-30px;width:96px;height:96px;border-radius:26px;
      background:rgba(255,255,255,.12);transform:rotate(18deg)}
    .banner .eyebrow{background:rgba(255,255,255,.18);color:#fff;margin-bottom:1rem}
    .banner .hero-title{color:#fff}.banner .hero-sub{color:rgba(255,255,255,.88)}
    .step{position:relative;display:flex;gap:1.2rem;margin-bottom:1.1rem;align-items:flex-start}
    .step:not(:last-child)::before{content:"";position:absolute;left:25px;top:4.4rem;bottom:-1.9rem;border-left:2px dashed #BFD0FF}
    .step .n{flex:none;width:52px;height:52px;border-radius:17px;background:linear-gradient(135deg,#2F6BFF,#1F4FD6);color:#fff;
      font:800 1.2rem var(--fx);display:flex;align-items:center;justify-content:center;margin-top:.9rem;
      box-shadow:0 10px 20px -8px rgba(47,107,255,.7)}
    .step .card{flex:1}
    .step code{background:var(--pri-l);color:var(--pri-d);padding:.05rem .45rem;border-radius:6px}
    .step ul{margin:.8rem 0 0;padding-left:1.1rem;color:var(--mute);line-height:1.8;font-size:.95rem}
    .demo{display:flex;gap:1rem;margin:1rem 0 .3rem;flex-wrap:wrap}
    .demo div{flex:1;min-width:150px;aspect-ratio:1.3;border-radius:16px;border:1px solid var(--line);display:flex;
      align-items:flex-end;padding:.6rem .8rem;font-size:.78rem;color:#e8eef5;
      background:radial-gradient(ellipse at 50% 45%,#8a94a0 0%,#4a535f 55%,#222831 100%)}
    .demo .heat{background:radial-gradient(circle at 66% 38%,rgba(214,40,40,.95) 0,rgba(240,138,43,.8) 12%,
      rgba(143,209,106,.35) 24%,transparent 38%),radial-gradient(ellipse at 50% 45%,#8a94a0 0%,#4a535f 55%,#222831 100%)}
    @media (prefers-reduced-motion:reduce){[data-aos]{animation:none!important}}
    </style>
    """
    html(css.replace("__HEX_BG__", HEX_BG).replace("__HEX_PANEL__", HEX_PANEL))


_BRAIN_HTML = r"""
<style>
  .b{font:600 12px system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.45);
     padding:6px 14px;border-radius:999px;cursor:pointer;transition:.15s}
  .b:hover{background:rgba(255,255,255,.3)}
  .b.on{background:#fff;color:#1F4FD6;border-color:#fff}
  .fp{position:absolute;pointer-events:none;background:#fff;color:#0B1B3A;font:600 12px system-ui,sans-serif;
      padding:6px 13px 6px 10px;border-radius:999px;box-shadow:0 8px 18px rgba(10,30,90,.28);animation:fl 5s ease-in-out infinite}
  .fp::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:#2F6BFF;margin-right:7px}
  @keyframes fl{50%{transform:translateY(-7px)}}
</style>
<div id="wrap" style="position:relative;width:100%;height:__H__px;border-radius:26px;overflow:hidden;
  background:radial-gradient(circle at 68% 22%,#5C8DFF 0%,#2F6BFF 46%,#1F4FD6 100%);border:none">
  <canvas id="c" style="width:100%;height:100%;display:block;cursor:grab;touch-action:none"></canvas>
  <div style="position:absolute;right:-70px;top:-70px;width:230px;height:230px;border-radius:50%;border:30px solid rgba(255,255,255,.09);pointer-events:none"></div>
  <div style="position:absolute;left:-45px;bottom:-45px;width:170px;height:170px;border-radius:50%;background:rgba(255,255,255,.08);pointer-events:none"></div>
  <div style="position:absolute;right:34px;bottom:96px;width:60px;height:60px;border-radius:18px;background:rgba(255,255,255,.14);transform:rotate(14deg);pointer-events:none"></div>
  <div class="fp" style="right:18px;top:64px">__P1__</div>
  <div class="fp" style="left:18px;bottom:62px;animation-delay:-1.6s">__P2__</div>
  <div class="fp" style="right:26px;bottom:150px;animation-delay:-3.2s">__P3__</div>
  <div style="position:absolute;left:14px;top:14px;display:flex;gap:6px;z-index:2">
    <button class="b on" data-m="anat">__L_ANAT__</button>
    <button class="b" data-m="heat">Grad-CAM</button>
    <button class="b" data-m="xray">X-ray</button>
  </div>
  <div id="lbl" style="position:absolute;left:0;top:0;pointer-events:none;font:600 12px system-ui,sans-serif;color:#14283C;transition:opacity .25s">
    <div style="position:absolute;left:0;top:0;width:34px;height:1px;background:#C62828;transform:rotate(-35deg);transform-origin:0 0"></div>
    <div style="position:absolute;left:30px;top:-34px;white-space:nowrap;background:#fff;border:1px solid #C62828;padding:3px 9px;border-radius:6px;box-shadow:0 2px 6px rgba(20,40,60,.12)">__L_LESION__</div>
  </div>
  <div style="position:absolute;left:14px;bottom:10px;font:12px system-ui,sans-serif;color:rgba(255,255,255,.88)">__L_HINT__</div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const wrap=document.getElementById('wrap'),cv=document.getElementById('c'),lbl=document.getElementById('lbl');
const renderer=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
const scene=new THREE.Scene();
const cam=new THREE.PerspectiveCamera(36,1,.1,50);cam.position.set(0,-.1,5.4);
scene.add(new THREE.HemisphereLight(0xffffff,0xb9c4d0,.95));
const key=new THREE.DirectionalLight(0xffffff,.9);key.position.set(3,4,5);scene.add(key);
const rim=new THREE.DirectionalLight(0xdfe8f3,.5);rim.position.set(-4,1,-4);scene.add(rim);

/* ---------- noise ---------- */
const hs=(x,y,z)=>{let h=Math.imul(x,374761393)^Math.imul(y,668265263)^Math.imul(z,1274126177);
  h=Math.imul(h^(h>>>13),1274126177);return((h^(h>>>16))>>>0)/4294967296;};
const lp=(a,b,t)=>a+(b-a)*t, cl=(x,a,b)=>Math.min(b,Math.max(a,x));
const sst=(a,b,x)=>{const t=cl((x-a)/(b-a),0,1);return t*t*(3-2*t);};
function vn(x,y,z){const xi=Math.floor(x),yi=Math.floor(y),zi=Math.floor(z);
  const f=t=>t*t*(3-2*t),xf=f(x-xi),yf=f(y-yi),zf=f(z-zi);
  return lp(lp(lp(hs(xi,yi,zi),hs(xi+1,yi,zi),xf),lp(hs(xi,yi+1,zi),hs(xi+1,yi+1,zi),xf),yf),
            lp(lp(hs(xi,yi,zi+1),hs(xi+1,yi,zi+1),xf),lp(hs(xi,yi+1,zi+1),hs(xi+1,yi+1,zi+1),xf),yf),zf);}

/* smooth normals across the sphere seam/poles */
function mergeN(g){g.computeVertexNormals();const p=g.attributes.position,n=g.attributes.normal,m={};
  for(let i=0;i<p.count;i++){const k=Math.round(p.getX(i)*1e4)+'_'+Math.round(p.getY(i)*1e4)+'_'+Math.round(p.getZ(i)*1e4);
    const a=m[k]||(m[k]=[0,0,0,[]]);a[0]+=n.getX(i);a[1]+=n.getY(i);a[2]+=n.getZ(i);a[3].push(i);}
  for(const k in m){const a=m[k],v=new THREE.Vector3(a[0],a[1],a[2]).normalize();a[3].forEach(i=>n.setXYZ(i,v.x,v.y,v.z));}}

/* ---------- cerebrum: lobes, fissures, gyri/sulci ---------- */
let G=0;
function cortex(d,out){
  let r=1;
  r-=.17*Math.exp(-Math.pow(d.x/.075,2))*sst(-.35,.45,d.y);                 // longitudinal fissure
  const s=d.x<0?-1:1,dx=d.x-s*.8,dy=d.y+.45,dz=d.z-.1;
  r+=.12*Math.exp(-(dx*dx+dy*dy+dz*dz)/.1);                                 // temporal lobes
  const q=d.y+.05-.28*d.z;
  r-=.07*Math.exp(-q*q/.005)*sst(.45,.75,Math.abs(d.x))*sst(-.3,.6,d.z);    // sylvian fissure
  const w=.55*(vn(d.x*3+9,d.y*3,d.z*3)-.5);
  const g1=1-sst(0,.2,Math.abs(2*vn(d.x*7+w,d.y*7+w,d.z*7+w+4)-1));          // main sulci
  const g2=1-sst(0,.16,Math.abs(2*vn(d.x*15+3,d.y*15,d.z*15+7)-1));          // fine sulci
  G=Math.max(g1,.55*g2);
  r+=.03*(vn(d.x*4,d.y*4+2,d.z*4)-.5)-.075*g1-.03*g2;
  const sy=.78-.26*sst(.1,-.5,d.y);                                         // flatter underside
  return out.set(d.x*r*.8,d.y*r*sy,d.z*r*1.12);
}
const brain=new THREE.Group();scene.add(brain);
const cg=new THREE.SphereGeometry(1,260,190),cp=cg.attributes.position,dv=new THREE.Vector3(),tmp=new THREE.Vector3();
const gr=new Float32Array(cp.count);
for(let i=0;i<cp.count;i++){dv.fromBufferAttribute(cp,i).normalize();cortex(dv,tmp);cp.setXYZ(i,tmp.x,tmp.y,tmp.z);gr[i]=G;}
mergeN(cg);

/* tumor location (right lateral surface) */
const dirT=new THREE.Vector3(.88,.32,.22).normalize(),P=cortex(dirT,new THREE.Vector3()),nrm=P.clone().normalize();
const TC=P.clone().multiplyScalar(.88);

/* vertex colours: anatomy + Grad-CAM heat */
const anat=new Float32Array(cp.count*3),heat=new Float32Array(cp.count*3);
const L=new THREE.Color(.94,.76,.72),D=new THREE.Color(.68,.44,.45),Y=new THREE.Color(1,.85,.2),R=new THREE.Color(1,.1,.1),c=new THREE.Color(),hc=new THREE.Color();
for(let i=0;i<cp.count;i++){
  c.copy(L).lerp(D,gr[i]*.9);anat.set([c.r,c.g,c.b],i*3);
  tmp.fromBufferAttribute(cp,i);const t=Math.exp(-tmp.distanceToSquared(P)/.07);
  hc.set(.15,.45,.9).lerp(Y,sst(.15,.5,t)).lerp(R,sst(.5,.95,t));
  c.lerp(hc,sst(.04,.3,t));heat.set([c.r,c.g,c.b],i*3);
}
const anatA=new THREE.BufferAttribute(anat,3),heatA=new THREE.BufferAttribute(heat,3);
cg.setAttribute('color',anatA);
const cMat=new THREE.MeshPhysicalMaterial({vertexColors:true,roughness:.5,clearcoat:.5,clearcoatRoughness:.35});
brain.add(new THREE.Mesh(cg,cMat));

/* cerebellum (striated) */
const bg=new THREE.SphereGeometry(1,120,80),bp=bg.attributes.position,bc=new Float32Array(bp.count*3);
for(let i=0;i<bp.count;i++){dv.fromBufferAttribute(bp,i).normalize();
  const s=Math.sin(dv.y*46+2*vn(dv.x*4,dv.y*2,dv.z*4)),r=1+.035*s;
  bp.setXYZ(i,dv.x*r*.62,dv.y*r*.32-.46,dv.z*r*.46-.8);
  const k=.88+.12*s;bc.set([.8*k,.5*k,.47*k],i*3);}
bg.setAttribute('color',new THREE.BufferAttribute(bc,3));mergeN(bg);
const bMat=new THREE.MeshStandardMaterial({vertexColors:true,roughness:.6});brain.add(new THREE.Mesh(bg,bMat));

/* brainstem */
const stem=new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(0,-.35,-.3),new THREE.Vector3(0,-.8,-.42),new THREE.Vector3(0,-1.2,-.5)]),32,.13,20);
const sMat=new THREE.MeshStandardMaterial({color:0xd9a89c,roughness:.6});brain.add(new THREE.Mesh(stem,sMat));

/* tumor mass + glow + ring */
const tg=new THREE.SphereGeometry(1,72,54),tp=tg.attributes.position;
for(let i=0;i<tp.count;i++){dv.fromBufferAttribute(tp,i).normalize();
  const r=(1+.28*(vn(dv.x*3+20,dv.y*3,dv.z*3)-.5)+.07*(vn(dv.x*9,dv.y*9,dv.z*9)-.5))*.21;tp.setXYZ(i,dv.x*r,dv.y*r,dv.z*r);}
mergeN(tg);
const tMat=new THREE.MeshStandardMaterial({color:0x6b1022,emissive:0xff2a1a,emissiveIntensity:.6,roughness:.55});
const tumor=new THREE.Mesh(tg,tMat);tumor.position.copy(TC);brain.add(tumor);
const gcv=document.createElement('canvas');gcv.width=gcv.height=128;const gx=gcv.getContext('2d'),gg=gx.createRadialGradient(64,64,0,64,64,64);
gg.addColorStop(0,'rgba(255,80,50,.95)');gg.addColorStop(.35,'rgba(255,170,60,.45)');gg.addColorStop(1,'rgba(255,60,40,0)');
gx.fillStyle=gg;gx.fillRect(0,0,128,128);
const glow=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(gcv),blending:THREE.NormalBlending,transparent:true,depthWrite:false}));
glow.position.copy(TC);brain.add(glow);
const ring=new THREE.Mesh(new THREE.RingGeometry(.3,.33,64),new THREE.MeshBasicMaterial({color:0xff3b3b,side:THREE.DoubleSide,transparent:true}));
ring.position.copy(P).multiplyScalar(1.02);ring.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),nrm);brain.add(ring);

/* modes */
let mode='anat';
function setMode(m){mode=m;const x=m==='xray';
  cg.setAttribute('color',m==='heat'?heatA:anatA);
  [cMat,bMat,sMat].forEach(t=>{t.transparent=x;t.opacity=x?.28:1;t.depthWrite=!x;t.side=x?THREE.DoubleSide:THREE.FrontSide;t.needsUpdate=true;});
  glow.visible=ring.visible=(m!=='anat');
  document.querySelectorAll('.b').forEach(b=>b.classList.toggle('on',b.dataset.m===m));}
document.querySelectorAll('.b').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.m)));
setMode('anat');

/* interaction */
let drag=false,lx=0,ly=0,uy=0,ux=0,moved=false,W=1,H=1;const clock=new THREE.Clock();
cv.addEventListener('pointerdown',e=>{if(!moved){uy+=Math.sin(clock.getElapsedTime()*.4)*.5;moved=true;}
  drag=true;lx=e.clientX;ly=e.clientY;cv.style.cursor='grabbing';});
addEventListener('pointerup',()=>{drag=false;cv.style.cursor='grab';});
addEventListener('pointermove',e=>{if(!drag)return;uy+=(e.clientX-lx)*.008;ux=cl(ux+(e.clientY-ly)*.006,-.9,.9);lx=e.clientX;ly=e.clientY;});
function resize(){W=wrap.clientWidth;H=wrap.clientHeight;renderer.setSize(W,H,false);cam.aspect=W/H;cam.updateProjectionMatrix();}
addEventListener('resize',resize);resize();

(function loop(){requestAnimationFrame(loop);const t=clock.getElapsedTime();
  brain.rotation.y=-1.15+uy+(moved?0:Math.sin(t*.4)*.5);brain.rotation.x=.08+ux;brain.position.y=.18+Math.sin(t*1.1)*.03;
  const pu=Math.sin(t*3);tMat.emissiveIntensity=(mode==='xray'?1.1:.55)+.15*pu;
  glow.scale.setScalar((mode==='xray'?1.5:1.0)+.08*pu);const rs=1+.06*pu;ring.scale.set(rs,rs,rs);ring.material.opacity=.9-.4*Math.abs(pu);
  brain.updateMatrixWorld();
  const wp=TC.clone().applyMatrix4(brain.matrixWorld),nw=nrm.clone().transformDirection(brain.matrixWorld);
  const vis=nw.dot(cam.position.clone().sub(wp).normalize())>.15,pj=wp.clone().project(cam);
  lbl.style.transform='translate('+((pj.x*.5+.5)*W)+'px,'+((-pj.y*.5+.5)*H)+'px)';lbl.style.opacity=vis?1:0;
  renderer.render(scene,cam);})();
</script>
"""


def brain_3d(height: int = 450):
    """Model 3D otak (Three.js): mode Anatomi / Grad-CAM / X-ray. Seret untuk memutar."""
    h = _BRAIN_HTML.replace("__H__", str(height))
    for k, v in {"__L_ANAT__": t("brain.anat"), "__L_LESION__": t("brain.lesion"), "__L_HINT__": t("brain.hint"),
                 "__P1__": t("brain.p1"), "__P2__": t("brain.p2"), "__P3__": t("brain.p3")}.items():
        h = h.replace(k, v)
    components.html(h, height=height + 6)


# ikon garis sederhana
IC_LAYERS = '<path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="m3 13 9 5 9-5"/>'
IC_EYE = '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>'
IC_TARGET = '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/>'
IC_SHIELD = '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>'
IC_NODES = '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8 11l8-4M8 13l8 4"/>'
IC_DROP = '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/>'
IC_CHIP = '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>'
IC_INFO = '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>'


def card(no, tag, title, body, icon, delay=0, anim="fade-up"):
    html(f"""<div data-aos="{anim}" data-aos-delay="{delay}" style="height:100%"><div class="card">
      <div class="big-no">{no}</div><div class="ic"><svg viewBox="0 0 24 24">{icon}</svg></div>
      <span class="tagp">{tag}</span><div class="h3">{title}</div><p>{body}</p></div></div>""")


def fact(icon, title, text, delay):
    return (f'<div class="fact" data-aos="fade-up" data-aos-delay="{delay}"><div class="ic"><svg viewBox="0 0 24 24">{icon}</svg></div>'
            f'<b>{title}</b><span>{text}</span></div>')


# =====================================================================
# HALAMAN 1: BERANDA & EDUKASI
# =====================================================================
def tampilkan_edukasi():
    inject_css(); inject_aos()

    with st.container(key="hero"):
        left, right = st.columns([1, 1.1], gap="large", vertical_alignment="center")
        with left:
            html(f"""
            <div data-aos="fade-up">
              <span class="pill">{t("hero.eyebrow")}</span>
              <div class="hero-title">{t("hero.title")}</div>
              <p class="hero-sub">{t("hero.sub")}</p>
              <div class="chips"><span>Explainable AI</span><span>EfficientNetB2</span><span>Grad-CAM</span></div>
            </div>""")
        with right:
            brain_3d(450)

    html('<div class="facts">'
         + fact(IC_LAYERS, t("fact1.t"), t("fact1.d"), 0)
         + fact(IC_EYE, t("fact2.t"), t("fact2.d"), 100)
         + fact(IC_TARGET, t("fact3.t"), t("fact3.d"), 200)
         + fact(IC_SHIELD, t("fact4.t"), t("fact4.d"), 300)
         + '</div>')

    html(f"""
    <div class="panel" data-aos="fade-up"><span class="eyebrow">{t("what.eyebrow")}</span>
    <div class="big">{t("what.body")}</div></div>""")

    html(f"""
    <div class="sec" data-aos="fade-up"><div class="h2">{t("sub.title")} <small>{t("sub.small")}</small></div>
    <p>{t("sub.desc")}</p></div>""")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        card("01", t("glioma.tag"), "Glioma", t("glioma.body"), IC_NODES, 0)
    with c2:
        card("02", t("mening.tag"), "Meningioma", t("mening.body"), IC_LAYERS, 120)
    with c3:
        card("03", t("pit.tag"), "Pituitary", t("pit.body"), IC_DROP, 240)

    with st.container(key="xai"):
        html(f"""
        <div class="xai-h" data-aos="fade-up"><span class="eyebrow">{t("xai.eyebrow")}</span>
        <div class="h2">{t("xai.title")}</div><p>{t("xai.p")}</p></div>""")
        a, b = st.columns(2, gap="medium")
        with a:
            card("01", t("xai.c1.tag"), "EfficientNetB2", t("xai.c1.body"), IC_CHIP)
        with b:
            card("02", t("xai.c2.tag"), "Grad-CAM", t("xai.c2.body"), IC_EYE, 120)
        html(f"""<div class="xai-h" data-aos="fade-up"><div class="legend"></div>
          <div class="legend-l"><span>{t("legend.low")}</span><span>{t("legend.high")}</span></div></div>""")

    html(f"""<div class="callout" data-aos="fade-up"><div class="ic"><svg viewBox="0 0 24 24">{IC_INFO}</svg></div>
      <div>{t("note.edu")}</div></div>""")


# =====================================================================
# HALAMAN 2: PANDUAN PENGGUNAAN
# =====================================================================
def tampilkan_panduan():
    inject_css(); inject_aos()

    html(f"""
    <div class="banner" data-aos="fade-up" style="max-width:100%">
      <span class="eyebrow">{t("guide.eyebrow")}</span>
      <div class="hero-title">{t("guide.title")}</div>
      <p class="hero-sub">{t("guide.sub")}</p>
    </div>""")

    def step(n, title, body, delay=0):
        html(f"""<div class="step" data-aos="fade-up" data-aos-delay="{delay}"><div class="n">{n}</div>
          <div class="card"><div class="big-no">0{n}</div><div class="h3">{title}</div>{body}</div></div>""")

    step(1, t("s1.t"), t("s1.b"))
    step(2, t("s2.t"), t("s2.b"))
    step(3, t("s3.t"), t("s3.b"))
    step(4, t("s4.t"),
         f"""<p>{t("s4.intro")}</p>
         <div class="demo"><div>{t("demo.orig")}</div><div class="heat">{t("demo.heat")}</div></div>
         <ul><li>{t("s4.l1")}</li><li>{t("s4.l2")}</li><li>{t("s4.l3")}</li></ul>""")

    html(f"""<div class="callout" data-aos="fade-up"><div class="ic"><svg viewBox="0 0 24 24">{IC_INFO}</svg></div>
      <div>{t("note.guide")}</div></div>""")