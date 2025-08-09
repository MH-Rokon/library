<!-- Library Management System -->
This project is a web-based Library Management System built to handle borrowing and returning books. It includes features for managing users, books, authors, and categories.



<!--1------------------- Setup Instructions  -->
To get the project running on your local machine, follow these steps:

Clone the repository from GitHub and navigate into the project directory:
git clone https://github.com/MH-Rokon/library.git
cd library





<!--2 c-------------reate and activate a virtual environment to manage project dependencies: -->
python3 -m venv venv
source venv/bin/activate
Install the required dependencies using pip:





<!-- 3--------------get the all requimended packeage  -->
pip install -r requirements.txt






<!-- 4-------------setup for the env file data -->
Configure environment variables. Create a file named .env in the project root and add your sensitive data, such as a secret key, database connection details, and email credentials for future features:
Ini, TOML
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgresql://user:password@host:port/dbname
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password







<!--5-------------- Apply database migrations to set up the necessary database tables: -->
python manage.py migrate






<!--6 --------------Create a superuser to access the administrative panel:
 -->
python manage.py createsuperuser







<!--7--------------- Run the development server to see the application in action: -->
python manage.py runserver













<!-- How Borrowing and Return Logic Works  -->
This section details the core logic for managing book transactions.

<!-- Borrowing Books: -->
 A user can borrow a book only if they have fewer than 3 active borrowings and the book has at least one available copy. When a borrow is created:

The available_copies count of the book is atomically decreased by 1.

The borrow_date is set to the current timestamp.

The due_date is automatically set to 14 days after the borrow_date.
<!-- 
Returning Books:  -->
Users can return books at any time. When a book is returned:

The return_date is recorded.

The book's available_copies count is incremented by 1 atomically.

If the book is returned after the due_date, penalty points are calculated.









<!-- How Penalty Points Are Calculated  -->
Penalty points are awarded for late returns to track a user's borrowing behavior.

Calculation: Penalty points are calculated as 1 point per day late.

Penalty points = Number of days late × 1 point

Purpose: These points accumulate on the user's profile and can be used to restrict future borrowing or for administrative review.






<!-- Assumptions and Known Limitations  -->
The current system operates under the following constraints:

The borrowing limit is strictly 3 active books per user; extensions and renewals are not supported.

The due date is fixed at 14 days and cannot be customized.

Penalty points accumulate indefinitely and require manual administrative intervention to be reset.

Only books with available copies can be borrowed; there is no waitlist or reservation system.

The management of authors, books, and categories is restricted to administrators.

Each book is associated with exactly one category and one author.