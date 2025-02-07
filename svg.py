from PIL import Image, ImageDraw, ImageFont

def create_round_logo(image_path, output_path, text="My Logo", font_size=40, text_position="below", resize_dim=(200, 200)):
    """
    Convert an image to a PNG logo with a round frame and text in white & bold.
    
    :param image_path: Path to the input image.
    :param output_path: Path to save the final PNG logo.
    :param text: The text to add below or beside the image.
    :param font_size: Font size for the text.
    :param text_position: Position of the text ('beside' or 'below').
    :param resize_dim: Tuple (width, height) to resize the image.
    """
    try:
        # Open the image and convert to RGBA (to handle transparency)
        img = Image.open(image_path).convert("RGBA")
        
        # Resize the image to make it smaller
        img = img.resize(resize_dim, Image.LANCZOS)  # Fix for Pillow 10+

        # Create a circular mask
        mask = Image.new("L", resize_dim, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, resize_dim[0], resize_dim[1]), fill=255)

        # Apply the circular mask to the image
        round_img = Image.new("RGBA", resize_dim, (0, 0, 0, 0))
        round_img.paste(img, (0, 0), mask=mask)

        # Set font (Uses default PIL font if Arial isn't available)
        try:
            font = ImageFont.truetype("arialbd.ttf", font_size)  # Bold font
        except IOError:
            font = ImageFont.load_default()

        # Get text size (Updated for Pillow 10+)
        text_bbox = font.getbbox(text)
        text_width, text_height = text_bbox[2], text_bbox[3]  # Width, Height

        if text_position == "beside":
            # Create a new image (width extended for text)
            new_width = resize_dim[0] + text_width + 20  # Extra space for text
            new_height = max(resize_dim[1], text_height)
            final_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

            # Paste the round image
            final_img.paste(round_img, (0, (new_height - resize_dim[1]) // 2), mask)

            # Draw text beside the image
            draw = ImageDraw.Draw(final_img)
            text_x = resize_dim[0] + 10  # 10px padding from image
            text_y = (new_height - text_height) // 2  # Center vertically
        else:  # Text below
            # Create a new image (height extended for text)
            new_width = max(resize_dim[0], text_width)
            new_height = resize_dim[1] + text_height + 20  # Extra space for text
            final_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

            # Paste the round image
            final_img.paste(round_img, ((new_width - resize_dim[0]) // 2, 0), mask)

            # Draw text below the image
            draw = ImageDraw.Draw(final_img)
            text_x = (new_width - text_width) // 2  # Center horizontally
            text_y = resize_dim[1] + 10  # 10px padding below image

        # Add white text
        draw.text((text_x, text_y), text, fill="white", font=font)

        # Save as PNG
        final_img.save(output_path, format="PNG")

        print(f"✅ Logo saved successfully as '{output_path}'")

    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage
input_image = "me1.jpg"  # Your input image
output_logo = "logo.png"

create_round_logo(input_image, output_logo, text="DREX", font_size=40, text_position="below", resize_dim=(200, 200))