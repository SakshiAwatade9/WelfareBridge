/**
 * Renders the top navigation into <div id="wb-navbar"></div>, present on every page.
 * Call renderNavbar("dashboard") etc. passing the current page's key so the matching
 * nav link gets the "active" style.
 */
function renderNavbar(activePage) {
  const root = document.getElementById("wb-navbar");
  if (!root) return;

  const user = Auth.getUser();
  const links = [];

  if (user && user.role === "USER") {
    links.push({ key: "dashboard", label: "Dashboard", href: "dashboard.html" });
    links.push({ key: "saved", label: "Saved Schemes", href: "saved.html" });
  }
  if (user && user.role === "ADMIN") {
    links.push({ key: "admin", label: "Admin", href: "admin.html" });
  }

  const linksHtml = links.map(l =>
    `<a class="wb-nav-link ${activePage === l.key ? "active" : ""}" href="${l.href}">${l.label}</a>`
  ).join("");

  const rightHtml = user
    ? `
      <span class="wb-badge-role d-none d-sm-inline">${escapeHtml(user.name)}</span>
      <button class="btn btn-wb-outline btn-sm" onclick="logout()">Log out</button>
    `
    : `<a class="btn btn-wb-outline btn-sm" href="auth.html">Log in</a>`;

  root.innerHTML = `
    <nav class="wb-topnav">
      <div class="container d-flex align-items-center justify-content-between" style="height:64px;">
        <a href="index.html" class="wb-brand">
          <span class="wb-brand-mark">
            <svg viewBox="0 0 20 20" width="16" height="16" fill="none">
              <path d="M10 2L17 5.5V10c0 4.5-3 7.5-7 8-4-.5-7-3.5-7-8V5.5L10 2z" fill="white" fill-opacity=".95"/>
              <path d="M7 10l2 2 4-4" stroke="#3b6ef6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          WelfareBridge
        </a>
        <div class="d-flex align-items-center gap-2">
          ${linksHtml}
          ${rightHtml}
        </div>
      </div>
    </nav>
  `;
}

function logout() {
  Auth.clearSession();
  window.location.href = "index.html";
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.innerText = str == null ? "" : str;
  return div.innerHTML;
}

/**
 * Redirects to auth.html if not logged in, or to index.html if logged in with the
 * wrong role. Call at the top of any protected page's script.
 * Returns the current user object if allowed to proceed, or null (and redirects) if not.
 */
function requireRole(role) {
  const user = Auth.getUser();
  if (!user) {
    window.location.href = "auth.html";
    return null;
  }
  if (role && user.role !== role) {
    window.location.href = "index.html";
    return null;
  }
  return user;
}
