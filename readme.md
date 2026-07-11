# Mini E-Commerce Production API

A production-ready, lightweight E-Commerce API built with Python and FastAPI. This project serves as a practical implementation of software engineering design patterns, focusing on strict Separation of Concerns (SoC), Dependency Injection, and a Feature-Based Project Structure.

---

## 🏗️ System Architecture

This project utilizes a **Feature-Based / Vertical Slice** architectural design. Each business domain contains its own decoupled presentation, business logic, and data access layers.
![alt text](image.png)

---

## ✨ Features & API Endpoints

### 👥 Users Feature
- **POST /users/** - Register a new user
  - Validates email uniqueness (prevents duplicate email registrations)
  - Returns user ID, email, and created user response
- **GET /users/{username}** - Retrieve user by username
  - Searches for user by exact username match
  - Returns 404 if user not found
- **GET /users/email/{email}** - Retrieve user by email
  - Searches for user by exact email match
  - Returns 404 if user not found

### 🏷️ Categories Feature
- **GET /categories/** - Retrieve all product categories
- **POST /categories/** - Create or retrieve category
  - Implements get-or-create pattern (returns existing category if it already exists with the same name)

### 📦 Products Feature
- **POST /products/** - Create a new product
  - Prevents duplicate product titles (same title cannot be used more than once)
  - Associates product with a category (auto-creates category if needed)
  - Returns product details with ID, title, price, stock, and category
- **GET /products/** - Retrieve all products in the catalog
- **GET /products/{product_id}** - Retrieve a specific product by ID

### 🛒 Orders Feature
- **POST /orders/** - Place a new order (checkout)
  - **Validation Logic:**
    - Verifies user exists in the system
    - Verifies product exists in the catalog
    - Checks inventory availability before order placement
  - **Business Logic:**
    - Automatically deducts order quantity from product stock
    - Calculates total price (product price × quantity)
  - **Returns:** Order confirmation with ID, user ID, product ID, quantity, and total price

### 🤖 Chatbot Feature
- **POST /chatbot/message** - Send a message to the AI assistant
  - Persists the incoming user message to the database
  - Calls the Gemini AI model to generate a response
  - Persists the generated assistant reply as chat history
  - Returns the stored chatbot response payload

---

## 🏛️ Architectural Layers

Each feature (Users, Categories, Products, Orders, Chatbot) follows a three-layer architecture:

1. **Routes Layer** (`*_routes.py`) - API endpoints and HTTP handling with dependency injection
2. **Service Layer** (`*_service.py`) - Business logic, validation rules, and domain coordination
3. **Repository Layer** (`*_repository.py`) - Database queries and data persistence
4. **Models Layer** (`*_models.py`) - Database entities (ORM) and Pydantic request/response schemas

---

## 🔗 Cross-Domain Integration

- Products can automatically create and assign categories on the fly
- Orders coordinate across multiple domains: users, products, and inventory
- ProductService is injected into OrderService to handle inventory validation and deduction
- The Chatbot feature stores conversation messages in the same application database, enabling history-aware persistence alongside the AI response flow

---

## 🚀 Running the API

```bash
PYTHONPATH=. fastapi dev app/main.py
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`