from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
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
     return render_template("buggy-form.html", buggy = record)
  elif request.method == 'POST':
    msg=""

    #input of data from database
    qty_wheels = request.form['qty_wheels']
    flag_color = request.form['flag_color']
    flag_pattern = request.form['flag_pattern']
    flag_color_secondary = request.form['flag_color_secondary']
    power_type = request.form['power_type']
    hamster_booster = request.form['hamster_booster']
    power_units = request.form['power_units']
    aux_power_type = request.form['aux_power_type']
    aux_power_units = request.form['aux_power_units']
    tyres = request.form['tyres']
    qty_tyres = request.form['qty_tyres']
    armour = request.form['armour']
    attack = request.form['attack']
    qty_attacks = request.form['qty_attacks']
    fireproof = request.form['fireproof']
    insulated = request.form['insulated']
    antibiotic = request.form['antibiotic']
    banging = request.form['banging']
    #Beggining of cost calculation
    total_cost = 0
    if fireproof == "True":
       fireproof = 1
    else:
       fireproof = 0
       
    if insulated == "True":
       insulated = 1
    else:
       insulated = 0
       
    if antibiotic == "True":
       antibiotic = 1
    else:
       antibiotic = 0

    if banging == "True":
       banging = 1
    else:
       banging = 0

    
    if power_type == "petrol":
       total_cost += int(power_units)*4
    elif power_type == "fusion":
       total_cost += int(power_units)*400
    elif power_type == "steam":
       total_cost += int(power_units)*3
    elif power_type == "bio":
       total_cost += int(power_units)*5
    elif power_type == "electric":
       total_cost += int(power_units)*20
    elif power_type == "rocket":
       total_cost += int(power_units)*16
    elif power_type == "hamster":
       total_cost += int(power_units)*3
    elif power_type == "thermo":
       total_cost += int(power_units)*300
    elif power_type == "solar":
       total_cost += int(power_units)*16
    elif power_type == "wind":
       total_cost += int(power_units)*3
       
    if aux_power_type == "petrol":
       total_cost += int(aux_power_units)*4
    elif aux_power_type == "fusion":
       total_cost += int(aux_power_units)*400
    elif aux_power_type == "steam":
       total_cost += int(aux_power_units)*3
    elif aux_power_type == "bio":
       total_cost += int(aux_power_units)*5
    elif aux_power_type == "electric":
       total_cost += int(aux_power_units)*20
    elif aux_power_type == "rocket":
       total_cost += int(aux_power_units)*16
    elif aux_power_type == "hamster":
       total_cost += int(aux_power_units)*3
    elif aux_power_type == "thermo":
       total_cost += int(aux_power_units)*300
    elif aux_power_type == "solar":
       total_cost += int(aux_power_units)*16
    elif vpower_type == "wind":
       total_cost += int(aux_power_units)*3

    total_cost += int(hamster_booster)*5

    if tyres == "knobbly":
       total_cost += int(qty_tyres)*15
    elif tyres == "slick":
       total_cost += int(qty_tyres)*10
    elif tyres == "steelband":
       total_cost += int(qty_tyres)*20
    elif tyres == "reactive":
       total_cost += int(qty_tyres)*40
    elif tyres == "maglev":
       total_cost += int(qty_tyres)*50

    if armour == "wood":
       total_cost += 40
    elif armour == "aluminium":
       total_cost += 200
    elif armour == "thinsteel":
       total_cost += 100
    elif armour == "thicksteel":
       total_cost += 200
    elif armour == "titanium":
       total_cost += 290

    if fireproof == 1:
       total_cost += 70
    if insulated == 1:
       total_cost +=100
    if antibiotic == 1:
       total_cost += 90
    if banging == 1:
       total_cost += 42

    if attack == "spike":
       total_cost += int(qty_attacks)*5
    elif attack == "flame":
       total_cost += int(qty_attacks)*20
    elif attack == "charge":
       total_cost += int(qty_attacks)*20
    elif attack == "biohazard":
       total_cost += int(qty_attacks)*40
         
    #Validation of data and rules
    if not qty_wheels.isdigit():
      msg = f"{qty_wheels} isn't a number, please try again"
      return render_template("buggy-form.html", msg = msg)
    if (int(qty_wheels)%2) != 0:
       msg = f"The number of wheels must be even."
       return render_template("buggy-form.html", msg = msg)
      #msg = f"qty_wheels={qty_wheels}"
     # msg = f"flag_color={flag_color}"
    try:
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, hamster_booster=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?,insulated=?, antibiotic=?,banging=?, total_cost=? WHERE id=?", (qty_wheels, flag_color, flag_color_secondary, flag_pattern, hamster_booster, power_type, power_units, aux_power_type, aux_power_units, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost, DEFAULT_BUGGY_ID))
        con.commit()
        msg = "Record successfully saved"
    except:
      con.rollback()
      msg = "error in update operation"
    finally:
      con.close()
      return render_template("updated.html", msg = msg)

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
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
   
   return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
