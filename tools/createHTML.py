def OTPHTML(num: int) -> str:
    ht = """
    <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP - Nova Gesti贸n de Inventarios</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
        }
        .container {
            width: 40%;
            max-width: 600px;
            padding: 20px;
            background-color: white;
            border-radius: 16px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .header {
            margin-bottom: 40px;
        }
        .header h1 {
            color: #F2542D;
            margin: 0;
        }
        .otp-section {
            background-color: #fff6ed;
            border: 2px solid #F2542D;
            border-radius: 16px;
            padding: 20px;
            margin: 20px 0;
            color:black;
            font-weight: bold;
            font-size: 24px;
        }
        .warning {
            color: #F2542D;
            margin: 20px 0;
            font-weight: bold;
        }
        .footer {
            margin-top: 40px;
        }
        .footer p {
            color: #000;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Verificación de dos pasos </h1>
        </div>
        <div class="otp-section">
            Tu código OTP es: <span>"""+str(num)+"""</span>
        </div>
        <div class="warning">
            No compartas este código con nadie.
        </div>
        <div class="footer">
            <p>Gracias por confiar en Nova.</p>
        </div>
    </div>
</body>
</html>"""
    return ht


def maintenanceHTML(maintenance: dict) -> str:
    ht = '''
    <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detalles de Mantenimiento</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #fff6ed;
            color: #0E9594;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #F2542D;
            border-radius: 10px;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0;
            color: #000;
        }
        .content {
            margin-bottom: 20px;
        }
        .content p {
            margin: 10px 0;
        }
        .footer {
            text-align: center;
            color: #562C2C;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Detalles de Mantenimiento</h1>
        </div>
        <div class="content">
            <p>Este correo se envió para notificar que se ha realizado un mantenimiento en su vivienda. 
            A continuación, se presentan los detalles:</p>
            <p><strong>Descripción: </strong>'''+maintenance["descripcion"]+'''</p>
            <p><strong>Fecha: </strong>'''+maintenance["fecha"]+'''</p>
        </div>
        <div class="footer">
            <p>Gracias por su atención.</p>
        </div>
    </div>
</body>
</html>
'''
    return ht


def inventoryHTML(inventory: dict) -> str:
    ht = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Diseño de Página Web</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                display: flex;
                justify-content: space-around;
            }
            .container {
                width: 40%;
                max-width: 1200px;
                padding: 20px;
            }
            .row {
                display: flex;
                gap: 20px;
                margin-bottom: 20px;
                justify-content: space-around;
            }
            .section {
                background-color: #fff6ed;
                border: 2px solid #F2542D;
                border-radius: 16px;
                padding: 20px;
                text-align: center;
                margin: 16px;
            }
            .section img {
                width: 100%;
                max-width: 150px;
                max-height: 150px;
                border: 1px solid #0E9594;
                border-radius: 12px;
                margin-bottom: 12px;
            }
            .section p {
                margin: 12px 0;
                color: #562C2C;
                font-weight: bold;
            }
            .container h1,h2 {
                color: #000;
                text-align: center;
            }
            .separator{
                margin-bottom: 64px;
            }
            .separator h1,h2 {
                margin-bottom: 48px;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <div class="separator">
                <h1>Inventario Propiedad</h1>
                <div class="section">
                    <p>''' + inventory["direccion"] + '''</p>
                    <img src="''' + obtener_link_imagen(inventory["imagen"]) + '''">
                </div>
            </div>
            <div class="separator">
                <h2>Habitaciones</h2>
'''
    list_muebles = []
    cont = 1
    for habitacion in inventory["habitaciones"]:
        list_muebles.extend(habitacion["muebles"])
        if cont == 1:
            ht += '''
                       <div class="row">
                           '''
        ht += '''
                       <div class="section">
                    <p>''' + habitacion["nombre"] + '''</p>
                    <img src="''' + obtener_link_imagen(habitacion["imagen"]) + '''">
                    <p>''' + habitacion["descripcion"] + '''</p>
                    </div>'''
        cont += 1
        if cont == 3:
            ht += '''
                       </div>'''
            cont = 1
    if cont == 2:
        ht += '''
                </div>'''

    ht += '''
            </div>
            <div class="separator">
                <h2>Muebles</h2>'''

    cont = 1
    for mueble in list_muebles:
        if cont == 1:
            ht += '''
                <div class="row">
                    '''
        ht += '''
                <div class="section">
                    <p>''' + mueble["nombre"] + '''</p>
                    <img src="''' + obtener_link_imagen(mueble["imagen"]) + '''">
                    <p>''' + mueble["estado"] + '''</p>
                    <p>''' + mueble["descripcion"] + '''</p>
                </div>'''
        cont += 1
        if cont == 3:
            ht += '''
                </div>'''
            cont = 1
    if cont == 2:
        ht += '''
                </div>'''

    ht += '''
        </div>
    </body>
    </html>'''

    return ht


def obtener_link_imagen(nombre_img):
    return "https://keynovaapi.onrender.com/static/images/" + nombre_img
