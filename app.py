import os
from flask import Flask, render_template, request, abort
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from pyairtable import Api
from datetime import datetime
from dotenv import load_dotenv

from sendgrid.helpers.mail import Asm

app = Flask(__name__)

# Clave secreta para la sesión de flask
app.secret_key = os.getenv('SECRET_KEY')

#Carga el file .env
load_dotenv('.env') 

#API Key de SendGrid
sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

#API Key & settings de Airtable
airtableApi = Api(os.environ.get('AIRTABLE_API_KEY'))
BASE_ID = 'apps6RTIL11SBA533'
TABLE_NAME = 'Users Waitlist'

# BASE_ID = 'appDTSitS55x2wF94'
# TABLE_NAME = 'table-test1'

table = airtableApi.table(BASE_ID, TABLE_NAME)

# Obtén el HTML del correo
with open('email-birthday.html', 'r') as file:
    html_content = file.read()


@app.route('/')
def index():
    sapo_value = request.args.get('sapo')
    if sapo_value != "dieal1107":
        abort(403)

    return render_template('index.html', sapo_value=sapo_value)

@app.route('/send_birthday_emails', methods=['POST'])
def send_birthday_emails():
    #Obtener la fecha actual cada vez que se presione el botón
    today = datetime.now().strftime('%m-%d')
    print(f"Fecha actual obtenida: {today}")

    all_records = table.all()

    # Lista para almacenar los correos electrónicos a los que se envió el mensaje
    sent_emails = []
    # Variable para rastrear si ocurrió un error
    error_occurred = False

    # Filtrar los registros para obtener los usuarios que cumplen años hoy. Se usa split('-') para convertir el formato de birthday a  ['AAAA', 'MM', 'DD'] y luego [1:] para ignorar el año y obtener solo['MM', 'DD'].
    birthday_users = [record for record in all_records if record.get('fields', {}).get('Birthday', '').split('-')[1:] == today.split('-')]
    
    for user in birthday_users:
        message = Mail(
            from_email=("casiano@birtdei.com", "Diego de Birtdei"),
            to_emails=user['fields']['Email'],
        )

        message.dynamic_template_data = {
        'subject': 'Es hoy! Feliz cumple! 🎁👀',
        }
        message.template_id = 'd-9f083c895d03468daa1fafae5ab2edc0'
        message.asm = Asm(group_id=26182)

        try:
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            print(f"Correo enviado exitosamente a {user['fields']['Email']}")

            # Agregar el correo electrónico a la lista de correos enviados
            sent_emails.append(user['fields']['Email'])

        except Exception as e:
            print(f"Error al enviar correo a {user['fields']['Email']}: {e}")
            error_occurred = True
    
    # Datos para pasar al template HTML
    if error_occurred:
        message = "Hubo un error al enviar el correo."
    elif len(sent_emails) > 0:
        message = "Correo de cumpleaños enviado con éxito."
    else:
        message = "Ningún usuario cumple años hoy"

    data = {
        'date': today,
        'message': message,
        'sent_emails': sent_emails,
        'num_emails_sent': len(sent_emails)
    }

    return render_template('result.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

    