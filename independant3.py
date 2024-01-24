from PIL import Image, ImageDraw
import os
# Define the size of a standard card in pixels (assuming 300 dpi)
card_width = int(2.5 * 300)
card_height = int(3.5 * 300)

# Define the size of an A4 sheet in pixels (assuming 300 dpi)
sheet_width = int(8.3 * 300)
sheet_height = int(11.7 * 300)

# Calculate the number of cards per row and per column
cards_per_row = 3
cards_per_column = 3

# Calculate the total margin width and height
total_margin_width = sheet_width - (cards_per_row * card_width)
total_margin_height = sheet_height - (cards_per_column * card_height)

# Calculate the margin between cards and the edge of the sheet
margin_x = total_margin_width // (cards_per_row + 1)
margin_y = total_margin_height // (cards_per_column + 1)

# List of your image files
file_names = os.listdir('croped_cards')
image_files = [os.path.relpath(os.path.join('croped_cards', file), '.') for file in file_names]

# Create groups of 9 images each
groups = [image_files[i:i+9] for i in range(0, len(image_files), 9)]

for i, group in enumerate(groups):
    # Create a new A4 sheet
    sheet = Image.new('RGB', (sheet_width, sheet_height), 'white')
    draw = ImageDraw.Draw(sheet)
    
    for j, image_file in enumerate(group):
        # Open the image file
        img = Image.open(image_file)
        
        # Resize the image to match the size of a standard card
        img = img.resize((card_width, card_height), Image.ANTIALIAS)
        
        # Calculate the position of the card on the sheet
        x = margin_x + (j % cards_per_row) * (card_width + margin_x)
        y = margin_y + (j // cards_per_row) * (card_height + margin_y)
        
        # Paste the card onto the sheet
        sheet.paste(img, (x, y))
        
        # Draw cut marks around the card
        draw.line([(x, y), (x + card_width, y)], fill='black')  # Top edge
        draw.line([(x, y), (x, y + card_height)], fill='black')  # Left edge
        draw.line([(x + card_width, y), (x + card_width, y + card_height)], fill='black')  # Right edge
        draw.line([(x, y + card_height), (x + card_width, y + card_height)], fill='black')  # Bottom edge
    
    # Save the sheet
    sheet.save(f"sheet-test{i+1}.png")