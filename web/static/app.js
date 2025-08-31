const statusEl = document.getElementById('status');
const tsEl = document.getElementById('astro-timestamp');
const detailsEl = document.getElementById('details');
const progressEl = document.getElementById('progress');
const btnRefresh = document.getElementById('btn-refresh');
const btnInstall = document.getElementById('btn-install');
const yearEl = document.getElementById('year');

yearEl.textContent = new Date().getFullYear();

let deferredPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  btnInstall.hidden = false;
});
btnInstall.addEventListener('click', async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  console.log('Install outcome', outcome);
  deferredPrompt = null;
  btnInstall.hidden = true;
});

async function fetchNow() {
  statusEl.textContent = 'FETCH';
  try {
    const r = await fetch('/api/now');
    if (!r.ok) throw new Error(r.status);
    const data = await r.json();
    statusEl.textContent = 'OK';
    renderData(data);
    localStorage.setItem('lastNow', JSON.stringify(data));
  } catch (e) {
    console.warn('Fetch failed, using last cache', e);
    statusEl.textContent = 'OFFLINE';
    const cached = localStorage.getItem('lastNow');
    if (cached) {
      renderData(JSON.parse(cached));
    } else {
      tsEl.textContent = 'No data (offline)';
    }
  }
}

function renderData(d) {
  tsEl.textContent = d.timestamp_proposed || '—';
  if (typeof d.milli_day === 'number') progressEl.value = d.milli_day;
  const lines = [];
  lines.push(`UTC: ${d.utc_iso}`);
  lines.push(`Frame Year: ${d.frame_year}`);
  if (d.day_index !== null) lines.push(`Day Index: ${d.day_index}`); else lines.push('Day Index: (pending)');
  if ('solar_longitude_deg' in d) lines.push(`Solar Lon (deg): ${d.solar_longitude_deg}`);
  if (d.note) lines.push(d.note);
  detailsEl.innerHTML = lines.map(l => escapeHtml(l)).join('<br>');
}

function escapeHtml(str){
  return str.replace(/[&<>\