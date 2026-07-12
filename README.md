# AssetFlow - Smart Asset Management System

AssetFlow is a web-based Asset Management System built for managing organizational resources efficiently.  
It provides features for asset tracking, employee management, resource booking, maintenance requests, audit cycles, notifications, and user role management.

## Features

### Asset Management
- Add and register new assets
- Track asset availability status
- Allocate assets to employees
- Release allocated assets back to availability
- Search assets by tag or name

### Employee Management
- Add employees with email details
- View employee records
- Allocate assets to employees

### Resource Booking
- Book resources for specific time periods
- Prevent overlapping bookings

### Maintenance Management
- Raise maintenance requests
- Track maintenance status
- Maintain repair history

### Audit Management
- Perform asset audit cycles
- Record asset condition
- Store audit history with date and auditor details

### Notifications
- Activity feed for important actions:
  - Login/logout activity
  - Asset registration
  - Asset allocation/release
  - Bookings
  - Maintenance requests
  - Audits
  - User creation

### User Roles
- Support for different user roles:
  - Admin
  - Manager
  - Employee

### Dashboard
Displays:
- Total assets
- Available assets
- Allocated assets
- Employees
- Bookings
- Maintenance records
- Audit records


## Technologies Used

- Python
- Flask
- SQLite Database
- HTML
- CSS
- Jinja2 Templates


## Project Structure

```
AssetFlow/
│
├── app.py
├── assetflow.db
│
├── templates/
│   ├── index.html
│   └── login.html
│
└── README.md
```


## Installation and Setup

### 1. Clone the repository

```
git clone <repository-link>
```

### 2. Navigate to project folder

```
cd AssetFlow
```

### 3. Install Flask

```
pip install flask
```

### 4. Run the application

```
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```


## Database

AssetFlow uses SQLite for storing:

- Assets
- Employees
- Bookings
- Allocations
- Maintenance Requests
- Audits
- Notifications
- Users and Roles


## Future Improvements

- Authentication with passwords
- Role-based access control
- Export reports
- Email notifications
- Cloud deployment
- Better UI design


## Developed For

Odoo Hackathon 2026

## Team Project

AssetFlow - Smart Asset Management System