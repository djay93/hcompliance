# HMDA Automation

An enterprise-grade HMDA automation tool.

## Features

- GUI interface
- Logging for better traceability
- Error handling and user feedback
- Event tracking and display

## Installation

1. Ensure you have Python 3.9+ and Poetry installed.
2. Clone this repository.
3. Run `poetry install` to install dependencies.

## Usage

1. Run `poetry run python hmda/main.py` to start the application.
2. Select the Excel file containing replacement instructions.
3. Select the JSON configuration file.
4. Click "Replace Files" to start the process.
5. View the Event Log to track HMDA file processing events.

## Development

- Run tests: `poetry run pytest`
- Check code style: `poetry run black . && poetry run isort .`
- Run type checking: `poetry run mypy .`

## License

This project is licensed under the MIT License.
