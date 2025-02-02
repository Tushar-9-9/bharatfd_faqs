# FAQ System with Multi-language Support

## Overview
This project implements a FAQ system where the FAQs are stored with multi-language translations for Hindi and Bengali. The system supports WYSIWYG content using CKEditor and dynamic translation using Google Translate API.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Tushar-9-9/bharatfd_faqs.git
   ```
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate  # For Windows
   source venv/bin/activate  # For macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python manage.py migrate
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

## API Usage

To fetch the FAQ question in a specific language, append the `lang` query parameter to the URL.

- For English (default):
  ```
  GET /api/faqs/
  ```
- For Hindi:
  ```
  GET /api/faqs/?lang=hi
  ```
- For Bengali:
  ```
  GET /api/faqs/?lang=bn
  ```

## Contribution Guidelines

- Fork the repository and create a new branch.
- Write tests for any new functionality.
- Follow the coding standards outlined in PEP8.
- Use conventional commit messages:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation updates

## License
This project is licensed under the MIT License.
