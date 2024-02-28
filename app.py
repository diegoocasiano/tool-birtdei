import os
from flask import Flask, render_template, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pyairtable import Api
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)

#Carga el file .env
load_dotenv('.env') 

#API Key de SendGrid
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

#API Key & settings de Airtable
airtableApi = Api(os.environ.get('AIRTABLE_API_KEY'))
BASE_ID = 'appDTSitS55x2wF94'
TABLE_NAME = 'table-test1'
table = airtableApi.table(BASE_ID, TABLE_NAME)

# Obtén el HTML del correo
with open('email-birthday.html', 'r') as file:
    html_content = file.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_birthday_emails', methods=['POST'])
def send_birthday_emails():
    #Obtener la fecha actual cada vez que se presione el botón
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"Fecha actual obtenida: {today}")

    #Obtener los usuarios que cumplen años hoy
    all_records = table.all()

    # Lista para almacenar los correos electrónicos a los que se envió el mensaje
    sent_emails = []

    for record in all_records:
        birthday = record.get('fields', {}).get('Birthday')
        if birthday == today:
            print(f"Birthday encontrado para {record['fields'].get('Email')}: {birthday}")
        else:
            print(f"Birthday no encontrado para {record['fields'].get('Email')}: {birthday}")
    
    # Filtrar los registros para obtener los usuarios que cumplen años hoy
    birthday_users = [record for record in all_records if record.get('fields', {}).get('Birthday') == today]
    
    for user in birthday_users:
        message = Mail(
            from_email=("casiano@birtdei.com", "Diego de Birtdei"),
            to_emails=user['fields']['Email'],
            
            subject='¡Feliz cumpleaños!',
            html_content=html_content
        )
        response = sg.send(message)

        # Agregar el correo electrónico a la lista de correos enviados
        sent_emails.append(user['fields']['Email'])
    
    # Datos para pasar al template HTML
    data = {
        'date': today,
        'sent_emails': sent_emails,
        'num_emails_sent': len(sent_emails)
    }

    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

    