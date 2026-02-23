# ms-agents-api
ms-agents is an api developed to offer a complete ecosystem for managing AI Agents (LLMs).

## Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (dependency manager)
- MongoDB (configure URL in the `.env` file)

## Installation

1. Clone the repository and access the project folder:
   ```bash
   git clone <repository-url>
   cd ms-agents-api
   ```

2. Create the `.env` file based on `.env.example` and set up the variables:
   ```bash
   cp .env.example .env
   # Edit the .env file as needed
   ```

3. Install dependencies:
   ```bash
   make install
   ```

## Running the server

- To start the server in production mode:
  ```bash
  make run
  ```
  The server will be available at `http://localhost:8000`.

- For development mode (hot reload):
  ```bash
  make run_dev
  ```

## Endpoints

Access the automatic documentation at `http://localhost:8000/ms-agents-api/docs` after starting the server.
