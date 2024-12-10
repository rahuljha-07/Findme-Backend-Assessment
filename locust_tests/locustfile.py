from locust import HttpUser, task, between
import random

class ProductManagementUser(HttpUser):
    wait_time = between(1, 2)  # Wait 1-2 seconds between tasks
    product_ids = []  # Shared list of product IDs for the user

    @task
    def add_product(self):
        """
        Test POST /api/products
        """
        payload = {
            "name": f"Test Product {random.randint(1, 1000)}",
            "price": random.uniform(5.0, 500.0),  # Random price between $5 and $500
            "quantity": random.randint(1, 100),  # Random quantity between 1 and 100
            "description": "A product for load testing",
            "category": "Test Category",
            "date_added": "2024-12-09",
            "image_url": "https://via.placeholder.com/150"
        }
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/api/products", json=payload, headers=headers)

        if response.status_code == 201:
            product = response.json()
            self.product_ids.append(product["id"])  # Save the product ID for other tasks
            print(f"Added product with ID: {product['id']}")
        else:
            print(f"Failed to add product: {response.status_code} - {response.text}")

    @task
    def fetch_all_products(self):
        """
        Test GET /api/products
        """
        response = self.client.get("/api/products")
        if response.status_code == 200:
            print(f"Fetched all products: {len(response.json())} items.")
        else:
            print(f"Failed to fetch all products: {response.status_code} - {response.text}")

    @task
    def fetch_product_by_id(self):
        """
        Test GET /api/products/<id>
        """
        if self.product_ids:
            product_id = random.choice(self.product_ids)  # Pick a random existing product ID
            response = self.client.get(f"/api/products/{product_id}")
            if response.status_code == 200:
                print(f"Fetched product ID: {product_id}")
            else:
                print(f"Failed to fetch product ID {product_id}: {response.status_code} - {response.text}")

    @task
    def update_product(self):
        """
        Test PUT /api/products/<id>
        """
        if self.product_ids:
            product_id = random.choice(self.product_ids)  # Pick a random existing product ID
            payload = {
                "name": "Updated Product Name",
                "price": random.uniform(10.0, 1000.0),
                "quantity": random.randint(1, 200),
                "description": "Updated product description",
                "category": "Updated Category",
                "date_added": "2024-12-10",
                "image_url": "https://via.placeholder.com/150"
            }
            headers = {"Content-Type": "application/json"}
            response = self.client.put(f"/api/products/{product_id}", json=payload, headers=headers)

            if response.status_code == 200:
                print(f"Updated product ID: {product_id}")
            else:
                print(f"Failed to update product ID {product_id}: {response.status_code} - {response.text}")

    @task
    def delete_product(self):
        """
        Test DELETE /api/products/<id>
        """
        if self.product_ids:
            product_id = random.choice(self.product_ids)  # Pick a random existing product ID
            response = self.client.delete(f"/api/products/{product_id}")

            if response.status_code == 200:
                self.product_ids.remove(product_id)  # Remove the product ID from the list
                print(f"Deleted product ID: {product_id}")
            else:
                print(f"Failed to delete product ID {product_id}: {response.status_code} - {response.text}")
