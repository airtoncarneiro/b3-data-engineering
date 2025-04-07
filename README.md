# b3_utils/README.md

# B3 Utils

B3 Utils is a Python package designed to facilitate the downloading, saving, and extraction of ZIP files from specified URLs. This project adheres to best practices and the Single Responsibility Principle by organizing its functionality into distinct modules.

## Project Structure

```
b3_utils
├── src
│   ├── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── logging_config.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── downloader.py
│   │   ├── file_handler.py
│   │   └── zip_extractor.py
│   └── utils
│       ├── __init__.py
│       └── error_handlers.py
├── tests
│   ├── __init__.py
│   └── test_services
│       ├── __init__.py
│       ├── test_downloader.py
│       ├── test_file_handler.py
│       └── test_zip_extractor.py
├── README.md
├── requirements.txt
└── setup.py
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

1. **Download ZIP File**: Use the `Downloader` class from the `services.downloader` module to download ZIP files.
2. **Save File**: Use the `FileHandler` class from the `services.file_handler` module to save files to disk.
3. **Extract ZIP File**: Use the `ZipExtractor` class from the `services.zip_extractor` module to extract files from a ZIP archive.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.