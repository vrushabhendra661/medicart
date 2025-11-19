# MediCart - Online Pharmacy Platform

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)

A comprehensive web application for managing an online pharmacy system with RESTful APIs and a modern web interface.

## Features

✨ **Complete CRUD Operations**
- Medicines management (Add, View, Update, Delete)
- Order processing and tracking
- Automated stock management

🔌 **RESTful APIs**
- Django REST Framework powered APIs
- JSON request/response format
- Comprehensive error handling

🎨 **Modern Web Interface**
- Beautiful, responsive UI
- User-friendly forms
- Real-time data display

📊 **Advanced Features**
- Automatic stock updates on orders
- Order status tracking (Pending → Processing → Shipped → Delivered)
- Medicine expiry date validation
- Detailed logging system

🧪 **Fully Tested**
- Comprehensive test suite
- Model, API, and view tests
- 100% critical path coverage

## Tech Stack

- **Backend**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (default, easily switchable)
- **Testing**: pytest, pytest-django
- **Python**: 3.8+

## Project Structure

```
Pharmacy_Ecom/
├── medicart/              # Main project directory
│   ├── __init__.py
│   ├── settings.py       # Project settings
│   ├── urls.py          # Root URL configuration
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── pharmacy/             # Main application
│   ├── models.py        # Medicine and Order models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API and template views
│   ├── urls.py          # App URL routing
│   ├── admin.py         # Admin interface
│   ├── utils.py         # Utility functions
│   └── tests.py         # Comprehensive tests
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   └── pharmacy/       # App-specific templates
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd Pharmacy_Ecom
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage Guide

### Web Interface

Access the web interface at `http://127.0.0.1:8000/`

#### Home Page
- Dashboard with statistics
- Quick action buttons
- API endpoint links

#### Medicines Management
- **View All Medicines**: `/medicines/`
- **Add Medicine**: `/medicines/add/`
- **Edit Medicine**: `/medicines/<id>/edit/`
- **Delete Medicine**: `/medicines/<id>/delete/`

#### Orders Management
- **View All Orders**: `/orders/`
- **Place Order**: `/orders/place/`
- **Order Details**: `/orders/<id>/`
- **Update Status**: `/orders/<id>/update-status/`

### API Usage

The API is accessible at `http://127.0.0.1:8000/api/`

#### Authentication
Currently, the API does not require authentication (can be added as needed).

#### API Browser
Django REST Framework provides a browsable API at `/api/` where you can:
- View all endpoints
- Test API calls directly in the browser
- See API documentation

## API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Medicines API

#### 1. List All Medicines
```http
GET /api/medicines/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Aspirin",
    "description": "Pain reliever and anti-inflammatory",
    "price": "9.99",
    "stock": 100,
    "expiry_date": "2025-12-31",
    "is_in_stock": true,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  }
]
```

#### 2. Get Single Medicine
```http
GET /api/medicines/{id}/
```

**Response:**
```json
{
  "id": 1,
  "name": "Aspirin",
  "description": "Pain reliever and anti-inflammatory",
  "price": "9.99",
  "stock": 100,
  "expiry_date": "2025-12-31",
  "is_in_stock": true,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

#### 3. Create Medicine
```http
POST /api/medicines/
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Paracetamol",
  "description": "Fever reducer",
  "price": "12.99",
  "stock": 200,
  "expiry_date": "2026-06-30"
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "name": "Paracetamol",
  "description": "Fever reducer",
  "price": "12.99",
  "stock": 200,
  "expiry_date": "2026-06-30",
  "is_in_stock": true,
  "created_at": "2025-01-15T11:00:00Z",
  "updated_at": "2025-01-15T11:00:00Z"
}
```

#### 4. Update Medicine (Full)
```http
PUT /api/medicines/{id}/
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Aspirin 500mg",
  "description": "Updated description",
  "price": "11.99",
  "stock": 150,
  "expiry_date": "2026-01-01"
}
```

**Response:** `200 OK`

#### 5. Update Medicine (Partial)
```http
PATCH /api/medicines/{id}/
Content-Type: application/json
```

**Request Body:**
```json
{
  "stock": 75
}
```

**Response:** `200 OK`

#### 6. Delete Medicine
```http
DELETE /api/medicines/{id}/
```

**Response:** `204 No Content`

**Note**: Medicines with pending orders cannot be deleted.

---

### Orders API

#### 1. List All Orders
```http
GET /api/orders/
```

**Response:**
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
  }
]
```

#### 2. Get Single Order
```http
GET /api/orders/{id}/
```

**Response:**
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

#### 3. Create Order
```http
POST /api/orders/
Content-Type: application/json
```

**Request Body:**
```json
{
  "customer_name": "Jane Smith",
  "medicine": 1,
  "quantity": 3
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "customer_name": "Jane Smith",
  "medicine": 1,
  "medicine_name": "Aspirin",
  "medicine_price": "9.99",
  "quantity": 3,
  "order_date": "2025-01-15T13:00:00Z",
  "status": "Pending",
  "total_price": "29.97"
}
```

**Note**: Stock is automatically reduced when an order is created.

#### 4. Update Order Status
```http
PATCH /api/orders/{id}/update_status/
Content-Type: application/json
```

**Request Body:**
```json
{
  "status": "Delivered"
}
```

**Response:** `200 OK`

**Valid Status Values:**
- `Pending`
- `Processing`
- `Shipped`
- `Delivered`
- `Cancelled`

#### 5. Update Order (Full)
```http
PUT /api/orders/{id}/
Content-Type: application/json
```

**Request Body:**
```json
{
  "customer_name": "John Doe Updated",
  "medicine": 1,
  "quantity": 5,
  "status": "Processing"
}
```

**Response:** `200 OK`

#### 6. Delete Order
```http
DELETE /api/orders/{id}/
```

**Response:** `204 No Content`

**Note**: Stock is restored when a pending order is deleted.

---

### Error Responses

All API endpoints return consistent error responses:

**400 Bad Request:**
```json
{
  "status": "error",
  "message": "Error description",
  "errors": {
    "field_name": ["Error details"]
  }
}
```

**404 Not Found:**
```json
{
  "status": "error",
  "message": "Not found.",
  "errors": {}
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "message": "An unexpected error occurred.",
  "error": "Error details"
}
```

## Testing

### Run All Tests

```bash
# Using Django test runner
python manage.py test

# Using pytest (recommended)
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=pharmacy
```

### Test Structure

- **Model Tests**: Test database models and business logic
- **API Tests**: Test all API endpoints (CRUD operations)
- **View Tests**: Test template views and form submissions

### Example Test Execution

```bash
$ pytest -v

pharmacy/tests.py::MedicineModelTest::test_medicine_creation PASSED
pharmacy/tests.py::MedicineModelTest::test_is_in_stock PASSED
pharmacy/tests.py::OrderModelTest::test_order_creation PASSED
pharmacy/tests.py::OrderModelTest::test_insufficient_stock PASSED
pharmacy/tests.py::MedicineAPITest::test_create_medicine PASSED
pharmacy/tests.py::MedicineAPITest::test_get_all_medicines PASSED
pharmacy/tests.py::OrderAPITest::test_create_order PASSED
pharmacy/tests.py::OrderAPITest::test_update_order_status PASSED
...

======================== 25 passed in 2.34s ========================
```

## Logging

The application includes comprehensive logging:

- **Log File**: `medicart.log` (in project root)
- **Console Output**: All logs appear in console during development
- **Log Levels**: INFO, WARNING, ERROR, DEBUG

### Log Format
```
INFO 2025-01-15 12:30:45 views Creating new medicine: Aspirin
INFO 2025-01-15 12:35:22 views New order created: 1 for John Doe
WARNING 2025-01-15 12:40:10 models Insufficient stock for Aspirin
```

## Database Schema

### Medicine Table
```sql
- id: INTEGER (Primary Key)
- name: VARCHAR(200) UNIQUE
- description: TEXT
- price: DECIMAL(10, 2)
- stock: INTEGER
- expiry_date: DATE
- created_at: DATETIME
- updated_at: DATETIME
```

### Order Table
```sql
- id: INTEGER (Primary Key)
- customer_name: VARCHAR(200)
- medicine_id: INTEGER (Foreign Key → Medicine)
- quantity: INTEGER
- order_date: DATETIME
- status: VARCHAR(20)
- total_price: DECIMAL(10, 2)
```

## Admin Interface

Access the Django admin at: `http://127.0.0.1:8000/admin/`

**Features:**
- Full CRUD operations
- Advanced filtering and search
- Bulk actions
- Order tracking

## Deployment Considerations

### Environment Variables

For production, set the following environment variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database

Switch to PostgreSQL for production:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'medicart_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files

Collect static files for production:

```bash
python manage.py collectstatic
```

### Security Checklist

- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS
- [ ] Add authentication to APIs
- [ ] Enable CSRF protection
- [ ] Configure CORS properly

## API Testing Examples

### Using cURL

**Create Medicine:**
```bash
curl -X POST http://127.0.0.1:8000/api/medicines/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vitamin C",
    "description": "Immune booster",
    "price": "15.99",
    "stock": 150,
    "expiry_date": "2026-12-31"
  }'
```

**Place Order:**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Alice Johnson",
    "medicine": 1,
    "quantity": 5
  }'
```

### Using Python requests

```python
import requests

# Create a medicine
medicine_data = {
    "name": "Ibuprofen",
    "description": "Anti-inflammatory",
    "price": "18.50",
    "stock": 200,
    "expiry_date": "2026-08-15"
}
response = requests.post(
    'http://127.0.0.1:8000/api/medicines/',
    json=medicine_data
)
print(response.json())

# Place an order
order_data = {
    "customer_name": "Bob Wilson",
    "medicine": 1,
    "quantity": 3
}
response = requests.post(
    'http://127.0.0.1:8000/api/orders/',
    json=order_data
)
print(response.json())
```

## Troubleshooting

### Common Issues

**Issue**: Module not found error
```
Solution: Ensure virtual environment is activated and dependencies are installed
```

**Issue**: Database migration errors
```bash
Solution: Delete db.sqlite3 and run migrations again
python manage.py migrate --run-syncdb
```

**Issue**: Port already in use
```bash
Solution: Use a different port
python manage.py runserver 8080
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is developed as an assignment and is available for educational purposes.

## Contact & Support

For questions or support, please create an issue in the GitHub repository.

---
