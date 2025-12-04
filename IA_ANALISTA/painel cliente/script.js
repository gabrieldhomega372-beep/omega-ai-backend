// script.js - controla telas e botões

function token() { return localStorage.getItem("token") }

function login() {
  const email = document.getElementById("email").value
  const senha = document.getElementById("senha").value
  fetch(API_BASE + "/login",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({email,senha})
  }).then(r=>r.json()).then(j=>{
    if(j.sucesso){ localStorage.setItem("token", j.token); location.href="dashboard.html" }
    else document.getElementById("erro").innerText = j.msg || "Credenciais inválidas"
  }).catch(e=>document.getElementById("erro").innerText="Erro de conexão")
}

function logout(){ localStorage.removeItem("token"); location.href="login.html" }

function abrirGerar(){ location.href="conteudo.html" }
function abrirAnalise(){ location.href="analise.html" }
function voltar(){ history.back() }

// fetch de dados do dashboard
async function carregarStats(){
  const t = token()
  if(!t){ location.href="login.html"; return }
  try {
    const res = await fetch(API_BASE + "/stats",{headers: { "Authorization": t }})
    const j = await res.json()
    document.getElementById("stat_conteudo").innerText = j.conteudos || 0
    document.getElementById("stat_analise").innerText = j.analises || 0
    document.getElementById("stat_users").innerText = j.users || 0
  } catch(e){
    console.error(e)
  }
}

async function gerarConteudo(){
  const tema = document.getElementById("tema").value
  const prompt = document.getElementById("prompt").value
  const t = token()
  const r = await fetch(API_BASE + "/gerar_conteudo", {
    method:"POST", headers: {"Content-Type":"application/json","Authorization":t},
    body: JSON.stringify({tema,prompt})
  })
  const j = await r.json()
  document.getElementById("resultado").innerText = j.resultado || JSON.stringify(j)
}

async function analisarTexto(){
  const texto = document.getElementById("texto_analise").value
  const t = token()
  const r = await fetch(API_BASE + "/analisar_texto", {
    method:"POST", headers: {"Content-Type":"application/json","Authorization":t},
    body: JSON.stringify({texto})
  })
  const j = await r.json()
  document.getElementById("analise_res").innerText = j.resultado || JSON.stringify(j)
}

async function carregarUsers(){
  const t = token()
  const r = await fetch(API_BASE + "/users",{headers:{ "Authorization": t }})
  const j = await r.json()
  const el = document.getElementById("users_list")
  if(j.users && j.users.length){
    el.innerHTML = j.users.map(u=>`<div class="user-row card"><b>${u.email}</b> • ${u.role||'user'}</div>`).join("")
  } else el.innerText = "Nenhum usuário"
}

async function salvarConfig(){
  const t = token()
  const modelo = document.getElementById("conf_modelo").value
  const limite = document.getElementById("conf_limite").value
  const res = await fetch(API_BASE + "/config", {
    method:"POST", headers: {"Content-Type":"application/json","Authorization":t},
    body: JSON.stringify({modelo,limite})
  })
  const j = await res.json()
  document.getElementById("conf_msg").innerText = j.msg || "Salvo"
}

// carrega stats ao abrir dashboard
if(location.pathname.endsWith("dashboard.html")) carregarStats()
if(location.pathname.endsWith("users.html")) carregarUsers()
