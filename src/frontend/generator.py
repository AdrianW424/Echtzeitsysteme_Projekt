from io import BytesIO
from PIL import Image

def next_frame():
    # Create a 100x100 PNG image with a red background
    image = Image.new('RGB', (100, 100), color='red')

    # Save the image to a byte buffer as PNG
    buffer = BytesIO()
    image.save(buffer, format='PNG')

    # Return the byte buffer as a byte array
    return buffer.getvalue()

def prev_frame():
    # Create a 100x100 PNG image with a red background
    image = Image.new('RGB', (100, 100), color='red')

    # Save the image to a byte buffer as PNG
    buffer = BytesIO()
    image.save(buffer, format='PNG')

    # Return the byte buffer as a byte array
    return buffer.getvalue()