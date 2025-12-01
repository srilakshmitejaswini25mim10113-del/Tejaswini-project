import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    RoundedModuleDrawer,
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    HorizontalBarsDrawer,
    VerticalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    RadialGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask,
    SquareGradiantColorMask
)
import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import json
from typing import List, Dict, Optional, Union
import csv
from pathlib import Path

def generate_qr_code(
    data: str,
    output_file: str = 'qrcode.png',
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "#000000",
    back_color: str = "#FFFFFF",
    style: str = 'default',
    logo_path: Optional[str] = None,
    size: tuple = (None, None),
    gradient_colors: Optional[List[str]] = None
) -> bool:
    """
    Generate a QR code with the given data and save it to a file.
    
    Args:
        data (str): The data to encode in the QR code (URL, text, etc.)
        output_file (str): Output file name (default: 'qrcode.png')
        box_size (int): Size of each box in pixels (default: 10)
        border (int): Border size in boxes (default: 4)
        fill_color (str): Color of the QR code in hex (default: '#000000')
        back_color (str): Background color in hex (default: '#FFFFFF')
        style (str): Style of QR code ('default', 'rounded', 'circle', 'gapped', 'bars')
        logo_path (str, optional): Path to logo image to embed in QR code
        size (tuple): Target size as (width, height) in pixels (default: auto)
        gradient_colors (list, optional): List of colors for gradient effect
    
    Returns:
        bool: True if generation was successful, False otherwise
    """
    try:
        # Create QR code instance with error correction for logo
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border,
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create an image from the QR Code instance
        if style == 'rounded':
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=RoundedModuleDrawer(),
                fill_color=fill_color,
                back_color=back_color
            )
        elif style == 'circle':
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=CircleModuleDrawer(),
                fill_color=fill_color,
                back_color=back_color
            )
        elif style == 'gapped':
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=GappedSquareModuleDrawer(),
                fill_color=fill_color,
                back_color=back_color
            )
        elif style == 'bars':
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=HorizontalBarsDrawer(),
                fill_color=fill_color,
                back_color=back_color
            )
        elif style == 'gradient' and gradient_colors:
            if len(gradient_colors) == 1:
                fill = gradient_colors[0]
                img = qr.make_image(fill_color=fill, back_color=back_color)
            else:
                if len(gradient_colors) == 2:
                    color_mask = VerticalGradiantColorMask(*gradient_colors)
                else:
                    color_mask = RadialGradiantColorMask(*gradient_colors)
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    color_mask=color_mask
                )
        else:
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Convert to RGB if needed for JPG support
        if output_file.lower().endswith(('.jpg', '.jpeg')):
            img = img.convert('RGB')
        
        # Add logo if provided
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path)
            
            # Calculate logo size (max 30% of QR code size)
            logo_max_size = min(img.size) // 3
            logo.thumbnail((logo_max_size, logo_max_size), Image.LANCZOS)
            
            # Calculate position to center the logo
            position = ((img.size[0] - logo.size[0]) // 2, 
                       (img.size[1] - logo.size[1]) // 2)
            
            # Create a transparent layer for the logo
            logo_mask = Image.new('L', logo.size, 0)
            draw = ImageDraw.Draw(logo_mask)
            draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
            
            # Paste the logo onto the QR code
            img.paste(logo, position, logo_mask)
        
        # Resize if target size is specified
        if all(size):
            img = img.resize(size, Image.LANCZOS)
        
        # Save the image
        img.save(output_file)
        print(f"QR code generated successfully! Saved as {os.path.abspath(output_file)}")
        return True
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return False

def batch_generate_qr_codes(csv_file: str, output_dir: str = 'qrcodes') -> None:
    """Generate multiple QR codes from a CSV file.
    
    CSV format should be: data,output_file,style,fill_color,back_color,logo_path
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_path = os.path.join(output_dir, row.get('output_file', f"qrcode_{row['data'][:10]}.png"))
                generate_qr_code(
                    data=row['data'],
                    output_file=output_path,
                    style=row.get('style', 'default'),
                    fill_color=row.get('fill_color', '#000000'),
                    back_color=row.get('back_color', '#FFFFFF'),
                    logo_path=row.get('logo_path', '')
                )
    except Exception as e:
        print(f"Error in batch generation: {str(e)}")

def get_style_choice() -> dict:
    """Get user input for QR code style."""
    print("\nChoose QR code style:")
    styles = {
        '1': {'name': 'Default', 'value': 'default'},
        '2': {'name': 'Rounded', 'value': 'rounded'},
        '3': {'name': 'Circle', 'value': 'circle'},
        '4': {'name': 'Gapped', 'value': 'gapped'},
        '5': {'name': 'Bars', 'value': 'bars'},
        '6': {'name': 'Gradient', 'value': 'gradient'}
    }
    
    for key, style in styles.items():
        print(f"{key}. {style['name']}")
    
    while True:
        choice = input("Select style (1-6, default: 1): ") or '1'
        if choice in styles:
            return styles[choice]
        print("Invalid choice. Please try again.")

def get_color(prompt: str, default: str = '#000000') -> str:
    """Get a color input from the user."""
    while True:
        color = input(f"{prompt} (e.g., '#RRGGBB' or color name, default: {default}): ") or default
        if color.startswith('#') and len(color) == 7 and all(c in '0123456789ABCDEFabcdef' for c in color[1:]):
            return color
        elif color.lower() in ['black', 'white', 'red', 'green', 'blue', 'yellow', 'purple', 'orange']:
            return color.lower()
        else:
            print("Invalid color format. Please use '#RRGGBB' format or a basic color name.")

def main():
    parser = argparse.ArgumentParser(description='Generate QR codes with advanced options')
    parser.add_argument('--data', type=str, help='Data to encode in QR code')
    parser.add_argument('--output', type=str, default='qrcode.png', help='Output file name (default: qrcode.png)')
    parser.add_argument('--style', type=str, choices=['default', 'rounded', 'circle', 'gapped', 'bars', 'gradient'], 
                       help='QR code style')
    parser.add_argument('--fill', type=str, default='#000000', help='Fill color (default: #000000)')
    parser.add_argument('--back', type=str, default='#FFFFFF', help='Background color (default: #FFFFFF)')
    parser.add_argument('--logo', type=str, help='Path to logo image to embed')
    parser.add_argument('--size', type=str, help='Target size as WxH (e.g., 300x300)')
    parser.add_argument('--batch', type=str, help='Generate multiple QR codes from a CSV file')
    
    # If no arguments, use interactive mode
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        args = parser.parse_args()
        
        if args.batch:
            batch_generate_qr_codes(args.batch)
            return
            
        size = (int(args.size.split('x')[0]), int(args.size.split('x')[1])) if args.size else (None, None)
        
        generate_qr_code(
            data=args.data,
            output_file=args.output,
            style=args.style or 'default',
            fill_color=args.fill,
            back_color=args.back,
            logo_path=args.logo,
            size=size
        )

def interactive_mode():
    print("=== QR Code Generator ===")
    
    while True:
        print("\nOptions:")
        print("1. Generate Single QR Code")
        print("2. Batch Generate QR Codes from CSV")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            data = input("Enter the data to encode (URL, text, etc.): ").strip()
            if not data:
                print("Error: Data cannot be empty!")
                continue
                
            output_file = input("Enter output file name (e.g., qrcode.png, qrcode.jpg, qrcode.svg): ") or 'qrcode.png'
            
            style_info = get_style_choice()
            style = style_info['value']
            
            fill_color = get_color("Enter fill color")
            back_color = get_color("Enter background color", '#FFFFFF')
            
            logo_path = input("Path to logo (press Enter to skip): ").strip()
            if logo_path and not os.path.exists(logo_path):
                print("Logo file not found. Proceeding without logo.")
                logo_path = None
            
            size_input = input("Target size as WxH (e.g., 300x300, press Enter for auto): ").strip()
            size = (int(size_input.split('x')[0]), int(size_input.split('x')[1])) if 'x' in size_input else (None, None)
            
            gradient_colors = None
            if style == 'gradient':
                colors_input = input("Enter gradient colors (comma-separated, e.g., '#FF0000,#00FF00,#0000FF'): ").strip()
                if colors_input:
                    gradient_colors = [c.strip() for c in colors_input.split(',') if c.strip()]
            
            generate_qr_code(
                data=data,
                output_file=output_file,
                style=style,
                fill_color=fill_color,
                back_color=back_color,
                logo_path=logo_path or None,
                size=size,
                gradient_colors=gradient_colors
            )
            
        elif choice == '2':
            csv_file = input("Enter path to CSV file: ").strip()
            if not os.path.exists(csv_file):
                print("Error: CSV file not found!")
                continue
                
            output_dir = input("Enter output directory (default: 'qrcodes'): ").strip() or 'qrcodes'
            batch_generate_qr_codes(csv_file, output_dir)
            
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    import sys
    main()
