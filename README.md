# DnD Campaign Manager

## Descripción
El DnD Campaign Manager es una aplicación web diseñada para gestionar campañas de Dragones y Mazmorras. Permite a los jugadores crear y gestionar sus personajes, mientras que los másters pueden crear campañas, definir misiones y gestionar combates. La aplicación utiliza Flask como framework principal y Redis como almacenamiento de datos.

### Scripts

#### migrate.py

El script `migrate.py` se utiliza para realizar migraciones de la base de datos. Esto es útil cuando se realizan cambios en los modelos de datos y se necesita actualizar la estructura de la base de datos.

Para ejecutar el script `migrate.py`, usa el siguiente comando:
```bash
python migrate.py
```

#### create_users.py

El script `create_users.py` se utiliza para restablecer la base de datos y poblarla con datos genéricos. Esto incluye la creación de usuarios, campañas, personajes, misiones y combates.

Para ejecutar el script `create_users.py`, usa el siguiente comando:
```bash
python create_users.py
```

Este script es útil para configurar rápidamente un entorno de desarrollo con datos de prueba.

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

## Requisitos
- Python 3.x
- Flask
- Flask-Login
- Redis

## Entidades principales

### Usuarios 👤
- Atributos:
  - `id`: ID del usuario
  - `username`: Nombre de usuario
  - `password`: Contraseña
  - `role`: Rol del usuario (jugador o máster)
- Relaciones:
  - Un usuario puede tener varios personajes.
  - Un usuario (máster) puede gestionar varias campañas.

### Personajes ⚔️
- Atributos:
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
- Relaciones:
  - Un personaje pertenece a un usuario (jugador).
  - Un personaje puede estar en una campaña.

### Campañas 📜
- Atributos:
  - `id`: ID de la campaña
  - `name`: Nombre de la campaña
  - `master_id`: ID del máster propietario
  - `is_public`: Indica si la campaña es pública o privada
  - `allowed_players`: Lista de jugadores permitidos
- Relaciones:
  - Una campaña pertenece a un máster (usuario).
  - Una campaña puede tener varios personajes asociados.
  - Una campaña tiene varias misiones.

### Misiones 🎭
- Atributos:
  - `id`: ID de la misión
  - `name`: Nombre de la misión
  - `description`: Descripción de la misión
  - `campaign_id`: ID de la campaña a la que pertenece
- Relaciones:
  - Una misión pertenece a una campaña.

### Combates ⚔️🔥
- Atributos:
  - `id`: ID del combate
  - `name`: Nombre del combate
  - `campaign_id`: ID de la campaña a la que pertenece
  - `participants`: Lista de participantes
  - `turn_order`: Orden de turnos
  - `active`: Indica si el combate está activo
- Relaciones:
  - Un combate pertenece a una campaña.
  - Puede incluir varios personajes y enemigos.

### Inventario y objetos 🏹
- Atributos:
  - `id`: ID del objeto
  - `name`: Nombre del objeto
  - `type`: Tipo de objeto
  - `effects`: Efectos del objeto
  - `quantity`: Cantidad
- Relaciones:
  - Un personaje puede tener varios objetos en su inventario.
  - Los objetos pueden estar disponibles en una campaña (recompensas, cofres, etc.).

