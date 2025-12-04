// api.js
const API_BASE = "http://127.0.0.1:8000";

async function fetchWithAuth(path, opts = {}){
  const token = localStorage.getItem("token");
  opts.headers = opts.headers || {};
  if(token) opts.headers["Authorization"] = token;
  return fetch(API_BASE + path, opts);
}
