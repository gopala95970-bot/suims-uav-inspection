const $ = (id) => document.getElementById(id);
async function api(url, options={}) {
  const r = await fetch(url, {headers: {"Content-Type":"application/json"}, ...options});
  return r.json();
}
function fmtTime(v){try{return new Date(v).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit",second:"2-digit"})}catch{return v}}
function render(s){
  const t=s.telemetry, r=s.risk, safe=s.safety, m=s.mission;
  $("missionState").textContent=m.state;
  $("battery").textContent=t.battery.toFixed(1); $("altitude").textContent=t.altitude_m; $("speed").textContent=t.speed_mps; $("sats").textContent=t.satellites;
  $("batteryBar").style.width=Math.max(4,t.battery)+"%";
  $("gps").textContent=t.gps_ok?"OK":"LOSS"; $("gps").style.color=t.gps_ok?"#6fe6b7":"#ff617d";
  $("link").textContent=t.telemetry_link?"OK":"LOSS"; $("link").style.color=t.telemetry_link?"#6fe6b7":"#ff617d";
  $("wind").textContent=t.wind_risk;
  $("riskScore").textContent=r.score; $("riskBar").style.width=r.score+"%"; $("riskLevel").textContent=r.level;
  $("riskExplain").textContent=r.explanation;
  $("proposal").textContent=s.proposed.action; $("finalAction").textContent=s.final_action; $("finalAction2").textContent=s.final_action;
  $("priority").textContent=safe.priority; $("decisionReason").textContent=safe.blocked ? "SAFETY ARBITRATION: "+safe.reason : s.proposed.reason;
  $("safetyStatus").textContent=safe.blocked ? "OVERRIDE ACTIVE" : "NORMAL";
  $("safetyReason").textContent=safe.reason;
  $("safetyBadge").textContent=safe.blocked ? "OVERRIDE" : "CLEAR";
  $("safetyBadge").className="badge "+(safe.blocked?"red":"green");
}
async function refresh(){
  try{ const s=await api("/api/snapshot"); render(s); loadAssets(); loadEvents(); }catch(e){console.error(e)}
}
async function loadAssets(){
  const rows=await api("/api/assets");
  $("assets").innerHTML=rows.map(x=>`<tr><td>${x.id}</td><td>${x.type}</td><td>${x.status}</td><td>${x.risk}</td><td>${x.distance_m}m</td></tr>`).join("");
}
async function loadEvents(){
  const rows=await api("/api/events");
  $("events").innerHTML=rows.map(x=>`<div class="event"><time>${fmtTime(x.timestamp)}</time><div><b>${x.event}</b><span>${x.detail}</span></div></div>`).join("");
}
async function startMission(){render(await api("/api/mission/start",{method:"POST"})); await refresh()}
async function tick(){render(await api("/api/simulate",{method:"POST"})); await loadEvents()}
async function setFailure(key,value){render(await api("/api/failures",{method:"POST",body:JSON.stringify({[key]:value})})); await loadEvents()}
async function resetSystem(){render(await api("/api/reset",{method:"POST"})); await loadEvents(); await loadAssets()}
async function runScenario(name){await startMission(); setTimeout(()=>setFailure("high_wind",true),700)}
loadAssets(); loadEvents(); refresh(); setInterval(refresh,3000);
