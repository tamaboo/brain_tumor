import streamlit as st
import streamlit.components.v1 as components

def _h(s: str) -> str:
    """Flatten HTML to one line so Streamlit markdown never treats indentation as a code block."""
    return " ".join(line.strip() for line in s.strip().splitlines())

def html(s: str):
    st.markdown(_h(s), unsafe_allow_html=True)

def inject_aos():
    components.html("""
    <script>
    const d = window.parent.document;
    if (!d.getElementById('aos-css')) {
      const l = d.createElement('link');
      l.id = 'aos-css'; l.rel = 'stylesheet';
      l.href = 'https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css';
      d.head.appendChild(l);
      d.body.setAttribute('data-aos-easing', 'ease-out-cubic');
      d.body.setAttribute('data-aos-duration', '800');
    }
    if (!window.parent.__aosObs) {
      const io = new IntersectionObserver((es) => es.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('aos-animate'); io.unobserve(e.target); }
      }), { threshold: 0.12 });
      const scan = () => d.querySelectorAll('[data-aos]:not([data-seen])')
        .forEach(el => { el.setAttribute('data-seen', '1'); io.observe(el); });
      new MutationObserver(scan).observe(d.body, { childList: true, subtree: true });
      window.parent.__aosObs = true; scan();
    }
    </script>""", height=0)

def inject_css():
    html("""
    <style>
    :root{--ink:#e8eef7;--mute:#8fa3bd;--line:rgba(120,160,210,.18);--cy:#3cc8e6;--bl:#4f8cff;--rd:#ff4d4d;--bg2:#0f1624}
    .hero-title{font-size:clamp(2.1rem,4.4vw,3.4rem);font-weight:800;line-height:1.1;margin:0 0 .6rem;
      background:linear-gradient(100deg,#4f8cff 0%,#3cc8e6 55%,#9be7ff 100%);-webkit-background-clip:text;
      background-clip:text;color:transparent}
    .hero-sub{font-size:1.08rem;color:var(--mute);line-height:1.7;max-width:34rem}
    .pill{display:inline-block;padding:.28rem .8rem;border:1px solid var(--line);border-radius:999px;
      color:var(--cy);font-size:.82rem;margin:0 .4rem .4rem 0;background:rgba(60,200,230,.06)}
    .sec-title{font-size:1.7rem;font-weight:700;margin:2.6rem 0 .5rem;color:var(--ink)}
    .sec-lead{color:var(--mute);line-height:1.75;max-width:48rem}
    .card{height:100%;padding:1.4rem 1.4rem 1.2rem;border-radius:16px;border:1px solid var(--line);
      background:linear-gradient(160deg,rgba(79,140,255,.08),rgba(15,22,36,.6));
      border-top:3px solid var(--accent,var(--cy));transition:transform .25s,box-shadow .25s}
    .card:hover{transform:translateY(-6px);box-shadow:0 14px 34px -14px var(--accent,var(--cy))}
    .card h3{margin:.2rem 0 .5rem;font-size:1.25rem;color:var(--ink)}
    .card p{margin:0;color:#b9c6d9;line-height:1.7;font-size:.96rem}
    .tag{display:inline-block;font-size:.76rem;padding:.12rem .6rem;border-radius:6px;margin-bottom:.5rem;
      background:rgba(255,255,255,.06);color:var(--accent,var(--cy))}
    .legend{height:12px;border-radius:99px;margin:.8rem 0 .3rem;
      background:linear-gradient(90deg,#1b3a8a,#2aa9c9,#9bd94b,#ffd23f,#ff7a2f,#ff2d2d)}
    .legend-l{display:flex;justify-content:space-between;color:var(--mute);font-size:.78rem}
    .tl{position:relative;margin:1rem 0 0 1.2rem;padding-left:2.2rem;border-left:2px dashed var(--line)}
    .step{position:relative;margin-bottom:1.5rem}
    .badge{position:absolute;left:-3.55rem;top:.9rem;width:2.4rem;height:2.4rem;border-radius:50%;
      display:flex;align-items:center;justify-content:center;font-weight:800;color:#06101f;
      background:linear-gradient(135deg,var(--cy),var(--bl));box-shadow:0 0 0 6px rgba(60,200,230,.14)}
    .step .card h3{display:flex;gap:.5rem;align-items:center}
    .step code{background:rgba(255,255,255,.08);padding:.05rem .4rem;border-radius:5px;color:#9be7ff}
    .step ul{margin:.6rem 0 0;padding-left:1.1rem;color:#b9c6d9;line-height:1.8}
    .demo{display:flex;gap:1rem;margin:1rem 0 .4rem;flex-wrap:wrap}
    .demo div{flex:1;min-width:150px;aspect-ratio:1.25;border-radius:12px;border:1px solid var(--line);
      display:flex;align-items:flex-end;padding:.5rem .7rem;font-size:.78rem;color:#dbe6f5;
      background:radial-gradient(ellipse at 50% 45%,#5b6577 0%,#2a3140 55%,#12161f 100%)}
    .demo .heat{background:radial-gradient(circle at 66% 38%,rgba(255,40,40,.95) 0,rgba(255,170,40,.8) 12%,
      rgba(120,220,120,.35) 24%,transparent 38%),radial-gradient(ellipse at 50% 45%,#5b6577 0%,#2a3140 55%,#12161f 100%)}
    .note{margin-top:1rem;padding:1rem 1.2rem;border-radius:12px;border:1px solid rgba(255,77,77,.35);
      background:rgba(255,77,77,.07);color:#f1c9c9;line-height:1.7}
    .stat{text-align:center;padding:1rem .5rem;border-radius:14px;border:1px solid var(--line);background:rgba(255,255,255,.02)}
    .stat b{display:block;font-size:1.5rem;color:var(--cy)}.stat span{font-size:.85rem;color:var(--mute)}
    @media (prefers-reduced-motion:reduce){[data-aos]{transition:none!important;transform:none!important;opacity:1!important}}
    </style>
    """)

def card(title, body, icon="", accent="#3cc8e6", tag="", anim="fade-up", delay=0):
    t = f'<span class="tag">{tag}</span><br>' if tag else ""
    html(f"""<div data-aos="{anim}" data-aos-delay="{delay}" style="height:100%">
      <div class="card" style="--accent:{accent}">{t}<h3>{icon} {title}</h3><p>{body}</p></div></div>""")

_BRAIN_HTML = r"""
<style>
  .b{font:600 12px system-ui,sans-serif;color:#b9c6d9;background:rgba(15,22,36,.7);border:1px solid rgba(120,160,210,.3);
     padding:5px 12px;border-radius:999px;cursor:pointer;transition:.2s}
  .b:hover{border-color:#3cc8e6;color:#fff}
  .b.on{background:#3cc8e6;color:#06101f;border-color:#3cc8e6}
</style>
<div id="wrap" style="position:relative;width:100%;height:__H__px;border-radius:20px;overflow:hidden;
  background:radial-gradient(circle at 50% 42%,#1a2845 0%,#0a0f1a 78%);border:1px solid rgba(120,160,210,.2)">
  <canvas id="c" style="width:100%;height:100%;display:block;cursor:grab;touch-action:none"></canvas>
  <div style="position:absolute;left:12px;top:12px;display:flex;gap:6px;z-index:2">
    <button class="b on" data-m="anat">Anatomi</button>
    <button class="b" data-m="heat">Grad-CAM</button>
    <button class="b" data-m="xray">X-ray</button>
  </div>
  <div id="lbl" style="position:absolute;left:0;top:0;pointer-events:none;font:600 12px system-ui,sans-serif;color:#fff;transition:opacity .25s">
    <div style="position:absolute;left:0;top:0;width:34px;height:1px;background:#ff6b6b;transform:rotate(-35deg);transform-origin:0 0"></div>
    <div style="position:absolute;left:30px;top:-34px;white-space:nowrap;background:rgba(255,60,60,.18);border:1px solid #ff6b6b;padding:3px 9px;border-radius:8px">Area lesi (simulasi)</div>
  </div>
  <div style="position:absolute;left:14px;bottom:10px;font:12px system-ui,sans-serif;color:#8fa3bd">Seret untuk memutar &bull; Ganti mode di kiri atas</div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const wrap=document.getElementById('wrap'),cv=document.getElementById('c'),lbl=document.getElementById('lbl');
const renderer=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
const scene=new THREE.Scene();
const cam=new THREE.PerspectiveCamera(36,1,.1,50);cam.position.set(0,-.1,5.4);
scene.add(new THREE.HemisphereLight(0xffffff,0x663344,.8));
const key=new THREE.DirectionalLight(0xfff0e6,1.1);key.position.set(3,4,5);scene.add(key);
const rim=new THREE.DirectionalLight(0x3cc8e6,.9);rim.position.set(-4,1,-4);scene.add(rim);

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
  r-=.17*Math.exp(-Math.pow(d.x/.075,2))*sst(-.35,.45,d.y);                  // longitudinal fissure
  const s=d.x<0?-1:1,dx=d.x-s*.8,dy=d.y+.45,dz=d.z-.1;
  r+=.12*Math.exp(-(dx*dx+dy*dy+dz*dz)/.1);                                  // temporal lobes
  const q=d.y+.05-.28*d.z;
  r-=.07*Math.exp(-q*q/.005)*sst(.45,.75,Math.abs(d.x))*sst(-.3,.6,d.z);    // sylvian fissure
  const w=.55*(vn(d.x*3+9,d.y*3,d.z*3)-.5);
  const g1=1-sst(0,.2,Math.abs(2*vn(d.x*7+w,d.y*7+w,d.z*7+w+4)-1));          // main sulci
  const g2=1-sst(0,.16,Math.abs(2*vn(d.x*15+3,d.y*15,d.z*15+7)-1));          // fine sulci
  G=Math.max(g1,.55*g2);
  r+=.03*(vn(d.x*4,d.y*4+2,d.z*4)-.5)-.075*g1-.03*g2;
  const sy=.78-.26*sst(.1,-.5,d.y);                                          // flatter underside
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
const L=new THREE.Color(.93,.68,.64),D=new THREE.Color(.55,.28,.3),Y=new THREE.Color(1,.85,.2),R=new THREE.Color(1,.1,.1),c=new THREE.Color(),hc=new THREE.Color();
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
const glow=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(gcv),blending:THREE.AdditiveBlending,transparent:true,depthWrite:false}));
glow.position.copy(TC);brain.add(glow);
const ring=new THREE.Mesh(new THREE.RingGeometry(.3,.33,64),new THREE.MeshBasicMaterial({color:0xff3b3b,side:THREE.DoubleSide,transparent:true}));
ring.position.copy(P).multiplyScalar(1.02);ring.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),nrm);brain.add(ring);

/* modes */
let mode='anat';
function setMode(m){mode=m;const x=m==='xray';
  cg.setAttribute('color',m==='heat'?heatA:anatA);
  [cMat,bMat,sMat].forEach(t=>{t.transparent=x;t.opacity=x?.2:1;t.depthWrite=!x;t.side=x?THREE.DoubleSide:THREE.FrontSide;t.needsUpdate=true;});
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
  const pu=Math.sin(t*3);tMat.emissiveIntensity=(mode==='xray'?1.1:.55)+.35*pu;
  glow.scale.setScalar((mode==='xray'?1.5:1.0)+.18*pu);const rs=1+.18*pu;ring.scale.set(rs,rs,rs);ring.material.opacity=.9-.4*Math.abs(pu);
  brain.updateMatrixWorld();
  const wp=TC.clone().applyMatrix4(brain.matrixWorld),nw=nrm.clone().transformDirection(brain.matrixWorld);
  const vis=nw.dot(cam.position.clone().sub(wp).normalize())>.15,pj=wp.clone().project(cam);
  lbl.style.transform='translate('+((pj.x*.5+.5)*W)+'px,'+((-pj.y*.5+.5)*H)+'px)';lbl.style.opacity=vis?1:0;
  renderer.render(scene,cam);})();
</script>
"""

def brain_3d(height: int = 460):
    """Realistic procedural 3D brain with a tumor. Modes: Anatomi / Grad-CAM / X-ray."""
    components.html(_BRAIN_HTML.replace("__H__", str(height)), height=height + 6)