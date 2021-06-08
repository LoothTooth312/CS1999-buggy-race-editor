from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------

def costcalc(ppower,punit,apower,aunit,hamster,tyre,tyreunit,armour,attack,attackunit,fireproof,insulated,antibiotic,banging,):
    cost = 0
    if ppower == "petrol":
        ppcost = 4
    elif ppower == "fusion":
        ppcost = 400
    elif ppower == "steam":
        ppcost = 3
    elif ppower == "bio":
        ppcost = 5
    elif ppower == "electric":
        ppcost = 20
    elif ppower == "rocket":
        ppcost = 16
    elif ppower == "hamster":
        ppcost = 2
    elif ppower == "thermo":
        ppcost = 300
    elif ppower == "solar":
        ppcost = 40
    elif ppower == "wind":
        ppcost = 20

    ppcost = ppcost * int(punit) 
    
    if apower == "petrol":
        apcost = 4
    elif apower == "fusion":
        apcost = 400
    elif apower == "steam":
        apcost = 3
    elif apower == "bio":
        apcost = 5
    elif apower == "electric":
        apcost = 20
    elif apower == "rocket":
        apcost = 16
    elif apower == "hamster":
        apcost = 2
    elif apower == "thermo":
        apcost = 300
    elif apower == "solar":
        apcost = 40
    elif apower == "wind":
        apcost = 20

    hamstercost = int(hamster) * 5
    apcost = apcost * int(aunit) 

    powercost = apcost + ppcost + hamstercost

    if tyre == "knobbly":
        tcost = 15
    elif tyre == "slick":
        tcost = 10
    elif tyre == "steelband":
        tcost = 20
    elif tyre == "reactive":
        tcost = 40
    elif tyre == "maglev":
        tcost = 50

    tcost = tcost * int(tyreunit)

    if armour == "none":
        armourcost = 0
    elif armour == "wood":
        armourcost = 40
    elif armour == "aluminium":
        armourcost = 200
    elif armour == "thinsteel":
        armourcost = 100
    elif armour == "thicksteel":
        armourcost = 200
    elif armour == "titanium":
        armourcost = 290

    if attack == "none":
        attackcost = 0 
    elif attack == "spike":
        attackcost = 5 
    elif attack == "flame":
        attackcost = 20 
    elif attack == "charge":
        attackcost = 28
    elif attack == "biohazard":
        attackcost = 30 

    attackcost = attackcost * int(attackunit)

    if fireproof == "1":
        fireproofcost = 70
    else:
        fireproofcost = 0
    if insulated == "1":
        insulatedcost = 100
    else:
        insulatedcost = 0
    if antibiotic == "1":
        antibioticcost = 90
    else:
        antibioticcost = 0
    if banging == "1":
        bangingcost = 42
    else:
        bangingcost = 0
        

    totalcost = powercost + tcost +armourcost + attackcost + fireproofcost + insulatedcost + antibioticcost + bangingcost
    
    return totalcost



@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
       con = sql.connect(DATABASE_FILE)
       con.row_factory = sql.Row
       cur = con.cursor()
       cur.execute("SELECT * FROM buggies")
       record = cur.fetchone(); 
       return render_template("buggy-form.html" , buggy = record)
    elif request.method == 'POST':
        msg = ''
        vio = ''
        qty_wheels = request.form['qty_wheels']
        if not qty_wheels.isdigit():
            msg = "The number of wheels must be a number"
            return render_template("updated.html" , msg = msg)
        elif int(qty_wheels) < 4:
            msg = "The number of wheels must be greater than four"
            return render_template("updated.html" , msg = msg)
        elif (int(qty_wheels) % 2) != 0:
            vio = "RULE VIOLATION: Please enter in an even number of wheels"
        flag_color = request.form['flag_color']
        flag_color_secondary = request.form['flag_color_secondary']
        flag_pattern = request.form['flag_pattern']
        if flag_color_secondary.lower() == flag_color.lower() and flag_pattern != "plain":
            vio = "RULE VIOLATION: Please enter in a different secondary colour "
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        if not power_units.isdigit():
            msg = "The input for units of power must be a number"
            return render_template("updated.html" , msg = msg)
        if int(power_units) < 1:
            msg = "The primary power must be greater than 1"
            return render_template("updated.html" , msg = msg)
        aux_power_type = request.form['aux_power_type']
        aux_power_unit = request.form['aux_power_unit']
        hamster_booster = request.form['hamster_booster']
        if not power_units.isdigit():
            msg = "The input for number of hamster boosters must be a number"
            return render_template("updated.html" , msg = msg)
        elif power_type != 'hamster' and int(hamster_booster) > 0 or aux_power_type != 'hamster' and int(hamster_booster) > 0:
            msg = "A power type must be set to hamster in order to use this"
            return render_template("updated.html" , msg = msg)
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        if int(qty_tyres) < int(qty_wheels):
            vio = "RULE VIOLATION: The number of tyres can not be less than the number of wheels "
            return render_template("updated.html" , msg = msg)
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        try:
            fireproof = request.form['fireproof']
        except:
            fireproof = False
        try:
            insulated = request.form['insulated']
        except:
            insulated = False
        try: 
            antibiotic = request.form['antibiotic']
        except:
            antibiotic = False 
        try:
            banging = request.form['banging']
        except:
            banging = False
        algo = request.form['algo']
        if algo == "buggy":
            vio = "RULE VIOLATION: the algorithm can not be buggy"
        total_cost = costcalc(power_type,power_units,aux_power_type,aux_power_unit,hamster_booster,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging)
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=? WHERE id=?",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, DEFAULT_BUGGY_ID),
                )
                cur.execute(
                    "UPDATE buggies set power_type=?, power_units=?, aux_power_type=?, aux_power_unit=?, hamster_booster=? WHERE id=?",
                    (power_type,power_units,aux_power_type,aux_power_unit,hamster_booster, DEFAULT_BUGGY_ID )
                )
                cur.execute(
                    "UPDATE buggies set tyres=?, qty_tyres=? WHERE id=?",
                    (tyres, qty_tyres, DEFAULT_BUGGY_ID),
                )
                cur.execute(
                    "UPDATE buggies set armour=?, attack=?,qty_attacks=?, fireproof=?, insulated=?, antibiotic=?,banging=?, algo=? WHERE id=?",
                    (armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, DEFAULT_BUGGY_ID),
                )
                con.commit()
                msg = f"Record successfully saved, the total cost is {total_cost}" 
                #msg = f"qty_wheels={qty_wheels}" ,f"flag_color={flag_color}"S

        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg, vio = vio)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone(); 
    return render_template("buggy.html" , buggy = record)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    return render_template("buggy-form.html")

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
