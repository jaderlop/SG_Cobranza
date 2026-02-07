# Dashboard API Examples

Complete documentation of dashboard endpoints with real JSON response examples.

## Base URL
```
http://localhost:8000/api/dashboard
```

---

## 1. Get Main KPIs

**Endpoint:** `GET /api/dashboard/kpis`

**Description:** Returns all 11 main KPIs for the dashboard including sales, purchases, products, clients, and stock metrics.

**Request:**
```bash
curl http://localhost:8000/api/dashboard/kpis
```

**Response:** `200 OK`
```json
{
  "total_sales_count": 150,
  "total_sales_amount": 75000.50,
  "total_purchases_amount": 45000.25,
  "total_products": 85,
  "total_clients": 42,
  "sales_today": 1250.00,
  "sales_this_month": 18500.75,
  "purchases_this_month": 12300.00,
  "pending_sales_count": 12,
  "paid_sales_count": 138,
  "low_stock_products_count": 7
}
```

**Field Descriptions:**
- `total_sales_count`: Total number of sales in the system
- `total_sales_amount`: Total sales amount (currency)
- `total_purchases_amount`: Total purchases amount (currency)
- `total_products`: Number of active products
- `total_clients`: Number of active clients
- `sales_today`: Sales amount for today (filtered by sale_date)
- `sales_this_month`: Sales amount for current month
- `purchases_this_month`: Purchases amount for current month
- `pending_sales_count`: Number of sales with payment_status = 'unpaid'
- `paid_sales_count`: Number of sales with payment_status = 'paid'
- `low_stock_products_count`: Products where stock_quantity <= min_stock_level

---

## 2. Get Sales By Day

**Endpoint:** `GET /api/dashboard/sales-by-day`

**Description:** Returns sales amounts grouped by day for the last N days.

**Query Parameters:**
- `days` (optional): Number of days to look back (1-365, default: 30)

**Request:**
```bash
curl "http://localhost:8000/api/dashboard/sales-by-day?days=30"
```

**Response:** `200 OK`
```json
[
  {
    "date": "2026-01-06",
    "total": 2500.50
  },
  {
    "date": "2026-01-07",
    "total": 1850.25
  },
  {
    "date": "2026-01-08",
    "total": 3200.00
  },
  ...
  {
    "date": "2026-02-04",
    "total": 1750.75
  }
]
```

**Notes:**
- Filtered by `sale_date >= (today - days)`
- Returns empty array if no sales in range
- Dates in ISO format (YYYY-MM-DD)
- Totals as float

---

## 3. Get Purchases By Day

**Endpoint:** `GET /api/dashboard/purchases-by-day`

**Description:** Returns purchases amounts grouped by day for the last N days.

**Query Parameters:**
- `days` (optional): Number of days to look back (1-365, default: 30)

**Request:**
```bash
curl "http://localhost:8000/api/dashboard/purchases-by-day?days=30"
```

**Response:** `200 OK`
```json
[
  {
    "date": "2026-01-10",
    "total": 5200.00
  },
  {
    "date": "2026-01-15",
    "total": 3800.50
  },
  {
    "date": "2026-01-28",
    "total": 4150.25
  },
  {
    "date": "2026-02-03",
    "total": 6200.00
  }
]
```

**Notes:**
- Filtered by `purchase_date >= (today - days)`
- Returns empty array if no purchases in range

---

## 4. Get Sales By Status

**Endpoint:** `GET /api/dashboard/sales-by-status`

**Description:** Returns sales distribution grouped by payment status.

**Request:**
```bash
curl http://localhost:8000/api/dashboard/sales-by-status
```

**Response:** `200 OK`
```json
[
  {
    "status": "paid",
    "count": 138,
    "total_amount": 68500.75
  },
  {
    "status": "unpaid",
    "count": 12,
    "total_amount": 6499.75
  },
  {
    "status": "partial",
    "count": 5,
    "total_amount": 2850.00
  }
]
```

**Notes:**
- Grouped by `payment_status` field
- Common statuses: `paid`, `unpaid`, `partial`
- Returns all unique statuses in database

---

## 5. Get Top Products

**Endpoint:** `GET /api/dashboard/top-products`

**Description:** Returns top N products ranked by quantity sold.

**Query Parameters:**
- `limit` (optional): Number of top products to return (1-50, default: 5)

**Request:**
```bash
curl "http://localhost:8000/api/dashboard/top-products?limit=5"
```

**Response:** `200 OK`
```json
[
  {
    "product_id": 5,
    "product_name": "Premium Widget",
    "total_quantity": 250,
    "total_amount": 12500.00
  },
  {
    "product_id": 12,
    "product_name": "Deluxe Gadget",
    "total_quantity": 180,
    "total_amount": 9800.50
  },
  {
    "product_id": 8,
    "product_name": "Standard Component",
    "total_quantity": 145,
    "total_amount": 5800.00
  },
  {
    "product_id": 3,
    "product_name": "Basic Item",
    "total_quantity": 120,
    "total_amount": 3600.00
  },
  {
    "product_id": 15,
    "product_name": "Advanced Tool",
    "total_quantity": 95,
    "total_amount": 7125.00
  }
]
```

**Notes:**
- Ranked by `total_quantity` (sum of SaleItem.quantity) descending
- Includes `total_amount` (sum of SaleItem.subtotal)
- Only includes products that have been sold

---

## Error Responses

### Validation Error (422 Unprocessable Entity)

**Example:** Invalid query parameter
```bash
curl "http://localhost:8000/api/dashboard/sales-by-day?days=500"
```

**Response:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["query", "days"],
      "msg": "Input should be less than or equal to 365",
      "input": "500"
    }
  ]
}
```

---

## Testing with Swagger UI

Access interactive API documentation at:
```
http://localhost:8000/api/docs
```

Navigate to the **Dashboard** section to test all endpoints with the built-in UI.

---

## SQL Queries Used

### KPIs Endpoint
- `SELECT COUNT(id) FROM sales`
- `SELECT SUM(total) FROM sales`
- `SELECT SUM(total) FROM purchases`
- `SELECT COUNT(id) FROM products WHERE is_active = TRUE`
- `SELECT COUNT(id) FROM clients WHERE is_active = TRUE`
- `SELECT SUM(total) FROM sales WHERE sale_date = TODAY()`
- `SELECT SUM(total) FROM sales WHERE sale_date >= FIRST_DAY_OF_MONTH`
- `SELECT COUNT(id) FROM sales WHERE payment_status = 'unpaid'`
- `SELECT COUNT(id) FROM products WHERE is_active = TRUE AND stock_quantity <= min_stock_level`

### Sales/Purchases By Day
- `SELECT sale_date, SUM(total) FROM sales WHERE sale_date >= (TODAY - N days) GROUP BY sale_date ORDER BY sale_date`

### Sales By Status
- `SELECT payment_status, COUNT(id), SUM(total) FROM sales GROUP BY payment_status`

### Top Products
- `SELECT products.id, products.name, SUM(sale_items.quantity), SUM(sale_items.subtotal) FROM products JOIN sale_items ON products.id = sale_items.product_id GROUP BY products.id ORDER BY SUM(sale_items.quantity) DESC LIMIT N`

---

## Performance Notes

All endpoints are optimized to:
- Avoid N+1 query problems
- Use database aggregation (not Python loops)
- Convert Decimal to float at service layer
- Handle NULL values gracefully
- Use indexed fields for filtering (sale_date, purchase_date, payment_status)
