# Order Management Service

This service is responsible for managing room service orders within the Hotel Order Management System. It handles the creation, modification, cancellation, and tracking of room service orders.

## Features

- Create new room service orders with items, quantities, guest details, and delivery instructions.
- View, modify, and cancel existing room service orders.
- Display real-time status of each room service order (e.g., "Pending," "In Progress," "Delivered," "Cancelled").
- Integration points for Property Management System (PMS) and Inventory Management Service.

## Architecture

This service is part of a microservices architecture, deployed on Google Cloud Platform (GCP) using Docker and Kubernetes.

## Setup Instructions

### Prerequisites

- Python 3.9+
- Docker (for containerization)
- Kubernetes (for orchestration, if deploying locally with Minikube/Kind)
- PostgreSQL database
- MongoDB database

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Sneha2002saji-pixel/Trial_MCP_Server_Location.git
    cd Trial_MCP_Server_Location/order_management_service
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    Create a `.env` file in the `order_management_service` directory based on `config.py` and `.env.example`.

4.  **Run the application:**
    ```bash
    python main.py
    ```

## API Endpoints (Planned)

- `POST /orders`: Create a new order
- `GET /orders/{order_id}`: Get order details
- `PUT /orders/{order_id}`: Update an order
- `DELETE /orders/{order_id}`: Cancel an order
- `PUT /orders/{order_id}/status`: Update order status

## Contributing

Please refer to the main repository's `CONTRIBUTING.md` for contribution guidelines.
