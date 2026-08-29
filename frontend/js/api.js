/**
 * Shared API client. Base URL points at the local Flask backend.
 * Change API_BASE if you run the backend on a different host/port.
 */
const API_BASE = "http://localhost:5000/api";

const Auth = {
  getToken() { return localStorage.getItem("wb_token"); },
  getUser() {
    const raw = localStorage.getItem("wb_user");
    return raw ? JSON.parse(raw) : null;
  },
  setSession(authResponse) {
    localStorage.setItem("wb_token", authResponse.token);
    localStorage.setItem("wb_user", JSON.stringify({
      id: authResponse.userId,
      name: authResponse.name,
      email: authResponse.email,
      role: authResponse.role,
    }));
  },
  clearSession() {
    localStorage.removeItem("wb_token");
    localStorage.removeItem("wb_user");
  },
  isLoggedIn() { return !!this.getToken(); },
  isAdmin() { const u = this.getUser(); return u && u.role === "ADMIN"; },
};

/**
 * Wrapper around fetch() that adds the JWT header, base URL, and JSON handling.
 * Returns the parsed JSON body. Throws an Error with .message set to the API's
 * error message on non-2xx responses.
 */
async function apiRequest(path, { method = "GET", body = null } = {}) {
  const headers = { "Content-Type": "application/json" };
  const token = Auth.getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (err) {
    throw new Error("Could not reach the backend. Is the Flask server running on http://localhost:5000?");
  }

  let data = null;
  try { data = await response.json(); } catch { /* empty body is fine */ }

  if (!response.ok) {
    if (response.status === 401) {
      // Token missing/expired/invalid - clear it so the UI doesn't get stuck in a broken state
      Auth.clearSession();
    }
    const message = (data && data.message) || `Request failed (${response.status})`;
    throw new Error(message);
  }

  return data;
}

const Api = {
  register: (payload) => apiRequest("/auth/register", { method: "POST", body: payload }),
  login: (payload) => apiRequest("/auth/login", { method: "POST", body: payload }),

  getProfile: () => apiRequest("/profile"),
  saveProfile: (payload) => apiRequest("/profile", { method: "PUT", body: payload }),

  listSchemes: () => apiRequest("/schemes"),
  getScheme: (id) => apiRequest(`/schemes/${id}`),

  checkEligibility: () => apiRequest("/eligibility/check"),
  checkOne: (id) => apiRequest(`/eligibility/check/${id}`),

  listSaved: () => apiRequest("/saved"),
  saveScheme: (id) => apiRequest(`/saved/${id}`, { method: "POST" }),
  unsaveScheme: (id) => apiRequest(`/saved/${id}`, { method: "DELETE" }),

  adminCreateScheme: (payload) => apiRequest("/admin/schemes", { method: "POST", body: payload }),
  adminUpdateScheme: (id, payload) => apiRequest(`/admin/schemes/${id}`, { method: "PUT", body: payload }),
  adminDeleteScheme: (id) => apiRequest(`/admin/schemes/${id}`, { method: "DELETE" }),
  adminStats: () => apiRequest("/admin/stats"),
};
