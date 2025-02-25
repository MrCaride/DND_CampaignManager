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

## Instalación
1. Clona el repositorio:
   ```
   git clone https://github.com/tu_usuario/dnd-campaign-manager.git
   ```
2. Navega al directorio del proyecto:
   ```
   cd dnd-campaign-manager
   ```
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso
1. Inicia el servidor:
   ```
   python app.py
   ```
2. Accede a la aplicación en tu navegador en `http://127.0.0.1:5000`.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT.