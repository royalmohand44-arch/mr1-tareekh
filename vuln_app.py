import sqlite3
from flask import Flask, request

app = Flask(__name__)

# إنشاء قاعدة بيانات مؤقتة وفيها حساب أدمن
conn = sqlite3.connect(':memory:', check_same_thread=False)
conn.execute("CREATE TABLE users (username TEXT, password TEXT)")
conn.execute("INSERT INTO users VALUES ('admin', 'SuperSecretPassword123!')")
conn.commit()

@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('user', '')
    pw = request.args.get('pass', '')
    
    # هنا الثغرة: دمج مدخلات المستخدم مباشرة في أمر قاعدة البيانات
    query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{pw}'"
    print(f"\n[DB Query Executed]: {query}\n")
    
    cursor = conn.execute(query)
    if cursor.fetchone():
        return "✅ Login Successful! Welcome Admin!"
    return "❌ Access Denied!"

if __name__ == '__main__':
    app.run(port=5000)
