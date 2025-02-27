# To DO:

- items
- Archivos con errores : operations, character/lists, fight
- Revisar Join de Combat, hacer que si el dm elimina le resetee el boton.
- Mensajes flash de login en otras pantallas. 



# DnD Campaign Manager

## Descripción
El DnD Campaign Manager es una aplicación web diseñada para gestionar campañas de Dragones y Mazmorras. Permite a los jugadores crear y gestionar sus personajes, mientras que los másters pueden crear campañas, definir misiones y gestionar combates. La aplicación utiliza Flask como framework principal y Redis como almacenamiento de datos.

## Estructura del Proyecto
```
dnd-campaign-manager
├── app
│   ├── __init__.py
│   ├── auth.py
│   ├── models
│   │   ├── user.py
│   │   ├── character.py
│   │   ├── campaign.py
│   │   ├── mission.py
│   │   ├── combat.py
│   │   └── item.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── characters.py
│   │   ├── campaigns.py
│   │   ├── combats.py
│   │   └── missions.py
│   ├── templates
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── characters
│   │   │   ├── create.html
│   │   │   ├── edit.html
│   │   │   └── list.html
│   │   ├── campaigns
│   │   │   ├── create.html
│   │   │   ├── edit.html
│   │   │   ├── list.html
│   │   │   ├── play_master.html
│   │   │   ├── play_player.html
│   │   │   ├── view.html
│   │   │   ├── operations_master.html
│   │   │   └── operations_player.html
│   │   ├── combats
│   │   │   ├── manage.html
│   │   │   └── view.html
│   │   ├── missions
│   │   │   ├── manage.html
│   │   │   └── view.html
│   │   └── index.html
│   ├── static
│   │   └── styles.css
│   └── main.py
├── migrations
├── create_users.py
├── migrate.py
├── requirements.txt
└── README.md
```

### Descripción de los folders
- **app**: Contiene la aplicación principal de Flask.
  - **__init__.py**: Inicializa la aplicación Flask.
  - **auth.py**: Maneja la autenticación de usuarios.
  - **models**: Contiene los modelos de datos.
    - **user.py**: Modelo de usuario.
    - **character.py**: Modelo de personaje.
    - **campaign.py**: Modelo de campaña.
    - **mission.py**: Modelo de misión.
    - **combat.py**: Modelo de combate.
    - **item.py**: Modelo de objeto.
  - **routes**: Contiene las rutas de la aplicación.
    - **__init__.py**: Inicializa las rutas.
    - **auth.py**: Rutas de autenticación.
    - **characters.py**: Rutas de personajes.
    - **campaigns.py**: Rutas de campañas.
    - **combats.py**: Rutas de combates.
    - **missions.py**: Rutas de misiones.
  - **templates**: Contiene las plantillas HTML.
    - **auth**: Plantillas de autenticación.
    - **characters**: Plantillas de personajes.
    - **campaigns**: Plantillas de campañas.
    - **combats**: Plantillas de combates.
    - **missions**: Plantillas de misiones.
    - **index.html**: Plantilla de la página principal.
  - **static**: Contiene archivos estáticos como CSS.
    - **styles.css**: Archivo de estilos CSS.
  - **main.py**: Archivo principal de la aplicación.
- **migrations**: Contiene archivos de migración de la base de datos.
- **create_users.py**: Script para crear usuarios y datos de prueba.
- **migrate.py**: Script para realizar migraciones de la base de datos.
- **requirements.txt**: Archivo de dependencias del proyecto.
- **README.md**: Archivo README del proyecto.

## Scripts

### migrate.py
El script `migrate.py` se utiliza para realizar migraciones de la base de datos. Esto es útil cuando se realizan cambios en los modelos de datos y se necesita actualizar la estructura de la base de datos.

Para ejecutar el script `migrate.py`, usa el siguiente comando:
```bash
python migrate.py
```

### create_users.py
El script `create_users.py` se utiliza para restablecer la base de datos y poblarla con datos genéricos. Esto incluye la creación de usuarios, campañas, personajes, misiones y combates.

Para ejecutar el script `create_users.py`, usa el siguiente comando:
```bash
python create_users.py
```

Este script es útil para configurar rápidamente un entorno de desarrollo con datos de prueba.

## Requisitos
- Python 3.x
- Flask
- Flask-Login
- Redis

## Tecnologías Usadas

### Backend
- **Flask**: Framework web utilizado para construir la aplicación.
- **Flask-Login**: Extensión de Flask para gestionar la autenticación de usuarios.
- **Redis**: Base de datos en memoria utilizada para almacenar datos de la aplicación.

### Frontend
- **HTML/CSS**: Lenguajes de marcado y estilo utilizados para construir la interfaz de usuario.
- **Jinja2**: Motor de plantillas utilizado por Flask para renderizar HTML dinámico.

### Otros
- **Python**: Lenguaje de programación utilizado para desarrollar la aplicación.
- **Werkzeug**: Biblioteca WSGI utilizada por Flask para gestionar solicitudes y respuestas HTTP.

## Entidades principales

### Usuarios 👤
- **Atributos**:
  - `id`: ID del usuario
  - `username`: Nombre de usuario
  - `password`: Contraseña
  - `role`: Rol del usuario (jugador o máster)
- **Relaciones**:
  - Un usuario puede tener varios personajes.
  - Un usuario (máster) puede gestionar varias campañas.

### Personajes ⚔️
- **Atributos**:
  - `id`: ID del personaje
  - `name`: Nombre del personaje
  - `user_id`: ID del usuario propietario
  - `race`: Raza del personaje
  - `character_class`: Clase del personaje
  - `level`: Nivel del personaje 
  - `strength`: Fuerza
  - `dexterity`: Destreza
  - `constitution`: Constitución
  - `intelligence`: Inteligencia
  - `wisdom`: Sabiduría
  - `charisma`: Carisma
  - `hit_points`: Puntos de vida
  - `armor_class`: Clase de armadura
  - `initiative`: Iniciativa
  - `speed`: Velocidad
  - `campaign_id`: ID de la campaña a la que pertenece (opcional)
- **Relaciones**:
  - Un personaje pertenece a un usuario (jugador).
  - Un personaje puede estar en una campaña.

### Campañas 📜
- **Atributos**:
  - `id`: ID de la campaña
  - `name`: Nombre de la campaña
  - `master_id`: ID del máster propietario
  - `is_public`: Indica si la campaña es pública o privada
  - `allowed_players`: Lista de jugadores permitidos
- **Relaciones**:
  - Una campaña pertenece a un máster (usuario).
  - Una campaña puede tener varios personajes asociados.
  - Una campaña tiene varias misiones.

### Misiones 🎭
- **Atributos**:
  - `id`: ID de la misión
  - `name`: Nombre de la misión
  - `description`: Descripción de la misión
  - `reward`: Recompensa de la misión
  - `campaign_id`: ID de la campaña a la que pertenece
- **Relaciones**:
  - Una misión pertenece a una campaña.

### Combates ⚔️🔥
- **Atributos**:
  - `id`: ID del combate
  - `name`: Nombre del combate
  - `campaign_id`: ID de la campaña a la que pertenece
  - `participants`: Lista de participantes
  - `turn_order`: Orden de turnos
  - `active`: Indica si el combate está activo
- **Relaciones**:
  - Un combate pertenece a una campaña.
  - Puede incluir varios personajes y enemigos.

## Roles

### Máster
- Puede crear y gestionar campañas.
- Puede definir misiones y combates.
- Tiene control total sobre las campañas y sus elementos.

### Jugador
- Puede crear y gestionar personajes.
- Puede unirse a campañas públicas o a las que ha sido invitado.
- Participa en misiones y combates definidos por el máster.

## Roles

### Máster
- Puede crear y gestionar campañas.
- Puede definir misiones y combates.
- Tiene control total sobre las campañas y sus elementos.

### Jugador
- Puede crear y gestionar personajes.
- Puede unirse a campañas públicas o a las que ha sido invitado.
- Participa en misiones y combates definidos por el máster.

