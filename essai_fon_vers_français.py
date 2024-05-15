import pandas as pd
import requests
import random


API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}


textes_aleatoires = [
    "I would like a terracotta calabash",
    "an ancestral African stool",
    "an African woman warrior"
]
# Chargement du DataFrame contenant les données
df = pd.read_csv("fondata.csv")  # Remplacez "votre_fichier.csv" par le chemin de votre fichier CSV

# Fonction pour rechercher les correspondances dans le DataFrame et envoyer à l'API
def generate_image(texte_entree):
    # Recherche de correspondances dans la colonne input_text
    correspondance = df[df['Fon'].str.contains(texte_entree)]['French'].values
    if len(correspondance) > 0:
        # S'il y a une correspondance, envoyer à l'API pour générer l'image
        image_bytes = query({"inputs": correspondance[0]})
        # Retourner l'image générée
        return image_bytes
    else:
        # Si aucune correspondance n'est trouvée, retourner None
        texte_aleatoire = random.choice(textes_aleatoires)
        image_bytes = query({"inputs": texte_aleatoire})
        return image_bytes

# Fonction pour interroger l'API et récupérer l'image générée
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# Exemple d'utilisation
texte_entree = input("Texte entré par l'utilisateur")
image_bytes = generate_image(texte_entree)
if image_bytes:
    # Vous pouvez accéder à l'image avec PIL.Image par exemple
    import io
    from PIL import Image
    image = Image.open(io.BytesIO(image_bytes))
    image.show()  # Afficher l'image
else:
    print("Aucune correspondance trouvée dans le dataset.")
