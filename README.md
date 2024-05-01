# Hr Log Service 
    A Calendar service for HR-related activities.

# Requirements
* POSTGRES

# BUILD:
* docker build -t {calendar} .
* docker run -p 8000:8000 {calendar}

# Design Pattern Used:
* Onion Pattern: [Onion](https://github.com/iktakahiro/dddpy)
* Unit of Work Pattern: [Unit of Work](https://www.cosmicpython.com/book/chapter_06_uow.html)
