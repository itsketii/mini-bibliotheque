/* Configuration API */
const API = "http://localhost:5000";

/* Catégories */
const CATS = [
  {key:"books",  label:"Livres",   icon:"📚", endpoint:"/books", authorField:"author", authorLabel:"Auteur"},
  {key:"movies", label:"Films",    icon:"🎬", endpoint:"/movies", authorField:"director", authorLabel:"Réalisateur"},
  {key:"shows",  label:"Séries",   icon:"📺", endpoint:"/shows", authorField:"creator", authorLabel:"Créateur"},
  {key:"games",  label:"Jeux",     icon:"🎮", endpoint:"/games", authorField:"developer", authorLabel:"Développeur"},
  {key:"music",  label:"Musiques", icon:"🎵", endpoint:"/music", authorField:"artist", authorLabel:"Artiste"},
  {key:"manga",  label:"Manga",    icon:"📖", endpoint:"/manga", authorField:"author", authorLabel:"Auteur"},
];

/* Thèmes */
const THEMES = [
  {id:"rose",  label:"Rose",  swatch:"#fff5f7"},
  {id:"rouge", label:"Rouge", swatch:"#ffffff"},
  {id:"or",    label:"Or",    swatch:"#fefdf4"},
  {id:"nuit",  label:"Nuit",  swatch:"#18181c"},
];

/* État global */
const S = {
  view: "home",
  data: { books:[], movies:[], shows:[], games:[], music:[], manga:[] },
  genres: {},
  search: "",
  filter: "Tous",
  formNote: 0,
};

/* ── SIDEBAR RÉTRACTABLE ── */
const sidebarEl = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");

function setSidebarCollapsed(collapsed){
  sidebarEl.classList.toggle("collapsed", collapsed);
  sidebarToggle.textContent = collapsed ? "›" : "‹";
  localStorage.setItem("kety_sidebar_collapsed", String(collapsed));
}

sidebarToggle.addEventListener("click", ()=> setSidebarCollapsed(!sidebarEl.classList.contains("collapsed")));

(function(){
  const saved = localStorage.getItem("kety_sidebar_collapsed");
  setSidebarCollapsed(saved !== null ? saved === "true" : window.innerWidth < 768);
})();

/* ── THÈME ── */
function renderThemeOptions(){
  const wrap = document.getElementById("theme-options");
  const current = document.documentElement.getAttribute("data-theme");
  wrap.innerHTML = THEMES.map(t => `
    <button type="button" class="theme-dot" data-theme-choice="${t.id}" style="background:${t.swatch}"
      title="${t.label}" aria-pressed="${current===t.id}"></button>
  `).join("");
  wrap.querySelectorAll(".theme-dot").forEach(btn=>{
    btn.addEventListener("click", ()=> applyTheme(btn.dataset.themeChoice));
  });
}

function applyTheme(themeId){
  document.documentElement.setAttribute("data-theme", themeId);
  localStorage.setItem("kety_theme", themeId);
  document.querySelectorAll(".theme-dot").forEach(btn=>{
    btn.setAttribute("aria-pressed", String(btn.dataset.themeChoice === themeId));
  });
}

renderThemeOptions();
applyTheme(localStorage.getItem("kety_theme") || "rose");

/* ── API: CHARGER LES GENRES ── */
async function loadGenres(){
  try {
    const res = await fetch(API + "/genres");
    if(!res.ok) throw new Error();
    S.genres = await res.json();
    console.log("✅ Genres chargés", S.genres);
  } catch (err) {
    console.log("⚠️ Genres non disponibles:", err);
  }
}

/* ── API: CHARGER TOUTES LES DONNÉES ── */
async function loadAllData(){
  console.log("📥 Chargement des données...");
  const promises = CATS.map(cat => 
    fetch(API + cat.endpoint)
      .then(r => {
        if(!r.ok) throw new Error(`Erreur ${r.status}`);
        return r.json();
      })
      .then(data => { 
        S.data[cat.key] = Array.isArray(data) ? data : [];
        console.log(`✅ ${cat.label} chargés:`, S.data[cat.key].length);
      })
      .catch(err => { 
        console.log(`⚠️ Erreur ${cat.label}:`, err);
        S.data[cat.key] = []; 
      })
  );
  await Promise.all(promises);
  render();
}

/* ── NAVIGATION ── */
function buildNav(){
  const nav = document.getElementById("nav");
  nav.querySelectorAll(".cat-nav-btn").forEach(e=>e.remove());
  CATS.forEach(cat => {
    const btn = document.createElement("button");
    btn.className = "nav-btn cat-nav-btn" + (S.view===cat.key ? " active" : "");
    btn.dataset.view = cat.key;
    btn.innerHTML = `<span class="icon">${cat.icon}</span><span class="nav-text">${cat.label}</span><span class="count">${S.data[cat.key]?.length||0}</span>`;
    btn.addEventListener("click", ()=> navigateTo(cat.key));
    nav.appendChild(btn);
  });
  document.getElementById("nav-home").classList.toggle("active", S.view==="home");
}

function navigateTo(view){
  S.view = view;
  S.search = "";
  S.filter = "Tous";
  document.getElementById("search-input").value = "";
  render();
}

document.getElementById("nav-home").addEventListener("click", ()=> navigateTo("home"));

/* ── UTILITAIRES DE RENDU ── */
function statusBadge(s){
  if(!s) return "";
  const done = ["Lu","Vu","Terminé","Écouté"];
  if(done.includes(s)) return `<span class="badge badge-done">${s}</span>`;
  if(s==="En cours") return `<span class="badge badge-progress">${s}</span>`;
  return `<span class="badge badge-todo">${s}</span>`;
}

function starsView(n){
  return Array.from({length:5},(_,i)=> `<span class="star ${i<n?'':'off'}">★</span>`).join("");
}

function starsInput(n){
  return Array.from({length:5},(_,i)=>
    `<button type="button" class="star-btn ${i<n?'filled':''}" onclick="setFormNote(${i+1})">★</button>`
  ).join("");
}

function esc(s){ 
  return String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); 
}

function getAuthorField(cat){
  return CATS.find(c=>c.key===cat)?.authorField || "author";
}

function getAuthorLabel(cat){
  return CATS.find(c=>c.key===cat)?.authorLabel || "Auteur";
}

function getGenreName(cat, genreId){
  const genres = S.genres[cat] || [];
  const genre = genres.find(g => g.id === genreId);
  return genre?.name || "Inconnu";
}

function cardHTML(item, cat){
  const af = getAuthorField(cat);
  const author = item[af] || "";
  const catInfo = CATS.find(c=>c.key===cat);
  return `
  <div class="card">
    <div class="card-top">
      <div class="card-icon">${catInfo.icon}</div>
      <div class="card-actions">
        <button class="card-action-btn" onclick="openEdit(${item.id},'${cat}')" title="Modifier">✏️</button>
        <button class="card-action-btn" onclick="openDelete(${item.id},'${cat}')" title="Supprimer">🗑️</button>
      </div>
    </div>
    <h3>${esc(item.title)}</h3>
    ${author ? `<p class="author">${esc(author)}</p>` : ""}
    <div class="badges">
      ${statusBadge(item.status)}
      ${item.genre_id ? `<span class="badge badge-genre">${esc(getGenreName(cat, item.genre_id))}</span>` : ""}
      ${item.year ? `<span class="badge badge-genre">${item.year}</span>` : ""}
    </div>
    ${item.rating ? `<div class="stars-row">${starsView(item.rating)}</div>` : ""}
  </div>`;
}

/* ── RENDU PRINCIPAL ── */
function render(){
  const catInfo = CATS.find(c=>c.key===S.view);
  const headerIcon = document.getElementById("header-icon");
  const headerTitle = document.getElementById("header-title-text");
  const headerSub = document.getElementById("header-sub");
  const addBtn = document.getElementById("add-btn");
  const filtersEl = document.getElementById("filters");
  const content = document.getElementById("content");

  if(S.view==="home"){
    headerIcon.textContent = "🏠";
    headerTitle.textContent = "Accueil";
    headerSub.textContent = "";
    addBtn.style.display = "none";
    filtersEl.style.display = "none";
    content.innerHTML = renderHome();
  } else {
    headerIcon.textContent = catInfo.icon;
    headerTitle.textContent = catInfo.label;
    const items = S.data[S.view]||[];
    headerSub.textContent = items.length + " entrée" + (items.length!==1?"s":"");
    addBtn.style.display = "";
    filtersEl.style.display = "";
    renderFilters();
    content.innerHTML = renderCatView();
  }
  buildNav();
}

function renderHome(){
  const all = CATS.flatMap(c=> (S.data[c.key]||[]).map(i=>({...i,_cat:c.key})));
  const total = all.length;
  const done = all.filter(i=>["Lu","Vu","Terminé","Écouté"].includes(i.status||"")).length;
  const inProg = all.filter(i=>i.status==="En cours").length;
  const recent = [...all].slice(-8).reverse();

  return `
  <section class="home-section">
    <p class="section-label">Vue d'ensemble</p>
    <div class="stats-row">
      <div class="stat-card"><p>Total</p><div class="num">${total}</div></div>
      <div class="stat-card"><p>Terminés</p><div class="num green">${done}</div></div>
      <div class="stat-card"><p>En cours</p><div class="num purple">${inProg}</div></div>
    </div>
    <div class="cat-grid">
      ${CATS.map(c=>`
        <button class="cat-tile" onclick="navigateTo('${c.key}')">
          <span class="tile-icon">${c.icon}</span>
          <span class="tile-label">${c.label}</span>
          <div class="tile-count">${(S.data[c.key]||[]).length}</div>
        </button>
      `).join("")}
    </div>
  </section>

  ${recent.length ? `
  <section class="home-section">
    <p class="section-label">Entrées récentes</p>
    <div class="cards-grid">${recent.map(i=>cardHTML(i,i._cat)).join("")}</div>
  </section>` : ""}
  `;
}

function renderFilters(){
  const statusOpts = {
    books:  ["À lire","En cours","Lu"],
    movies: ["À voir","Vu"],
    shows:  ["À voir","En cours","Terminé"],
    games:  ["À faire","En cours","Terminé"],
    music:  ["À écouter","Écouté"],
    manga:  ["À lire","En cours","Lu"],
  };
  const opts = ["Tous", ...(statusOpts[S.view]||[])];
  const pills = document.getElementById("filter-pills");
  pills.innerHTML = opts.map(s=>`<button type="button" class="pill ${S.filter===s?'active':''}" onclick="setFilter('${s}')">${s}</button>`).join("");
}

function setFilter(f){ S.filter = f; renderCatContent(); }
document.getElementById("search-input").addEventListener("input", e=>{ S.search = e.target.value; renderCatContent(); });

function renderCatContent(){ 
  document.getElementById("content").innerHTML = renderCatView(); 
}

function renderCatView(){
  const items = S.data[S.view]||[];
  const q = S.search.toLowerCase();
  const filtered = items.filter(i=>{
    const matchSearch = !q || Object.values(i).some(v=>String(v).toLowerCase().includes(q));
    const matchStatus = S.filter==="Tous" || i.status===S.filter;
    return matchSearch && matchStatus;
  });
  const catInfo = CATS.find(c=>c.key===S.view);
  if(!filtered.length) return `
    <div class="empty">
      <span class="icon">${catInfo.icon}</span>
      <h3>${S.search||S.filter!=="Tous" ? "Aucun résultat" : "Aucun "+catInfo.label.toLowerCase()}</h3>
      <p>${S.search||S.filter!=="Tous" ? "Essaie d'autres filtres" : "Clique sur + Ajouter pour commencer"}</p>
    </div>`;
  return `<div class="cards-grid">${filtered.map(i=>cardHTML(i,S.view)).join("")}</div>`;
}

/* ── MODAL ── */
function openModal(title, bodyHTML){
  document.getElementById("modal-title").textContent = title;
  document.getElementById("modal-body").innerHTML = bodyHTML;
  document.getElementById("modal").style.display = "flex";
}

function closeModal(){ 
  document.getElementById("modal").style.display = "none"; 
}

document.getElementById("modal-close").addEventListener("click", closeModal);
document.getElementById("modal").addEventListener("click", e=>{ if(e.target.id==="modal") closeModal(); });
document.addEventListener("keydown", e=>{ if(e.key==="Escape") closeModal(); });

/* ── FORMULAIRE ── */
function setFormNote(n){
  S.formNote = n;
  document.querySelectorAll(".star-btn").forEach((b,i)=> b.classList.toggle("filled", i<n));
}

function openAdd(cat){
  const catInfo = CATS.find(c=>c.key===cat);
  S.formNote = 0;
  openModal("Ajouter — " + catInfo.label, formHTML(cat, null));
}

function formHTML(cat, item){
  const af = getAuthorField(cat);
  const al = getAuthorLabel(cat);
  const statusOpts = {
    books:  ["À lire","En cours","Lu"],
    movies: ["À voir","Vu"],
    shows:  ["À voir","En cours","Terminé"],
    games:  ["À faire","En cours","Terminé"],
    music:  ["À écouter","Écouté"],
    manga:  ["À lire","En cours","Lu"],
  };
  const opts = statusOpts[cat] || [];
  const val = (k) => item ? esc(item[k]||"") : "";
  const selStat = item ? item.status : opts[0];
  S.formNote = item ? (item.rating||0) : 0;
  
  const genres = S.genres[cat] || [];
  const genreId = item ? item.genre_id : "";

  let specFields = "";
  if(cat==="games"){
    specFields = `
      <div class="form-group">
        <label class="form-label">Éditeur</label>
        <input class="form-input" id="f-editor" value="${item?esc(item.editor||''):''}">
      </div>
      <div class="form-group">
        <label class="form-label">Plateforme</label>
        <input class="form-input" id="f-platform" value="${item?esc(item.platform||''):''}">
      </div>
      <div class="form-group">
        <label class="form-label">Heures jouées</label>
        <input class="form-input" id="f-hours" type="number" value="${item?item.hours_played||'':''}">
      </div>`;
  } else if(cat==="shows"){
    specFields = `
      <div class="form-group">
        <label class="form-label">Année de fin</label>
        <input class="form-input" id="f-end-year" type="number" value="${item?item.end_year||'':''}">
      </div>
      <div class="form-group">
        <label class="form-label">Nombre de saisons</label>
        <input class="form-input" id="f-seasons" type="number" value="${item?item.nb_seasons||'':''}">
      </div>
      <div class="form-group">
        <label class="form-label">Saison actuelle</label>
        <input class="form-input" id="f-actual-season" type="number" value="${item?item.actual_season||'':''}">
      </div>
      <div class="form-group">
        <label class="form-label">Épisode actuel</label>
        <input class="form-input" id="f-actual-episode" type="number" value="${item?item.actual_episode||'':''}">
      </div>`;
  } else if(cat==="movies"){
    specFields = `
      <div class="form-group">
        <label class="form-label">Durée (minutes)</label>
        <input class="form-input" id="f-duration" type="number" value="${item?item.duration||'':''}">
      </div>`;
  } else if(cat==="music"){
    specFields = `
      <div class="form-group">
        <label class="form-label">Album</label>
        <input class="form-input" id="f-album" value="${item?esc(item.album||''):''}">
      </div>
      <div class="form-group">
        <label class="form-label">Mood/Playlist</label>
        <input class="form-input" id="f-mood" value="${item?esc(item.playlist_mood||''):''}">
      </div>`;
  } else if(cat==="manga"){
    specFields = `
      <div class="form-group">
        <label class="form-label">Nombre de chapitres</label>
        <input class="form-input" id="f-chapters" type="number" value="${item?item.nb_chapters||'':''}">
      </div>
      <div class="form-group">
        <label class="form-label">Chapitre actuel</label>
        <input class="form-input" id="f-actual-chapter" type="number" value="${item?item.actual_chapter||'':''}">
      </div>
      <div class="form-group">
        <label class="form-label">Nombre de volumes</label>
        <input class="form-input" id="f-volumes" type="number" value="${item?item.nb_volumes||'':''}">
      </div>
      <div class="form-group">
        <label class="form-label">Volume actuel</label>
        <input class="form-input" id="f-actual-volume" type="number" value="${item?item.actual_volume||'':''}">
      </div>`;
  }

  return `
  <form onsubmit="return handleFormSubmit(event, '${cat}', ${item ? item.id : 'null'})">
    <div class="form-group">
      <label class="form-label">Titre *</label>
      <input class="form-input" id="f-title" value="${val('title')}" required>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label class="form-label">${al}</label>
        <input class="form-input" id="f-author" value="${val(af)}">
      </div>
      <div class="form-group">
        <label class="form-label">Année</label>
        <input class="form-input" id="f-year" type="number" value="${item?item.year||'':''}">
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label class="form-label">Genre</label>
        <select class="form-input" id="f-genre-id">
          <option value="">-- Choisir --</option>
          ${genres.map(g=>`<option value="${g.id}" ${genreId==g.id?'selected':''}>${esc(g.name)}</option>`).join("")}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Statut</label>
        <select class="form-input" id="f-status">
          ${opts.map(o=>`<option value="${o}" ${selStat===o?'selected':''}>${o}</option>`).join("")}
        </select>
      </div>
    </div>
    ${specFields}
    <div class="form-group">
      <label class="form-label">Note</label>
      <div class="stars-input">${starsInput(S.formNote)}</div>
    </div>
    <div class="form-group">
      <label class="form-label">Description/Avis</label>
      <textarea class="form-input" id="f-review">${val('review')}</textarea>
    </div>
    <div class="form-actions">
      <button type="submit" class="btn-save">${item ? "Enregistrer" : "Ajouter"}</button>
      <button type="button" class="btn-cancel" onclick="closeModal()">Annuler</button>
    </div>
  </form>`;
}

async function handleFormSubmit(e, cat, id){
  e.preventDefault();
  const af = getAuthorField(cat);
  const item = { 
    title: document.getElementById("f-title").value.trim(),
    user_id: 1,
  };
  if(!item.title) return false;
  
  item[af] = document.getElementById("f-author").value || null;
  item.year = parseInt(document.getElementById("f-year").value) || null;
  item.genre_id = parseInt(document.getElementById("f-genre-id").value) || null;
  item.status = document.getElementById("f-status").value || null;
  item.rating = S.formNote || null;
  item.review = document.getElementById("f-review").value || null;
  
  // Champs spécifiques
  if(cat==="games"){
    item.editor = document.getElementById("f-editor").value || null;
    item.platform = document.getElementById("f-platform").value || null;
    item.hours_played = parseInt(document.getElementById("f-hours").value) || null;
  } else if(cat==="shows"){
    item.end_year = parseInt(document.getElementById("f-end-year").value) || null;
    item.nb_seasons = parseInt(document.getElementById("f-seasons").value) || null;
    item.actual_season = parseInt(document.getElementById("f-actual-season").value) || null;
    item.actual_episode = parseInt(document.getElementById("f-actual-episode").value) || null;
  } else if(cat==="movies"){
    item.duration = parseInt(document.getElementById("f-duration").value) || null;
  } else if(cat==="music"){
    item.album = document.getElementById("f-album").value || null;
    item.playlist_mood = document.getElementById("f-mood").value || null;
  } else if(cat==="manga"){
    item.nb_chapters = parseInt(document.getElementById("f-chapters").value) || null;
    item.actual_chapter = parseInt(document.getElementById("f-actual-chapter").value) || null;
    item.nb_volumes = parseInt(document.getElementById("f-volumes").value) || null;
    item.actual_volume = parseInt(document.getElementById("f-actual-volume").value) || null;
  }

  if(id){ 
    item.id = id; 
    await apiEdit(item, cat); 
  } else { 
    const now = new Date().toISOString().split('T')[0];
    item.added = now;
    await apiAdd(item, cat); 
  }
  return false;
}

/* ── API: AJOUTER ── */
async function apiAdd(item, cat){
  const endpoint = CATS.find(c=>c.key===cat).endpoint;
  try{
    const res = await fetch(API+endpoint,{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify(item)
    });
    if(res.ok){
      const newItem = await res.json();
      S.data[cat] = [...(S.data[cat]||[]), newItem];
      console.log("✅ Ajouté:", newItem);
    } else {
      console.log("❌ Erreur réponse:", res.status);
    }
  } catch(err){
    console.log("❌ Erreur ajout:", err);
  }
  closeModal(); render();
}

/* ── API: MODIFIER ── */
function openEdit(id, cat){
  const item = (S.data[cat]||[]).find(i=>i.id===id);
  if(!item) return;
  openModal("Modifier — " + item.title, formHTML(cat, item));
}

async function apiEdit(item, cat){
  const endpoint = CATS.find(c=>c.key===cat).endpoint;
  try{
    const res = await fetch(`${API}${endpoint}/${item.id}`,{
      method:"PUT",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify(item)
    });
    if(res.ok){
      S.data[cat] = (S.data[cat]||[]).map(i=> i.id===item.id ? item : i);
      console.log("✅ Modifié:", item);
    } else {
      console.log("❌ Erreur réponse:", res.status);
    }
  } catch(err){
    console.log("❌ Erreur modification:", err);
  }
  closeModal(); render();
}

/* ── API: SUPPRIMER ── */
function openDelete(id, cat){
  const item = (S.data[cat]||[]).find(i=>i.id===id);
  if(!item) return;
  openModal("Supprimer ?", `
    <p class="delete-msg">Supprimer <strong>${esc(item.title)}</strong> ? Cette action est irréversible.</p>
    <div class="form-actions">
      <button class="btn-delete-confirm" onclick="confirmDelete(${id},'${cat}')">Supprimer</button>
      <button class="btn-cancel" onclick="closeModal()">Annuler</button>
    </div>
  `);
}

async function confirmDelete(id, cat){
  const endpoint = CATS.find(c=>c.key===cat).endpoint;
  try{
    const res = await fetch(`${API}${endpoint}/${id}`,{method:"DELETE"});
    if(res.ok){
      S.data[cat] = (S.data[cat]||[]).filter(i=> i.id!==id);
      console.log("✅ Supprimé");
    } else {
      console.log("❌ Erreur réponse:", res.status);
    }
  } catch(err){
    console.log("❌ Erreur suppression:", err);
  }
  closeModal(); render();
}

/* ── BOUTON AJOUTER ── */
document.getElementById("add-btn").addEventListener("click", ()=> openAdd(S.view));

/* ── INITIALISATION ── */
(async () => {
  console.log("🚀 Démarrage de Mini-Bibliothèque...");
  await loadGenres();
  await loadAllData();
  console.log("✨ Prêt!");
})();