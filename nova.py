import os, sys, re, json, unicodedata
from pathlib import Path

VERSION = "0.1.0"
ROOT = Path.home() / "NovaProjects"
CYAN = "\033[96m"; RESET = "\033[0m"

def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.lower()) if not unicodedata.combining(c))

def detect(text):
    s=normalize(text)
    if "roblox" in s or "luau" in s: return "roblox"
    if "calculadora" in s and "python" in s: return "python"
    if "calculadora" in s: return "calculator"
    if "tarefas" in s or "todo" in s: return "todo"
    if any(x in s for x in ("site","pagina","portfolio")): return "site"
    return None

def web_page(kind, light):
    bg, panel, fg = ("#f1f5f9","#ffffff","#182235") if light else ("#0b1020","#151e32","#f8fafc")
    style = """
*{box-sizing:border-box}body{font:16px system-ui;min-height:100vh;margin:0;display:grid;place-items:center;padding:20px;background:var(--bg);color:var(--fg)}
main{width:min(100%,480px);background:var(--panel);padding:30px;border-radius:22px;box-shadow:0 20px 70px #0002}
h1{margin:0 0 20px}button,input{font:inherit;padding:14px;border:1px solid #7788aa55;border-radius:10px}
button{background:#4565db;color:white;cursor:pointer}button:hover{filter:brightness(1.15)}
input{background:var(--bg);color:var(--fg);width:100%}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
ul{padding:0;list-style:none}li{display:flex;justify-content:space-between;gap:8px;padding:8px;border-bottom:1px solid #8884}
"""
    if kind=="calculator":
        body='<h1>Calculadora</h1><input id="display" readonly value="0" style="text-align:right;font-size:30px;margin-bottom:14px"><div id="keys" class="grid"></div>'
        js=r"""
let expr='',d=document.getElementById('display');
function press(k){
 if(k==='C'){expr='';d.value='0';return}
 if(k==='⌫'){expr=expr.slice(0,-1);d.value=expr||'0';return}
 if(k==='='){
  try{
   let tokens=expr.match(/\d+(?:\.\d+)?|[()+*/-]/g)||[],i=0;
   function f(){let t=tokens[i++];if(t==='-')return -f();if(t==='+')return f();if(t==='('){let n=a();if(tokens[i++]!==')')throw Error();return n}if(!t||!/^\d/.test(t))throw Error();return +t}
   function m(){let n=f();while(tokens[i]==='*'||tokens[i]==='/'){let op=tokens[i++],v=f();n=op==='*'?n*v:n/v}return n}
   function a(){let n=m();while(tokens[i]==='+'||tokens[i]==='-'){let op=tokens[i++],v=m();n=op==='+'?n+v:n-v}return n}
   let out=a();if(i!==tokens.length||!Number.isFinite(out))throw Error();expr=String(+out.toPrecision(12));d.value=expr
  }catch(e){d.value='Erro';expr=''}return
 }
 if(/^[0-9.+*/()-]$/.test(k)){expr+=k;d.value=expr}
}
for(let k of ['C','⌫','(',')','7','8','9','/','4','5','6','*','1','2','3','-','0','.','=','+']){
 let b=document.createElement('button');b.textContent=k;b.onclick=()=>press(k);document.getElementById('keys').append(b)
}
document.addEventListener('keydown',e=>{let k={'Enter':'=','Backspace':'⌫','Escape':'C'}[e.key]||e.key;if(k.length===1||k==='='||k==='⌫'||k==='C')press(k)});
"""
    elif kind=="todo":
        body='<h1>Minhas tarefas</h1><form id="form"><input id="task" placeholder="Nova tarefa" required maxlength="160"><button>Adicionar</button></form><ul id="items"></ul>'
        js=r"""
let tasks=[];try{tasks=JSON.parse(localStorage.getItem('nova-tasks')||'[]')}catch(e){}if(!Array.isArray(tasks))tasks=[];
function draw(){let root=document.getElementById('items');root.replaceChildren();tasks.forEach((t,i)=>{let li=document.createElement('li'),span=document.createElement('span'),btn=document.createElement('button');span.textContent=t;btn.textContent='Excluir';btn.onclick=()=>{tasks.splice(i,1);save()};li.append(span,btn);root.append(li)})}
function save(){localStorage.setItem('nova-tasks',JSON.stringify(tasks));draw()}
document.getElementById('form').onsubmit=e=>{e.preventDefault();let x=document.getElementById('task');if(x.value.trim()){tasks.push(x.value.trim());x.value='';save()}};draw();
"""
    else:
        body='<h1>Meu site</h1><p>Projeto gerado pela Nova CLI.</p><button onclick="alert(\'Funcionando!\')">Começar</button>'
        js=""
    return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nova Project</title><style>:root{--bg:'+bg+';--panel:'+panel+';--fg:'+fg+'}'+style+'</style></head><body><main>'+body+'</main><script>'+js+'</script></body></html>'

PYTHON_CALC = '''def main():
    print("Calculadora Python - digite sair para encerrar")
    while True:
        a=input("Numero 1: ")
        if a.lower()=="sair":break
        try:
            x=float(a); op=input("Operacao (+,-,*,/): "); y=float(input("Numero 2: "))
            if op=="+":print(x+y)
            elif op=="-":print(x-y)
            elif op=="*":print(x*y)
            elif op=="/":print(x/y)
            else:print("Operacao invalida")
        except (ValueError,ZeroDivisionError):print("Entrada invalida ou divisao por zero")
if __name__=="__main__":main()
'''
ROBLOX='''-- Luau: coloque em ServerScriptService
local Players = game:GetService("Players")
Players.PlayerAdded:Connect(function(player)
    print("[Nova] " .. player.Name .. " entrou")
end)
'''

def make(request):
    kind=detect(request)
    if not kind:
        print("Ainda nao existe regra para esse pedido. Digite /help.");return
    root=ROOT
    base={"calculator":"calculadora","python":"calculadora-python","todo":"tarefas","site":"meu-site","roblox":"roblox-script"}[kind]
    folder=root/base
    number=2
    while folder.exists():
        folder=root/(base+"-"+str(number));number+=1
    try:
        folder.mkdir(parents=True)
        if kind in ("calculator","todo","site"):
            light=any(t in normalize(request) for t in ("claro","branco","light"))
            (folder/"index.html").write_text(web_page(kind,light),encoding="utf-8")
        elif kind=="python":
            (folder/"calculadora.py").write_text(PYTHON_CALC,encoding="utf-8")
        else:
            (folder/"ServerScript.lua").write_text(ROBLOX,encoding="utf-8")
        (folder/"nova.json").write_text(json.dumps({"engine":VERSION,"type":kind,"request":request},ensure_ascii=False,indent=2),encoding="utf-8")
    except OSError as e:
        print("Erro ao criar projeto:",e);return
    print("\033[92m✓ Projeto criado:\033[0m",folder)
    print("Arquivos:",", ".join(x.name for x in folder.iterdir()))

HELP="""Comandos:
  /help       - Ajuda
  /files      - Lista projetos
  /clear      - Limpa terminal
  /version    - Mostra versao
  /exit       - Encerra
  /new PEDIDO - Gera projeto
Exemplos:
  crie uma calculadora com interface escura
  crie uma lista de tarefas com tema claro
  crie um site
  crie uma calculadora python
  crie um script roblox
Motor por regras: nao entende pedidos arbitrarios.
"""

def main():
    if os.name=="nt":
        try:
            import ctypes
            h=ctypes.windll.kernel32.GetStdHandle(-11)
            mode=ctypes.c_uint32()
            if ctypes.windll.kernel32.GetConsoleMode(h,ctypes.byref(mode)):
                ctypes.windll.kernel32.SetConsoleMode(h,mode.value|4)
        except Exception:pass
    if len(sys.argv)>1:
        arg=" ".join(sys.argv[1:])
        if arg in ("--help","-h"):print(HELP)
        elif arg in ("--version","-v"):print(VERSION)
        else:make(arg)
        return
    print(CYAN+"  ✦ NOVA CLI  v"+VERSION+RESET)
    print("  Offline • Sem IA • Rule-Based Engine")
    print("  Workspace:",ROOT)
    print("  Digite /help para ajuda.\n")
    while True:
        try:line=input(CYAN+" nova ❯ "+RESET).strip()
        except (EOFError,KeyboardInterrupt):print("\nAte logo!");break
        if not line:continue
        if line in ("/exit","/quit","sair"):break
        if line=="/help":print(HELP)
        elif line=="/version":print(VERSION)
        elif line=="/clear":os.system("cls" if os.name=="nt" else "clear")
        elif line=="/files":
            print("\n".join(str(x) for x in ROOT.iterdir() if x.is_dir()) if ROOT.exists() else "Nenhum projeto.")
        else:make(line[5:] if line.startswith("/new ") else line)

if __name__=="__main__":main()
