# 🚀 Guide de déploiement Streamlit Cloud

## Étapes rapides (3 clics)

### 1. Créer un compte (si pas encore)
- Allez sur https://streamlit.io/cloud
- Cliquez sur **"Sign up"**
- Authentifiez-vous avec votre **compte GitHub**

### 2. Créer une nouvelle app
- Cliquez sur **"New app"** (bouton rouge en haut à droite)
- Remplissez:
  - **Repository**: `seifbenfraj17/eg-simulator`
  - **Branch**: `main`
  - **Main file path**: `streamlit_app.py`

### 3. Déployement automatique
- Cliquez sur **"Deploy"**
- Attendez 30-60 secondes
- 🎉 L'app est en ligne !

## ✨ Avantages Streamlit Cloud vs Railway

| Feature | Streamlit Cloud | Railway |
|---------|-----------------|---------|
| **Coût** | Gratuit | ~5$/mois |
| **Limite de temps** | ❌ Illimitée | ✅ 25 jours gratuits |
| **Déploiement** | Automatique (GitHub) | Manuel |
| **Performance** | Excellente | Très bonne |
| **Facilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Support** | Très bon | Correct |

## 🔄 Déploiements automatiques

Une fois connectée, **chaque push sur GitHub déclenche automatiquement un redéploiement** sur Streamlit Cloud. C'est magique! 

### Exemple workflow:
```bash
git add .
git commit -m "Update simulateur"
git push  # ← Déclenche auto-déploiement!
```

## 📱 URL public

Une fois déployée, votre app sera accessible via:
```
https://eg-simulator-<votre-username>.streamlit.app
```

## 🐛 Dépannage

### "Module not found" error
→ Vérifier que `streamlit_app.py` est dans `requirements.txt`

### App crash au démarrage
→ Consulter les logs: cliquez sur les 3 points → "View logs"

### Vérifier les logs en temps réel
```bash
streamlit run streamlit_app.py --logger.level=debug
```

## 📞 Support

- Docs Streamlit: https://docs.streamlit.io
- Issues GitHub: https://github.com/seifbenfraj17/eg-simulator/issues
- Streamlit Community: https://discuss.streamlit.io

---

**C'est tout! Votre app est maintenant sur Streamlit Cloud.** 🎉
