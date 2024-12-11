
# Updated Python Backend
import json
import http.server
import socketserver
from decimal import Decimal
from database import connect_db

PORT = 8000

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not json serializable")

class ExpenseHandler(http.server.SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        cursor.execute("SELECT amount FROM budget LIMIT 1")
        budget = cursor.fetchone()

        cursor.execute("SELECT category, SUM(amount) as total FROM expenses GROUP BY category")
        category_summary = {row['category']: row['total'] for row in cursor.fetchall()}

        response = {
            "expenses": expenses,
            "budget": budget["amount"] if budget else 0,
            "categorySummary": category_summary
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  
        self.end_headers()

        self.wfile.write(json.dumps(response, default=decimal_to_float).encode())

        connection.close()

    def do_POST(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        connection = connect_db()
        cursor = connection.cursor()

        if data.get("type") == "expense":
            cursor.execute("INSERT INTO expenses (name, amount, category) VALUES (%s, %s, %s)", 
                           (data["name"], data["amount"], data["category"]))
        elif data.get("type") == "budget":
            cursor.execute("DELETE FROM budget")
            cursor.execute("INSERT INTO budget (id, amount) VALUES (1, %s)", (data["amount"],))
        elif data.get("username") and data.get("password"):
            if "confirmPassword" in data:  # Registration
                cursor.execute("SELECT * FROM users WHERE username = %s", (data["username"],))
                if cursor.fetchone():
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "message": "Username already exists."}).encode())
                    return

                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                               (data["username"], data["password"]))
                connection.commit()
                self.wfile.write(json.dumps({"success": True, "message": "Registration successful."}).encode())
            else:  # Login
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                               (data["username"], data["password"]))
                if cursor.fetchone():
                    self.wfile.write(json.dumps({"success": True, "message": "Login successful."}).encode())
                else:
                    self.send_response(401)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "message": "Invalid credentials."}).encode())

        connection.commit()
        connection.close()

    def do_DELETE(self):
        expense_id = self.path.split('/')[-1]

        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        connection.commit()
        connection.close()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*") 
        self.wfile.write(json.dumps({"message": "Expense deleted successfully"}).encode())

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ExpenseHandler) as httpd:
        print("Server running at port", PORT)
        httpd.serve_forever()

# Updated Python Backend
import json
import http.server
import socketserver
from decimal import Decimal
from database import connect_db

PORT = 8000

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not json serializable")

class ExpenseHandler(http.server.SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        cursor.execute("SELECT amount FROM budget LIMIT 1")
        budget = cursor.fetchone()

        cursor.execute("SELECT category, SUM(amount) as total FROM expenses GROUP BY category")
        category_summary = {row['category']: row['total'] for row in cursor.fetchall()}

        response = {
            "expenses": expenses,
            "budget": budget["amount"] if budget else 0,
            "categorySummary": category_summary
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  
        self.end_headers()

        self.wfile.write(json.dumps(response, default=decimal_to_float).encode())

        connection.close()

    def do_POST(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        connection = connect_db()
        cursor = connection.cursor()

        if data.get("type") == "expense":
            cursor.execute("INSERT INTO expenses (name, amount, category) VALUES (%s, %s, %s)", 
                           (data["name"], data["amount"], data["category"]))
        elif data.get("type") == "budget":
            cursor.execute("DELETE FROM budget")
            cursor.execute("INSERT INTO budget (id, amount) VALUES (1, %s)", (data["amount"],))
        elif data.get("username") and data.get("password"):
            if "confirmPassword" in data:  # Registration
                cursor.execute("SELECT * FROM users WHERE username = %s", (data["username"],))
                if cursor.fetchone():
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "message": "Username already exists."}).encode())
                    return

                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                               (data["username"], data["password"]))
                connection.commit()
                self.wfile.write(json.dumps({"success": True, "message": "Registration successful."}).encode())
            else:  # Login
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                               (data["username"], data["password"]))
                if cursor.fetchone():
                    self.wfile.write(json.dumps({"success": True, "message": "Login successful."}).encode())
                else:
                    self.send_response(401)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "message": "Invalid credentials."}).encode())

        connection.commit()
        connection.close()

    def do_DELETE(self):
        expense_id = self.path.split('/')[-1]

        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        connection.commit()
        connection.close()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*") 
        self.wfile.write(json.dumps({"message": "Expense deleted successfully"}).encode())

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ExpenseHandler) as httpd:
        print("Server running at port", PORT)
        httpd.serve_forever()
