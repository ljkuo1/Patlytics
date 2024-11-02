# Stage 1: Build React app
FROM node:16 as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the React app's source code
COPY frontend/ .

# Build the React app
RUN npm run build

# Stage 2: Set up Flask environment
FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app source code
COPY backend/ .

# Copy the React build files from the first stage
COPY --from=build /app/dist ./static

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
