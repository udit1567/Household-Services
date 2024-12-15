# Household Services Application

**A Modern Application Development Project**

## Overview

The Household Services Application is a multi-user platform designed to provide comprehensive home servicing and solutions. It supports three roles: **Admin**, **Service Professionals**, and **Customers**, each with unique functionalities. Built using Flask, Jinja2 templates, Bootstrap, and SQLite, the application demonstrates efficient role-based management of services and user interactions.

## Features

### Admin Role
- **Login**: Admin has root access and does not require registration.
- **Dashboard**:
  - Manage all users (customers and service professionals).
  - Approve service professionals after verifying profile documents.
  - Block customers or service professionals based on fraudulent activities or poor reviews.
- **Service Management**:
  - Create new services with a base price.
  - Update existing services (e.g., name, price, time required).
  - Delete services.
- **Search**:
  - Search for professionals to block, unblock, or review.

### Service Professional Role
- **Login/Register**: Manage their profile and accept/reject service requests.
- **Profile**:
  - Contains ID, name, date created, description, service type, and experience.
  - Visible to customers based on reviews.
- **Service Request Management**:
  - View all service requests from customers.
  - Accept/reject assigned service requests.
  - Mark service requests as completed after exiting the location.

### Customer Role
- **Login/Register**: Access the platform to book services.
- **Service Requests**:
  - Create new service requests based on available services.
  - Edit existing requests (e.g., update date, status, remarks).
  - Close completed service requests.
- **Search Services**:
  - Search by name, location, or pin code.
- **Reviews**:
  - Post reviews/remarks on closed service requests.

## Technology Stack

- **Backend**: Flask
- **Frontend**: Jinja2 templates, Bootstrap
- **Database**: SQLite

## Database Models

### Users Table
- `id` (Primary Key)
- `username`
- `password`
- `role` (admin, professional, customer)
- Other relevant fields...

### Services Table
- `id` (Primary Key)
- `name`
- `price`
- `time_required`
- `description`

### Service Requests Table
- `id` (Primary Key)
- `service_id` (Foreign Key)
- `customer_id` (Foreign Key)
- `professional_id` (Foreign Key)
- `date_of_request`
- `date_of_completion`
- `service_status` (requested/assigned/closed)
- `remarks`

### Additional Tables
- **Customer Reviews Table**
- **Professional Profile Documents Table**

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd household-services-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. Run the application:
   ```bash
   flask run --host=0.0.0.0
   ```

5. Access the application on `http://127.0.0.1:5000`.

## Usage

1. **Admin**: Access the admin dashboard after login to manage users and services.
2. **Service Professionals**: Register or login to view and manage assigned service requests.
3. **Customers**: Register or login to browse, request, and review services.

## Application Wireframe

The application adheres to the following flow:
- **Home Page**: Role-based login and registration.
- **Admin Dashboard**: Manage services and users.
- **Customer Dashboard**: Search for and request services.
- **Professional Dashboard**: View and manage assigned requests.

## Screenshots

(Add screenshots of the application here to showcase the interface and functionality.)

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or support, please contact:
- uditmaurya2003@gmail.com



