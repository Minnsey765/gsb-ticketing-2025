FROM python:3.13-alpine3.20

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

# Set the working directory
WORKDIR /app
# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Collect static files for Django (if needed)
RUN python manage.py collectstatic --noinput

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Start Gunicorn to serve the Django app on the specified port
CMD ["sh", "./boot.sh"]