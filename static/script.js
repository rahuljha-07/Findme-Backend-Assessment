const apiEndpoint = '/api/products';

// Fetch and display products
async function fetchProducts() {
    try {
        const response = await fetch(apiEndpoint);
        if (!response.ok) {
            throw new Error('Failed to fetch products.');
        }
        const products = await response.json();

        const productGrid = document.getElementById('product-grid');
        productGrid.innerHTML = ''; // Clear previous content

        products.forEach(product => {
            const tile = document.createElement('div');
            tile.className = 'product-tile';
            tile.innerHTML = `
                <img src="${product.image_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p><strong>Price:</strong> $${product.price}</p>
                <p><strong>Quantity:</strong> ${product.quantity}</p>
                <p><strong>Description:</strong> ${product.description}</p>
                <p><strong>Category:</strong> ${product.category}</p>
                <p><strong>Date Added:</strong> ${product.date_added}</p>
                <button onclick="editProduct(${product.id})">Edit</button>
                <button onclick="deleteProduct(${product.id})">Delete</button>
            `;
            productGrid.appendChild(tile);
        });
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Open Modal for Add Product
document.getElementById('add-product-button').addEventListener('click', () => {
    openModal(); // Open empty modal for adding a product
});

// Close Modal
document.getElementById('close-modal').addEventListener('click', closeModal);

// Close Modal Functionality
function closeModal() {
    const modal = document.getElementById('product-modal');
    modal.style.display = 'none';
    document.getElementById('product-form').reset(); // Clear form fields
}

// Open Modal for Add/Edit Product
function openModal(product = null) {
    const modal = document.getElementById('product-modal');
    modal.style.display = 'flex';

    document.getElementById('modal-title').innerText = product ? 'Edit Product' : 'Add Product';

    // Pre-fill the form if editing an existing product
    document.getElementById('product-id').value = product ? product.id : '';
    document.getElementById('name').value = product ? product.name : '';
    document.getElementById('price').value = product ? product.price : '';
    document.getElementById('quantity').value = product ? product.quantity : '';
    document.getElementById('description').value = product ? product.description : '';
    document.getElementById('category').value = product ? product.category : '';
    document.getElementById('date-added').value = product ? product.date_added : '';
    document.getElementById('image-url').value = product ? product.image_url : '';
}

// Save Product (Add or Update)
document.getElementById('product-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const productId = document.getElementById('product-id').value;

    // Extract only the valid fields
    const productData = {
        name: document.getElementById('name').value,
        price: parseFloat(document.getElementById('price').value),
        quantity: parseInt(document.getElementById('quantity').value),
        description: document.getElementById('description').value,
        category: document.getElementById('category').value,
        date_added: document.getElementById('date-added').value,
        image_url: document.getElementById('image-url').value,
    };

    const method = productId ? 'PUT' : 'POST';
    const url = productId ? `${apiEndpoint}/${productId}` : apiEndpoint;

    try {
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(productData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to save product');
        }

        closeModal();
        fetchProducts(); // Refresh the product list
    } catch (error) {
        console.error('Error saving product:', error);
        alert(`Error: ${error.message}`);
    }
});

// Delete Product
async function deleteProduct(id) {
    try {
        const response = await fetch(`${apiEndpoint}/${id}`, { method: 'DELETE' });
        if (!response.ok) {
            throw new Error('Failed to delete product');
        }
        fetchProducts(); // Refresh the product list after deletion
    } catch (error) {
        console.error('Error deleting product:', error);
    }
}

// Edit Product
async function editProduct(id) {
    try {
        const response = await fetch(`${apiEndpoint}/${id}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch product with ID ${id}`);
        }
        const product = await response.json();
        openModal(product); // Open modal pre-filled with product data
    } catch (error) {
        console.error('Error editing product:', error);
        alert(`Error: ${error.message}`);
    }
}

// Initial Fetch
window.onload = fetchProducts;
