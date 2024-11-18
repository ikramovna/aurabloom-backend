# Project Installation Guide

This guide will help you set up the project on your local machine for development and testing purposes.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Installation Steps

1. Clone the repository to your local machine:

```bash
https://github.com/ikramovna/aurabloom-backend.git
```

2. Navigate to the project directory:

```bash
cd aurabloom-backend
```

3. It's recommended to create a virtual environment to isolate your project and avoid version conflicts with packages.
   You can do it using the following commands:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

4. Once the virtual environment is activated, you can install the required packages using pip:

```bash
pip install -r requirements.txt
```

or use makefile

```bash
make install-req
```

## Running the Application

To run the application, execute the following command in the project directory:

```bash
python manage.py runserver
```

The application will start running at `http://127.0.0.1:8000/`.

## Running Tests

To run the tests for the application, execute the following command in the project directory:

```bash
python manage.py test
```

# Project Structure and Purpose

## Purpose

The project is a backend service for a beauty salon booking system. It allows users to book services provided by the
salon. The system manages bookings, services, and user accounts.
This system is not just a scheduling tool but a full-fledged platform that caters to various stakeholders including customers, salon managers, and possibly salon staff. Here's more information about the system's capabilities, components, and functionalities:

### Key Features:

1. **User Account Management:**
   - Allows customers to create, manage, and customize their profiles, including personal information and preferences.
   - Salon staff and managers can also have accounts with different access levels to manage their schedules, view bookings, and interact with customers.

2. **Service Catalog:**
   - A detailed list of services offered by the salon, including descriptions, durations, prices, and any other relevant details.
   - Option for salon managers to add, update, or remove services based on availability and new offerings.

3. **Booking Engine:**
   - A calendar-based booking system where customers can view available slots for different services and book appointments.
   - Features to modify or cancel bookings with predefined rules regarding notice periods and possible penalties.

4. **Appointment Management:**
   - Dashboard for salon staff and managers to view daily schedules, upcoming appointments, and customer details.
   - Functionality to confirm, reschedule, or cancel appointments from the salon's end.



5. **Reviews and Ratings:**
   - System for customers to rate services and leave reviews, helping future customers make informed decisions.
  

### Future Enhancements:

- **Loyalty Programs:** Implement loyalty and rewards programs to encourage repeat bookings and customer loyalty.
- **Personalized Marketing:** Utilize customer data and preferences for targeted promotions, personalized service recommendations, and exclusive offers.
- **Virtual Consultations:** Incorporate options for online consultations or preliminary meetings, especially for extensive or specialized services.

This comprehensive approach not only aims to streamline salon operations but also enhance the customer experience, ensuring a high level of satisfaction and operational efficiency for the salon.

## Structure

The project is structured as follows:

- `beauty/serializers/booking.py`: This file contains the serializers for the Booking model. Serializers allow complex
  data types, such as querysets and model instances, to be converted to Python datatypes that can then be easily
  rendered into JSON, XML, or other content types.

- `beauty/models/booking.py`: This file contains the Booking model. The Booking model is a representation of a booking
  made by a user. It includes fields such as date, time, service, and user.

- `beauty/models/service.py`: This file contains the Service model. The Service model represents the services provided
  by the beauty salon. It includes fields such as name, description, price, and duration.

- `users/serializers.py`: This file contains the serializers for the User model. It is responsible for converting User
  model instances into formats that can be easily rendered into JSON, XML, or other content types.

The project uses Django, a high-level Python Web framework that encourages rapid development and clean, pragmatic
design. It follows the model-view-controller architectural pattern. It is maintained by the Django Software Foundation,
an independent organization established as a 501(c)(3) non-profit.

The project also uses Django Rest Framework, a powerful and flexible toolkit for building Web APIs. It provides features
such as authentication policies, serialization, view sets, routers, etc.

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other
method with the owners of this repository before making a change.

[//]: # (## License)

[//]: # ()

[//]: # (This project is licensed under the MIT License - see the LICENSE.md file for details.)