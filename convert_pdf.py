"""
convert_pdf.py
----------------
Script de conversion : /raw (PDF) -> /wiki (articles markdown structures et lies)

Utilisation :
    python convert_pdf.py

Prerequis :
    pip install pypdf groq python-dotenv

Variable d'environnement necessaire :
    GROQ_API_KEY   (a mettre dans le fichier .env a la racine du projet)

Ce que fait le script :
    1. Scanne le dossier /raw a la recherche de fichiers .pdf
    2. Extrait le texte de chaque PDF
    3. Recupere la liste des articles deja presents dans /wiki (pour permettre les liens croises)
    4. Appelle l'API Anthropic pour transformer le texte brut en article markdown structure,
       avec des liens internes [[Nom Article]] vers les articles existants quand c'est pertinent
    5. Ecrit le fichier .md resultant dans /wiki
    6. Deplace le PDF traite dans /raw/_traites pour ne pas le reconvertir la prochaine fois
"""

import os
import sys
import shutil
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Erreur : le module 'pypdf' n'est pas installe. Lance : pip install pypdf")
    sys.exit(1)

try:
    from groq import Groq
except ImportError:
    print("Erreur : le module 'groq' n'est pas installe. Lance : pip install groq")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()  # charge automatiquement le fichier .env s'il existe a la racine
except ImportError:
    print("Erreur : le module 'python-dotenv' n'est pas installe. Lance : pip install python-dotenv")
    sys.exit(1)

if not os.environ.get("GROQ_API_KEY"):
    print("Erreur : GROQ_API_KEY n'est pas definie.")
    print("Ajoute-la dans le fichier .env a la racine du projet, sous la forme :")
    print("  GROQ_API_KEY=ta_cle_ici")
    sys.exit(1)


# --- Configuration ---------------------------------------------------------

# Racine du projet = dossier contenant ce script
ROOT_DIR = Path(__file__).resolve().parent
RAW_DIR = ROOT_DIR / "raw"
WIKI_DIR = ROOT_DIR / "wiki"
TRAITES_DIR = RAW_DIR / "_traites"

MODEL = "llama-3.3-70b-versatile"  # modele Groq ; change si besoin (voir console.groq.com/docs/models)


# --- Fonctions ---------------------------------------------------------

def extraire_texte_pdf(chemin_pdf: Path) -> str:
    """Lit un PDF et retourne tout son texte concatene."""
    reader = PdfReader(str(chemin_pdf))
    texte_complet = []
    for page in reader.pages:
        texte_complet.append(page.extract_text() or "")
    return "\n".join(texte_complet)


def lister_articles_wiki_existants() -> list[str]:
    """Retourne la liste des noms d'articles deja presents dans /wiki (sans l'extension .md)."""
    if not WIKI_DIR.exists():
        return []
    return [f.stem for f in WIKI_DIR.glob("*.md") if f.stat().st_size > 0]


def generer_article_markdown(texte_pdf: str, nom_source: str, articles_existants: list[str]) -> str:
    """Appelle l'API Anthropic pour transformer le texte brut du PDF en article markdown
    structure, avec des liens internes vers les articles existants du wiki quand pertinent."""

    client = Groq()  # lit GROQ_API_KEY depuis l'environnement (charge via .env)

    liste_articles = "\n".join(f"- {a}" for a in articles_existants) if articles_existants else "(aucun article existant pour le moment)"

    prompt = f"""Tu es un assistant charge de transformer une documentation technique brute en un article de wiki markdown clair, structure et bien lie a une base de connaissances existante.

Voici la liste des articles DEJA PRESENTS dans le wiki (utilise ces noms exacts pour les liens) :
{liste_articles}

Voici le texte brut extrait du document source "{nom_source}" :
---
{texte_pdf[:15000]}
---

Consignes :
1. Redige un article markdown propre avec des titres (##), des sections logiques, et des listes si utile.
2. Ne te contente PAS de recopier le texte brut : synthetise et clarifie.
3. Chaque fois qu'un concept mentionne dans le texte correspond a un article DEJA existant dans la liste ci-dessus, cree un lien interne au format [[Nom Exact De L'Article]].
4. Si un concept important n'existe pas encore comme article mais merite d'etre cree plus tard, tu peux quand meme creer un lien [[Nouveau Concept]] vers lui (l'article sera cree plus tard).
5. Termine par une section "## Voir aussi" listant les liens crees.
6. Reponds UNIQUEMENT avec le contenu markdown de l'article, sans commentaire ni preambule.
"""

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def nom_fichier_wiki(nom_pdf: str) -> str:
    """Genere un nom de fichier .md propre a partir du nom du PDF."""
    nom = Path(nom_pdf).stem
    nom = nom.replace(" ", "-").replace("(", "").replace(")", "")
    return f"{nom}.md"


def traiter_un_pdf(chemin_pdf: Path, articles_existants: list[str]) -> None:
    print(f"\n--- Traitement de : {chemin_pdf.name} ---")

    print("  1. Extraction du texte du PDF...")
    texte = extraire_texte_pdf(chemin_pdf)
    if not texte.strip():
        print("  /!\\ Aucun texte extrait (PDF scanne / image ?). Skip.")
        return
    print(f"  -> {len(texte)} caracteres extraits.")

    print("  2. Generation de l'article via l'API Anthropic...")
    article_md = generer_article_markdown(texte, chemin_pdf.name, articles_existants)

    nom_sortie = nom_fichier_wiki(chemin_pdf.name)
    chemin_sortie = WIKI_DIR / nom_sortie

    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    chemin_sortie.write_text(article_md, encoding="utf-8")
    print(f"  3. Article ecrit : wiki/{nom_sortie}")

    # Deplace le PDF traite pour ne pas le reconvertir au prochain lancement
    TRAITES_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(str(chemin_pdf), str(TRAITES_DIR / chemin_pdf.name))
    print(f"  4. PDF deplace vers raw/_traites/{chemin_pdf.name}")

    print(f"  OK Article genere : wiki/{nom_sortie}")


def main():
    if not RAW_DIR.exists():
        print(f"Erreur : le dossier {RAW_DIR} n'existe pas.")
        sys.exit(1)

    pdfs = [f for f in RAW_DIR.glob("*.pdf")]

    if not pdfs:
        print("Aucun PDF trouve dans /raw. Rien a faire.")
        return

    print(f"{len(pdfs)} PDF(s) trouve(s) dans /raw : {[p.name for p in pdfs]}")

    articles_existants = lister_articles_wiki_existants()
    print(f"Articles existants dans /wiki : {articles_existants}")

    for pdf in pdfs:
        traiter_un_pdf(pdf, articles_existants)
        # Met a jour la liste des articles existants pour les prochains PDF de ce batch
        articles_existants = lister_articles_wiki_existants()

    print("\nTermine.")


if __name__ == "__main__":
    main()
