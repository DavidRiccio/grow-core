# Archivo de configuración para el generador de documentación Sphinx.
#
# Para la lista completa de valores de configuración incorporados, consulta la documentación:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Información del proyecto ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Api-Grow'
copyright = '2025, David Riccio de Abreu y César Domínguez Romero'
author = 'David Riccio de Abreu y César Domínguez Romero'
release = '1.0.0'

import os
import sys

# Añadir la ruta del proyecto al sistema
sys.path.insert(0, os.path.abspath('../../'))

# Configurar el módulo de ajustes de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

import django

# Inicializar Django
django.setup()

# -- Extensiones de Sphinx ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',  # Generación automática de documentación a partir de docstrings
    'sphinx.ext.viewcode',  # Añadir enlaces a la fuente de código
    'sphinx.ext.napoleon',  # Soporte para Google y NumPy style docstrings
    'sphinx_autodoc_typehints',  # Soporte para anotaciones de tipo en la documentación
]

# -- Opciones para la salida HTML ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'  # Tema para la documentación HTML
html_static_path = ['_static']  # Ruta para archivos estáticos
templates_path = ['_templates']  # Ruta para plantillas personalizadas
exclude_patterns = []  # Patrones de exclusión para archivos
language = 'es'  # Idioma de la documentación
