import json
import http.server
import socketserver
from decimal import Decimal
from database import connect_db

PORT = 8000

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} isnot json serializable")

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
        
        response = {
            "expenses": expenses,
            "budget": budget["amount"] if budget else 0
        }
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  
        self.end_headers()
        
        self.wfile.write(json.dumps(response, default=decimal_to_float).encode())
        
        connection.close()

    def do_POST(self):
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
        
        connection.commit()
        connection.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*") 
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Data saved successfully"}).encode())

    def do_DELETE(self):
        expense_id = self.path.split('/')[-1]
        
        connection = connect_db()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        connection.commit()
        connection.close()
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*") 
        self.wfile.write(json.dumps({"message": "Expense deleted successfully"}).encode())

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ExpenseHandler) as httpd:
        print("Server running at port", PORT)
        httpd.serve_forever()
