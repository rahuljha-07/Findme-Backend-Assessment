from threading import Lock
from .models import products

product_lock = Lock() # Create a lock for thread-safe operations

def fetch_all_products():
    """
    This function gets all the products stored in memory.

    Returns:
        list: A list containing all products.
    """
    with product_lock:
        return products[:]  # Return a copy of the product list

def find_product_by_id(item_id):
    """
    Find an item in the inventory using its ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        dict: The item with the given ID, or None if not found.
    """
    with product_lock:
        for item in products:
            if item["id"] == item_id:
                return item
        return None

def add_product(new_product):
    """
    Add a new product.

    Args:
        new_product (dict): A dictionary containing the product details.

    Returns:
        dict: The newly added product.
    """
    with product_lock:
        products.append(new_product)  # Append the new product
        return new_product

def update_product(item_id, updated_data):
    """
    Update an existing product.

    Args:
        item_id (int): The ID identifier of the product to be updated.
        updated_data (dict): A dictionary containing the updated product details.

    Returns:
        dict: The updated product if found, or None if the product does not exist.
    """
    with product_lock:
        product = find_product_by_id(item_id)
        if product:
            product.update(updated_data)
            return product
        return None

def delete_product(item_id):
    """
    Remove an item from the inventory using its ID.

    Args:
        item_id (int): The ID of the item to be deleted.

    Returns:
        bool: True if the product was successfully deleted, False otherwise.
    """
    with product_lock:
        global products  # Access the global `products` list
        updated_products = []  # Initialize an empty list to store the items

        for item in products:
            if item["id"] != item_id:  # Add items that do not match the given ID
                updated_products.append(item)

        # Update the global `products` list
        products = updated_products

        return True
