"""Buble Book: protótipo de biblioteca digital em Flask."""
from __future__ import annotations

import os
import unicodedata
from pathlib import Path
from typing import Any

from flask import Flask, abort, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
BOOKS_DIR = STATIC_DIR / "books"

# Caminhos absolutos tornam a localização dos templates e arquivos estáticos
# explícita, evitando erros quando o Render inicia a aplicação.
app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path="/static",
)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024

# Os textos marcados como amostra são originais e foram criados para o protótipo.
# O título comercial abaixo só abre um EPUB se um arquivo autorizado estiver
# presente em static/books/diario-banana-20.epub.
LIVROS: list[dict[str, Any]] = [
    {
        "slug": "jardim-estrelas",
        "titulo": "O Jardim das Pequenas Estrelas",
        "autor": "Lia Monteiro",
        "genero": "Fantasia",
        "simbolo": "✦",
        "capa": "rosa",
        "selo": "Amostra original",
        "descricao": "Um jardim secreto, sonhos esquecidos e a coragem de descobrir o desconhecido.",
        "texto": [
            "Na pequena cidade de Aurora, existia um jardim que só aparecia quando o céu ficava completamente escuro. Diziam que cada flor guardava um sonho esquecido por alguém.",
            "Clara encontrou aquele lugar numa noite de primavera. Entre folhas brilhantes e pétalas que pareciam pequenas estrelas, percebeu que algumas aventuras começam quando temos coragem de fazer uma pergunta.",
            "Naquela noite, Clara decidiu voltar ao jardim. Não sabia o que encontraria, mas descobriu que a curiosidade pode ser a primeira página de uma grande história.",
        ],
    },
    {
        "slug": "cartas-lua",
        "titulo": "Cartas para a Lua",
        "autor": "Marina Alves",
        "genero": "Romance",
        "simbolo": "☾",
        "capa": "lilas",
        "selo": "Amostra original",
        "descricao": "Uma narrativa delicada sobre sentimentos, encontros inesperados e novos começos.",
        "texto": [
            "Todas as noites, Sofia escrevia uma carta para a lua. Não esperava resposta. Era apenas seu jeito de organizar os pensamentos antes de dormir.",
            "Numa terça-feira chuvosa, ela conheceu alguém que também gostava de escrever. A conversa começou por causa de um livro esquecido no banco de uma praça.",
            "A partir daquele dia, as cartas ficaram diferentes. Sofia continuou olhando para a lua, mas começou também a prestar atenção nas pessoas ao seu redor.",
        ],
    },
    {
        "slug": "cidade-segredos",
        "titulo": "A Cidade dos Segredos",
        "autor": "Caio Nunes",
        "genero": "Mistério",
        "simbolo": "⌕",
        "capa": "azul",
        "selo": "Amostra original",
        "descricao": "Uma rua silenciosa, uma chave antiga e um mistério esperando para ser investigado.",
        "texto": [
            "A rua das Acácias tinha vinte e três casas e apenas uma janela que permanecia iluminada depois da meia-noite.",
            "Quando Miguel encontrou uma chave de cobre perto do portão da biblioteca, percebeu que havia algo estranho naquele bairro. O objeto trazia uma pequena inscrição quase apagada.",
            "Ele abriu seu caderno, anotou as primeiras pistas e decidiu começar pelo lugar onde todos diziam não haver nada interessante: a velha estação.",
        ],
    },
    {
        "slug": "clube-coisas-perdidas",
        "titulo": "O Clube das Coisas Perdidas",
        "autor": "Nina Duarte",
        "genero": "Aventura",
        "simbolo": "☁",
        "capa": "menta",
        "selo": "Amostra original",
        "descricao": "Quatro amigos descobrem que os objetos esquecidos guardam histórias especiais.",
        "texto": [
            "O clube funcionava no quartinho dos fundos de uma papelaria. Sua regra principal era simples: nenhum objeto encontrado poderia ser considerado sem importância.",
            "Uma luva sem par, um botão dourado e uma fotografia antiga foram as primeiras pistas da semana. Cada descoberta levava os amigos a um canto diferente do bairro.",
            "Eles logo perceberam que encontrar o dono de alguma coisa era só parte da aventura. A outra parte era descobrir a história que aquele objeto tinha para contar.",
        ],
    },
    {
        "slug": "pequenas-coisas",
        "titulo": "Pequenas Coisas, Grandes Mundos",
        "autor": "Clara Reis",
        "genero": "Poesia",
        "simbolo": "❀",
        "capa": "amarelo",
        "selo": "Amostra original",
        "descricao": "Pequenos textos sobre a natureza, o cotidiano e os detalhes que tornam um dia especial.",
        "texto": [
            "A manhã chegou devagar, vestindo as folhas com gotas de luz. No quintal, o vento ensaiava uma canção que ninguém precisava entender para gostar de ouvir.",
            "Há mundos inteiros escondidos nas coisas pequenas: uma semente, uma conversa, o cheiro da chuva chegando antes da primeira gota.",
            "Talvez viver também seja isso: prestar atenção, guardar alguns instantes com carinho e permitir que os dias comuns tenham sua própria beleza.",
        ],
    },
    {
        "slug": "cafe-paginas",
        "titulo": "O Café das Páginas",
        "autor": "Tomás Vidal",
        "genero": "Contos",
        "simbolo": "☕",
        "capa": "pessego",
        "selo": "Amostra original",
        "descricao": "Histórias acolhedoras que se encontram em uma pequena livraria de bairro.",
        "texto": [
            "A livraria abria às oito, mas o aroma do café já escapava pela porta antes mesmo de o primeiro cliente chegar.",
            "Dona Elisa acreditava que toda pessoa entrava ali procurando alguma coisa. Às vezes era um livro específico; em outras, era apenas um lugar tranquilo para respirar.",
            "Naquela manhã, seis desconhecidos escolheram mesas diferentes. Nenhum deles imaginava que, antes do fim do dia, suas histórias acabariam se cruzando.",
        ],
    },
    {
        "slug": "diario-banana-20",
        "titulo": "Diário de um Banana 20: Festa Insana",
        "autor": "Jeff Kinney",
        "genero": "Humor",
        "simbolo": "☺",
        "capa": "pink",
        "selo": "No catálogo",
        "descricao": "Título listado na biblioteca. A leitura integral só fica disponível quando uma edição que possa ser distribuída online for adicionada ao projeto.",
        "epub": "books/diario-banana-20.epub",
        "texto": [],
    },
]


def normalizar(texto: str) -> str:
    """Compara buscas sem distinguir maiúsculas e acentos."""
    normalizado = unicodedata.normalize("NFD", texto.casefold())
    return "".join(char for char in normalizado if unicodedata.category(char) != "Mn")


def preparar_livro(livro: dict[str, Any]) -> dict[str, Any]:
    """Retorna uma cópia com estado de leitura calculado no servidor."""
    item = dict(livro)
    caminho_epub = item.get("epub")
    epub_path = (BOOKS_DIR / Path(caminho_epub).name) if caminho_epub else None
    item["epub_disponivel"] = bool(epub_path and epub_path.is_file())
    item["epub_url"] = (
        url_for("static", filename=f"books/{epub_path.name}")
        if item["epub_disponivel"] and epub_path
        else None
    )
    item["pronto_para_leitura"] = bool(item.get("texto") or item["epub_disponivel"])
    return item


@app.context_processor
def inject_globals() -> dict[str, int]:
    from datetime import datetime
    return {"ano_atual": datetime.now().year}


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


@app.get("/")
def inicio():
    busca = request.args.get("q", "").strip()[:100]
    categoria = request.args.get("categoria", "Todas").strip()
    categorias = ["Todas"] + sorted({livro["genero"] for livro in LIVROS})
    if categoria not in categorias:
        categoria = "Todas"

    consulta = normalizar(busca)
    resultados = []
    for livro in LIVROS:
        pesquisavel = normalizar(
            f"{livro['titulo']} {livro['autor']} {livro['genero']} {livro['descricao']}"
        )
        combina_busca = consulta in pesquisavel
        combina_categoria = categoria == "Todas" or livro["genero"] == categoria
        if combina_busca and combina_categoria:
            resultados.append(preparar_livro(livro))

    return render_template(
        "index.html",
        livros=resultados,
        categorias=categorias,
        busca=busca,
        categoria=categoria,
        total_livros=len(LIVROS),
    )


@app.get("/livro/<slug>")
def ler_livro(slug: str):
    livro_original = next((item for item in LIVROS if item["slug"] == slug), None)
    if livro_original is None:
        abort(404)
    livro = preparar_livro(livro_original)
    return render_template("reader.html", livro=livro)


@app.get("/health")
def health():
    return {"status": "ok", "app": "Buble Book"}, 200


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
