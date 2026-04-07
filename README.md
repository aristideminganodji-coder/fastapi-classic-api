# FastAPI Classic API

<div align="center">
  
  ![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
  ![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
  ![License](https://img.shields.io/badge/License-MIT-yellow.svg)
  
  *Une API RESTful moderne construite avec FastAPI et PostgreSQL*
</div>

## 📋 Table des matières
- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Stack Technique](#-stack-technique)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Documentation API](#-documentation-api)
- [Structure du projet](#-structure-du-projet)
- [Tests](#-tests)
- [Auteur](#-auteur)
- [Licence](#-licence)

---

## 🎯 Présentation

**FastAPI Classic API** est une API RESTful conçue pour servir de base solide pour des applications web modernes. Elle implémente un système d'authentification complet et des opérations CRUD.

### ✨ Points clés
- ✅ Architecture modulaire et scalable
- ✅ Authentification sécurisée (JWT + bcrypt)
- ✅ Documentation interactive automatique
- ✅ Code 100% typé avec Pydantic

## 🚀 Fonctionnalités

### 🔐 Authentification
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Inscription utilisateur |
| POST | `/auth/login` | Connexion avec JWT |

### 👥 Utilisateurs
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/users/` | Liste des utilisateurs |
| GET | `/users/{id}` | Détail d'un utilisateur |
| PUT | `/users/{id}` | Mise à jour |
| DELETE | `/users/{id}` | Suppression |

### 📝 Tâches
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/tasks/` | Créer une tâche |
| GET | `/tasks/` | Liste des tâches |
| GET | `/tasks/{id}` | Détail d'une tâche |
| PUT | `/tasks/{id}` | Modifier une tâche |
| DELETE | `/tasks/{id}` | Supprimer une tâche |

## 🛠 Stack Technique

```python
{
  "backend": {
    "framework": "FastAPI",
    "orm": "SQLAlchemy 2.0",
    "validation": "Pydantic",
    "auth": "JWT + bcrypt"
  },
  "database": {
    "system": "PostgreSQL",
    "driver": "psycopg2"
  },
  "environment": {
    "python": "3.11+",
    "os": "Linux/WSL"
  }
}