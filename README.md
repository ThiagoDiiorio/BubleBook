# Buble Book — protótipo responsivo

Buble Book é um protótipo acadêmico de biblioteca digital, reconstruído com uma estrutura simples para funcionar localmente e ser publicado no Render. O visual usa como referência as peças de identidade enviadas: rosa e vermelho vibrantes, fundos creme, letras fortes, bolhas decorativas e o pato como mascote. As duas ilustrações do pato foram incluídas como imagens locais otimizadas em WebP.

## O que funciona nesta versão

- Página inicial responsiva para desktop e celular.
- Mascote do pato visível na página inicial e nas páginas de leitura.
- Catálogo com cartões de livros e capas decorativas criadas em CSS.
- Busca por título, autor, gênero e descrição, sem diferenciar acentos.
- Filtros de gênero.
- Páginas individuais dos livros.
- Amostras de leitura original para os livros demonstrativos.
- Leitor EPUB integrado quando um EPUB autorizado estiver presente na pasta configurada.
- Rota de verificação `/health` para o Render.
- Página 404 personalizada.
- Pastas de templates e arquivos estáticos configuradas com caminhos absolutos.

## Arquivos do projeto

```text
BubleBook_Rebuild/
├── app.py
├── requirements.txt
├── render.yaml
├── run_windows.bat
├── run_local.sh
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── reader.html
│   └── 404.html
└── static/
    ├── css/style.css
    ├── js/site.js
    ├── images/
    │   ├── pato-cafe.webp
    │   ├── pato-leitura.webp
    │   └── favicon.svg
    └── books/README.txt
```

## Rodar no Windows

1. Instale Python 3.11 ou mais recente, se ainda não estiver instalado.
2. Extraia o ZIP inteiro para uma pasta no computador.
3. Dê dois cliques em `run_windows.bat`.
4. Na primeira execução, o script cria o ambiente virtual e instala as dependências. É necessário ter conexão com a internet na primeira execução.
5. O script abre o navegador em `http://127.0.0.1:5000`. Mantenha a janela do servidor aberta enquanto usa o site.
6. Para encerrar, volte à janela do servidor e pressione `Ctrl+C`.

Se o comando `py -3` não existir, instale Python pelo site oficial e marque a opção de adicionar Python ao PATH, ou execute manualmente os comandos abaixo na pasta do projeto:

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Depois abra `http://127.0.0.1:5000` no navegador.

## Publicar no Render

O ZIP foi montado sem uma pasta externa envolvendo os arquivos. Portanto, ao enviar para o GitHub, os arquivos `app.py`, `requirements.txt`, `render.yaml` e as pastas `templates/` e `static/` devem ficar diretamente na raiz do repositório.

1. Crie um repositório no GitHub.
2. Envie o **conteúdo desta pasta** para a raiz do repositório (não envie só o ZIP).
3. No Render, selecione **New + → Web Service** e conecte o repositório.
4. Defina `Root Directory` como vazio.
5. Build Command: `pip install -r requirements.txt`.
6. Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`.
7. Escolha o plano que preferir e clique em **Deploy Web Service**.
8. Depois que o deploy estiver concluído, teste `/health`, por exemplo `https://SEU-SITE.onrender.com/health`; a resposta deve ser `{"app":"Buble Book","status":"ok"}`.

O `render.yaml` inclui essas configurações. Se o Render não detectar automaticamente o Blueprint, copie manualmente os comandos acima.

## EPUB no leitor integrado

A entrada `Diário de um Banana 20: Festa Insana` já aparece no catálogo, mas o arquivo EPUB não vem incluído neste pacote. Para habilitar a leitura automática, coloque um EPUB cuja disponibilização integral pela internet esteja autorizada em:

```text
static/books/diario-banana-20.epub
```

Depois envie a alteração ao GitHub e aguarde o novo deploy. A página do livro detectará o arquivo e abrirá o leitor integrado automaticamente. O leitor usa EPUB.js por CDN, então o navegador precisa ter acesso à internet para carregar a biblioteca JavaScript.

**Atenção:** os arquivos dentro de `static/` são públicos. Adicione somente arquivos cuja distribuição online esteja autorizada. Ter um EPUB local ou recebê-lo de outra pessoa não significa, por si só, ter autorização para disponibilizar a obra integralmente na internet.

## Se der erro

- `TemplateNotFound`: confirme que `templates/` fica ao lado de `app.py` e que o Render está com `Root Directory` vazio.
- `ModuleNotFoundError: flask` ou `gunicorn`: confira `requirements.txt` e o Build Command.
- Erro de porta no Render: use exatamente `gunicorn --bind 0.0.0.0:$PORT app:app`.
- O site abre localmente, mas não no Render: abra os Logs do último deploy e verifique a primeira mensagem de erro.
- Mudanças não aparecem: confirme que os arquivos novos foram enviados ao GitHub e que o último deploy terminou com sucesso.

## Nota sobre dados

O catálogo fica definido em `app.py`. Não há banco de dados nesta versão; o conteúdo do protótipo não requer migrações ou configuração de armazenamento persistente.
