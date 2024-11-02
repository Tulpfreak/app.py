from flask import Flask, request, render_template_string, url_for
import pandas as pd
import re
import os

app = Flask(__name__)

# Functie om het Excel-bestand in te lezen en om te zetten naar een dictionary
def lees_excel_bestand_als_dict(bestandspad):
    df = pd.read_excel(bestandspad)
    begrippen_dict = pd.Series(df['betekenis'].values, index=df['Begrip'].str.lower()).to_dict()
    return begrippen_dict

# Pad naar je Excel-bestand
bestandspad_excel = 'begrippen.xlsx'
begrippen_dict = lees_excel_bestand_als_dict(bestandspad_excel)

# Functie om begrip uit de vraag te halen en antwoord te geven
def beantwoord_vraag(vraag):
    # Zet de vraag om in kleine letters en verwijder eventuele leestekens
    vraag = vraag.lower().strip()

    # Patroonherkenning voor verschillende manieren om een begrip te vragen
    patronen = [
        r"wat is (.+)",
        r"wat betekent (.+)",
        r"wat houdt (.+) in",
        # Voeg hier andere patronen toe indien nodig
    ]

    # Zoek naar het begrip in de vraag met behulp van regex
    for patroon in patronen:
        match = re.search(patroon, vraag)
        if match:
            begrip = match.group(1).strip()
            # Zoek het begrip in de dictionary
            uitleg = begrippen_dict.get(begrip, "Het begrip is niet gevonden in het bestand.")
            return uitleg

    # Als geen van de patronen overeenkomt, geef een standaard antwoord
    return "Ik begrijp de vraag niet. Probeer een vraag zoals 'Wat is inflatie?'"

# Route voor de hoofdpagina
@app.route('/', methods=['GET', 'POST'])
def index():
    antwoord = ""
    if request.method == 'POST':
        vraag = request.form['vraag'].strip()
        antwoord = beantwoord_vraag(vraag)
    
    achtergrond_url = url_for('static', filename='background_image')  # Vervang 'jouw_afbeelding.png' door de naam van je achtergrondafbeelding

    html = '''
    <!doctype html>
    <html>
    <head>
        <title>Economische Begrippen Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-image: url('{{ achtergrond_url }}');
                background-size: cover;
                background-position: center;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
            }
            .container {
                width: 80%;
                max-width: 600px; /* Maak de container smaller */
                text-align: center;
                background-color: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .antwoord {
                font-size: 1.2em;
                margin-bottom: 20px;
                padding: 10px;
                background-color: #e0e7ff;
                border-radius: 5px;
                border: 1px solid #c7d2fe;
            }
            input[type="text"] {
                width: 90%; /* Maak de zoekbalk smaller */
                padding: 15px;
                font-size: 1.1em;
                margin-bottom: 20px;
                border-radius: 5px;
                border: 1px solid #c7d2fe;
                box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            input[type="submit"] {
                padding: 10px 20px;
                font-size: 1.1em;
                color: #fff;
                background-color: #4f46e5;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #4338ca;
            }
        </style>
    </head>
    <body>
        <div class="container">
            {% if antwoord %}
            <div class="antwoord"><strong>Antwoord:</strong> {{ antwoord }}</div>
            {% endif %}
            <form method="post">
                <input type="text" id="vraag" name="vraag" placeholder="Stel een vraag, bijv. 'Wat is inflatie?'" autofocus>
                <input type="submit" value="Zoek">
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, antwoord=antwoord, achtergrond_url=achtergrond_url)

# Zorg ervoor dat de app luistert op de juiste host en poort
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Gebruik poort uit de omgevingsvariabele, of standaard 8080
    app.run(host='0.0.0.0', port=port, debug=True)
