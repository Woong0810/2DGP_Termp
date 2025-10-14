from PIL import Image
import os

def extract_frames(image_path, border_colors, background_color):
    """
    Extract frame information from sprite sheet with colored borders
    """
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size

    frames = []
    visited = set()

    # Scan the image for frames
    for y in range(height):
        for x in range(width):
            if (x, y) in visited:
                continue

            pixel = img.getpixel((x, y))

            # Check if this is a border pixel
            if pixel in border_colors:
                # Find the frame bounds
                left = x
                top = y

                # Find right edge of border
                right = left
                while right < width and img.getpixel((right, top)) in border_colors:
                    right += 1

                # Find bottom edge of border
                bottom = top
                while bottom < height and img.getpixel((left, bottom)) in border_colors:
                    bottom += 1

                # Check if we found a valid rectangular border
                if right > left + 2 and bottom > top + 2:
                    # Frame content is inside the border
                    frame_left = left + 1
                    frame_top = top + 1
                    frame_right = right - 1
                    frame_bottom = bottom - 1

                    # Verify this is actually a frame (not just random lines)
                    if frame_right > frame_left and frame_bottom > frame_top:
                        # Check if bottom-right corner has border
                        if (frame_right < width and frame_bottom < height and
                            img.getpixel((frame_right, frame_bottom)) in border_colors):

                            frame_width = frame_right - frame_left
                            frame_height = frame_bottom - frame_top

                            # Only add frames with reasonable size
                            if frame_width > 0 and frame_height > 0:
                                # Convert to bottom-left origin for pico2d
                                frame_bottom_origin = height - frame_bottom

                                frames.append({
                                    'left': frame_left,
                                    'bottom': frame_bottom_origin,
                                    'width': frame_width,
                                    'height': frame_height
                                })

                                # Mark this area as visited
                                for vy in range(top, bottom):
                                    for vx in range(left, right):
                                        visited.add((vx, vy))

    return frames

def create_transparent_image(image_path, output_path, background_color, border_colors):
    """
    Create a transparent version of the image by replacing background and borders
    """
    img = Image.open(image_path)
    img = img.convert('RGBA')

    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Replace background color with transparent
            if (r, g, b) == background_color:
                pixels[x, y] = (0, 0, 0, 0)
            # Replace border colors with transparent
            elif (r, g, b) in border_colors:
                pixels[x, y] = (0, 0, 0, 0)

    img.save(output_path, 'PNG')
    print(f"Saved transparent image to {output_path}")

def save_frames_to_file(frames, output_path, original_image_name):
    """
    Save frame data to a Python file
    """
    with open(output_path, 'w') as f:
        f.write(f"# Auto-generated frame data for {original_image_name}\n")
        f.write("FRAMES = [\n")
        for frame in frames:
            f.write(f"    {{'left': {frame['left']}, 'bottom': {frame['bottom']}, "
                   f"'width': {frame['width']}, 'height': {frame['height']}}},\n")
        f.write("]\n")
    print(f"Saved {len(frames)} frames to {output_path}")

if __name__ == "__main__":
    # Configuration for Jiraiya sprite
    image_path = "Characters_Jiraiya.png"
    border_colors = [(0, 160, 160), (80, 152, 80)]
    background_color = (0, 255, 255)

    print(f"Processing {image_path}...")
    print(f"Border colors: {border_colors}")
    print(f"Background color: {background_color}")

    # Extract frames
    frames = extract_frames(image_path, border_colors, background_color)
    print(f"Found {len(frames)} frames")

    # Save frame data
    save_frames_to_file(frames, "characters_jiraiya_frames.py", image_path)

    # Create transparent image
    create_transparent_image(image_path, "Characters_Jiraiya_clean.png",
                            background_color, border_colors)

    print("Done!")

