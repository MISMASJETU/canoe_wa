from flask import Flask, render_template, request, jsonify
import re
import json

# Function to save registrace_list to a JSON file
def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

# Function to load registrace_list from a JSON file
def load_from_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Initialize registrace_list from a JSON file (if available)
#registrace_list = load_from_json('registrace.json')
registrace_list = []

# ...


app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
registrace_list = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('prvni_stranka.html', ucastnici=registrace_list), 200

@app.route('/druha_stranka', methods=['GET', 'POST'])
def druha_stranka():
    return render_template('druha_stranka.html', zprava="Tajná zpráva.."), 200

@app.route('/registrace', methods=['GET', 'POST'])
def registrace():
    if request.method == 'POST':
        nick = request.form.get('nick')
        prijmeni = request.form.get('prijmeni')
        trida = request.form.get('trida')
        je_plavec = request.form.get('je_plavec')
        kanoe_kamarad = request.form.get('kanoe_kamarad')

        # Kontrola zda-li je osoba je_plavec true
        if je_plavec != '1':
            return "Chyba: Je potřeba být plavcem.", 400

        # Kontrola zda-li nick je validní (znaky anglické abecedy, číslice, délka 2-20 znaků)
        if not (nick.isalnum() and 2 <= len(nick) <= 20):
            return "Chyba: Nick není platný.", 400

        # Client-side validation for prijmeni
        if not (prijmeni.isalnum() and 2 <= len(prijmeni) <= 20):
            return "Chyba: Příjmení není platné.", 400

        # Client-side validation for trida
        if not re.match(r'^[AEC][1234][ABC]?$', trida):
            return "Chyba: Třída není platná.", 400

        # Kontrola kanoe_kamarad, pokud je vyplněn
        if kanoe_kamarad:
            if not (len(kanoe_kamarad) <= 20):
                return "Chyba: Kamarád na kanoe není platný.", 400

        if kanoe_kamarad is None:
            kanoe_kamarad = 'Nevyplneno'



        # Uložení registrace
        registrace = [
            nick,
            prijmeni,
            trida,
            kanoe_kamarad
        ]
        print(registrace)
        registrace_list.append(registrace)

        # Save registrace_list to a JSON file
        #save_to_json('registrace.json', registrace_list)
        return index()

    return render_template('registrace.html'), 200


def is_duplicate_nickname(nick):
    return any(registrace[0] == nick for registrace in registrace_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
