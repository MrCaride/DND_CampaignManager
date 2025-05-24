# DnD Campaign Manager

Aplicación web para gestionar campañas de D&D, donde los masters pueden crear campañas y misiones, y los jugadores pueden unirse con sus personajes.

## Pasos para arrancar la aplicación
1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Crear datos iniciales (opcional):
```bash
python create_users.py
```
Este script crea los siguientes usuarios de prueba:

Masters:
- username: "master", password: "masterpass"
- username: "master2", password: "masterpass2"
- username: "master3", password: "masterpass3"

Jugadores:
- username: "user1", password: "password1"
- username: "user2", password: "password2"
- username: "user3", password: "password3"
- username: "user4", password: "password4"
- username: "user5", password: "password5"
- username: "player1", password: "playerpass1"
- username: "player2", password: "playerpass2"

Además crea datos de campañas, misiones y otros. 

3. Arrancar el servidor (cualquiera de estas dos opciones):
```bash
python app.py
```
o
```bash
flask run
```
La aplicación estará disponible en http://127.0.0.1:5000

## Otros archivos
- `uninstall_all_packages.py`: Script para desinstalar todos los paquetes pip instalados (usar solo si es necesario limpiar el entorno)
- `create_users.py`: Script para crear usuarios y datos de prueba iniciales






