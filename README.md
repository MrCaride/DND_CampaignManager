# DnD Campaign Manager

## Descripción
El DnD Campaign Manager es una aplicación web diseñada para gestionar campañas de Dragones y Mazmorras. Permite a los jugadores crear y gestionar sus personajes, mientras que los másters pueden crear campañas, definir misiones y gestionar combates. La aplicación utiliza Flask como framework principal y Sirope como capa de persistencia sobre Redis.

## Estructura del Proyecto
```
dnd-campaign-manager
├── app
│   ├── __init__.py
│   ├── auth.py
│   ├── routes.py
│   ├── models
│   │   ├── user.py
│   │   ├── character.py
│   │   ├── campaign.py
│   │   └── mission.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── characters.py
│   │   ├── campaigns.py
│   │   ├── missions.py
│   │   └── main.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── operations_master.html
│   │   ├── operations_player.html
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── characters
│   │   │   ├── create.html
│   │   │   ├── edit.html
│   │   │   ├── list.html
│   │   │   └── view.html
│   │   ├── campaigns
│   │   │   ├── create.html
│   │   │   ├── edit.html
│   │   │   ├── list.html
│   │   │   ├── join.html
│   │   │   ├── play.html
│   │   │   ├── play_master.html
│   │   │   ├── play_player.html
│   │   │   └── view.html
│   │   └── missions
│   │       ├── edit.html
│   │       ├── manage.html
│   │       └── view.html
│   └── static
│       └── styles.css
├── app.py
├── create_users.py
├── requirements.txt
├── uninstall_all_packages.py
└── README.md
```

### Descripción de los folders
- **app**: Contiene la aplicación principal de Flask.
  - **__init__.py**: Inicializa la aplicación Flask y la instancia de Sirope.
  - **auth.py**: Maneja la autenticación de usuarios.
  - **routes.py**: Define las rutas de la aplicación.
  - **models**: Contiene los modelos de datos.
    - **user.py**: Modelo de usuario con gestión de autenticación.
    - **character.py**: Modelo de personaje con atributos y estadísticas.
    - **campaign.py**: Modelo de campaña con gestión de permisos.
    - **mission.py**: Modelo de misión con sistema de votos.
  - **routes**: Contiene las rutas específicas de la aplicación.
    - **auth.py**: Rutas de autenticación.
    - **characters.py**: Rutas para gestión de personajes.
    - **campaigns.py**: Rutas para gestión de campañas.
    - **missions.py**: Rutas para gestión de misiones.
    - **main.py**: Rutas principales.
  - **templates**: Contiene las plantillas HTML.
    - **base.html**: Plantilla base con la estructura común.
    - **index.html**: Página principal.
    - **operations_master.html**: Operaciones para másters.
    - **operations_player.html**: Operaciones para jugadores.
  - **static**: Contiene archivos estáticos como CSS.
- **app.py**: Punto de entrada de la aplicación.
- **create_users.py**: Script para crear datos de prueba.
- **requirements.txt**: Dependencias del proyecto.
- **uninstall_all_packages.py**: Script para desinstalar todos los paquetes de Python.
- **netlify.toml**: Configuración para despliegue en Netlify.
- **README.md**: Documentación del proyecto.

## Configuración del Entorno

1. Asegúrate de tener Python 3.x instalado
2. Instala Redis en tu sistema
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```
4. Inicia Redis
5. Ejecuta la aplicación usando uno de estos métodos:

   Opción 1 - Usando Flask:
   ```bash
   python -m flask run
   ```

   Opción 2 - Usando el script de PowerShell:
   ```powershell
   .\start_app.ps1
   ```

### Datos de Prueba
Para poblar la base de datos con datos de prueba, ejecuta:
```bash
python create_users.py
```

Este script creará:
- Usuarios de prueba (masters y jugadores)
- Campañas de ejemplo
- Personajes de muestra
- Misiones predefinidas

## Tecnologías Utilizadas

### Backend
- **Flask**: Framework web para Python
- **Flask-Login**: Gestión de autenticación de usuarios
- **Sirope**: Capa de persistencia sobre Redis
- **Redis**: Base de datos en memoria

### Frontend
- **HTML/CSS**: Interfaz de usuario
- **Jinja2**: Motor de plantillas

## Arquitectura de Persistencia

La aplicación utiliza Sirope como capa de persistencia, proporcionando:

- Mapeo objeto-documento transparente
- Gestión automática de identificadores únicos (OIDs)
- Búsquedas eficientes
- Integración con Redis

### Modelos Principales

#### User
```python
class User:
    username: str
    password_hash: str
    role: str  # 'master' o 'player'
```

#### Character
```python
class Character:
    name: str
    race: str
    character_class: str
    level: int
    # Atributos D&D
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    # Stats de combate
    armor_class: int
    initiative: int
    hit_points: int
    speed: int
    # Referencias
    user_id: str
    campaign: str
```

#### Campaign
```python
class Campaign:
    name: str
    is_public: bool
    master_id: str
    allowed_players: List[str]
```

#### Mission
```python
class Mission:
    name: str
    description: str
    campaign_name: str
    rewards: str
    votes: int
    voters: List[str]
```

## Roles y Permisos

### Máster
- Crear y gestionar campañas
- Crear y gestionar misiones
- Aceptar/rechazar jugadores
- Ver todos los personajes en sus campañas

### Jugador
- Crear y gestionar personajes
- Unirse a campañas públicas
- Solicitar unirse a campañas Privadas
- Votar misiones
- Ver detalles de campañas y misiones

## Contribución

1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Push a la rama
5. Crea un Pull Request

