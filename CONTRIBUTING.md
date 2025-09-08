# Contributing to FinetuneOrch

We welcome contributions to FinetuneOrch! By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### 1. Fork the Repository

Fork the FinetuneOrch repository to your GitHub account.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/FinetuneOrch.git
cd FinetuneOrch
```

### 3. Create a New Branch

Create a new branch for your feature or bug fix.

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bug-fix-name
```

### 4. Set Up Your Development Environment

Ensure you have Docker and Docker Compose installed. The project is fully containerized.

```bash
# Copy the example environment file
cp .env.example .env

# Build and start all services
docker compose up --build -d
```

The main dashboard will be available at `http://localhost:3000`.

### 5. Make Your Changes

-   Implement your feature or fix the bug.
-   Ensure your code adheres to the project's coding standards.
-   Write clear, concise commit messages.

### 6. Test Your Changes

Before submitting a pull request, thoroughly test your changes to ensure they work as expected and do not introduce new issues.

### 7. Update Documentation

If your changes affect the functionality or usage of the project, please update the relevant documentation (e.g., `README.md`).

### 8. Commit and Push

```bash
git add .
git commit -m "feat: Add your feature description"
# or
git commit -m "fix: Fix your bug description"
git push origin feature/your-feature-name
```

### 9. Create a Pull Request

-   Go to the original FinetuneOrch repository on GitHub.
-   Click on "New pull request" and select your branch.
-   Provide a clear and detailed description of your changes.
-   Reference any related issues.

## Code Style

-   **Python (Backend):** Follow PEP 8 guidelines.
-   **TypeScript/React (Frontend):** Adhere to standard React best practices and TypeScript conventions.
-   **Dockerfiles:** Keep them clean, efficient, and well-commented.

## Reporting Bugs

If you find a bug, please open an issue on GitHub with the following information:

-   A clear and concise description of the bug.
-   Steps to reproduce the behavior.
-   Expected behavior.
-   Screenshots or error messages (if applicable).
-   Your environment details (OS, Docker version, GPU, etc.).

## Feature Requests

We welcome ideas for new features! Please open an issue on GitHub to propose your idea.

Thank you for contributing to FinetuneOrch!