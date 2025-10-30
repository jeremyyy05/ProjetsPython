import os
import time
import requests
import pandas as pd
from scrapy import Selector

BASE_URL = "https://books.toscrape.com/"

os.makedirs("outputs/csv", exist_ok=True)
os.makedirs("outputs/images", exist_ok=True)

def parse_product_page(url):
    r = requests.get(url)
    s = Selector(text=r.text)
    titre = s.css(".product_main h1::text").get()
    prix = s.css(".price_color::text").get().replace("£", "")
    dispo = "".join([t.strip() for t in s.css(".instock.availability ::text").getall() if t.strip()])
    note = s.css(".star-rating::attr(class)").get().split()[-1]
    upc = s.css("table tr:nth-child(1) td::text").get()
    cat = s.css("ul.breadcrumb li:nth-child(3) a::text").get()
    img_rel = s.css(".item.active img::attr(src)").get().replace("../", "")
    img_url = BASE_URL + img_rel
    return {
        "Titre": titre,
        "Prix (£)": prix,
        "Disponibilité": dispo,
        "Note": note,
        "UPC": upc,
        "Catégorie": cat,
        "Image_URL": img_url,
        "URL_Produit": url
    }

exemple = parse_product_page("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
print("=== PHASE 1 : UNE PAGE ===")
for k, v in exemple.items():
    print(f"{k}: {v}")
print()

urls = [
    "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    "https://books.toscrape.com/catalogue/soumission_998/index.html"
]

livres = [parse_product_page(u) for u in urls]
df = pd.DataFrame(livres)
df.to_csv("outputs/csv/livres.csv", index=False, encoding="utf-8")
print("=== PHASE 2 : PLUSIEURS LIVRES ===")
print(f"[OK] {len(df)} livres enregistrés dans outputs/csv/livres.csv\n")

def get_links_category(category_url):
    r = requests.get(category_url)
    s = Selector(text=r.text)
    liens = s.css("article.product_pod h3 a::attr(href)").getall()
    return [BASE_URL + "catalogue/" + l.replace("../../../", "") for l in liens]

def scrape_category(name, category_url):
    print(f"=== Catégorie : {name} ===")
    links = get_links_category(category_url)
    livres = [parse_product_page(l) for l in links]
    df = pd.DataFrame(livres)
    path = f"outputs/csv/{name.lower()}.csv"
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"[OK] {len(df)} livres enregistrés dans {path}")
    return df

df_poetry = scrape_category("Poetry", "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html")

def download_images(df):
    for _, row in df.iterrows():
        category = row["Catégorie"].lower()
        folder = os.path.join("outputs/images", category)
        os.makedirs(folder, exist_ok=True)
        titre = row["Titre"].replace(" ", "_").replace("/", "_")
        img_path = os.path.join(folder, f"{row['UPC']}_{titre}.jpg")
        if not os.path.exists(img_path):
            r = requests.get(row["Image_URL"])
            with open(img_path, "wb") as f:
                f.write(r.content)
            print(f"[IMG] {titre} téléchargée.")
        time.sleep(0.1)

print("\n=== PHASE 4 : TÉLÉCHARGEMENT IMAGES ===")
download_images(df_poetry)

def get_all_categories():
    r = requests.get(BASE_URL)
    s = Selector(text=r.text)
    cats = []
    for a in s.css("div.side_categories ul li ul li a"):
        name = a.css("a::text").get().strip()
        href = a.css("a::attr(href)").get()
        url = BASE_URL + href
        cats.append((name, url))
    return cats

print("\n=== PHASE 5 : TOUTES LES CATÉGORIES ===")
categories = get_all_categories()
print(f"{len(categories)} catégories trouvées.\n")

for name, url in categories:
    df_cat = scrape_category(name, url)
    download_images(df_cat)
print("\n[OK] Toutes les catégories ont été enregistrées avec leurs images.\n")

def analyse_categorie(nom):
    path = f"outputs/csv/{nom.lower()}.csv"
    if not os.path.exists(path):
        print(f"❌ Aucun fichier trouvé pour {nom}.")
        return
    df = pd.read_csv(path)
    df["Prix (£)"] = df["Prix (£)"].astype(float)
    print(f"\n=== Analyse de la catégorie : {nom} ===")
    print(f"Nombre de livres : {len(df)}")
    print(f"Prix moyen : {round(df['Prix (£)'].mean(), 2)} £")
    print("\nRépartition des notes :")
    print(df["Note"].value_counts())

analyse_categorie("Poetry")
print("\n=== PROJET TERMINÉ AVEC SUCCÈS ✅ ===")
