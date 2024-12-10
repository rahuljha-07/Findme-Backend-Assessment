from flask import Blueprint, request, jsonify
from app.services import (
    fetch_all_products,
    find_product_by_id,
    add_product,
    update_product,
    delete_product
)
from app.utils import generate_error_response, validate_required_fields
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

blueprint = Blueprint('api', __name__)
limiter = Limiter(get_remote_address, app=blueprint)

@blueprint.route('/products', methods=['GET'])
@limiter.limit("100 per minute")  # Limit to 100 requests per minute
def list_all_items():
    """
    Fetch all items from the products.
    ---
    responses:
      200:
        description: A list of all products
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  price:
                    type: number
                  quantity:
                    type: integer
                  description:
                    type: string
                  category:
                    type: string
                  date_added:
                    type: string
                  image_url:
                    type: string
    """
    all_items = fetch_all_products()
    return jsonify(all_items), 200

@blueprint.route('/products/<int:item_id>', methods=['GET'])
@limiter.limit("50 per minute")  # Limit to 50 requests per minute
def get_single_item(item_id):
    """
    Fetch a single item by its ID.
    ---
    parameters:
      - name: item_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: A single product
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                price:
                  type: number
                quantity:
                  type: integer
                description:
                  type: string
                category:
                  type: string
                date_added:
                  type: string
                image_url:
                  type: string
      404:
        description: Product not found
    """
    item = find_product_by_id(item_id)
    if item:
        return jsonify(item), 200
    return generate_error_response("Item not found", 404)

@blueprint.route('/products', methods=['POST'])
@limiter.limit("30 per minute")  # Limit to 30 POST requests per minute
def create_new_item():
    """
    Add a new item to the inventory.
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              price:
                type: number
              quantity:
                type: integer
              description:
                type: string
              category:
                type: string
              date_added:
                type: string
              image_url:
                type: string
    responses:
      201:
        description: Product created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                price:
                  type: number
                quantity:
                  type: integer
                description:
                  type: string
                category:
                  type: string
                date_added:
                  type: string
                image_url:
                  type: string
      400:
        description: Invalid data
    """
    item_details = request.json
    required_keys = ["id", "name", "price", "quantity", "description", "category", "date_added", "image_url"]
    is_valid, error_message = validate_required_fields(item_details, required_keys)
    if not is_valid:
        return generate_error_response(error_message, 400)

    new_item = add_product(item_details)
    return jsonify(new_item), 201

@blueprint.route('/products/<int:item_id>', methods=['PUT'])
@limiter.limit("20 per minute")  # Limit to 20 PUT requests per minute
def update_item(item_id):
    """
    Update an existing item in the inventory.
    ---
    parameters:
      - name: item_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              price:
                type: number
              quantity:
                type: integer
              description:
                type: string
              category:
                type: string
              date_added:
                type: string
              image_url:
                type: string
    responses:
      200:
        description: Product updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                price:
                  type: number
                quantity:
                  type: integer
                description:
                  type: string
                category:
                  type: string
                date_added:
                  type: string
                image_url:
                  type: string
      404:
        description: Product not found
    """
    updated_data = request.json
    allowed_keys = ["name", "price", "quantity", "description", "category", "date_added", "image_url"]
    if any(key not in allowed_keys for key in updated_data.keys()):
        return generate_error_response("Invalid field(s) in request.", 400)

    updated_item = update_product(item_id, updated_data)
    if updated_item:
        return jsonify(updated_item), 200
    return generate_error_response("Item not found", 404)

@blueprint.route('/products/<int:item_id>', methods=['DELETE'])
@limiter.limit("10 per minute")  # Limit to 10 DELETE requests per minute
def delete_item(item_id):
    """
    Delete an item from the inventory by its ID.
    ---
    parameters:
      - name: item_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Product deleted successfully
      404:
        description: Product not found
    """
    delete_product(item_id)
    return jsonify({"message": "Item deleted successfully"}), 200
