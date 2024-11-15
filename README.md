
# Logic-Sunrise RSS

<img src="./img/demo.png" width="450"/>

Un simple script Python pour surveiller le flux RSS du site logic-sunrise.com et envoyer des news aux canaux Discord à l'aide de webhooks.

## Fonctionnalités

- Surveille un flux RSS et identifie les nouvelles entrées.
- Envoie des notifications aux canaux Discord via des webhooks.
- Prend en charge plusieurs webhooks avec un suivi séparé pour chacun.
- Nettoie et extrait automatiquement le texte et les images des descriptions RSS.

## Pré-requis

- Python 3.8 ou supérieur
- Dépendances listées dans `requirements.txt`

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/ghost0159/ls-rss
   cd ls-rss
   ```

2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez vos webhooks :
   - Créez un fichier `webhooks.json` dans le répertoire racine.
   - Exemple de structure :
     ```json
     {
         "webhooks": [
             {
                 "url": "https://discord.com/api/webhooks/<webhook_id>",
                 "thread_id": null,
             },
             {
                 "url": "https://discord.com/api/webhooks/<un_autre_webhook_id>",
                 "thread_id": "987654321"
             }
         ]
     }
     ```
     *je précise que le ``thread_id`` n'est pas obligatoire, c'est pour ceux souhaitant envoyer des news dans un "threads" ou "fil de discussion" en français, pour l'avoir il vous suffit de copier l'url de votre thread par exemple: ``https://discord.com/channels/123456755/987654321`` ici ce sera donc 987654321*

4. Exécutez le script :
   ```bash
   python main.py
   ```

## Exemple de déploiement

Bon, ce qui serez quand même intéressant c'est de le déployer afin qu'il soit tout le temps actif, n'est-ce pas? 🙂

Pour faire cela il y as donc mille est une façon de le faire, mais personnelement je fait un déploiement en tant que service sur un VPS ubuntu, si cela vous intéresse j'ai fait un guide [ici](./README_deployement.md).

## Structure des fichiers

- `main.py` : Le script principal.
- `webhooks.json` : Configuration des webhooks Discord.
- `sent_news/` : Répertoire pour le suivi des entrées RSS déjà envoyées (créé automatiquement).
- `requirements.txt` : Liste des dépendances Python nécessaires.

## Remarques

- Assurez-vous que le fichier `webhooks.json` est correctement configuré avant de lancer le script.
- Les entrées RSS envoyées sont stockées séparément pour chaque webhook dans le répertoire `sent_news/`.

## Licence

Ce projet est open-source et disponible sous la licence MIT.