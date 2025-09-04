// Astronomical Watch Front-End Logic
// Refactored: single SW registration, robust escapeHtml, periodic longitude-inclusive fetch.

const statusEl   = document.getElementById('status');
const tsEl       = document.getElementById('astro-timestamp');
const detailsEl  = document.getElementById('details');
const progressEl = document.getElementById('progress');
const btnRefresh = document.getElementById('btn-refresh');
const btnInstall = document.getElementById('btn-install');
const yearEl     = document.getElementById('year');

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
  try {
    await deferredPrompt.userChoice;
  } catch (_) {
    // ignore
  }
  deferredPrompt = null;
  btnInstall.hidden = true;
});

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, c => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[c]));
}

async function fetchNow() {
  statusEl.textContent = 'FETCH';
  try {
    const r = await fetch('/api/now?include_longitude=true');
    if (!r.ok) throw new Error(r.status);
    const data = await r.json();
    statusEl.textContent = 'OK';
    renderData(data);
    localStorage.setItem('lastNow', JSON.stringify(data));
  } catch (e) {
    console.warn('Fetch failed, using cache if available', e);
    statusEl.textContent = 'OFFLINE';
    const cached = localStorage.getItem('lastNow');
    if (cached) {
      renderData(JSON.parse(cached));
    } else {
      tsEl.textContent = 'No data (offline)';
      detailsEl.textContent = '';
      progressEl.value = 0;
    }
  }
}

function renderData(d) {
  tsEl.textContent = d.timestamp_proposed || '—';

  if (typeof d.milli_day === 'number' && d.milli_day >= 0 && d.milli_day <= 999) {
    progressEl.value = d.milli_day;
  } else {
    progressEl.value = 0;
  }

  const lines = [];
  lines.push(`UTC: ${d.utc_iso}`);
  lines.push(`Frame Year: ${d.frame_year}`);
  lines.push(`Day Index: ${d.day_index === null ? '(pending)' : d.day_index}`);

  if ('solar_longitude_deg' in d) {
    if (typeof d.solar_longitude_deg === 'number') {
      lines.push(`Solar Lon (deg): ${d.solar_longitude_deg.toFixed(4)}`);
    } else if (d.solar_longitude_deg === null) {
      lines.push('Solar Lon (deg): (unavailable)');
    }
  }
  if (d.solar_longitude_error) lines.push(`Solar Lon Error: ${d.solar_longitude_error}`);
  if (d.solar_longitude_note)  lines.push(d.solar_longitude_note);
  if (d.note) lines.push(d.note);

  detailsEl.innerHTML = lines.map(l => escapeHtml(l)).join('<br>');
}

btnRefresh.addEventListener('click', fetchNow);

// Periodic refresh every 5 s
const INTERVAL_MS = 5000;
setInterval(fetchNow, INTERVAL_MS);
fetchNow();

// Single service worker registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/static/service-worker.js')
      .catch(err => console.error('Service worker registration failed:', err));
  });
  }
