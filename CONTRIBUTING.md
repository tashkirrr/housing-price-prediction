# Contributing to California House Price Prediction

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/housing-price-prediction.git
   cd housing-price-prediction
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

## 📝 Development Workflow

1. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure:
   - Code follows PEP 8 style guidelines
   - All tests pass
   - New features include tests
   - Documentation is updated

3. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

4. **Check code style**:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## 📋 Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Test additions or modifications
- `chore:` - Build process or auxiliary tool changes

Examples:
```
feat: add XGBoost model support
fix: correct feature scaling in preprocessor
docs: update API documentation
test: add unit tests for data processing
```

## 🧪 Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Use meaningful test names that describe the behavior

## 📚 Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update API documentation for endpoint changes
- Include examples where helpful

## 🐛 Reporting Bugs

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs

## 💡 Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Describe the use case clearly
- Explain why it would be valuable
- Consider contributing the feature yourself!

## 🏆 Recognition

Contributors will be recognized in our README.md file.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

Feel free to open an issue for questions or join discussions!

Thank you for contributing! 🎉
