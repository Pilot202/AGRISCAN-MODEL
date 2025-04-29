import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# JWT Secret Key
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "defaultsecretkey")  # Replace with a secure secret key

# AWS Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Application Settings
APP_NAME = os.getenv("APP_NAME", "AgroScan")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # 'development' or 'production'

# Email Configuration (for password reset OTP)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
