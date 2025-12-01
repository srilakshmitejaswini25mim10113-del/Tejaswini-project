# QR Code Generator

A powerful and feature-rich QR code generator built with Python. Create beautiful, customizable QR codes with advanced styling options.

## Features

- **Multiple QR Code Styles**:
  - Default
  - Rounded corners
  - Circular modules
  - Gapped squares
  - Horizontal/Vertical bars
  - Gradient colors
- **Customization Options**:
  - Custom colors (fill and background)
  - Logo embedding
  - Custom size output
  - Multiple output formats (PNG, JPG, SVG)
  - Gradient color support
- **Batch Processing**:
  - Generate multiple QR codes from a CSV file
  - Custom naming and styling for each code
- **User-Friendly**:
  - Interactive command-line interface
  - Command-line arguments support
  - Detailed error messages

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the files to your local machine.

2. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

## Installation

1. Clone this repository or download the files to your local machine.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Interactive Mode

1. Run the QR code generator:
   ```
   python qr_generator.py
   ```

2. Choose an option:
   - **Generate Single QR Code**: Create a single QR code with custom options
   - **Batch Generate QR Codes**: Create multiple QR codes from a CSV file
   - **Exit**: Close the program

### Command Line Mode

Generate a single QR code:
```bash
python qr_generator.py --data "https://example.com" --output qrcode.png --style rounded --fill "#FF5733" --back "#FFFFFF" --logo logo.png --size 300x300
```

Generate multiple QR codes from a CSV file:
```bash
python qr_generator.py --batch input.csv
```

### CSV Format for Batch Processing
Create a CSV file with the following columns:
- `data`: The data to encode in the QR code (required)
- `output_file`: Output filename (default: auto-generated)
- `style`: Style of QR code (default: 'default')
- `fill_color`: Fill color in hex (default: '#000000')
- `back_color`: Background color in hex (default: '#FFFFFF')
- `logo_path`: Path to logo image (optional)

Example CSV:
```csv
data,output_file,style,fill_color,back_color,logo_path
https://example.com,example1.png,rounded,#FF5733,#FFFFFF,logo.png
https://google.com,google_qr.png,circle,#4285F4,#FFFFFF,
```

## Examples

### Generate a QR code with a logo
```bash
python qr_generator.py --data "https://example.com" --output with_logo.png --logo your_logo.png
```

### Create a gradient QR code
```bash
python qr_generator.py --data "Gradient QR" --output gradient.png --style gradient --fill "#FF0000,#00FF00,#0000FF"
```

### Batch generate QR codes
1. Create a CSV file `urls.csv`:
   ```csv
   data,output_file,style,fill_color
   https://example.com,example1.png,rounded,#FF5733
   https://google.com,google_qr.png,circle,#4285F4
   ```
2. Run the batch command:
   ```bash
   python qr_generator.py --batch urls.csv
   ```

## Advanced Customization

### Available Styles
- `default`: Standard square modules
- `rounded`: Rounded corner modules
- `circle`: Circular modules
- `gapped`: Gapped square modules
- `bars`: Horizontal bar modules
- `gradient`: Gradient color effect

### Color Formats
- Hex: `#RRGGBB` (e.g., `#FF5733`)
- Color names: `red`, `green`, `blue`, etc.
- Gradient: Comma-separated colors (e.g., `#FF0000,#00FF00,#0000FF`)

## Dependencies

- `qrcode`: For generating QR codes
- `Pillow`: For image processing

## License

This project is open source and available under the [MIT License](LICENSE).
