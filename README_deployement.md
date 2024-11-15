
## Déploiement en tant que Service sur Ubuntu

Pour s'assurer que le script fonctionne en continu, vous pouvez le déployer en tant que service `systemd`.

### 1. Préparer l'Environnement

1. **Mettre à jour le serveur** :
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Installer Python et venv (si vous ne les avez pas déjà)** :
   ```bash
   sudo apt install python3 python3-venv python3-pip -y
   ```

3. **Créer un répertoire pour le projet** :
   ```bash
   mkdir -p ~/ls-rss
   cd ~/ls-rss
   ```

4. **Copier vos fichiers dans ce répertoire** :
   Placez `main.py`, `requirements.txt` et `webhooks.json` dans ce répertoire.

5. **Configurer un environnement virtuel Python** :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 2. Configurer le Service

1. **Créer un fichier de service systemd** :
   ```bash
   sudo nano /etc/systemd/system/ls-rss.service
   ```

   **Exemple de configuration** :
   ```ini
   [Unit]
   Description=LS-RSS : RSS vers Discord
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/home/your-username/ls-rss
   ExecStart=/home/your-username/ls-rss/venv/bin/python /home/your-username/ls-rss/main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

   Remplacez `your-username` par votre nom d'utilisateur sur le serveur.

2. **Recharger les services systemd et activer le service** :
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable ls-rss
   sudo systemctl start ls-rss
   ```

3. **Vérifier le statut du service** :
   ```bash
   sudo systemctl status ls-rss
   ```

### 3. Gestion du Service

- **Voir les journaux** :
  ```bash
  sudo journalctl -u ls-rss
  ```

- **Arrêter le service** :
  ```bash
  sudo systemctl stop ls-rss
  ```

- **Redémarrer le service** :
  ```bash
  sudo systemctl restart ls-rss
  ```

Avec cette configuration, le script fonctionnera en permanence et redémarrera automatiquement après un redémarrage du serveur.
