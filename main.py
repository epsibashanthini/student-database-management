from flask import Flask,render_template,request,message_flashed,url_for,redirect
import sqlite3

app=Flask(__name__)
app.secret_key="123"

# create database
con=sqlite3.connect("database.db")
con.execute(
    """CREATE TABLE IF NOT EXISTS student_record(
        reg_no INTEGER PRIMARY KEY NOT NULL, 
        name TEXT,
        dob DATE,
        sex TEXT,
        department TEXT,
        address TEXT,
        contact INTEGER,
        mail TEXT)      
    """)
con.close()

# create home page
@app.route('/home')
def home():
    return render_template('index.html')

# create add student record page
@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addata',methods=['POST','GET'])
def addata():
    if request.method=="POST":
        try:
            name=request.form['name']
            dob=request.form['dob']
            sex=request.form['sex']
            department=request.form['department']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("INSERT INTO student_record(name,dob,sex,department,address,contact,mail)VALUES(?,?,?,?,?,?,?)",(name,dob,sex,department,address,contact,mail))
            con.commit()
            message_flashed("Record Added successfully")
        except:
            message_flashed("Inserting error")
        finally:
            return redirect(url_for("home"))
            con.close()

@app.route('/view')
def view():
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM student_record")
    data = cur.fetchall()
    con.close()
    return render_template("view.html",student_record=data)

@app.route("/update/<string:reg_no>",methods=["POST","GET"])
def update(reg_no):
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM student_record WHERE reg_no=?",(reg_no))
    data = cur.fetchone()
    con.close()


    if request.method=='POST':
            try:
                name=request.form['name']
                dob=request.form['dob']
                sex=request.form['sex']
                department=request.form['department']
                address=request.form['address']
                contact=request.form['contact']
                mail=request.form['mail']
                con=sqlite3.connect("database.db")
                cur=con.cursor()
                cur.execute("UPDATE student_record SET name=?,dob=?,sex=?,department=?,address=?,contact=?,mail=? WHERE reg_no=?",(name,dob,sex,department,address,contact,mail,reg_no))
                con.commit()
                message_flashed("Update Successfully","success")

            except:
                message_flashed("error in update operation","danger")
            
            finally:
                return redirect(url_for("home"))
                con.close()
                
    return render_template('update.html',student_record=data)

@app.route('/delete/<string:reg_no>')
def delete(reg_no):
    try:
        con=sqlite3.connect("database.db")
        cur=con.cursor()
        cur.execute("DELETE FROM student_record WHERE reg_no=?",(reg_no))
        con.commit()
        message_flashed("Deleted Successfully","success")

    except:
        message_flashed("delete failed","danger")

    finally:
        return redirect(url_for("home"))
        con.close()


if __name__ == "__main__":
    app.run(debug=True)