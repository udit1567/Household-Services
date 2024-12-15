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
![schemaa](https://github.com/user-attachments/assets/7ec37275-4bd9-4f3a-9c51-c505945776e4)

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
![Screenshot 2024-12-15 203716](https://github.com/user-attachments/assets/1879ba38-70a3-4b51-af84-0874d07802b0)
![Screenshot 2024-12-15 201907](https://github.com/user-attachments/assets/dba041a1-e40c-4290-a429-329a1e94b9e8)
![Screenshot 2024-12-15 203738](https://github.com/user-attachments/assets/b9455ae7-81cb-43c1-99fe-39e4255b7665)

- **Admin Dashboard**: Manage services and users.
![Screenshot 2024-12-15 200951](https://github.com/user-attachments/assets/76ff5fa0-49ab-4a44-be6d-e313f87b980f)
![Screenshot 2024-12-15 201925](https://github.com/user-attachments/assets/7e8aa4d3-6ef3-484d-a803-0851e8bd2120)
![Screenshot 2024-12-15 201003](https://github.com/user-attachments/assets/59be8868-7e81-409b-a8c4-8ba14e191632)

- **Customer Dashboard**: Search for and request services.
![Screenshot 2024-12-15 201447](https://github.com/user-attachments/assets/64dcc7a7-9568-4b2c-83f6-a1953fabc435)
![Screenshot 2024-12-15 201717](https://github.com/user-attachments/assets/fd9b3562-8e83-410e-a78a-35d6bc73b379)
![Screenshot 2024-12-15 201625](https://github.com/user-attachments/assets/6add70a2-b3dd-40d5-8d1b-844a51f3559f)

- **Professional Dashboard**: View and manage assigned requests.
![Screenshot 2024-12-15 201351](https://github.com/user-attachments/assets/9ef9d57e-f3e6-4c35-a23f-0da9faf1375e)
![Screenshot 2024-12-15 201150](https://github.com/user-attachments/assets/baee29cb-38f8-4a94-95b3-82907b791717)
![Screenshot 2024-12-15 201417](https://github.com/user-attachments/assets/96116d2a-0f22-41fd-a037-c8d5dbd45558)






## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or support, please contact:
- uditmaurya2003@gmail.com



