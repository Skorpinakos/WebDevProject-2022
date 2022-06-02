import pandas as pd
import csv
import string
import random
import pathlib
from faker import Faker
from unidecode import unidecode
import datetime


def create_all():
    # path = str(pathlib.Path(__file__).parent.resolve())+'\\images\\'
    fake = Faker('el_GR')

    entities_properties = {

        'Location': {"id": ['integer', True], "building": ['string', False], "coordinates_x": ['integer', False], "coordinates_y": ['integer', False]},

        'Ticket': {"id": ['integer', True], "title": ['string', False], "description": ['text', False], "creation_date": ['date', False],
                   "closure_date": ['date', False], "state": ['string', False], "image_path": ['string', False], "contact_phone": ['string', False], "contact_email": ['string', False],
                   "locale": ['integer', False, 'Location', 'id'], "category": ['string', False]},

        'Contract': {"id": ['integer', True], "key": ['string', False, True], "details": ['text', False], "date": ['date', False],
                     "cost": ['float', False], "damage": ['integer', False, 'Ticket', 'id'], "technician_firstname": ['string', False], "technician_lastname": ['string', False]}
    }

    def get_random_string(letters_count, digits_count=0):
        letters = ''.join((random.choice(string.ascii_letters)
                          for i in range(letters_count)))
        digits = ''.join((random.choice(string.digits)
                         for i in range(digits_count)))

        # Convert resultant string to list and shuffle it to mix letters and digits
        sample_list = list(letters + digits)
        random.shuffle(sample_list)
        # convert list to string
        final_string = ''.join(sample_list)
        return final_string

    def get_relevant(entity, attribute):
        df = pd.read_csv("data/{}.csv".format(entity))
        saved_column = df[attribute]
        return list(saved_column)

    def make_without_foreign(leksiko, entity):

        buildings = ['Ηλεκτρολόγων 1', 'Ηλεκτρολόγων 2', 'Μηχανολόγων',
                     'Χημικών Μηχανικών', 'Φυσικό', 'Μαθηματικό', 'Πρυτανεία', 'Εστία']
        primaryKey = 1
        entity_diction = leksiko[entity]
        list_of_dicts = []
        primaries = []
        if entity == 'Location':
            end = 50
        else:
            end = random.randint(60, 90)
        for i in range(1, end):
            temp_dict = {}
            for attribute in entity_diction.keys():
                typos = entity_diction[attribute][0]
                primary = entity_diction[attribute][1]
                name = attribute
                if primary == False:
                    if typos == 'integer':
                        if name == 'coordinates_x':
                            temp_dict[name] = random.randint(200, 800)
                        elif name == 'coordinates_y':
                            temp_dict[name] = random.randint(200, 800)

                    elif typos == 'string':
                        if name == 'building':
                            building = random.choice(buildings)
                            temp_dict[name] = building

                    else:
                        print('error   ', typos, entity)

                if primary == True:
                    while True:
                        temp = primaryKey
                        primaryKey += 1
                        if temp not in primaries:
                            temp_dict[name] = temp
                            primaries.append(temp)
                            break
            list_of_dicts.append(temp_dict)
            with open('data/{}.csv'.format(entity), 'w', encoding='utf8') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=entity_diction.keys())
                writer.writeheader()
                writer.writerows(list_of_dicts)
        return primaries

    def make_with_foreign(leksiko, entity, primars):

        damage_titles = ['Διαρροή νερού σε σωλήνα', 'Σπασμένη λάμπα στο διάδρομο',
                         'Χαλασμένο έδρανο', 'Δεν ανάβουν τα φώτα στην αίθουσα', 'Σπασμένα μάρμαρα στη σκάλα']
        damage_descriptions = ["""Περνώντας το πρωί πριν πάω στο μάθημα γλίστρησα και παρατήρησα ότι το πάτωμα ήταν βρεγμένο.
            Ψάχνοντας λίγο παρατήρησα ότι ένας σωλήνας που περνάει από πάνω έχει σπάσει και εμφανίζεται διαρροή.""",
                               """Φεύγοντας το βράδυ από το μάθημα παρατήρησα ότι ο διάδρομος ήταν σκοτεινός.
                               Μετά από λίγο είδα ότι η δεύτερη κατά σειρά λάμπα έχει σπάσει""",
                               """ Το πρωί ένα φίλος μου πήγε να κάτσει στο έδρανο και το έδρανο έσπασε με αποτέλεσμα αυτός να πέσει κάτω και να τραυματιστεί.
                               Το συγκεκριμμένο έδρανο βρίσκεται στην 3η σειρά και είναι το δεύτερο από δεξιά.""",
                               """ Σήμερα ενώ κάναμε μάθηκα και είχε αρχίσει να σκοτεινιάζει ο καθηγητής προσπάθησε να ανάψει τα φώτα αλλά άναβαν. Ως αποτέλεσμα
                               δεν μπορέσαμε να χρησιμοποιήσουμε τον πίνακα γιατί ήταν αργά, είχε σκοτεινιάσει και δεν βλέπαμε.""",
                               """Το τρίτο σκαλί έχει σπάσει και είναι επικίνδυνο να σκοντάψει ή να γλιστρίσει κάποιος"""]
        contract_details = ['Αλλαγή σπασμένου σωλήνα', 'Αλλαγή λάμπας',
                            'Επισκευή έδρανου', 'Αλλαγή διακόπτη', 'Πρόχειρη συγκόληση μαρμάρων στη σκάλα']
        states = ['Υπό επεξεργασία', 'Επιβεβαιωμένη',
                  'Ανοιχτή', 'Υπό επισκευή', 'Κλειστή']
        categories = ['Ηλεκτρολoγικά',
                      'Υδραυλικά', 'Μηχανολογικά', 'Οικοδομικά', 'Ελαιοχρωματιστικά']
        primaryKey = 1
        entity_diction = leksiko[entity]
        list_of_dicts = []
        primaries = []
        if entity == 'Contract':
            end = 74
        if entity == 'Ticket':
            end = 350
        for i in range(1, end):
            temp_dict = {}
            for attribute in entity_diction.keys():
                typos = entity_diction[attribute][0]
                primary = entity_diction[attribute][1]
                name = attribute
                t = random.randint(0, 4)
                if len(entity_diction[attribute]) < 4:
                    if primary == False:
                        if typos == 'string':
                            if name == 'title':
                                temp_dict[name] = damage_titles[t]
                            elif name == 'state':
                                temp_dict[name] = random.choice(states)
                            elif name == 'key':
                                temp_dict[name] = fake.unique.localized_ean8()
                            elif name == 'image_path':
                                temp_dict[name] = str(
                                    'images/a' + str(random.randint(1, 6)) + '.jpg')
                            elif name == 'contact_phone':
                                temp_dict[name] = fake.phone_number()
                            elif name == 'contact_email':
                                temp_dict[name] = fake.email()
                            elif name == 'category':
                                temp_dict[name] = random.choice(categories)
                            elif name == 'technician_firstname':
                                if i % 2:
                                    fname = fake.first_name_female()
                                else:
                                    fname = fake.first_name_male()
                                temp_dict[name] = fname
                            elif name == 'technician_lastname':
                                if i % 2:
                                    sname = fake.last_name_female()
                                else:
                                    sname = fake.last_name_male()
                                temp_dict[name] = sname

                        elif typos == 'text':
                            if name == 'description':
                                temp_dict[name] = damage_descriptions[t]
                            elif name == 'details':
                                temp_dict[name] = contract_details[t]

                        elif typos == 'float':
                            if name == 'cost':
                                temp_dict[name] = random.random() * 50.0

                        elif typos == 'date':
                            if name == 'date':
                                temp_dict[name] = fake.date()
                            elif name == 'creation_date':
                                creation_date = fake.date_between(
                                    start_date='-10y')
                                temp_dict[name] = creation_date
                            elif name == 'closure_date':
                                closure_date = fake.date_between_dates(
                                    date_start=creation_date, date_end=datetime.datetime.now())
                                temp_dict[name] = closure_date
                    else:
                        while True:
                            temp = primaryKey
                            primaryKey += 1
                            if temp not in primaries:
                                temp_dict[name] = temp
                                primaries.append(temp)
                                break
                elif len(entity_diction[attribute]) == 4:
                    if primary == True:
                        while True:
                            temp = random.choice(get_relevant(
                                entity_diction[attribute][2], entity_diction[attribute][3]))
                            if temp not in primaries:
                                temp_dict[name] = temp
                                primaries.append(temp)
                                break
                    else:
                        temp_dict[name] = random.choice(get_relevant(
                            entity_diction[attribute][2], entity_diction[attribute][3]))

            list_of_dicts.append(temp_dict)
            with open("data/{}.csv".format(entity), 'w', encoding='utf8') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=entity_diction.keys())
                writer.writeheader()
                writer.writerows(list_of_dicts)

        return primaries

    prims = {}

    location_prim = make_without_foreign(entities_properties, 'Location')
    prims['Location'] = location_prim
    prims['Ticket'] = make_with_foreign(entities_properties, 'Ticket', prims)
    prims['Contract'] = make_with_foreign(
        entities_properties, 'Contract', prims)
    return
