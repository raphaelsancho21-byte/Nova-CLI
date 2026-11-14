# Nova CLI V0.1

Motor de programacao offline por regras, sem IA, API ou tokens. Nao interpreta pedidos arbitrarios.

## Instalar no Windows

Instale Python 3 e Git. Abra CMD:

~~~cmd
git clone https://github.com/raphaelsancho21-byte/Nova-CLI.git
cd Nova-CLI
install.bat
~~~

Feche e reabra o CMD. Execute: Nova

Alternativa: Code > Download ZIP, extrair e executar install.bat.

O instalador configura o PATH do usuario e copia a CLI para LOCALAPPDATA/NovaCLI.

## Exemplos

~~~text
nova > crie uma calculadora com interface moderna escura
nova > crie uma lista de tarefas clara
nova > crie um site
nova > crie uma calculadora python
nova > crie um script roblox
~~~

Projetos ficam na pasta NovaProjects do usuario. Calculadora, lista de tarefas e site geram HTML/CSS/JS; os outros geram Python ou Luau. Abra index.html no navegador.

## Comandos

/help - Ajuda
/files - Lista projetos
/new PEDIDO - Gera projeto
/clear - Limpa terminal
/version - Versao
/exit - Sair

## Limites

V0.1 apenas reconhece regras e palavras-chave predefinidas. Nao possui inteligencia artificial nem edicao universal de codigo.
