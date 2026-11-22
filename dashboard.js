async function init(){
 const res=await fetch('/api/analytics'); const d=await res.json();
 document.getElementById('data-note').textContent=d.data_note;
 const total=d.routes.reduce((s,x)=>s+x.passengers,0);
 const avg=d.routes.length?d.routes.reduce((s,x)=>s+x.avg_delay*x.observations,0)/d.record_count:0;
 const stops=d.stops.length, trips=d.record_count;
 const cards=[['Passenger boardings',total.toLocaleString()],['Route groups',d.routes.length],['Stop locations',stops],['Avg. delay (min)',avg.toFixed(1)]];
 document.getElementById('kpis').innerHTML=cards.map(x=>`<div class="kpi"><span>${x[0]}</span><strong>${x[1]}</strong></div>`).join('');
 const routes=[...d.routes].sort((a,b)=>b.passengers-a.passengers);
 new Chart(document.getElementById('routeChart'),{type:'bar',data:{labels:routes.map(x=>x.id),datasets:[{label:'Boardings',data:routes.map(x=>x.passengers),backgroundColor:'#3986c8',borderRadius:5}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});
 new Chart(document.getElementById('hourChart'),{type:'line',data:{labels:d.hours.map(x=>String(x.hour).padStart(2,'0')+':00'),datasets:[{label:'Boardings',data:d.hours.map(x=>x.passengers),borderColor:'#159b82',backgroundColor:'#159b8222',fill:true,tension:.3}]},options:{responsive:true,plugins:{legend:{display:false}}}});
 const delays=['0-5 min','6-15 min','16+ min']; const delayCounts=delays.map(b=>(d.delays.find(x=>x.bucket===b)||{}).observations||0);
 new Chart(document.getElementById('delayChart'),{type:'doughnut',data:{labels:delays,datasets:[{data:delayCounts,backgroundColor:['#20a47a','#e7ad42','#d66c68']}]},options:{responsive:true}});
 document.getElementById('routeRows').innerHTML=routes.map(r=>`<tr><td><b>${r.id}</b> — ${r.name}</td><td>${r.passengers.toLocaleString()}</td><td>${r.observations}</td><td>${r.avg_delay.toFixed(1)} min</td></tr>`).join('');
 const map=L.map('map').setView([12.9716,77.5946],10); L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'&copy; OpenStreetMap'}).addTo(map);
 d.stops.forEach(s=>L.circleMarker([s.lat,s.lon],{radius:Math.max(6,Math.min(18,s.passengers/90)),color:'#1769aa',fillOpacity:.55}).addTo(map).bindPopup(`<b>${s.name}</b><br>Boardings: ${s.passengers}`));
}
init().catch(e=>{document.getElementById('data-note').textContent='Could not load analytics. Run the MapReduce pipeline and refresh.';console.error(e)});