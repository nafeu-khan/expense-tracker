const http = require('http');
const mysql = require('mysql2');
const url = require('url');

// Setup the MySQL connection
const dbConfig = {
    host:"localhost",
    user:"root",
    password:"1234",
    database:"expense_tracker"
};

const connection = mysql.createConnection(dbConfig);

// Helper function to convert decimal to float for JSON serialization
function decimalToFloat(value) {
  if (value instanceof Decimal) {
    return parseFloat(value);
  }
  return value;
}

// Create the server to handle HTTP requests
const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle OPTIONS request
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // Handle GET request
  if (req.method === 'GET') {
    if (req.url === '/expenses') {
      connection.query('SELECT * FROM expenses', (err, expenses) => {
        if (err) {
          res.writeHead(500);
          res.end(JSON.stringify({ message: 'Database error' }));
          return;
        }

        connection.query('SELECT amount FROM budget LIMIT 1', (err, budget) => {
          if (err) {
            res.writeHead(500);
            res.end(JSON.stringify({ message: 'Database error' }));
            return;
          }

          const response = {
            expenses: expenses,
            budget: budget.length > 0 ? budget[0].amount : 0
          };

          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(response, decimalToFloat));
        });
      });
    } else {
      res.writeHead(404);
      res.end('Not Found');
    }
  }

  // Handle POST request
  else if (req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString(); // convert Buffer to string
    });

    req.on('end', () => {
      const data = JSON.parse(body);

      if (data.type === 'expense') {
        const { name, amount, category } = data;
        connection.query('INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)', 
          [name, amount, category], (err) => {
            if (err) {
              res.writeHead(500);
              res.end(JSON.stringify({ message: 'Database error' }));
              return;
            }
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: 'Expense saved successfully' }));
        });
      } else if (data.type === 'budget') {
        connection.query('DELETE FROM budget', (err) => {
          if (err) {
            res.writeHead(500);
            res.end(JSON.stringify({ message: 'Database error' }));
            return;
          }

          connection.query('INSERT INTO budget (id, amount) VALUES (1, ?)', [data.amount], (err) => {
            if (err) {
              res.writeHead(500);
              res.end(JSON.stringify({ message: 'Database error' }));
              return;
            }
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: 'Budget saved successfully' }));
          });
        });
      } else {
        res.writeHead(400);
        res.end(JSON.stringify({ message: 'Invalid data type' }));
      }
    });
  }

  // Handle DELETE request
  else if (req.method === 'DELETE') {
    const pathname = url.parse(req.url).pathname;
    const expenseId = pathname.split('/').pop();

    connection.query('DELETE FROM expenses WHERE id = ?', [expenseId], (err) => {
      if (err) {
        res.writeHead(500);
        res.end(JSON.stringify({ message: 'Database error' }));
        return;
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ message: 'Expense deleted successfully' }));
    });
  }

  // Handle all other HTTP methods
  else {
    res.writeHead(405);
    res.end('Method Not Allowed');
  }
});

// Start the server
const PORT = 8000;
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
