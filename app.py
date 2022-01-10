from flask import Flask, render_template, g, request, url_for, flash
import sqlite3

app_info = {
'db_file' : 'c:/PythonScripts/sqllitedata/cantor.db' 
}
 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Sdfdfdfdfdfdfdfdiigihgigh'

#definiowanie połączenia
def get_db():
    if not hasattr(g,  'sqlite_db'):
        conn  =sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db

#zamykanie połaczenia w przypadku błedu
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite3_db'):
        g.sqlite_db.close()



@app.route('/')
def index():
    return render_template('index.html' )


@app.route('/new_trans', methods=['GET','POST'])
def new_trans():
    if request.method =='GET':
        return render_template('new_trans.html' )



@app.route('/new_trans_resoult', methods=['GET','POST'])
def new_trans_resoult():
    #currency = "PLN"
    if request.method == 'GET':
        return render_template('new_trans.html')
    else:
        #sprawdzenie czy jest pole o nazwie currency, jesli tak to przypisujemy do zmiennej currency
        if 'currency' in request.form:
            currency = request.form['currency']
 
        if 'date_trans' in request.form:
            date_trans = request.form['date_trans']

        if 'budget' in request.form:
            budget = request.form['budget']

        if 'amount' in request.form:
            amount = request.form['amount']

        if 'course' in request.form:
            course = request.form['course']

        if 'cost' in request.form:
            cost = request.form['cost']
        
        if 'type' in request.form:
            type = request.form['type']

        db = get_db()
        sql_command = 'insert into new_trans(currency, date_trans,budget,amount,course, cost, type) values (?,?,?,?,?,?,?)'
        db.execute(sql_command,[ currency, date_trans, budget, amount, course, cost, type])
        db.commit()
     

        return render_template('new_trans_resoult.html', currency=currency, date_trans=date_trans,budget=budget, amount=amount, course=course,cost=cost, type=type )



@app.route('/history')
def history():
    db = get_db()
    sql_command = 'select id, currency, date_trans,budget,amount,course, cost, type from new_trans;'
    cur = db.execute(sql_command)
    transakcje = cur.fetchall()

    return render_template('history.html' , transakcje = transakcje)


# dodałem komnentarz


if __name__ == '__main__':
    app.run()
