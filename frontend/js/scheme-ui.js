/**
 * Shared rendering helpers for scheme cards and the scheme detail modal.
 * Used by dashboard.html and saved.html.
 */

function statusClass(status) {
  return status === "Eligible" ? "wb-status-eligible" : status === "Maybe Eligible" ? "wb-status-maybe" : "wb-status-not";
}
function statusIcon(status) {
  return status === "Eligible" ? "✓" : status === "Maybe Eligible" ? "✦" : "✕";
}
function matchClass(pct) {
  return pct >= 80 ? "wb-match-high" : pct >= 50 ? "wb-match-mid" : "wb-match-low";
}

function renderSchemeCard(result, onOpenName, onToggleSaveName) {
  const isSaved = !!result.saved;
  return `
    <div class="col-md-6">
      <div class="wb-scheme-card" onclick="${onOpenName}(${result.id})">
        <div class="d-flex justify-content-between align-items-start mb-2 gap-2">
          <div>
            <div class="wb-scheme-name">${escapeHtml(result.name)}</div>
            <div class="wb-scheme-dept">${escapeHtml(result.department)}</div>
          </div>
          <div class="wb-match-badge ${matchClass(result.matchPercent)} mono">${result.matchPercent}% match</div>
        </div>
        <span class="wb-status-tag ${statusClass(result.status)}">${statusIcon(result.status)} ${result.status}</span>
        <div class="wb-scheme-benefit">${escapeHtml(result.benefit)}</div>
        <div class="wb-scheme-foot">
          <span class="wb-tag-cat">${escapeHtml(result.category)}</span>
          <button class="wb-save-btn ${isSaved ? 'saved' : ''}" onclick="event.stopPropagation(); ${onToggleSaveName}(${result.id})">${isSaved ? '★' : '☆'}</button>
        </div>
      </div>
    </div>
  `;
}

function openSchemeModal(result, onToggleSave) {
  window._modalToggleSaveHandler = onToggleSave;
  let modalEl = document.getElementById("scheme-modal");
  if (!modalEl) {
    modalEl = document.createElement("div");
    modalEl.id = "scheme-modal";
    modalEl.className = "modal fade";
    modalEl.tabIndex = -1;
    document.body.appendChild(modalEl);
  }

  const hasEval = result.status !== undefined;

  modalEl.innerHTML = `
    <div class="modal-dialog modal-dialog-scrollable" style="max-width:620px;">
      <div class="modal-content" style="border-radius:14px; border:none;">
        <div class="modal-header" style="border-bottom:1px solid var(--gray-100);">
          <div>
            <div style="font-size:12px; color:var(--gray-400); margin-bottom:4px;">${escapeHtml(result.department)} · ${escapeHtml(result.category)}</div>
            <div style="font-size:18px; font-weight:800; color:var(--gray-900);">${escapeHtml(result.name)}</div>
          </div>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          ${hasEval ? `
          <div class="wb-modal-section mb-3">
            <span class="wb-status-tag ${statusClass(result.status)}">${statusIcon(result.status)} ${result.status} — ${result.matchPercent}% match</span>
            <div class="wb-explain-box mt-2">${escapeHtml(result.explanation)}</div>
          </div>
          <div class="wb-modal-section mb-3">
            <h6>Eligibility breakdown</h6>
            ${(result.criteria && result.criteria.length) ? result.criteria.map(c => `
              <div class="wb-reason-row">
                <span style="color:${c.pass ? 'var(--green-600)' : 'var(--red-600)'}">${c.pass ? '✓' : '✕'}</span>
                ${escapeHtml(c.label)}
              </div>`).join("") : `<div class="wb-reason-row">✓ No specific age, income, or occupation restriction — open to all applicants.</div>`}
          </div>` : ""}
          <div class="wb-modal-section mb-3">
            <h6>Benefit</h6>
            <div style="font-size:13.5px; color:var(--gray-700); line-height:1.6;">${escapeHtml(result.benefit)}</div>
          </div>
          <div class="wb-modal-section mb-3">
            <h6>About this scheme</h6>
            <div style="font-size:13.5px; color:var(--gray-700); line-height:1.6;">${escapeHtml(result.description)}</div>
          </div>
          <div class="wb-modal-section mb-3">
            <h6>Required documents</h6>
            <div>${result.documents.map(d => `<span class="wb-doc-chip">📄 ${escapeHtml(d)}</span>`).join("")}</div>
          </div>
          <div class="wb-modal-section mb-0">
            <div class="wb-kv"><span class="k">Application deadline</span><span class="v">${escapeHtml(result.deadline)}</span></div>
          </div>
        </div>
        <div class="modal-footer" style="border-top:1px solid var(--gray-100);">
          <button class="btn btn-wb-outline" id="modal-save-btn" onclick="modalToggleSave(${result.id})">${result.saved ? "Remove from saved" : "Save scheme"}</button>
          <a class="btn btn-wb-accent" href="${result.applyLink}" target="_blank" rel="noopener noreferrer">Apply on official portal →</a>
        </div>
      </div>
    </div>
  `;

  const modal = new bootstrap.Modal(modalEl);
  modal.show();
}

function modalToggleSave(schemeId) {
  if (window._modalToggleSaveHandler) window._modalToggleSaveHandler(schemeId);
}
