# MediCart API Documentation

## Overview

MediCart provides a RESTful API for managing an online pharmacy system. This document provides detailed information about all available endpoints, request/response formats, and usage examples.

## Base Information

- **Base URL**: `http://127.0.0.1:8000/api/`
- **API Version**: 1.0
- **Content Type**: `application/json`
- **Authentication**: None (can be added as needed)

## Table of Contents

1. [Medicines API](#medicines-api)
2. [Orders API](#orders-api)
3. [Error Handling](#error-handling)
4. [Response Codes](#response-codes)
5. [Usage Examples](#usage-examples)

---

## Medicines API

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/medicines/` | List all medicines |
| GET | `/api/medicines/{id}/` | Get a specific medicine |
| POST | `/api/medicines/` | Create a new medicine |
| PUT | `/api/medicines/{id}/` | Update a medicine (full) |
| PATCH | `/api/medicines/{id}/` | Update a medicine (partial) |
| DELETE | `/api/medicines/{id}/` | Delete a medicine |

---

### List All Medicines

Retrieve a list of all medicines in the database.

**Endpoint**: `GET /api/medicines/`

**Request**:
```http
GET /api/medicines/ HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
```

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "Aspirin",
    "description": "Pain reliever and anti-inflammatory drug",
    "price": "9.99",
    "stock": 100,
    "expiry_date": "2025-12-31",
    "is_in_stock": true,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "name": "Paracetamol",
    "description": "Fever reducer and mild pain reliever",
    "price": "12.99",
    "stock": 200,
    "expiry_date": "2026-06-30",
    "is_in_stock": true,
    "created_at": "2025-01-15T11:00:00Z",
    "updated_at": "2025-01-15T11:00:00Z"
  }
]
```

**Fields**:
- `id` (integer): Unique identifier
- `name` (string): Medicine name (max 200 chars)
- `description` (string): Detailed description
- `price` (decimal): Price in USD
- `stock` (integer): Available quantity
- `expiry_date` (date): Expiration date (YYYY-MM-DD)
- `is_in_stock` (boolean): Computed field indicating availability
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

---

### Get Single Medicine

Retrieve details of a specific medicine.

**Endpoint**: `GET /api/medicines/{id}/`

**Request**:
```http
GET /api/medicines/1/ HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "Aspirin",
  "description": "Pain reliever and anti-inflammatory drug",
  "price": "9.99",
  "stock": 100,
  "expiry_date": "2025-12-31",
  "is_in_stock": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

**Error Response**: `404 Not Found`
```json
{
  "status": "error",
  "message": "Not found.",
  "errors": {}
}
```

---

### Create Medicine

Add a new medicine to the inventory.

**Endpoint**: `POST /api/medicines/`

**Request**:
```http
POST /api/medicines/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "name": "Vitamin C",
  "description": "Immune system booster and antioxidant",
  "price": "15.99",
  "stock": 150,
  "expiry_date": "2026-12-31"
}
```

**Required Fields**:
- `name` (string): Unique medicine name
- `description` (string): Medicine description
- `price` (decimal): Price (must be > 0)
- `stock` (integer): Stock quantity (must be ≥ 0)
- `expiry_date` (date): Must be a future date

**Response**: `201 Created`
```json
{
  "id": 3,
  "name": "Vitamin C",
  "description": "Immune system booster and antioxidant",
  "price": "15.99",
  "stock": 150,
  "expiry_date": "2026-12-31",
  "is_in_stock": true,
  "created_at": "2025-01-15T14:00:00Z",
  "updated_at": "2025-01-15T14:00:00Z"
}
```

**Validation Errors**: `400 Bad Request`
```json
{
  "status": "error",
  "message": {
    "name": ["This field is required."],
    "price": ["Price must be greater than 0."],
    "expiry_date": ["Expiry date cannot be in the past."]
  },
  "errors": {}
}
```

---

### Update Medicine (Full)

Completely update a medicine. All fields must be provided.

**Endpoint**: `PUT /api/medicines/{id}/`

**Request**:
```http
PUT /api/medicines/1/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "name": "Aspirin 500mg",
  "description": "Updated: High-strength pain reliever",
  "price": "11.99",
  "stock": 150,
  "expiry_date": "2026-01-01"
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "Aspirin 500mg",
  "description": "Updated: High-strength pain reliever",
  "price": "11.99",
  "stock": 150,
  "expiry_date": "2026-01-01",
  "is_in_stock": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T15:00:00Z"
}
```

---

### Update Medicine (Partial)

Update specific fields of a medicine.

**Endpoint**: `PATCH /api/medicines/{id}/`

**Request**:
```http
PATCH /api/medicines/1/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "stock": 75,
  "price": "10.99"
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "Aspirin",
  "description": "Pain reliever and anti-inflammatory drug",
  "price": "10.99",
  "stock": 75,
  "expiry_date": "2025-12-31",
  "is_in_stock": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T15:30:00Z"
}
```

---

### Delete Medicine

Remove a medicine from the inventory.

**Endpoint**: `DELETE /api/medicines/{id}/`

**Request**:
```http
DELETE /api/medicines/1/ HTTP/1.1
Host: 127.0.0.1:8000
```

**Response**: `204 No Content`

**Error - Medicine has pending orders**: `400 Bad Request`
```json
{
  "detail": "Cannot delete medicine with 3 pending orders."
}
```

**Notes**:
- Medicines with pending orders cannot be deleted
- This prevents data inconsistency

---

## Orders API

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | List all orders |
| GET | `/api/orders/{id}/` | Get a specific order |
| POST | `/api/orders/` | Create a new order |
| PUT | `/api/orders/{id}/` | Update an order (full) |
| PATCH | `/api/orders/{id}/` | Update an order (partial) |
| PATCH | `/api/orders/{id}/update_status/` | Update order status only |
| DELETE | `/api/orders/{id}/` | Delete an order |

---

### List All Orders

Retrieve a list of all orders.

**Endpoint**: `GET /api/orders/`

**Request**:
```http
GET /api/orders/ HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
```

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "customer_name": "John Doe",
    "medicine": 1,
    "medicine_name": "Aspirin",
    "medicine_price": "9.99",
    "quantity": 5,
    "order_date": "2025-01-15T12:30:00Z",
    "status": "Pending",
    "total_price": "49.95"
  },
  {
    "id": 2,
    "customer_name": "Jane Smith",
    "medicine": 2,
    "medicine_name": "Paracetamol",
    "medicine_price": "12.99",
    "quantity": 3,
    "order_date": "2025-01-15T13:00:00Z",
    "status": "Processing",
    "total_price": "38.97"
  }
]
```

**Fields**:
- `id` (integer): Unique order identifier
- `customer_name` (string): Customer's name
- `medicine` (integer): Medicine ID (foreign key)
- `medicine_name` (string): Medicine name (read-only)
- `medicine_price` (decimal): Unit price (read-only)
- `quantity` (integer): Order quantity
- `order_date` (datetime): Order creation time (auto-set)
- `status` (string): Order status
- `total_price` (decimal): Calculated total (read-only)

**Status Options**:
- `Pending`: Initial status
- `Processing`: Order being processed
- `Shipped`: Order shipped
- `Delivered`: Order delivered
- `Cancelled`: Order cancelled

---

### Get Single Order

Retrieve details of a specific order.

**Endpoint**: `GET /api/orders/{id}/`

**Request**:
```http
GET /api/orders/1/ HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "customer_name": "John Doe",
  "medicine": 1,
  "medicine_name": "Aspirin",
  "medicine_price": "9.99",
  "quantity": 5,
  "order_date": "2025-01-15T12:30:00Z",
  "status": "Pending",
  "total_price": "49.95"
}
```

---

### Create Order

Place a new order. Stock is automatically reduced.

**Endpoint**: `POST /api/orders/`

**Request**:
```http
POST /api/orders/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "customer_name": "Alice Johnson",
  "medicine": 1,
  "quantity": 3
}
```

**Required Fields**:
- `customer_name` (string): Customer name
- `medicine` (integer): Medicine ID
- `quantity` (integer): Order quantity (must be > 0)

**Response**: `201 Created`
```json
{
  "id": 3,
  "customer_name": "Alice Johnson",
  "medicine": 1,
  "medicine_name": "Aspirin",
  "medicine_price": "9.99",
  "quantity": 3,
  "order_date": "2025-01-15T14:30:00Z",
  "status": "Pending",
  "total_price": "29.97"
}
```

**Automatic Actions**:
1. Validates sufficient stock
2. Calculates `total_price` (quantity × unit price)
3. Reduces medicine stock
4. Sets status to "Pending"
5. Logs the transaction

**Insufficient Stock Error**: `400 Bad Request`
```json
{
  "status": "error",
  "message": {
    "quantity": ["Insufficient stock. Only 2 units available."]
  },
  "errors": {}
}
```

---

### Update Order Status

Update only the status of an order.

**Endpoint**: `PATCH /api/orders/{id}/update_status/`

**Request**:
```http
PATCH /api/orders/1/update_status/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "status": "Delivered"
}
```

**Valid Status Values**:
- `Pending`
- `Processing`
- `Shipped`
- `Delivered`
- `Cancelled`

**Response**: `200 OK`
```json
{
  "status": "Delivered"
}
```

**Invalid Status Error**: `400 Bad Request`
```json
{
  "status": [
    "Invalid status. Choose from: Pending, Processing, Shipped, Delivered, Cancelled"
  ]
}
```

---

### Update Order (Full)

Completely update an order.

**Endpoint**: `PUT /api/orders/{id}/`

**Request**:
```http
PUT /api/orders/1/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "customer_name": "John Doe Updated",
  "medicine": 1,
  "quantity": 5,
  "status": "Processing"
}
```

**Response**: `200 OK`

**Note**: Updating quantity does NOT adjust stock. Only initial creation reduces stock.

---

### Update Order (Partial)

Update specific fields of an order.

**Endpoint**: `PATCH /api/orders/{id}/`

**Request**:
```http
PATCH /api/orders/1/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "status": "Shipped"
}
```

**Response**: `200 OK`

---

### Delete Order

Remove an order. Stock is restored if status is "Pending".

**Endpoint**: `DELETE /api/orders/{id}/`

**Request**:
```http
DELETE /api/orders/1/ HTTP/1.1
Host: 127.0.0.1:8000
```

**Response**: `204 No Content`

**Automatic Actions**:
- If status is "Pending", stock is restored
- Order is permanently deleted
- Transaction is logged

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "status": "error",
  "message": "Error description or field errors",
  "errors": {}
}
```

### Common Error Scenarios

#### Validation Errors (400)
```json
{
  "status": "error",
  "message": {
    "name": ["This field is required."],
    "price": ["Price must be greater than 0."]
  },
  "errors": {}
}
```

#### Not Found (404)
```json
{
  "status": "error",
  "message": "Not found.",
  "errors": {}
}
```

#### Server Error (500)
```json
{
  "status": "error",
  "message": "An unexpected error occurred.",
  "error": "Detailed error message"
}
```

---

## Response Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Validation error or invalid data |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

---

## Usage Examples

### Python (requests library)

```python
import requests

BASE_URL = 'http://127.0.0.1:8000/api'

# Create a medicine
medicine_data = {
    'name': 'Ibuprofen',
    'description': 'Anti-inflammatory',
    'price': '18.50',
    'stock': 200,
    'expiry_date': '2026-08-15'
}
response = requests.post(f'{BASE_URL}/medicines/', json=medicine_data)
medicine = response.json()
print(f"Created medicine: {medicine['id']}")

# Place an order
order_data = {
    'customer_name': 'Bob Wilson',
    'medicine': medicine['id'],
    'quantity': 5
}
response = requests.post(f'{BASE_URL}/orders/', json=order_data)
order = response.json()
print(f"Order placed: #{order['id']}, Total: ${order['total_price']}")

# Update order status
status_data = {'status': 'Shipped'}
response = requests.patch(
    f'{BASE_URL}/orders/{order["id"]}/update_status/',
    json=status_data
)
print(f"Order status: {response.json()['status']}")

# Get all medicines
response = requests.get(f'{BASE_URL}/medicines/')
medicines = response.json()
print(f"Total medicines: {len(medicines)}")
```

### JavaScript (fetch API)

```javascript
const BASE_URL = 'http://127.0.0.1:8000/api';

// Create a medicine
async function createMedicine() {
  const response = await fetch(`${BASE_URL}/medicines/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: 'Vitamin D',
      description: 'Bone health supplement',
      price: '22.99',
      stock: 180,
      expiry_date: '2026-10-31'
    })
  });
  const medicine = await response.json();
  console.log('Created medicine:', medicine);
  return medicine;
}

// Place an order
async function placeOrder(medicineId) {
  const response = await fetch(`${BASE_URL}/orders/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      customer_name: 'Charlie Brown',
      medicine: medicineId,
      quantity: 2
    })
  });
  const order = await response.json();
  console.log('Order placed:', order);
  return order;
}

// Update order status
async function updateOrderStatus(orderId) {
  const response = await fetch(
    `${BASE_URL}/orders/${orderId}/update_status/`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        status: 'Delivered'
      })
    }
  );
  const result = await response.json();
  console.log('Status updated:', result);
}

// Usage
createMedicine().then(medicine => {
  return placeOrder(medicine.id);
}).then(order => {
  return updateOrderStatus(order.id);
});
```

### cURL Examples

```bash
# List all medicines
curl -X GET http://127.0.0.1:8000/api/medicines/

# Create a medicine
curl -X POST http://127.0.0.1:8000/api/medicines/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Zinc Supplement",
    "description": "Immune support",
    "price": "14.99",
    "stock": 120,
    "expiry_date": "2026-07-31"
  }'

# Get single medicine
curl -X GET http://127.0.0.1:8000/api/medicines/1/

# Update medicine stock
curl -X PATCH http://127.0.0.1:8000/api/medicines/1/ \
  -H "Content-Type: application/json" \
  -d '{"stock": 95}'

# Place an order
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "David Lee",
    "medicine": 1,
    "quantity": 4
  }'

# Update order status
curl -X PATCH http://127.0.0.1:8000/api/orders/1/update_status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "Shipped"}'

# Delete an order
curl -X DELETE http://127.0.0.1:8000/api/orders/1/
```

---

## Best Practices

1. **Always validate input** before sending requests
2. **Handle errors gracefully** on the client side
3. **Check stock availability** before placing orders
4. **Use appropriate HTTP methods** (GET for reading, POST for creating, etc.)
5. **Log API calls** for debugging and auditing
6. **Monitor rate limits** if implemented
7. **Use HTTPS** in production
8. **Implement authentication** for production environments

---

## Support & Feedback

For questions, issues, or feature requests, please contact the development team or create an issue in the GitHub repository.

---

**MediCart API v1.0** | Last Updated: January 2025

