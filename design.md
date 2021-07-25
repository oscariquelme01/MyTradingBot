# Descripción y objetivos del proyecto
Este proyecto es el primer ensayo/acercamiento a algo trading. A día de hoy no se demasiado de estrategias y por lo tanto no espero que  sea muy rentable. 

Como primer intento de algo trading, el proyecto debería de ser capaz de cumplir las siguientes funcionalidades:

    - Recoger datos de la api de binance de distintas monedas listadas en un fichero
    - Procesar los datos y decidir en base a una estrategia simple que monedas son candidatas a compras
    - Ejecutar ordenes sobre la estrategia implementada 
    - Mostrar el backtest en una aplicación de la estrategia implementada
    - Alguna forma de autentificación para entrar a la página 
    - Mostrar el balance del portfolio
    - Mostrar un historial de las ordenes que ha ido ejecutando

 # Diseño y lenguajes utilizados para cumplir los objetivos

 Los 4 primeros requisitos se cumplirán en python en los siguientes archivos:
    
    - Strategy.py: Implementará toda la interacción con los datos recibidos de la API de binance y tendrá funciones que darán como output la información de la orden que se debe procesar
    -Order.py: Implementará toda la funcionalidad para ejecutar una orden en cualquier dirección 
    -Backtest.py: Implementará el backtest de la estrategia definida en Strategy.py

 El resto de requisitos se harán en una web app con HTML, css y vanilla javascript y será lo último a implementar en los siguientes archivos:

    - index.html: Estructura básica de la web app
    - styles.css: Estilizado de la página 
    - history.js: Funcionalidad para controlar el backend del historial de compras
    - portfolio.js: Funcionalidad para controlar la información del portfolio
