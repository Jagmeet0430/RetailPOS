# System Architecture

The desktop UI must never manipulate the database directly.

```text
Electron Desktop
React + TypeScript UI
        |
        | HTTP
        v
FastAPI API
- Auth
- Products
- Sales
- Inventory
- Customers
- Reports
        |
        | SQLAlchemy
        v
PostgreSQL
- Products
- Sales
- Inventory
- Payments
- Users
- Audit Logs
```

Correct dependency flow:

```text
React
  -> FastAPI
  -> Service
  -> Repository
  -> PostgreSQL
```

Avoid:

```text
React
  -> PostgreSQL
```

This separation will become important later when adding cloud sync, a mobile app, or multiple registers.
