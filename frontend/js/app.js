// ============================================================
// APP — logique principale du frontend
// ============================================================

let currentUserId = null;
let currentFilter = 'all';
let allGames = [];
let allTags = [];
let allUsers = [];

// ============================================================
// INITIALISATION
// ============================================================
document.addEventListener('DOMContentLoaded', async () => {
  setupNavigation();
  setupForms();
  setupFilters();

  await loadInitialData();
});

async function loadInitialData() {
  try {
    [allUsers, allGames, allTags] = await Promise.all([
      api.getUsers(),
      api.getGames(),
      api.getTags(),
    ]);

    // Sélecteur utilisateur en haut
    const select = document.getElementById('currentUser');
    select.innerHTML = allUsers
      .map(u => `<option value="${u.id}">${u.username}</option>`)
      .join('');

    if (allUsers.length > 0) {
      currentUserId = allUsers[0].id;
      select.addEventListener('change', e => {
        currentUserId = parseInt(e.target.value);
        loadDashboard();
      });
    }

    // Sélecteur jeu dans le form d'ajout au backlog
    document.getElementById('newGameId').innerHTML = allGames
      .map(g => `<option value="${g.id}">${g.title}</option>`)
      .join('');

    await loadDashboard();
    renderGames();
    renderUsers();
    renderTags();
  } catch (err) {
    showToast('Impossible de charger les données. L\'API tourne-t-elle ?', 'error');
    console.error(err);
  }
}

// ============================================================
// NAVIGATION ENTRE LES ONGLETS
// ============================================================
function setupNavigation() {
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tab = btn.dataset.tab;
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(tab).classList.add('active');
    });
  });
}

// ============================================================
// DASHBOARD (backlog + stats du user courant)
// ============================================================
async function loadDashboard() {
  if (!currentUserId) return;

  try {
    const [stats, backlog] = await Promise.all([
      api.getUserStats(currentUserId),
      api.getUserBacklog(currentUserId),
    ]);

    // Stats
    document.getElementById('statToPlay').textContent = stats.to_play || 0;
    document.getElementById('statPlaying').textContent = stats.playing || 0;
    document.getElementById('statFinished').textContent = stats.finished || 0;
    document.getElementById('statDropped').textContent = stats.dropped || 0;

    // Backlog
    renderBacklog(backlog);
  } catch (err) {
    showToast('Erreur de chargement du dashboard', 'error');
  }
}

function renderBacklog(entries) {
  const list = document.getElementById('backlogList');
  let filtered = entries;

  if (currentFilter !== 'all') {
    filtered = entries.filter(e => e.status === currentFilter);
  }

  if (filtered.length === 0) {
    list.innerHTML = '<div class="empty">Aucun jeu dans cette catégorie</div>';
    return;
  }

  list.innerHTML = filtered
    .map(e => `
      <div class="backlog-item status-${e.status}">
        <div class="status-indicator"></div>
        <div class="backlog-info">
          <div class="game-title">${e.game_title || 'Jeu inconnu'}</div>
          <div class="game-meta">
            ${e.review ? '« ' + escapeHtml(e.review) + ' »' : 'Aucun avis'}
          </div>
        </div>
        <div class="backlog-status">${formatStatus(e.status)}</div>
        <div class="backlog-rating">${e.rating != null ? e.rating + '/10' : '—'}</div>
        <button class="btn-delete" onclick="deleteEntry(${e.id})">×</button>
      </div>
    `)
    .join('');
}

function setupFilters() {
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.filter;
      loadDashboard();
    });
  });
}

async function deleteEntry(id) {
  if (!confirm('Retirer ce jeu du backlog ?')) return;
  try {
    await api.deleteBacklogEntry(id);
    showToast('Jeu retiré du backlog');
    loadDashboard();
  } catch (err) {
    showToast('Erreur lors de la suppression', 'error');
  }
}

// ============================================================
// FORMS
// ============================================================
function setupForms() {
  // Ajout au backlog
  document.getElementById('addBacklogForm').addEventListener('submit', async e => {
    e.preventDefault();
    if (!currentUserId) return showToast('Sélectionne un utilisateur', 'error');

    const data = {
      game_id: parseInt(document.getElementById('newGameId').value),
      status: document.getElementById('newStatus').value,
    };
    const rating = document.getElementById('newRating').value;
    const review = document.getElementById('newReview').value.trim();
    if (rating) data.rating = parseInt(rating);
    if (review) data.review = review;

    try {
      await api.addToBacklog(currentUserId, data);
      showToast('Jeu ajouté au backlog');
      e.target.reset();
      loadDashboard();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Toggle add game
  document.getElementById('showAddGame').addEventListener('click', () => {
    document.getElementById('addGameForm').classList.toggle('hidden');
  });
  document.getElementById('cancelAddGame').addEventListener('click', () => {
    document.getElementById('addGameForm').classList.add('hidden');
  });

  // Ajouter un jeu
  document.getElementById('addGameForm').addEventListener('submit', async e => {
    e.preventDefault();
    const data = {
      title: document.getElementById('gameTitle').value.trim(),
    };
    const dev = document.getElementById('gameDeveloper').value.trim();
    const year = document.getElementById('gameYear').value;
    if (dev) data.developer = dev;
    if (year) data.release_year = parseInt(year);

    try {
      await api.createGame(data);
      showToast(`Jeu "${data.title}" créé`);
      e.target.reset();
      document.getElementById('addGameForm').classList.add('hidden');
      allGames = await api.getGames();
      renderGames();
      // Mettre à jour le sélecteur de jeu
      document.getElementById('newGameId').innerHTML = allGames
        .map(g => `<option value="${g.id}">${g.title}</option>`)
        .join('');
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Toggle add user
  document.getElementById('showAddUser').addEventListener('click', () => {
    document.getElementById('addUserForm').classList.toggle('hidden');
  });
  document.getElementById('cancelAddUser').addEventListener('click', () => {
    document.getElementById('addUserForm').classList.add('hidden');
  });

  // Ajouter un user
  document.getElementById('addUserForm').addEventListener('submit', async e => {
    e.preventDefault();
    const data = {
      email: document.getElementById('userEmail').value.trim(),
      username: document.getElementById('userUsername').value.trim(),
    };

    try {
      await api.createUser(data);
      showToast(`Utilisateur "${data.username}" créé`);
      e.target.reset();
      document.getElementById('addUserForm').classList.add('hidden');
      allUsers = await api.getUsers();
      renderUsers();
      // Mettre à jour le sélecteur en haut
      const select = document.getElementById('currentUser');
      select.innerHTML = allUsers
        .map(u => `<option value="${u.id}">${u.username}</option>`)
        .join('');
    } catch (err) {
      showToast(err.message, 'error');
    }
  });

  // Ajouter un tag
  document.getElementById('addTagForm').addEventListener('submit', async e => {
    e.preventDefault();
    const name = document.getElementById('tagName').value.trim();
    if (!name) return;

    try {
      await api.createTag({ name });
      showToast(`Tag "${name}" créé`);
      e.target.reset();
      allTags = await api.getTags();
      renderTags();
    } catch (err) {
      showToast(err.message, 'error');
    }
  });
}

// ============================================================
// GAMES
// ============================================================
function renderGames() {
  const list = document.getElementById('gamesList');

  if (allGames.length === 0) {
    list.innerHTML = '<div class="empty">Aucun jeu en base</div>';
    return;
  }

  list.innerHTML = allGames
    .map(g => `
      <div class="game-card">
        <div class="game-id">#${g.id.toString().padStart(3, '0')}</div>
        <div class="game-title">${escapeHtml(g.title)}</div>
        <div class="game-meta">
          ${g.developer ? escapeHtml(g.developer) : 'Dev inconnu'}
          ${g.release_year ? ' · ' + g.release_year : ''}
        </div>
        <div class="game-tags">
          ${g.tags && g.tags.length > 0
            ? g.tags.map(t => `<span class="tag-chip">${escapeHtml(t)}</span>`).join('')
            : '<span style="color: var(--text-dim); font-size: 11px; font-family: var(--font-mono);">Sans tag</span>'}
        </div>
      </div>
    `)
    .join('');
}

// ============================================================
// USERS
// ============================================================
function renderUsers() {
  const list = document.getElementById('usersList');

  if (allUsers.length === 0) {
    list.innerHTML = '<div class="empty">Aucun utilisateur</div>';
    return;
  }

  list.innerHTML = allUsers
    .map(u => `
      <div class="user-card">
        <div class="user-header">
          <div class="user-avatar">${u.username.substring(0, 2).toUpperCase()}</div>
          <div>
            <div class="user-name">${escapeHtml(u.username)}</div>
            <div class="user-email">${escapeHtml(u.email)}</div>
          </div>
        </div>
        <div class="user-profile">
          ${u.profile ? `
            <div>${u.profile.bio ? '« ' + escapeHtml(u.profile.bio) + ' »' : 'Pas de bio'}</div>
            ${u.profile.favorite_platform
              ? `<span class="profile-platform">${escapeHtml(u.profile.favorite_platform)}</span>`
              : ''}
          ` : '<em style="color: var(--text-dim);">Pas de profil configuré</em>'}
        </div>
      </div>
    `)
    .join('');
}

// ============================================================
// TAGS
// ============================================================
function renderTags() {
  const list = document.getElementById('tagsList');

  if (allTags.length === 0) {
    list.innerHTML = '<div class="empty">Aucun tag créé</div>';
    return;
  }

  list.innerHTML = allTags
    .map(t => `<div class="tag-cloud-item">${escapeHtml(t.name)}</div>`)
    .join('');
}

// ============================================================
// UTILS
// ============================================================
function formatStatus(s) {
  return ({
    to_play: 'À JOUER',
    playing: 'EN COURS',
    finished: 'FINI',
    dropped: 'ABANDONNÉ',
  })[s] || s;
}

function escapeHtml(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className = 'toast show' + (type === 'error' ? ' error' : '');
  setTimeout(() => toast.classList.remove('show'), 3000);
}
