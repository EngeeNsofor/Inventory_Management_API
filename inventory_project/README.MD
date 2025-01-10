# Endpoints For Inventory Management App

### Registration

---

**URL**: `http://localhost:8000/api/register/`

**HTTP Header** `POST`

**Request JSON Body**

```
{
  "username": "testuser3",
  "email": "testuser3@yahoo.com",
  "password": "testpassword3",
  "confirm_password": "testpassword3"
}
```

**Response JSON**

```
{
    "message": "Registration successful.",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNjM0NDMxMywiaWF0IjoxNzM2MjU3OTEzLCJqdGkiOiI2ZWM4ZjZjOGUyNDM0MjJlYjM2MTIyN2IyYzc3MGJiOCIsInVzZXJfaWQiOjR9.A6rmJKAE-UQPF8OnoL7gUN5qtrAsmE2Z51jHAyRZ36U",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MjU5NzEzLCJpYXQiOjE3MzYyNTc5MTMsImp0aSI6ImUzNTNkOTQ2ZTRjMzQxZWU4OTcyZTA1M2FkY2Q1OThlIiwidXNlcl9pZCI6NH0.UlRlSb-BT8jfaDqjMjFBw9-NPkfDFp4BTuBMdowRqY4"
}
```

---

### Login User

**URL**: `http://localhost:8000/api/login/`

**HTTP Header** `POST`

**Request JSON Body**

```
{
  "username": "testuser3",
  "password": "testpassword3"
}
```

**Response JSON**

```
{
    "message": "Login successful.",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNjM0NDMxMywiaWF0IjoxNzM2MjU3OTEzLCJqdGkiOiI2ZWM4ZjZjOGUyNDM0MjJlYjM2MTIyN2IyYzc3MGJiOCIsInVzZXJfaWQiOjR9.A6rmJKAE-UQPF8OnoL7gUN5qtrAsmE2Z51jHAyRZ36U",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2MjU5NzEzLCJpYXQiOjE3MzYyNTc5MTMsImp0aSI6ImUzNTNkOTQ2ZTRjMzQxZWU4OTcyZTA1M2FkY2Q1OThlIiwidXNlcl9pZCI6NH0.UlRlSb-BT8jfaDqjMjFBw9-NPkfDFp4BTuBMdowRqY4"
}
```

---

### Create Inventory Item

**URL**: `http://localhost:8000/api/items/`

**HTTP Header** `POST`

**Authorization Required**: `Bearer Token (access token)`

**Request JSON Body**

```
  {
    "name": "Samsung 65\" QLED TV",
    "description": "High-definition 4K TV",
    "category": "Electronics",
    "price": 1400,
    "quantity": 12
  }
```

**Response JSON**

```
{
    "id": 38,
    "managed_by": "ngnsofor",
    "name": "coconut Juice",
    "description": "Juicy coconut",
    "quantity": 200,
    "price": "600.00",
    "category": "food",
    "date_added": "2025-01-07T22:26:01.898952Z",
    "last_updated": "2025-01-07T22:26:01.899018Z",
    "message": "Item successfully created"
}
```

---

### Delete Inventory Item

**URL**: `http://localhost:8000/api/items/<id>/`

**HTTP Header** `DELETE`

**Authorization Required**: `Bearer Token (access token)`

**Response JSON**

```
{
    "message": "Item successfully deleted"
}
```

---

### Update Inventory Item

**URL**: `http://localhost:8000/api/items/<id>/`

**HTTP Header** `PUT`

**Authorization Required**: `Bearer Token (access token)`

**Request JSON Body**

```
  {
    "name": "coconut Juice",
    "description": "Juicy coconut hjd",
    "category": "food and drinks",
    "price": 600,
    "quantity": 160,
    "change_reason": "restock"    #(Optional)
  }
```

**Response JSON**

```
{
    "id": 38,
    "managed_by": "ngnsofor",
    "name": "coconut Juice",
    "description": "Juicy coconut hjd",
    "quantity": 160,
    "price": "600.00",
    "category": "food and drinks",
    "date_added": "2025-01-07T22:26:01.898952Z",
    "last_updated": "2025-01-07T22:29:29.597646Z",
    "message": "Item successfully updated"
}
```

**NOTE**: The `"change_reason"` in the request body is only needed when there is a change in the value of `quantity`, in which you must choose from 3 options `restock`, `sold` or `damaged`. It no change to quatity, the it is automatically saved as `rebrand`.

---

### Get Inventory Item

**URL**: `http://localhost:8000/api/items/<id>/`

**HTTP Header** `GET`

**Authorization Required**: `Bearer Token (access token)`

**Response JSON**

```
{
    "id": 38,
    "managed_by": "ngnsofor",
    "name": "coconut Juice",
    "description": "Juicy coconut hjd",
    "quantity": 160,
    "price": "600.00",
    "category": "food and drinks",
    "date_added": "2025-01-07T22:26:01.898952Z",
    "last_updated": "2025-01-07T22:29:29.597646Z"
}
```

---

### Get All Inventory Items

**URL**: `http://localhost:8000/api/items/`

**HTTP Header** `GET`

**Authorization Required**: `Bearer Token (access token)`

**Response JSON**

```
{
    "count": 14,
    "next": "http://localhost:8000/api/items/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Macbook Air",
            "description": "Lightweight Apple laptop",
            "quantity": 15,
            "price": "1200.00",
            "category": "Electronics",
            "date_added": "2025-01-07T09:22:22.860584Z",
            "last_updated": "2025-01-07T09:22:22.860626Z",
            "managed_by": 3
        },
        {
            "id": 2,
            "name": "Sony TV",
            "description": "Lightweight Televison",
            "quantity": 10,
            "price": "4200.00",
            "category": "Electronics",
            "date_added": "2025-01-07T09:23:27.384098Z",
            "last_updated": "2025-01-07T09:23:27.384122Z",
            "managed_by": 3
        }
    ]
}
```

**Filtering Methods**

- **By Pagination**: http://localhost:8000/api/items/?page=2
- **By Item Name**: http://localhost:8000/api/items/?name=Rice
- **By Price Range**: http://localhost:8000/api/items/?price_gte=1000&price_lte=2000
- **By Quantity**: http://localhost:8000/api/items/?quantity__lt=5
- **By Category**: http://localhost:8000/api/items/?category=Electronics

---

### Get Inventory Item Logs For An Inventory Item

**URL**: `http://localhost:8000/api/logs/<id>/`

**HTTP Header** `GET`

**Authorization Required**: `Bearer Token (access token)`

**Response JSON**

```
{
    "count": 29,
    "next": "http://localhost:8000/api/logs/?page=2",
    "previous": null,
    "results": [
        {
            "id": 55,
            "change_type": "DELETE",
            "change_reason": "unwanted",
            "quantity_before": 160,
            "quantity_after": 0,
            "timestamp": "2025-01-07T22:31:00.554704Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },,
        {
            "id": 53,
            "change_type": "UPDATE",
            "change_reason": "restock",
            "quantity_before": 60,
            "quantity_after": 160,
            "timestamp": "2025-01-07T22:29:22.874137Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 52,
            "change_type": "UPDATE",
            "change_reason": "sold",
            "quantity_before": 100,
            "quantity_after": 60,
            "timestamp": "2025-01-07T22:29:10.442217Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 51,
            "change_type": "UPDATE",
            "change_reason": "damaged",
            "quantity_before": 200,
            "quantity_after": 100,
            "timestamp": "2025-01-07T22:28:48.050956Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 50,
            "change_type": "UPDATE",
            "change_reason": "rebrand",
            "quantity_before": 200,
            "quantity_after": 200,
            "timestamp": "2025-01-07T22:28:08.052275Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 49,
            "change_type": "CREATE",
            "change_reason": "new-item",
            "quantity_before": 0,
            "quantity_after": 200,
            "timestamp": "2025-01-07T22:26:01.902193Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        }
    ]
}
```

---

### Get All Inventory Item logs For A User

**URL**: `http://localhost:8000/api/logs/`

**HTTP Header** `GET`

**Authorization Required**: `Bearer Token (access token)`

**Response JSON**

```
{
    "count": 29,
    "next": "http://localhost:8000/api/logs/?page=2",
    "previous": null,
    "results": [
        {
            "id": 55,
            "change_type": "DELETE",
            "change_reason": "unwanted",
            "quantity_before": 160,
            "quantity_after": 0,
            "timestamp": "2025-01-07T22:31:00.554704Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 54,
            "change_type": "UPDATE",
            "change_reason": "rebrand",
            "quantity_before": 160,
            "quantity_after": 160,
            "timestamp": "2025-01-07T22:29:29.600005Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 53,
            "change_type": "UPDATE",
            "change_reason": "restock",
            "quantity_before": 60,
            "quantity_after": 160,
            "timestamp": "2025-01-07T22:29:22.874137Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 52,
            "change_type": "UPDATE",
            "change_reason": "sold",
            "quantity_before": 100,
            "quantity_after": 60,
            "timestamp": "2025-01-07T22:29:10.442217Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 51,
            "change_type": "UPDATE",
            "change_reason": "damaged",
            "quantity_before": 200,
            "quantity_after": 100,
            "timestamp": "2025-01-07T22:28:48.050956Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 50,
            "change_type": "UPDATE",
            "change_reason": "rebrand",
            "quantity_before": 200,
            "quantity_after": 200,
            "timestamp": "2025-01-07T22:28:08.052275Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 49,
            "change_type": "CREATE",
            "change_reason": "new-item",
            "quantity_before": 0,
            "quantity_after": 200,
            "timestamp": "2025-01-07T22:26:01.902193Z",
            "item": null,
            "item_name": "coconut Juice",
            "changed_by": "ngnsofor"
        },
        {
            "id": 48,
            "change_type": "DELETE",
            "change_reason": "unwanted",
            "quantity_before": 150,
            "quantity_after": 0,
            "timestamp": "2025-01-07T21:45:13.613475Z",
            "item": null,
            "item_name": "coconut",
            "changed_by": "ngnsofor"
        },
        {
            "id": 47,
            "change_type": "UPDATE",
            "change_reason": "restock",
            "quantity_before": 50,
            "quantity_after": 150,
            "timestamp": "2025-01-07T21:41:19.697404Z",
            "item": null,
            "item_name": "",
            "changed_by": "ngnsofor"
        },
        {
            "id": 46,
            "change_type": "UPDATE",
            "change_reason": "sold",
            "quantity_before": 70,
            "quantity_after": 50,
            "timestamp": "2025-01-07T21:41:07.942917Z",
            "item": null,
            "item_name": "",
            "changed_by": "ngnsofor"
        }
    ]
}
```

---

### WEB BROWSER URLS

- **Home**: `http://localhost:8000/`
- **Admin**: `http://localhost:8000/admin/`
- **Login**: `http://localhost:8000/login/`
- **Register**: `http://localhost:8000/register/`
