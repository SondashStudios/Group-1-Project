from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("sqlite_db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # Retrieve the username from the cookie set by Django
    user_id = request.cookies.get('gradpath_user')

    if not user_id:
        return "User not logged in or no user ID provided.", 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ModuleItemID FROM UserSelections WHERE user_id = ?", (user_id,))
    selected_items = [row['ModuleItemID'] for row in cursor.fetchall()]
    conn.close()
    
    return render_template("checklist.html", userSelections=selected_items)

@app.route('/saveChecklist', methods=['POST'])
def saveChecklist():
    user_id = request.cookies.get('gradpath_user')
    
    if not user_id:
        return "User not logged in or no user ID provided.", 403

    selected_items = request.form.getlist("moduleItemCheckboxInput")

    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM UserSelections WHERE user_id = ?", (user_id,))
    
    for item_id in selected_items:
        cursor.execute("INSERT INTO UserSelections (user_id, ModuleItemID) VALUES (?, ?)", (user_id, item_id))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
