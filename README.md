# Proyecto Integrador 4: Sistema Backend de una aplicaion web que facilita la busqueda de empleos a estudiantes egresados y que ayuda a buscar empleados a las empresas

## Integrantes:
- Judith de Jesús Orozco Vanega
- Nathaly Andrea Umaña Jorge
- Leandro Alejandro Gutiérrez Ampie
## Guía de configuración de proyecto 📕
Este documento será una guía en los pasos necesarios para poner en marcha el proyecto. Sigue cada paso para configurar correctamente el entorno de desarrollo.
## Requisitos Previos 📃
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) instalado en tu sistema.
- [Python](https://www.python.org/downloads/) instalado en tu sistema.
- [Postman](https://www.postman.com/downloads/) para hacer solicitudes HTTP.
- [Papertrail](https://papertrailapp.com/) para la visualización de los logs.
- [SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15) para la creación de la base de datos.

## Configuración 🧰

### 1. Crear un Entorno de Desarrollo en Conda
Para empezar, configura un entorno virtual usando conda con Python 3.12:
```bash
conda create -n nombre_entorno python=3.12
```
Activa el entorno de desarrollo creado:
```bash
conda activate nombre_entorno
```
### 2. Instalar las Dependencias
Con el entorno activado, instala las dependencias necesarias desde el archivo de requisitos:
```bash
pip install -r requirements.txt
```
### 3. Crear la Base de Datos
Usando SQL Server Management Studio, crea una nueva base de datos para el proyecto. Puedes asignarle el nombre que gustes.
### 4. Crear una cuenta en Papertrail
Crea una cuenta en Papertrail para obtener los detalles del Host y Puerto que te permitirán monitorear los logs.
### 5. Configurar las Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:
```bash
DB_NAME = 'El nombre de tu base de datos'
DB_HOST = 'El host de tu base de datos'
HOST_PAPERTRAIL = 'El host de tu Papertrail'
PORT_PAPERTRAIL = 'El puerto de tu Papertrail'
```
### 6. Realiza las migraciones
Genera las migraciones de los modelos a tu base de datos
```bash
python manage.py makemigrations 
```
Luego, aplica las migraciones
```bash
python manage.py migrate
```
### 7. Ejecutar el Proyecto
Ejecuta el proyecto con la configuración de desarrollador:
```bash
python manage.py runserver --settings=config.dev
```
### 8. Crear un superusuario
Para acceder al panel de administración de Django `/admin` o usarlo para generar un token, crea un superusuario:
```bash
python manage.py createsuperuser
```
### 9. Genera un token
Para poder consumir las API, accede a la interfaz de Swagger en /swagger, y genera un token utilizando las credenciales del superusuario o cualquier usuario con permisos.
Puedes generar el token y encontrar la documentación de las API en la URL `/swagger`.
### 8. Consumir las API
Utiliza Postman para realizar solicitudes a las API a travez de los endpoint. En la sección de autorización, selecciona "Bearer Token" e ingresa el token generado en el paso anterior.

## ¡Y listo! tendrás todo configurado para poder consumir las API creadas.