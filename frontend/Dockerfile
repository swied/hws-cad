# frontend/Dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json
COPY package.json .

# Install Node dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the React development server port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]