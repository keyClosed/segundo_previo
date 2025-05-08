# Ride-Sharing API

Este proyecto es una API REST para una aplicación de “Mini-Uber” desarrollada con Django y Django REST Framework. Incluye migraciones que crean datos iniciales (usuarios, vehículos, viajes y calificaciones).

---

## Requisitos previos

- Python 3.8+  
- pip  
- Virtualenv (recomendado)  
- Git  

---

## Instalación y puesta en marcha

1. **Clona o haz fork** de este repositorio en tu cuenta de GitHub:  
   ```bash
   git clone https://github.com/andresstbn/segundo_previo.git
   cd segundo_previo
   ```

2. **Crea un entorno virtual** (opcional pero recomendado):  
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows usa `env\Scripts\activate`
   ```
3. **Instala las dependencias**:  
   ```bash
   pip install -r requirements.txt
   ```
4. **Realiza las migraciones**:  
   ```bash
   python manage.py migrate
   ```
5. **Usa tu correo electrónico como usuario y tu código de estudiante como contraseña** para iniciar sesión.  
