// ============================================================
// API CLIENT — communication avec l'API Flask
// ============================================================

const API_URL = 'http://localhost:5000';

const api = {
  // ===== USERS =====
  async getUsers() {
    const res = await fetch(`${API_URL}/users`);
    return res.json();
  },

  async getUser(id) {
    const res = await fetch(`${API_URL}/users/${id}`);
    if (!res.ok) throw new Error('User not found');
    return res.json();
  },

  async createUser(data) {
    const res = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.erreur || 'Erreur');
    return json;
  },

  async updateProfile(userId, profile) {
    const res = await fetch(`${API_URL}/users/${userId}/profile`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.erreur || 'Erreur');
    return json;
  },

  // ===== GAMES =====
  async getGames() {
    const res = await fetch(`${API_URL}/games`);
    return res.json();
  },

  async createGame(data) {
    const res = await fetch(`${API_URL}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.erreur || 'Erreur');
    return json;
  },

  async deleteGame(id) {
    const res = await fetch(`${API_URL}/games/${id}`, { method: 'DELETE' });
    return res.json();
  },

  async addTagToGame(gameId, tagId) {
    const res = await fetch(`${API_URL}/games/${gameId}/tags/${tagId}`, {
      method: 'POST',
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.erreur || 'Erreur');
    return json;
  },

  async removeTagFromGame(gameId, tagId) {
    const res = await fetch(`${API_URL}/games/${gameId}/tags/${tagId}`, {
      method: 'DELETE',
    });
    return res.json();
  },

  // ===== TAGS =====
  async getTags() {
    const res = await fetch(`${API_URL}/tags`);
    return res.json();
  },

  async createTag(data) {
    const res = await fetch(`${API_URL}/tags`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.erreur || 'Erreur');
    return json;
  },

  // ===== BACKLOG =====
  async getUserBacklog(userId, status = null) {
    const url = status
      ? `${API_URL}/users/${userId}/backlog?status=${status}`
      : `${API_URL}/users/${userId}/backlog`;
    const res = await fetch(url);
    return res.json();
  },

  async addToBacklog(userId, data) {
    const res = await fetch(`${API_URL}/users/${userId}/backlog`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.erreur || 'Erreur');
    return json;
  },

  async updateBacklogEntry(id, data) {
    const res = await fetch(`${API_URL}/backlog/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.erreur || 'Erreur');
    return json;
  },

  async deleteBacklogEntry(id) {
    const res = await fetch(`${API_URL}/backlog/${id}`, { method: 'DELETE' });
    return res.json();
  },

  async getUserStats(userId) {
    const res = await fetch(`${API_URL}/users/${userId}/stats`);
    return res.json();
  },
};
