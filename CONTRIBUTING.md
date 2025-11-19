# Contributing to MediCart

Thank you for considering contributing to MediCart! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the project
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear title and description
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please provide:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach
- Any relevant examples

### Code Contributions

1. **Fork the Repository**
   ```bash
   git clone <your-fork-url>
   cd Pharmacy_Ecom
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   ```

4. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed
   - Ensure all tests pass

5. **Run Tests**
   ```bash
   python manage.py test
   pytest -v
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```

   Commit message format:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Test:` for test-related changes

7. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Provide a clear description of your changes

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and concise
- Maximum line length: 100 characters

### Django Specific
- Use Django's built-in features when possible
- Follow Django naming conventions
- Use class-based views appropriately
- Properly handle database transactions

### API Design
- Follow RESTful principles
- Use appropriate HTTP methods
- Return meaningful status codes
- Provide clear error messages

### Testing
- Write tests for all new features
- Maintain test coverage above 80%
- Test both success and failure cases
- Use descriptive test names

## Project Structure

```
Pharmacy_Ecom/
├── medicart/          # Project settings
├── pharmacy/          # Main app
│   ├── models.py     # Database models
│   ├── views.py      # Views and APIs
│   ├── serializers.py # DRF serializers
│   ├── urls.py       # URL routing
│   └── tests.py      # Tests
├── templates/         # HTML templates
└── static/           # Static files
```

## Development Workflow

1. Create an issue for the feature/bug
2. Get feedback on your approach
3. Fork and create a branch
4. Implement your changes
5. Write/update tests
6. Update documentation
7. Submit pull request

## Testing Guidelines

### Running Tests
```bash
# All tests
python manage.py test

# Specific test
python manage.py test pharmacy.tests.MedicineModelTest

# With pytest
pytest -v
pytest pharmacy/tests.py::MedicineModelTest
```

### Writing Tests
```python
from django.test import TestCase
from .models import Medicine

class MedicineTest(TestCase):
    def setUp(self):
        # Setup test data
        pass
    
    def test_medicine_creation(self):
        # Test logic
        pass
```

## Documentation

- Update README.md for user-facing changes
- Update API_DOCUMENTATION.md for API changes
- Add inline comments for complex logic
- Update docstrings for modified functions

## Review Process

1. Code review by maintainers
2. Automated tests must pass
3. Documentation must be updated
4. At least one approval required
5. Merge by maintainer

## Questions?

- Create an issue for questions
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing to MediCart! 🎉

