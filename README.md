# Hr Log Service 
    A Calendar service for HR-related activities.

# Requirements
* POSTGRES


# BUILD:
* docker build -t {calendar} .
* docker run -p 8000:8000 {calendar}

# .env Configuration
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=postgres
* POSTGRES_HOST=localhost
* POSTGRES_PORT=5434
* SERVER_HOST=localhost
* SERVER_PORT=9090
* POSTGRES_DB=calendar

* AUTH_HOST=test.com
* AUTH_PORT=443
* AUTH_INTERNAL_USERNAME=example_username
* AUTH_INTERNAL_PASSWORD=example_password
* AUTH_USE_TLS=True

# Design Pattern Used:
* Onion Pattern: [Onion](https://github.com/iktakahiro/dddpy)
* Unit of Work Pattern: [Unit of Work](https://www.cosmicpython.com/book/chapter_06_uow.html)
