# Contributing to DevFest Lecce 2025 Backend

Thank you for your interest in contributing to the DevFest Lecce 2025 Backend! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Your environment (OS, Python version, etc.)

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:

1. A clear description of the feature
2. Why you think it would be useful
3. Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Test your changes** thoroughly
   ```bash
   # Run linting
   uv run ruff check --fix
   
   # Run formatting
   uv run ruff format
   
   # Run Django checks
   cd devfest_lecce_2025_be
   uv run python manage.py check
   ```

4. **Commit your changes** with clear, descriptive messages
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** with:
   - A clear title and description
   - Reference to any related issues
   - Screenshots (if applicable)

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use `ruff` for linting and formatting
- Maximum line length: 88 characters (black/ruff default)
- Use type hints where appropriate

### Code Organization

- Keep functions and methods focused on a single responsibility
- Add docstrings to all public functions, classes, and modules
- Use meaningful variable and function names
- Add comments for complex logic

### Django Best Practices

- Use Django ORM instead of raw SQL when possible
- Keep views thin, move business logic to models or services
- Use Django's built-in security features (CSRF, XSS protection, etc.)
- Follow the Django app structure

### Documentation

- Update README.md if you add new features or change setup instructions
- Add docstrings to new functions and classes
- Update API documentation if you change endpoints
- Add inline comments for complex algorithms

### Git Commit Messages

Write clear commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Start with a capital letter
- Keep the first line under 72 characters
- Add a blank line before detailed explanation (if needed)

Example:
```
Add user profile endpoint

- Create UserProfile model
- Add serializer for user profiles
- Implement GET and PUT endpoints
- Add tests for profile operations
```

## Development Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

3. Create a `.env` file based on `.env.example`

4. Run migrations:
   ```bash
   cd devfest_lecce_2025_be
   uv run python manage.py migrate
   ```

5. Start the development server:
   ```bash
   uv run python manage.py runserver
   ```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Aim for good test coverage of your changes

## Security

- Never commit sensitive data (API keys, passwords, etc.)
- Use environment variables for configuration
- Follow OWASP security best practices
- Report security vulnerabilities privately to the maintainers

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Reach out to the maintainers
- Check existing issues and PRs for similar questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be recognized in the project documentation. Thank you for making DevFest Lecce 2025 better!
