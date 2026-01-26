import mysql.connector 
from mysql.connector import errorcode
from flask import Flask, render_template, render_template , request , redirect, url_for,flash,session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123" #later we will secure this

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tan*221004*",
        database="task_manager"
    )

@app.route("/test-db")
def test_db():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    db.cursor()
    return str(tables)

@app.route("/",methods=["GET","POST"])
def login():
    db = None
    cursor = None 
    if request.method == "POST":
        # login logic will come later
        # return "Login POST received"
        # now login logic below
        email = request.form["email"].strip()
        password = request.form["password"]

        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE     email = %s"
            cursor.execute(query,(email,))
            user = cursor.fetchone()

            if user is None:
                flash("Email not register!")
                return redirect(url_for("login"))
        
            if not check_password_hash(user    ["password"],password):
                flash("Incorrect password!")
                return redirect(url_for("login"))

        # login successful - create session
            session["user_id"] = user["id"]
            session["user_email"] = user["email"]

            return redirect(url_for("dashboard"))
        except Exception as e:
            print("LOGIN ERROR:",e)
            flash(f"Login failed due to server error: {e}")
            return redirect(url_for("login"))

        finally:
            # close only if created
            if cursor:
                cursor.close()

            if db:
                db.close()

    return render_template("login.html")

@app.route("/register", methods= ["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("Password do not match!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        try:
            db = get_db_connection()
            cursor = db.cursor()

            query = "INSERT INTO users (email, password) VALUES (%s,%s)"
            cursor.execute(query,(email,hashed_password))
            db.commit()
            cursor.close()
            db.close()

            flash("Registration successful! Please login.")
            return redirect(url_for("login"))
        
        except mysql.connector.Error as err:
            print("MYSQL ERROR : ",err)
            if err.errno == errorcode.ER_DUP_ENTRY:
                flash("Email already exists!")
            else:
                flash(f"Database error occured!: {err.msg}")
            return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    status = request.args.get("status")
    priority = request.args.get("priority")
    category = request.args.get("category")   # ✅ NEW

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM tasks WHERE user_id = %s"
    params = [session["user_id"]]

    if status:
        query += " AND status = %s"
        params.append(status)

    if priority:
        query += " AND priority = %s"
        params.append(priority)

    if category:
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY id DESC"

    cursor.execute(query, tuple(params))
    tasks = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        selected_status=status,
        selected_priority=priority,
        selected_category=category
    )

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    status = request.args.get("status")
    priority = request.args.get("priority")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM tasks WHERE user_id = %s "
    parms = [session["user_id"]]

    if status:
        query += "AND status = %s"
        parms.append(status)

    if priority:
        query += "AND priority = %s"
        parms.append(priority)

    query +="ORDER BY id DESC"

    cursor.execute(query,tuple(parms))
    tasks = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html", 
        tasks = tasks,
        selected_status= status,
        selected_priority=priority
        )

# adding task route (INSERT into DB)
@app.route("/add-task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title")
    description = request.form.get("description")
    priority = request.form.get("priority")
    category = request.form.get("category")  # ✅ NEW

    if not title:
        flash("Task title is required")
        return redirect(url_for("dashboard"))

    db = get_db_connection()
    cursor = db.cursor()

    query = """
        INSERT INTO tasks (user_id, title, description, priority, category)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (session["user_id"], title, description, priority, category)
    )
    db.commit()

    cursor.close()
    db.close()

    flash("Task added successfully")
    return redirect(url_for("dashboard"))

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    title = request.form.get("title")
    description = request.form.get("desciption")
    priority = request.form["priority"]

    # adding check
    if not title:
        flash("Task title is requried.")
        return redirect(url_for("dashboard"))

    db = get_db_connection()
    cursor = db.cursor()

    query = """
         INSERT INTO tasks (user_id , title , description , priority)
         VALUES (%s,%s,%s,%s)
    """
    cursor.execute(query , (session["user_id"], title, description, priority))
    db.commit()

    cursor.close()
    db.close()

    flash("Task added Successfully!!")
    return redirect(url_for("dashboard"))

# DELETE TASK ROUTE(secure)
@app.route("/delete-task/<int:task_id>")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor()

    # ensure user can delete ONLY their own tasks
    query = "DELETE FROM tasks WHERE id = %s AND user_id = %s"
    cursor.execute(query, (task_id, session["user_id"]))
    db.commit()

    cursor.close()
    db.close()

    flash("Task deleted!")
    return redirect(url_for("dashboard"))

# adding logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
# tEMPORARY ADD
@app.route("/db-info")
def db_info():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT DATABASE()")
    current_db = cursor.fetchone()
    cursor.close()
    db.close()
    return f"Connected database: {current_db}"

# Toggle for pending and completed Tasks
@app.route("/toggle-task/<int:task_id>")
def toggle_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT status FROM tasks WHERE id=%s AND user_id=%s",
        (task_id,session["user_id"])
    )
    task = cursor.fetchone()

    if not task:
        cursor.close()
        db.close()
        flash("Task not found")
        return redirect(url_for("dashboard"))

    new_status = "Completed" if task["status"] == "Pending" else "Pending"

    cursor.execute(
        "UPDATE tasks SET status=%s WHERE id=%s",
        (new_status , task_id)
    )
    db.commit()

    cursor.close()
    db.close()

    flash("Task status updated")
    return redirect(url_for("dashboard"))

# Edit task
@app.route("/edit-task/<int:task_id>", methods=["GET","POST"])
def edit_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Fetch task(security: only owner)
    cursor.execute(
        "SELECT*FROM tasks WHERE id=%s AND user_id=%s",
        (task_id,session["user_id"])
    )
    task = cursor.fetchone()

    if not task:
        cursor.close()
        db.close()
        flash("Task not found")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form.get("title")
        desciption = request.form.get("description")
        priority = request.form.get("priority")

        if not title:
            flash("Title is requried")
            return redirect(url_for("edit_task", task_id=task_id))

        cursor.execute(
            '''
            UPDATE tasks
            SET title=%s , description=%s , priority=%s
            WHERE id=%s AND user_id=%s
            ''',
            (title,desciption,priority,task_id,session["user_id"])
        )
        db.commit()

        cursor.close()
        db.close()

        flash("Task updated successfully!")
        return redirect(url_for("dashboard"))

    cursor.close()
    db.close()
    return render_template("edit_task.html", task=task)
if __name__ == "__main__":
    app.run(debug= True)