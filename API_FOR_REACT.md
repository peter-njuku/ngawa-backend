# API Guide for React Frontend

## Public Access (No Authentication Required)

Your API is fully configured for **public access**. Customers can browse products and categories without any password or login.

---

## Base URL

```
http://localhost:8000/api/
```

For production, replace `localhost:8000` with your production domain.

---

## Endpoints for Buyers (Public)

### 1. Get All Categories
```
GET /api/categories/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Desktops",
    "description": "Desktop computers and systems"
  },
  {
    "id": 2,
    "name": "Laptops",
    "description": "Laptop computers"
  },
  {
    "id": 3,
    "name": "Printers",
    "description": "Printer devices"
  },
  {
    "id": 4,
    "name": "Accessories",
    "description": "Computer accessories"
  }
]
```

---

### 2. Get Single Category
```
GET /api/categories/{id}/
```

Example: `GET /api/categories/1/`

---

### 3. Get All Products
```
GET /api/products/
```

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Dell XPS 13",
      "description": "Ultra-portable laptop",
      "price": "999.99",
      "category": {
        "id": 2,
        "name": "Laptops"
      },
      "image": null,
      "is_active": true,
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

### 4. Get Single Product
```
GET /api/products/{id}/
```

Example: `GET /api/products/1/`

---

### 5. Get Products by Category
```
GET /api/products/?category_id={category_id}
```

Example: `GET /api/products/?category_id=2`

This returns only products in the Laptops category.

---

### 6. Get Products Grouped by Category
```
GET /api/products/by_category/
```

**Response:**
```json
{
  "Desktops": [
    {
      "id": 1,
      "name": "iMac 24\"",
      "price": "1299.99",
      "category": {...},
      "is_active": true
    }
  ],
  "Laptops": [
    {
      "id": 2,
      "name": "MacBook Pro",
      "price": "1999.99",
      "category": {...},
      "is_active": true
    }
  ],
  "Printers": [...],
  "Accessories": [...]
}
```

---

### 7. Get All Active Products Only
```
GET /api/products/active/
```

This returns only products where `is_active = true`.

---

## React Code Examples

### Fetch All Products
```javascript
const [products, setProducts] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  fetch('http://localhost:8000/api/products/')
    .then(res => res.json())
    .then(data => {
      setProducts(data.results);
      setLoading(false);
    })
    .catch(err => {
      console.error('Error fetching products:', err);
      setLoading(false);
    });
}, []);
```

### Fetch Categories
```javascript
const [categories, setCategories] = useState([]);

useEffect(() => {
  fetch('http://localhost:8000/api/categories/')
    .then(res => res.json())
    .then(data => setCategories(data))
    .catch(err => console.error('Error:', err));
}, []);
```

### Filter Products by Category
```javascript
const [selectedCategory, setSelectedCategory] = useState(null);
const [filteredProducts, setFilteredProducts] = useState([]);

useEffect(() => {
  if (selectedCategory) {
    fetch(`http://localhost:8000/api/products/?category_id=${selectedCategory}`)
      .then(res => res.json())
      .then(data => setFilteredProducts(data.results))
      .catch(err => console.error('Error:', err));
  }
}, [selectedCategory]);
```

### Get Products Grouped by Category
```javascript
const [groupedProducts, setGroupedProducts] = useState({});

useEffect(() => {
  fetch('http://localhost:8000/api/products/by_category/')
    .then(res => res.json())
    .then(data => setGroupedProducts(data))
    .catch(err => console.error('Error:', err));
}, []);
```

---

## CORS Configuration

The backend is already configured to accept requests from:
- `http://localhost:3000` (typical React dev server)
- `http://127.0.0.1:3000`
- `http://localhost:8000` (backend itself)

If your React app runs on a different port, update the `CORS_ALLOWED_ORIGINS` in `.env`:

```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://yourproductionurl.com
```

---

## Admin-Only Endpoints (Password Required)

**You do NOT need to share these with buyers**, but your admin can use them:

### Create Product (Admin Only)
```
POST /api/products/
```

Requires admin login at `/admin/`

### Update Product (Admin Only)
```
PUT /api/products/{id}/
PATCH /api/products/{id}/
```

### Delete Product (Admin Only)
```
DELETE /api/products/{id}/
```

Same for categories - only admins can create, update, or delete.

---

## Pagination

Products are paginated with 20 items per page. The response includes:
- `count`: Total number of products
- `next`: URL to next page
- `previous`: URL to previous page
- `results`: Array of products

To get page 2:
```
GET /api/products/?page=2
```

---

## Filtering & Pagination Together

```
GET /api/products/?category_id=2&page=2
```

This gets page 2 of products in category 2.

---

## No Authentication Needed

✅ All GET endpoints are **completely public**
✅ No API key required
✅ No login for viewing products
✅ Only admins can create/edit/delete products

---

## Production Deployment

When deploying:

1. Update `CORS_ALLOWED_ORIGINS` to your production React domain
2. Update `ALLOWED_HOSTS` to your production domain
3. Set `DEBUG=False` in production
4. Use a strong `SECRET_KEY`

Example for production:
```
ALLOWED_HOSTS=ngawasolutions.com,www.ngawasolutions.com
CORS_ALLOWED_ORIGINS=https://ngawasolutions.com,https://www.ngawasolutions.com
DEBUG=False
SECRET_KEY=your-secret-key-here
```

---

## Troubleshooting

### CORS Error in Browser Console
**Problem:** "Access to XMLHttpRequest blocked by CORS policy"

**Solution:** Make sure your React app URL is in `CORS_ALLOWED_ORIGINS` in the `.env` file

### 404 Error on Endpoints
**Problem:** Endpoint not found

**Solution:** Make sure you're using the correct base URL. Should be `http://localhost:8000/api/` not `http://localhost:8000`

### Connection Refused
**Problem:** Can't connect to backend

**Solution:** Make sure backend is running: `docker-compose up`

---

## Summary

- **For Buyers:** Use GET endpoints to view products and categories (NO authentication needed)
- **For Admin:** Use admin panel at `http://localhost:8000/admin/` to manage products
- **CORS:** Already configured for localhost:3000
- **Pagination:** Results are paginated with 20 items per page
- **Filtering:** Filter by category_id or get products by_category

Your React app can freely fetch and display products without any password or authentication! 🎉
