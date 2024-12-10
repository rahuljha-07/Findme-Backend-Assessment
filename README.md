# Product Management API

This is a **Product Management API** built using **Flask**. The API provides endpoints to manage products, including creating, updating, deleting, and fetching product details. It supports concurrent user handling using **Tornado** and provides Swagger documentation for easy API exploration.

## Features
- CRUD operations on products:
  - Add a new product.
  - Fetch all products.
  - Fetch a single product by ID.
  - Update an existing product.
  - Delete a product.
- Swagger integration for interactive API documentation.
- Concurrent user handling using **Tornado**.
- Load testing setup using **Locust**.

---

## How to Run the Project

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone <repository-url>
cd Findme-Backend-Assessment
```

### 2. Install Dependencies
Make sure you have Python installed (3.8 or above is recommended). Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the Flask application using **Tornado** for handling concurrent requests:
```bash
python app.py
```

- The application will run on `http://127.0.0.1:5000` by default.

---

## Access Swagger Documentation

Once the application is running, access the Swagger UI for the API documentation:

- Swagger URL: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

You can interact with the API directly through this interface.

---

## Locust Load Testing

### 1. Install Locust
Ensure Locust is installed for load testing:
```bash
pip install locust
```

### 2. Run the Locust Test File
Run the `locustfile.py` for testing the API under concurrent load:
```bash
locust -f locustfile.py
```

### 3. Open Locust Web Interface
Once Locust is running, access the web interface at:
```
http://localhost:8089
```

### 4. Configure the Test
- **Host**: Set this to `http://127.0.0.1:5000`
- **Number of Users**: Enter the number of simulated users.
- **Spawn Rate**: Enter the rate at which users are spawned (e.g., 5 users per second).

Click **Start Swarming** to begin the load test and monitor the results.

---

## Project Structure

```
Findme-Backend-Assessment/
│
├── app/                        # Main application folder
│   ├── __init__.py             # Application initialization
│   ├── routes.py               # API route definitions
│   ├── services.py             # Business logic for managing products
│   ├── utils.py                # Utility functions
│   ├── models.py               # In-memory product data
│
├── static/                     # Static files (e.g., index.html)
│
├── locustfile.py               # Locust test script for load testing
├── requirements.txt            # Project dependencies
├── app.py                      # Application entry point
├── README.md                   # Project documentation
└── ...
```

---

## Technologies Used

- **Flask**: Python web framework for building the API.
- **Tornado**: Used as the WSGI server for handling concurrent requests.
- **Flasgger**: Provides Swagger integration for API documentation.
- **Locust**: Used for load testing and performance monitoring.

---
