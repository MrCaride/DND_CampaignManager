# DnD Campaign Manager

## Descripción
El DnD Campaign Manager es una aplicación web diseñada para gestionar campañas de Dragones y Mazmorras. Permite a los jugadores crear y gestionar sus personajes, mientras que los másters pueden crear campañas, definir misiones y gestionar combates. La aplicación utiliza Flask como framework principal y Redis como almacenamiento de datos.

## Estructura del Proyecto
```
dnd-campaign-manager
├── app
│   ├── __init__.py
│   ├── models
│   │   ├── user.py
│   │   ├── character.py
│   │   ├── campaign.py
│   │   ├── mission.py
│   │   ├── combat.py
│   │   └── item.py
│   ├── routes
│   │   ├── auth.py
│   │   ├── characters.py
│   │   ├── campaigns.py
│   │   └── combats.py
│   ├── templates
│   └── static
├── app.py
├── requirements.txt
└── README.md
```

## Requisitos
- Python 3.x
- Flask
- Flask-Login
- Redis

  
🛠️ Entidades principales

    Usuarios 👤
        Atributos: ID, nombre, email, contraseña (hash), rol (jugador o máster).
        Relaciones:
            Un usuario puede tener varios personajes.
            Un usuario (máster) puede gestionar varias campañas.

    Personajes ⚔️
        Atributos: ID, nombre, raza, clase, nivel, estadísticas (fuerza, destreza, etc.), inventario.
        Relaciones:
            Un personaje pertenece a un usuario (jugador).
            Un personaje puede estar en varias campañas.

    Campañas 📜
        Atributos: ID, nombre, descripción, estado (abierta/cerrada), máster asignado.
        Relaciones:
            Una campaña pertenece a un máster (usuario).
            Una campaña puede tener varios personajes asociados.
            Una campaña tiene varias misiones.

    Misiones 🎭
        Atributos: ID, nombre, descripción, estado (pendiente/en progreso/completada), votos de jugadores.
        Relaciones:
            Una misión pertenece a una campaña.
            Una misión puede estar vinculada a combates.

    Combates ⚔️🔥
        Atributos: ID, enemigos, estado del combate, log de acciones.
        Relaciones:
            Un combate pertenece a una campaña.
            Puede incluir varios personajes y enemigos.

    Inventario y objetos 🏹
        Atributos: ID, nombre, tipo, efectos, cantidad.
        Relaciones:
            Un personaje puede tener varios objetos en su inventario.
            Los objetos pueden estar disponibles en una campaña (recompensas, cofres, etc.).
