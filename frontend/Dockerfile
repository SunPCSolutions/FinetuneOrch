# Use an official Node runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application's code
COPY . .

# Declare the build arguments
ARG VITE_LLAMA_FACTORY_URL
ARG VITE_EASY_DATASET_URL
ARG VITE_TENSORBOARD_URL

# Set the build arguments as environment variables
ENV VITE_LLAMA_FACTORY_URL=$VITE_LLAMA_FACTORY_URL
ENV VITE_EASY_DATASET_URL=$VITE_EASY_DATASET_URL
ENV VITE_TENSORBOARD_URL=$VITE_TENSORBOARD_URL

# Build the React app for production
RUN npm run build

# Install a simple static server
RUN npm install -g serve

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Serve the built static files from the 'dist' directory
CMD ["serve", "-s", "dist", "-l", "3000"]