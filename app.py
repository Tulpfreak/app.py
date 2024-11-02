from flask import Flask, request, render_template_string
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
        r"kun je uitleggen wat (.+) is",
        r"wat betekent de term (.+)",
        r"waar staat (.+) voor",
        r"geef een definitie van (.+)",
        r"kun je me vertellen wat (.+) betekent",
        r"wat bedoelen ze met (.+)",
        r"wat is de betekenis van (.+)",
        r"leg (.+) uit",
        r"wat houdt de term (.+) in",
        r"wat verstaan we onder (.+)",
        r"kun je uitleg geven over (.+)",
        r"beschrijf (.+)",
        r"kun je beschrijven wat (.+) is",
        r"hoe definieer je (.+)",
        r"wat houdt het begrip (.+) in",
        r"kun je een uitleg geven van (.+)",
        r"wat is de uitleg van (.+)",
        r"wat houdt de uitdrukking (.+) in",
        r"kun je toelichten wat (.+) betekent",
        r"wat valt er te zeggen over (.+)",
        r"wat houdt (.+) precies in",
        r"kun je kort uitleggen wat (.+) is",
        r"waar gaat (.+) over",
        r"kun je me helpen begrijpen wat (.+) betekent",
        r"wat is een eenvoudige uitleg van (.+)",
        r"wat houdt het woord (.+) in",
        r"leg het begrip (.+) uit",
        r"wat betekent het begrip (.+)",
        r"kun je me meer vertellen over (.+)",
        r"hoe zou je (.+) uitleggen",
        r"wat moet ik weten over (.+)",
        r"wat houdt het in als we het over (.+) hebben",
        r"wat kun je me vertellen over (.+)",
        r"waar gaat de term (.+) over",
        r"waar verwijst (.+) naar",
        r"wat zijn de details van (.+)",
        r"wat beschrijft (.+)",
        r"kun je specificeren wat (.+) betekent",
        r"hoe zou je (.+) definiëren",
        r"kun je (.+) nader toelichten",
        r"wat zijn de kenmerken van (.+)",
        r"wat omvat (.+)",
        r"kun je een samenvatting geven van (.+)",
        r"waar draait (.+) om",
        r"wat moet ik begrijpen over (.+)",
        r"kun je een kort overzicht geven van (.+)",
        r"wat zijn de belangrijkste punten van (.+)",
        r"kun je me een voorbeeld geven van (.+)",
        r"wat impliceert (.+)",
        r"wat komt er kijken bij (.+)",
        r"hoe zou je kort (.+) omschrijven",
        r"wat valt er te begrijpen over (.+)",
        r"kun je (.+) in eenvoudige woorden uitleggen",
        r"wat omvat de definitie van (.+)",
        r"wat valt er te weten over (.+)",
        r"wat zou je moeten weten over (.+)"
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
    
    html = '''
    <!doctype html>
    <html>
    <head>
        <title>Economische Begrippen Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                flex-direction: column;
            }
            .container {
                width: 80%;
                max-width: 800px;
                text-align: center;
                background-color: #ffffff;
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
                width: 100%;
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
    return render_template_string(html, antwoord=antwoord)

# Zorg ervoor dat de app luistert op de juiste host en poort
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Gebruik poort uit de omgevingsvariabele, of standaard 8080
    app.run(host='0.0.0.0', port=port, debug=True)
