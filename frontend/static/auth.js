(function () {
  const REQUIRED_CONFIG_KEYS = [
    "apiKey",
    "authDomain",
    "projectId",
    "appId"
  ];

  function hasFirebaseConfig() {
    const cfg = window.FIREBASE_CONFIG || {};
    return REQUIRED_CONFIG_KEYS.every((key) => Boolean(cfg[key]));
  }

  function initFirebase() {
    if (!hasFirebaseConfig()) {
      return false;
    }

    if (!window.firebase) {
      return false;
    }

    if (!firebase.apps.length) {
      firebase.initializeApp(window.FIREBASE_CONFIG);
    }

    firebase
      .auth()
      .setPersistence(firebase.auth.Auth.Persistence.SESSION)
      .catch((err) => console.error("Failed to set Firebase session persistence", err));

    return true;
  }

  function showConfigWarning(targetId) {
    const target = document.getElementById(targetId);
    if (!target || hasFirebaseConfig()) {
      return;
    }

    target.innerHTML = "<p class='err-sub'>Firebase config is missing. Set FIREBASE_* environment variables in backend before using login.</p>";
  }

  function onAuthStateChange(callback) {
    if (!initFirebase()) {
      callback(null);
      return null;
    }

    return firebase.auth().onAuthStateChanged(callback);
  }

  function requireAuth(redirectTo) {
    const redirectPath = redirectTo || "/login";
    onAuthStateChange((user) => {
      if (!user) {
        window.location.href = redirectPath;
      }
    });
  }

  function getCurrentUser() {
    if (!initFirebase()) {
      return null;
    }
    return firebase.auth().currentUser;
  }

  function signInWithEmail(email, password) {
    initFirebase();
    return firebase.auth().signInWithEmailAndPassword(email, password);
  }

  function signUpWithEmail(email, password) {
    initFirebase();
    return firebase.auth().createUserWithEmailAndPassword(email, password);
  }

  function signInWithGoogle() {
    initFirebase();
    const provider = new firebase.auth.GoogleAuthProvider();
    return firebase.auth().signInWithPopup(provider);
  }

  function signOut() {
    if (!initFirebase()) {
      return Promise.resolve();
    }
    return firebase.auth().signOut();
  }

  function signOutAndRedirect(path) {
    const target = path || "/login";
    return signOut().finally(() => {
      window.location.href = target;
    });
  }

  function getHistoryKey(uid) {
    return "detectai_history_" + uid;
  }

  function getUserHistory(uid) {
    const raw = localStorage.getItem(getHistoryKey(uid));
    if (!raw) {
      return [];
    }

    try {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (err) {
      console.error("Failed parsing user history", err);
      return [];
    }
  }

  function saveUserHistory(uid, items) {
    localStorage.setItem(getHistoryKey(uid), JSON.stringify(items));
  }

  function addUserHistory(uid, item) {
    const history = getUserHistory(uid);
    history.unshift(item);
    const capped = history.slice(0, 50);
    saveUserHistory(uid, capped);
    return capped;
  }

  window.AppAuth = {
    hasFirebaseConfig,
    initFirebase,
    showConfigWarning,
    onAuthStateChange,
    requireAuth,
    getCurrentUser,
    signInWithEmail,
    signUpWithEmail,
    signInWithGoogle,
    signOut,
    signOutAndRedirect,
    getUserHistory,
    addUserHistory
  };
})();
