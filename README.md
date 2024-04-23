# Job Search CRM

## Description

Job Search CRM is a web application designed to help job seekers manage their application process efficiently. It allows users to track job applications, interactions with potential employers, follow-up tasks, and application statuses, all in one centralized location.

## Technologies

- **Frontend:** React
- **Backend:** Python with Flask
- **Database:** SQL (SQLite for development, PostgreSQL for production)
- **Hosting:** AWS (EC2, RDS)

## Features

- Manage contacts and interactions with companies
- Track job application status and history
- Set reminders for application follow-ups and deadlines
- Keep notes for each job application
- User authentication to manage personal data securely

## Setup

### Prerequisites

- Node.js and npm
- Python 3.x
- pip and virtualenv
- AWS Account

### Clone the repository

```bash
git clone https://github.com/jbarneyVBFD/Job_Search_CRM.git
cd Job_Search_CRM
```

### Backend Setup

1. Set up a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

2. Initialize the database:

```bash
flask db upgrade
```

3. Start the backend server:

```bash
flask run
```

### Frontend Setup

1. Install npm packages:

```bash
cd frontend
npm install
```

2. Start the React development server:

```bash
npm start
```

The React application will be available at http://localhost:3000, and the Flask server will be running on http://localhost:5000.

## Deployment

### AWS Configuration

- **EC2 for Flask Backend:**
  - Create an EC2 instance.
  - Deploy your Flask application to the EC2 instance.
  - Ensure security groups allow traffic on port 5000.

- **RDS for PostgreSQL:**
  - Set up an RDS instance for PostgreSQL.
  - Configure your Flask application to connect to the RDS instance.

- **S3 for React Frontend:**
  - Build your React application with `npm run build`.
  - Configure an S3 bucket for website hosting.
  - Upload the build files to the S3 bucket and set up the bucket policy for public access.

- **Environment Variables**
  - Set up environment variables for your production settings, such as database URLs, secret keys, and other necessary configurations.

## Contributing

Contributions to the Job Search CRM are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.