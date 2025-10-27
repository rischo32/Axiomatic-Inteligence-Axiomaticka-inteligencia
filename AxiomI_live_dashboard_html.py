<!doctype html>
<html lang="sk">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>AxiomI — Live Dashboard (demo)</title>
<link rel="icon" href="data:;base64,iVBORw0KGgo=">
<style>
:root{
  --bg:#071018; --card:#0f1720; --muted:#89a0b3; --accent:#7ad1ff; --glass:rgba(255,255,255,0.02);
  --good:#10b981; --warn:#f59e0b; --bad:#ef4444;
}
html,body{height:100%;margin:0;font-family:system-ui,Arial;background:var(--bg);color:#e6eef8}
.app{display:flex;flex-direction:column;height:100vh}
.header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:linear-gradient(180deg,rgba(255,255,255,0.02),transparent)}
.title{font-size:18px;font-weight:700}
.controls{display:flex;gap:8px;align-items:center}
.btn{background:var(--card);border:1px solid rgba(255,255,255,0.03);color:inherit;padding:8px;border-radius:8px;cursor:pointer}
.main{display:flex;flex:1;gap:12px;padding:12px;box-sizing:border-box}
.left{flex:1;display:flex;flex-direction:column;gap:12px}
.toprow{display:flex;gap:12px}
.card{background:var(--card);padding:12px;border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,0.6);min-height:80px}
.row{display:flex;gap:12px;align-items:center}
.small{font-size:12px;color:var(--muted)}
.panel-right{width:360px;min-width:260px;display:flex;flex-direction:column;gap:12px}
.axiom-list{display:flex;flex-direction:column;gap:8px;max-height:42vh;overflow:auto}
.axiom-item{display:flex;justify-content:space-between;align-items:center;padding:8px;border-radius:8px;background:var(--glass)}
.table-wrap{overflow:auto;max-height:30vh;border-radius:8px}
table{width:100%;border-collapse:collapse}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.03);font-size:13px}
.badge{padding:6px 8px;border-radius:999px;font-weight:700;font-size:12px}
.banner{padding:10px;border-radius:8px;font-weight:800}
.banner.warn{background:var(--warn);color:#111}
.banner.ok{background:var(--good);color:#042c17}
.footer{font-size:12px;color:var(--muted);margin-top:8px}
.slider{width:100%}
.controls input[type=file]{display:none}
.inline{display:flex;gap:8px;align-items:center}
.legend{display:flex;gap:8px;align-items:center;margin-top:8px}
.legend .sw{width:24px;height:12px;border-radius:6px}
@media(max-width:900px){
  .main{flex-direction:column}
  .panel-right{width:100%}
}
</style>
</head>
<body>
<div class="app">
  <div class="header">
    <div class="title">AxiomI — Live Dashboard</div>
    <div class="controls">
      <label class="btn">
        <input id="fileInput" type="file" accept=".csv,.json" />
        Načítať CSV
      </label>
      <button id="btnFetch" class="btn">Fetch (./data/rozhodnutia_with_aav.csv)</button>
      <button id="btnExport" class="btn">Export PNG</button>
      <button id="btnSaveWeights" class="btn">Uložiť váhy</button>
      <button id="btnLoadWeights" class="btn">Načítať váhy</button>
      <input id="weightsFile" type="file" accept=".json" style="display:none">
    </div>
  </div>

  <div class="main">
    <div class="left">
      <div class="toprow">
        <div class="card" style="flex:1">
          <canvas id="radarChart" height="220"></canvas>
        </div>
        <div class="card" style="width:420px">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div><strong>Časová os AAV</strong><div class="small">prehrávanie snapshotov</div></div>
            <div class="inline">
              <button id="playBtn" class="btn">Play</button>
              <button id="pauseBtn" class="btn">Pause</button>
            </div>
          </div>
          <canvas id="lineChart" height="140" style="margin-top:8px"></canvas>
          <div class="small" id="timelineInfo" style="margin-top:8px"></div>
        </div>
      </div>

      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div><strong>Force-graph axiomov</strong><div class="small">drag & pan, klik pre detail</div></div>
          <div id="rep7banner" class="banner ok" style="display:none"></div>
        </div>
        <div id="graph" style="height:280px;margin-top:8px"></div>
      </div>

      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div><strong>Rozhodnutia</strong><div class="small">tabuľka s AAV</div></div>
          <div class="small">Počet záznamov: <span id="countSpan">0</span></div>
        </div>
        <div class="table-wrap" id="tableWrap" style="margin-top:8px">
          <table id="decisionsTable"><thead><tr id="theadRow"></tr></thead><tbody id="tbody"></tbody></table>
        </div>
      </div>
    </div>

    <div class="panel-right">
      <div class="card">
        <div><strong>Simulátor váh axiomov</strong></div>
        <div class="small" style="margin-top:6px">Posuň váhy a vidíš okamžitú zmenu AAV</div>
        <div id="sliders" style="margin-top:8px"></div>
        <div style="margin-top:8px;display:flex;gap:8px">
          <button id="applyWeights" class="btn">Aplikovať</button>
          <button id="resetWeights" class="btn">Reset</button>
        </div>
      </div>

      <div class="card">
        <div><strong>Štatistiky</strong></div>
        <div class="small" style="margin-top:6px">Avg AAV: <span id="avgAav">—</span></div>
        <div class="small" style="margin-top:6px">Min / Max: <span id="minAav">—</span> / <span id="maxAav">—</span></div>
        <div class="legend">
          <div class="sw" style="background:var(--good)"></div><div class="small">ACCEPT ≥ 0.80</div>
          <div class="sw" style="background:var(--warn)"></div><div class="small">CONDITIONAL</div>
          <div class="sw" style="background:var(--bad)"></div><div class="small">REJECT</div>
        </div>
      </div>

      <div class="card">
        <div><strong>Info & Tipy</strong></div>
        <div class="small" style="margin-top:8px">Ak prehliadač zlyhá s file://, spusti v adresári: <code>python3 -m http.server 8000</code> a otvori <code>http://127.0.0.1:8000/axiom_live_dashboard.html</code></div>
        <div class="small" style="margin-top:6px">Môžem to nasadiť na GitHub Pages ak chceš — povieš a pripravím ZIP.</div>
      </div>
    </div>
  </div>
</div>

<!-- libs -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.2/papaparse.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

<script>
/* --------- SETTINGS & STATE ---------- */
const AXIOMS = [
  {id:"INT", label:"Zámer (INT)"},
  {id:"LEX", label:"Existencia (LEX)"},
  {id:"WIS", label:"Múdrosť (WIS)"},
  {id:"REL", label:"Vzájomnosť (REL)"},
  {id:"VER", label:"Pravda (VER)"},
  {id:"LIB", label:"Sloboda (LIB)"},
  {id:"UNI", label:"Jednota (UNI)"},
  {id:"CRE", label:"Tvorba (CRE)"}
];
let weights = {}; AXIOMS.forEach(a=>weights[a.id]=1.0);
const REP7_THRESHOLD = 0.15;

let rawRows = []; // parsed rows
let aavSeries = []; // per-row AAV
let currentIndex = 0;
let playTimer = null;

/* --------- UTIL ---------- */
function parseNumber(s){ const n = parseFloat(String(s).replace(',', '.')); return isNaN(n)?null:n; }
function statusColor(status){
  if(!status) return '#95a5a6';
  const s = String(status).toUpperCase();
  if(s.includes('ACCEPT')) return '#10b981';
  if(s.includes('CONDITIONAL')||s.includes('WARN')) return '#f59e0b';
  if(s.includes('REJECT')||s.includes('DENY')) return '#ef4444';
  return '#95a5a6';
}

/* --------- UI HOOKS ---------- */
const fileInput = document.getElementById('fileInput');
const btnFetch = document.getElementById('btnFetch');
const btnExport = document.getElementById('btnExport');
const btnSaveWeights = document.getElementById('btnSaveWeights');
const btnLoadWeights = document.getElementById('btnLoadWeights');
const weightsFile = document.getElementById('weightsFile');
const playBtn = document.getElementById('playBtn');
const pauseBtn = document.getElementById('pauseBtn');

/* --------- Charts init ---------- */
// Radar
const radarCtx = document.getElementById('radarChart').getContext('2d');
const radarChart = new Chart(radarCtx, {
  type: 'radar',
  data: {
    labels: AXIOMS.map(a=>a.label),
    datasets: [{
      label: 'Priemery axiomu',
      data: AXIOMS.map(()=>0),
      backgroundColor: 'rgba(122, 209, 255,0.12)',
      borderColor: '#7ad1ff',
      pointBackgroundColor: '#7ad1ff'
    }]
  },
  options: {
    scales: { r: { beginAtZero:true, max:1, ticks:{display:false} } },
    plugins:{legend:{display:false}}
  }
});

// Line chart
const lineCtx = document.getElementById('lineChart').getContext('2d');
const lineChart = new Chart(lineCtx, {
  type: 'line',
  data: { labels: [], datasets: [{ label:'AAV', data: [], borderColor:'#9ad0f5', tension:0.2, fill:true, backgroundColor:'rgba(154,208,245,0.06)' }] },
  options: { plugins:{legend:{display:false}}, scales:{ y:{min:0,max:1} } }
});

/* --------- Force graph ---------- */
const graphEl = document.getElementById('graph');
const width = graphEl.clientWidth || 800, height = graphEl.clientHeight || 300;
const svg = d3.select(graphEl).append('svg').attr('width','100%').attr('height','100%');
let gLinks = svg.append('g'), gNodes = svg.append('g');
let forceSim = null;
let graphNodes = AXIOMS.map((a,i)=>({id:a.id,label:a.label,score:0,r:20,color:null})),
    graphLinks = [
      {source:"INT",target:"WIS"},{source:"INT",target:"REL"},{source:"LEX",target:"VER"},
      {source:"WIS",target:"CRE"},{source:"REL",target:"UNI"},{source:"VER",target:"LIB"}
    ];
function renderGraph(){
  if(forceSim) forceSim.stop();
  graphNodes.forEach(n=>{ n.r = 10 + (n.score||0)*40; n.color = `hsl(${Math.round((1-(n.score||0))*160)},70%,60%)`; });
  const link = gLinks.selectAll('line').data(graphLinks, d=>d.source+'-'+d.target);
  link.join('line').attr('stroke','#284b5b').attr('stroke-width',1.4);
  const node = gNodes.selectAll('g').data(graphNodes, d=>d.id);
  const nodeEnter = node.join(enter=>{
    const g = enter.append('g').call(d3.drag().on('start',d=>{ if(!d3.event){} }).on('start', dragstarted).on('drag', dragged).on('end', dragended));
    g.append('circle').attr('r', d=>d.r).attr('fill', d=>d.color).attr('stroke','#fff').attr('stroke-width',1);
    g.append('text').text(d=>d.id).attr('text-anchor','middle').attr('dy',4).style('pointer-events','none').style('font-size','11px');
    return g;
  });
  nodeEnter.on('mouseover', (event,d)=>{ showTooltip(event,d.label + '<br/>Priemer: ' + ((d.score||0).toFixed(4))); })
           .on('mouseout', hideTooltip)
           .on('click', (event,d)=>{ alert(d.label + '\\nPriemer: ' + ((d.score||0).toFixed(6))); });

  forceSim = d3.forceSimulation(graphNodes)
    .force('link', d3.forceLink(graphLinks).id(d=>d.id).distance(120).strength(0.6))
    .force('charge', d3.forceManyBody().strength(-380))
    .force('center', d3.forceCenter(width/2, height/2))
    .force('collide', d3.forceCollide().radius(d=>d.r+6).iterations(2))
    .on('tick', ()=>{
      gLinks.selectAll('line').attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
      gNodes.selectAll('g').attr('transform', d=>`translate(${d.x},${d.y})`);
    });
}

function dragstarted(event,d){ if(!event.active) forceSim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }
function dragged(event,d){ d.fx = event.x; d.fy = event.y; }
function dragended(event,d){ if(!event.active) forceSim.alphaTarget(0); /* leave fixed */ }

/* --------- Tooltip ---------- */
const tip = d3.select('body').append('div').attr('class','small').style('position','absolute').style('display','none').style('padding','6px 8px').style('background','rgba(0,0,0,0.8)').style('border-radius','6px').style('pointer-events','none');
function showTooltip(evt,html){ tip.html(html).style('left',(evt.pageX+12)+'px').style('top',(evt.pageY-20)+'px').style('display','block'); }
function hideTooltip(){ tip.style('display','none'); }

/* --------- Table rendering ---------- */
function renderTable(rows, fields){
  const thead = document.getElementById('theadRow');
  thead.innerHTML = '';
  fields.forEach(f=>{ const th=document.createElement('th'); th.textContent=f; thead.appendChild(th); });
  const tbody = document.getElementById('tbody'); tbody.innerHTML='';
  rows.forEach(r=>{
    const tr = document.createElement('tr');
    fields.forEach(f=>{
      const td = document.createElement('td');
      if(f.toLowerCase().endsWith('aav')){
        const val = parseNumber(r[f]) ?? null;
        const bar = document.createElement('div');
        bar.style.display='flex'; bar.style.gap='8px'; bar.style.alignItems='center';
        const lab = document.createElement('div'); lab.style.minWidth='70px'; lab.style.fontWeight='700'; lab.textContent = val !== null ? val.toFixed(6) : '';
        const barWrap = document.createElement('div'); barWrap.style.flex='1'; barWrap.style.background='#222'; barWrap.style.borderRadius='6px'; barWrap.style.height='12px';
        const fill = document.createElement('div'); fill.style.height='100%'; fill.style.width = (val?Math.max(0,Math.min(100,val*100)):0)+'%';
        fill.style.background = statusColor(r['Status']||r['status']);
        barWrap.appendChild(fill);
        bar.appendChild(lab); bar.appendChild(barWrap);
        td.appendChild(bar);
      } else {
        td.textContent = r[f] ?? '';
      }
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

/* --------- Compute AAVs given current weights ---------- */
function computeAavsFromRows(rows){
  // expected axiom columns like "Zámer (INT)" etc. do heuristics
  const headers = Object.keys(rows[0] || {});
  const norm = {}; headers.forEach(h=>norm[h.trim().toLowerCase()]=h);
  const map = {};
  for(const a of AXIOMS){
    const aliases = [a.label.toLowerCase(), a.id.toLowerCase()];
    let found = null;
    for(const k in norm){
      for(const al of aliases){
        if(k.includes(al)) { found = norm[k]; break; }
      }
      if(found) break;
    }
    map[a.id] = found; // column name or null
  }
  const aavs = [];
  // compute per-row aav using current weights
  for(const r of rows){
    let numerator = 0, denom = 0;
    for(const a of AXIOMS){
      const col = map[a.id];
      const w = Math.max(0, parseFloat(weights[a.id]||1));
      let v = null;
      if(col && r[col] !== undefined && r[col] !== '') v = parseNumber(r[col]);
      if(v === null){
        // try AAV directly if exists
        const av = Object.keys(r).find(k=>k.toLowerCase().includes('aav'));
        if(av) v = parseNumber(r[av]);
      }
      if(v !== null){
        numerator += w * v;
        denom += w;
      }
    }
    const aav = denom>0 ? numerator/denom : 0;
    aavs.push(aav);
  }
  return aavs;
}

/* --------- Update visual state ---------- */
function updateAll(){
  if(!rawRows.length) return;
  aavSeries = computeAavsFromRows(rawRows);
  // update line chart
  lineChart.data.labels = rawRows.map((r,i)=> String(r['Dátum'] || r['Date'] || (i+1)));
  lineChart.data.datasets[0].data = aavSeries;
  lineChart.update();

  // stats
  const clean = aavSeries.filter(v=>isFinite(v));
  const avg = clean.length ? (clean.reduce((a,b)=>a+b,0)/clean.length) : null;
  document.getElementById('avgAav').textContent = avg!==null ? avg.toFixed(6) : '—';
  document.getElementById('minAav').textContent = clean.length ? Math.min(...clean).toFixed(6) : '—';
  document.getElementById('maxAav').textContent = clean.length ? Math.max(...clean).toFixed(6) : '—';
  document.getElementById('countSpan').textContent = rawRows.length;

  // radar averages per axiom
  const axMeans = AXIOMS.map(a=>{
    const vals = [];
    for(const r of rawRows){
      const col = Object.keys(r).find(k=>k.toLowerCase().includes(a.id.toLowerCase())||k.toLowerCase().includes(a.label.toLowerCase().split(' ')[0]));
      if(col) { const v = parseNumber(r[col]); if(v!==null) vals.push(v); }
    }
    return vals.length ? vals.reduce((x,y)=>x+y,0)/vals.length : 0;
  });
  radarChart.data.datasets[0].data = axMeans;
  radarChart.update();

  // graph node scores
  graphNodes.forEach(n=>{
    const idx = AXIOMS.findIndex(a=>a.id===n.id);
    n.score = axMeans[idx] || 0;
  });
  renderGraph();

  // table
  const visible = Object.keys(rawRows[0] || {});
  if(!visible.some(h=>/aav/i.test(h))) visible.push('AAV');
  // attach computed AAV to per-row view copy
  const rowsWithAav = rawRows.map((r,i)=> {
    const copy = Object.assign({}, r);
    copy['AAV'] = aavSeries[i]!==undefined ? aavSeries[i].toFixed(6) : '';
    return copy;
  });
  renderTable(rowsWithAav, visible);

  // REP7 check (first 25% vs last 25%)
  runRep7Check(aavSeries);
}

/* --------- REP7 ---------- */
function runRep7Check(series){
  const banner = document.getElementById('rep7banner');
  banner.style.display='none';
  if(!series || series.length<4) return;
  const n = series.length, slice = Math.max(1, Math.floor(n*0.25));
  const first = series.slice(0,slice); const last = series.slice(n-slice);
  const avgFirst = first.reduce((a,b)=>a+b,0)/first.length;
  const avgLast = last.reduce((a,b)=>a+b,0)/last.length;
  const delta = avgLast - avgFirst;
  if(Math.abs(delta) >= REP7_THRESHOLD){
    banner.textContent = `REP7 ALERT • ΔAAV = ${delta.toFixed(4)}`;
    banner.className = 'banner warn';
  } else {
    banner.textContent = `AAV stabilné • ΔAAV = ${delta.toFixed(4)}`;
    banner.className = 'banner ok';
  }
  banner.style.display='block';
}

/* --------- File loading ---------- */
fileInput.addEventListener('change', (e)=>{
  const f = e.target.files[0]; if(!f) return;
  const name = f.name.toLowerCase();
  if(name.endsWith('.csv')){
    Papa.parse(f,{header:true,skipEmptyLines:true,complete: (res)=> { rawRows = res.data; updateAll(); }});
  } else {
    const r=new FileReader(); r.onload=ev=>{ try{ const obj = JSON.parse(ev.target.result); if(obj.nodes) { /* graph */ } else if(Array.isArray(obj)) { rawRows = obj; updateAll(); } } catch(err){ alert('Chybný JSON'); } }; r.readAsText(f);
  }
});

btnFetch.addEventListener('click', ()=>{
  fetch('./data/rozhodnutia_with_aav.csv').then(r=>{
    if(!r.ok) throw new Error('Not found');
    return r.text();
  }).then(txt=>{
    const parsed = Papa.parse(txt,{header:true,skipEmptyLines:true});
    rawRows = parsed.data; updateAll();
  }).catch(err=>{
    alert('Fetch zlyhal: ' + err.message + '. Použi súbor alebo spusti lokálny server.');
  });
});

/* --------- Sliders for weights ---------- */
const slidersDiv = document.getElementById('sliders');
function buildSliders(){
  slidersDiv.innerHTML = '';
  AXIOMS.forEach(a=>{
    const wrap = document.createElement('div'); wrap.style.marginTop='6px';
    const label = document.createElement('div'); label.textContent = `${a.label} (${a.id}) — ${weights[a.id].toFixed(2)}`; label.className='small';
    const input = document.createElement('input'); input.type='range'; input.min='0'; input.max='2'; input.step='0.01'; input.value=weights[a.id]; input.className='slider';
    input.addEventListener('input', ()=>{ weights[a.id]=parseFloat(input.value); label.textContent = `${a.label} (${a.id}) — ${weights[a.id].toFixed(2)}`; });
    wrap.appendChild(label); wrap.appendChild(input); slidersDiv.appendChild(wrap);
  });
}
document.getElementById('applyWeights').addEventListener('click', ()=>{ updateAll(); });
document.getElementById('resetWeights').addEventListener('click', ()=>{ AXIOMS.forEach(a=>weights[a.id]=1.0); buildSliders(); updateAll(); });

btnSaveWeights.addEventListener('click', ()=>{
  const blob = new Blob([JSON.stringify(weights,null,2)],{type:'application/json'});
  const url = URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='axiom_weights.json'; document.body.appendChild(a); a.click(); a.remove();
});
btnLoadWeights.addEventListener('click', ()=> weightsFile.click());
weightsFile.addEventListener('change', e=>{ const f=e.target.files[0]; if(!f) return; const r=new FileReader(); r.onload=ev=>{ try{ const obj=JSON.parse(ev.target.result); AXIOMS.forEach(a=>{ if(obj[a.id]!==undefined) weights[a.id]=parseFloat(obj[a.id]); }); buildSliders(); updateAll(); }catch{ alert('Chybný weights JSON'); } }; r.readAsText(f); });

/* --------- Play / Pause timeline ---------- */
playBtn.addEventListener('click', ()=> {
  if(!aavSeries || !aavSeries.length) return alert('Žiadne dáta');
  if(playTimer) return;
  playTimer = setInterval(()=>{
    currentIndex = (currentIndex + 1) % aavSeries.length;
    highlightIndex(currentIndex);
  }, 650);
});
pauseBtn.addEventListener('click', ()=> { if(playTimer){ clearInterval(playTimer); playTimer=null; } });

function highlightIndex(i){
  // simple highlight: set a dot style or show info
  const info = document.getElementById('timelineInfo');
  info.textContent = `Snapshot ${i+1} — AAV=${aavSeries[i]!==undefined? aavSeries[i].toFixed(6):'—'}`;
  // draw vertical line on chart (approx) by creating annotation? we'll just update dataset point size temporarily
  const ds = lineChart.data.datasets[0];
  ds.pointRadius = ds.data.map((_,idx)=> idx===i?6:2);
  lineChart.update();
}

/* --------- Export ---------- */
btnExport.addEventListener('click', ()=>{
  html2canvas(document.querySelector('.main'), {backgroundColor:null, scale:2}).then(canvas=>{
    canvas.toBlob(blob=>{ const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='axiom_dashboard.png'; document.body.appendChild(a); a.click(); a.remove(); });
  });
});

/* --------- Init ---------- */
buildSliders();
renderGraph();
updateAll();

// load demo data if none (light sample)
const DEMO_CSV = `ID Rozhodnutia,Dátum,Zámer (INT),Existencia (LEX),Múdrosť (WIS),Vzájomnosť (REL),Pravda (VER),Sloboda (LIB),Jednota (UNI),Tvorba (CRE),Status,Notes
1,2025-10-22,0.85,0.78,0.92,0.70,0.95,0.82,0.88,0.91,ACCEPT,Prvý
2,2025-10-23,0.60,0.50,0.55,0.40,0.60,0.70,0.65,0.60,CONDITIONAL,Druhý
3,2025-10-24,0.30,0.20,0.25,0.15,0.40,0.35,0.30,0.20,REJECT,Tretí
4,2025-10-25,0.82,0.79,0.88,0.72,0.90,0.80,0.85,0.87,ACCEPT,Štvrtý
5,2025-10-26,0.58,0.55,0.60,0.45,0.63,0.68,0.66,0.64,CONDITIONAL,Piaty`;
if(!rawRows.length){
  Papa.parse(DEMO_CSV,{header:true,skipEmptyLines:true,complete:(res)=>{ rawRows=res.data; updateAll(); }});
}
</script>
</body>
</html>
