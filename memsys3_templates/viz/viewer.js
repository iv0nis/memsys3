// Memory Visualizer - Carrega i renderitza YAMLs

// Utilitzem js-yaml carregat via CDN

// State
let contextData = null;
let projectStatusData = null;
let fullADRs = null;
let fullSessions = null;

// Tab handling
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    const targetTab = tab.dataset.tab;

    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

    tab.classList.add('active');
    document.getElementById(targetTab).classList.add('active');
  });
});

// Load data
async function loadData() {
  try {
    updateStatus('loading', 'Loading memory data...');

    // Load context.yaml
    try {
      const contextRes = await fetch('/context.yaml');
      const contextText = await contextRes.text();
      contextData = jsyaml.load(contextText);
    } catch (e) {
      console.warn('context.yaml not found - expected if not compiled yet');
    }

    // Load project-status.yaml
    try {
      const statusRes = await fetch('/project-status.yaml');
      const statusText = await statusRes.text();
      projectStatusData = jsyaml.load(statusText);
    } catch (e) {
      console.warn('project-status.yaml not found');
    }

    // Load full/adr.yaml
    try {
      const adrRes = await fetch('/full/adr.yaml');
      const adrText = await adrRes.text();
      fullADRs = jsyaml.load(adrText);
    } catch (e) {
      console.warn('full/adr.yaml not found');
    }

    // Load full/sessions.yaml
    try {
      const sessionsRes = await fetch('/full/sessions.yaml');
      const sessionsText = await sessionsRes.text();
      fullSessions = jsyaml.load(sessionsText);
    } catch (e) {
      console.warn('full/sessions.yaml not found');
    }

    renderAll();
    updateStatus('success', 'Memory loaded successfully');
  } catch (error) {
    updateStatus('error', `Error loading data: ${error.message}`);
    console.error(error);
  }
}

function updateStatus(type, message) {
  const dot = document.getElementById('statusDot');
  const text = document.getElementById('statusText');

  text.textContent = message;

  if (type === 'success') {
    dot.style.background = 'var(--success)';
  } else if (type === 'error') {
    dot.style.background = 'var(--error)';
  } else {
    dot.style.background = 'var(--warning)';
  }
}

function renderAll() {
  renderAgentView();
  renderFullHistory();
  renderProjectStatus();
  renderStats();
}

// Render Agent View (context.yaml)
function renderAgentView() {
  if (!contextData) {
    document.getElementById('agentProject').innerHTML = '<p class="error">context.yaml not found. Run Context Agent first.</p>';
    return;
  }

  // Project info
  const project = contextData.project || {};
  document.getElementById('agentProject').innerHTML = `
    <p><strong>Nom:</strong> ${project.nom || 'N/A'}</p>
    <p><strong>Descripció:</strong> ${project.descripcio || 'N/A'}</p>
    <p><strong>Fase:</strong> ${project.fase || 'N/A'}</p>
    <p><strong>Última feature:</strong> ${project.ultima_feature || 'N/A'}</p>
    <p><strong>Següent milestone:</strong> ${project.seguent_milestone || 'N/A'}</p>
  `;

  // Features
  const features = contextData.features || {};
  const featuresHTML = Object.keys(features).map(key => {
    const f = features[key];
    return `
      <div class="feature-card">
        <span class="feature-status status-${f.estat || 'pendent'}">${f.estat || 'pendent'}</span>
        <h4>${f.nom || key}</h4>
        <p>${f.descripcio || ''}</p>
        ${f.url ? `<p><a href="${f.url}" target="_blank">${f.url}</a></p>` : ''}
      </div>
    `;
  }).join('');
  document.getElementById('agentFeatures').innerHTML = featuresHTML || '<p>No features</p>';

  // ADRs
  const adrs = contextData.adrs || [];
  const adrsHTML = (Array.isArray(adrs) ? adrs : []).map(adr => `
    <div class="adr-card">
      <div class="adr-header">
        <div class="adr-title">ADR-${adr.id}: ${adr.titol}</div>
      </div>
      <p><strong>Decisió:</strong> ${adr.decisio}</p>
      <p><strong>Motiu:</strong> ${adr.motiu}</p>
      <p><strong>Impacte:</strong> ${adr.impacte}</p>
    </div>
  `).join('');
  document.getElementById('agentADRs').innerHTML = adrsHTML || '<p>No ADRs</p>';

  // Última sessió
  const session = contextData.ultima_sessio || {};
  const sessionHTML = `
    <p><strong>Data:</strong> ${session.data || 'N/A'}</p>
    <p><strong>Durada:</strong> ${session.durada || 'N/A'}</p>
    ${session.que_es_va_fer ? `
      <h4>Què es va fer:</h4>
      <ul>${(Array.isArray(session.que_es_va_fer) ? session.que_es_va_fer : []).map(item => `<li>${item}</li>`).join('')}</ul>
    ` : ''}
    ${session.decisions ? `
      <h4>Decisions:</h4>
      <ul>${(Array.isArray(session.decisions) ? session.decisions : []).map(item => `<li>${item}</li>`).join('')}</ul>
    ` : ''}
  `;
  document.getElementById('agentSession').innerHTML = sessionHTML;

  // Gotchas
  const gotchas = contextData.gotchas || [];
  const gotchasHTML = (Array.isArray(gotchas) ? gotchas : []).map(g => `
    <div class="gotcha-item">
      <strong>${g.id}:</strong> ${g.problema}<br>
      <em>Solució: ${g.solucio}</em>
    </div>
  `).join('');
  document.getElementById('agentGotchas').innerHTML = gotchasHTML || '<p>No gotchas</p>';

  // Pendents
  const pendents = contextData.pendents || [];
  const pendentsHTML = (Array.isArray(pendents) ? pendents : []).map(p => `
    <div class="pendent-item">
      <strong>P${p.prioritat}:</strong> ${p.tasca}<br>
      ${p.detall ? `<em>${p.detall}</em>` : ''}
    </div>
  `).join('');
  document.getElementById('agentPendents').innerHTML = pendentsHTML || '<p>No pendents</p>';
}

// Render Full History
function renderFullHistory() {
  // Full ADRs
  if (fullADRs && fullADRs.adrs) {
    const adrsHTML = fullADRs.adrs.map(adr => `
      <div class="adr-card">
        <div class="adr-header">
          <div class="adr-title">ADR-${adr.id}: ${adr.titol}</div>
          <span class="adr-badge badge-${adr.estat}">${adr.estat}</span>
        </div>
        <p><strong>Data:</strong> ${adr.data}</p>
        <p><strong>Àrea:</strong> ${adr.area}</p>
        <p>${adr.decisio}</p>
      </div>
    `).join('');
    document.getElementById('fullADRs').innerHTML = adrsHTML;
  } else {
    document.getElementById('fullADRs').innerHTML = '<p class="error">full/adr.yaml not found</p>';
  }

  // Full Sessions
  if (fullSessions && fullSessions.sessions) {
    const sessionsHTML = fullSessions.sessions.map(session => {
      const featuresHTML = session.features_implementades ?
        '<h4>Features Implementades:</h4><ul>' +
        session.features_implementades.map(f => `<li><strong>${f.nom}:</strong> ${f.descripcio}</li>`).join('') +
        '</ul>' : '';

      const problemesHTML = session.problemes_resolts ?
        '<h4>Problemes Resolts:</h4><ul>' +
        session.problemes_resolts.map(p => `<li><strong>${p.problema}:</strong> ${p.solucio}</li>`).join('') +
        '</ul>' : '';

      const decisionsHTML = session.decisions_preses ?
        '<h4>Decisions Preses:</h4><ul>' +
        session.decisions_preses.map(d => {
          const adrLink = d.adr_relacionada ? ` <span class="adr-link">(ADR-${d.adr_relacionada})</span>` : '';
          return `<li><strong>${d.decisio}:</strong> ${d.justificacio}${adrLink}</li>`;
        }).join('') +
        '</ul>' : '';

      const techHTML = session.tecnologies_afegides ?
        '<h4>Tecnologies Afegides:</h4><ul>' +
        session.tecnologies_afegides.map(t => `<li><strong>${t.nom}:</strong> ${t.motiu}</li>`).join('') +
        '</ul>' : '';

      const deploysHTML = session.deployments ?
        '<h4>Deployments:</h4><ul>' +
        session.deployments.map(d => `<li><strong>${d.servei}:</strong> <a href="${d.url}" target="_blank">${d.url}</a></li>`).join('') +
        '</ul>' : '';

      const pendentsHTML = session.proxims_passos ?
        '<h4>Pròxims Passos:</h4><ul>' +
        session.proxims_passos.map(p => `<li>${p}</li>`).join('') +
        '</ul>' : '';

      return `
        <div class="session-card">
          <h3>${session.titol || session.id}</h3>
          <div class="session-meta">
            <span><strong>Data:</strong> ${session.data}</span>
            <span><strong>Durada:</strong> ${session.durada}</span>
            <span><strong>Participants:</strong> ${Array.isArray(session.participants) ? session.participants.join(', ') : session.participants}</span>
          </div>
          <p class="session-objective"><strong>Objectiu:</strong> ${session.objectiu}</p>
          ${featuresHTML}
          ${problemesHTML}
          ${decisionsHTML}
          ${techHTML}
          ${deploysHTML}
          ${pendentsHTML}
          ${session.notes_addicionals ? `<div class="session-notes"><h4>Notes Addicionals:</h4><pre>${session.notes_addicionals}</pre></div>` : ''}
        </div>
      `;
    }).join('');
    document.getElementById('fullSessions').innerHTML = sessionsHTML;
  } else {
    document.getElementById('fullSessions').innerHTML = '<p class="error">full/sessions.yaml not found</p>';
  }
}

// Helper per renderitzar dades estructurades
function renderValue(value, level = 0) {
  if (value === null || value === undefined) return '<em>N/A</em>';

  if (typeof value === 'string') {
    return value.includes('\n') ? `<pre class="multiline">${value}</pre>` : value;
  }

  if (typeof value === 'number' || typeof value === 'boolean') {
    return `<code>${value}</code>`;
  }

  if (Array.isArray(value)) {
    if (value.length === 0) return '<em>Empty</em>';
    return '<ul>' + value.map(item => `<li>${renderValue(item, level + 1)}</li>`).join('') + '</ul>';
  }

  if (typeof value === 'object') {
    return '<dl class="nested-data">' +
      Object.keys(value).map(k => `
        <dt><strong>${k}:</strong></dt>
        <dd>${renderValue(value[k], level + 1)}</dd>
      `).join('') +
      '</dl>';
  }

  return String(value);
}

// Render Project Status
function renderProjectStatus() {
  if (!projectStatusData) {
    document.getElementById('projectStatusContent').innerHTML = '<p class="error">project-status.yaml not found</p>';
    return;
  }

  // Render as structured data
  const html = Object.keys(projectStatusData).map(key => {
    const value = projectStatusData[key];
    return `
      <div class="card">
        <h3>${key.replace(/_/g, ' ').toUpperCase()}</h3>
        ${renderValue(value)}
      </div>
    `;
  }).join('');

  document.getElementById('projectStatusContent').innerHTML = html;
}

// Render Stats
function renderStats() {
  if (!contextData || !contextData.notes_compilacio) {
    return;
  }

  const notes = contextData.notes_compilacio;

  document.getElementById('statADRsTotal').textContent = notes.adrs_totals || '-';
  document.getElementById('statADRsFiltered').textContent = notes.adrs_incloses || '-';
  document.getElementById('statSessionsTotal').textContent = notes.sessions_totals || '-';

  if (contextData.metadata) {
    document.getElementById('statLastCompiled').textContent = contextData.metadata.ultima_compilacio || '-';
  }

  // Rough token estimation
  const contextStr = JSON.stringify(contextData);
  const tokens = Math.round(contextStr.length / 4); // Rough estimate
  document.getElementById('statContextTokens').textContent = tokens.toLocaleString();

  // Compilation notes
  document.getElementById('compilationNotes').innerHTML = `
    <p><strong>Criteris de filtratge:</strong> ${notes.criteris_filtratge || 'N/A'}</p>
  `;
}

// Initialize on load
window.addEventListener('DOMContentLoaded', loadData);
