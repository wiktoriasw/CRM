# Customer Relationship Management (CRM)

## Overview

**CRM** is a **FastAPI-based** application for managing trips — for example, bike or hiking trips. It provides endpoints for creating, updating, and tracking trips, participants, news, payments, insurance, and post-trip feedback.

## Run

1. Clone the repository:
```bash
git clone https://github.com/wiktoriasw/CRM.git
```

2. Navigate to project directory
```bash
cd CRM
```

3. Install required libraries:
```bash
pip install -r requirements.txt
```
4. Configure the SECRET_KEY

Add `SECRET_KEY` to your configuration.py file:

- `SECRET_KEY` — JWT secret key. **No default value; you need to assign it.**
   
    - Generate key:
        ```bash
        openssl rand -hex 32
        ```
    - Example: 
        ```bash
        SECRET_KEY=4jfjir...
        ```
5. Run the server with:
```bash
    fastapi dev main.py
```