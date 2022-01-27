# FT Booking(Flight Ticket Booking)

This project is going to be a simple booking ticket.

# What is FT Booking?
FT Booking is a platform for buy flight tickets, it's small and just use for flights.

<hr style="border:2px solid gray"> </hr>


## Installation

### First step

create FTBooking directory:

    mkdir FTBooking

go to FTBooking directory:

    cd FTBooking

---

### Second step

clone the project:

    https://github.com/MrMohammadY/flight_booking_service.git

create virtualenv in Delivery_Management directory:

    virtualenv booking_venv

now active your virtualenv:

    source booking_venv/bin/activate

---

### Third step

go to project by:

    cd flight_booking_service

install package with:

    pip install -r requirements.txt

---

### Fourth step

in delivery-management-challenge directory you should create .env file for some django settings(.env files is hidden files):

    touch .env

and fill this argument in env file:

- SECRET_KEY = '\<django secret key (you can generate from this [site](https://djecrety.ir/)) >'
- DEBUG = True
- ALLOWED_HOSTS = ['*']

---

### Fifth step

now make migrations with:

    python manage.py makemigrations

and after that applying migrations:

    python manage.py migrate

and after apply migrations run celery:

    celery -A booking worker -l info

and run celery beat:

    celery -A booking beat -l info

and run redis server:
    
    redis-server    

---

### In the last

you can now run project by:

    python manage.py runserver