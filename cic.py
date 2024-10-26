import png
import zlib

def save_as_compressed_pd(png_filename, pd_filename):
    # Read the PNG file
    with open(png_filename, 'rb') as f:
        reader = png.Reader(file=f)
        width, height, pixels, metadata = reader.read_flat()
        
        # If the PNG has an alpha channel, ignore it
        pixel_depth = 4 if metadata['alpha'] else 3
        
        # Prepare raw pixel data
        raw_pixel_data = bytearray()
        for row_index in range(height):
            for col_index in range(width):
                start_index = (row_index * width + col_index) * pixel_depth
                raw_pixel_data.extend([
                    pixels[start_index],     # Red
                    pixels[start_index + 1], # Green
                    pixels[start_index + 2]  # Blue
                ])

        # Compress pixel data using zlib
        compressed_pixel_data = zlib.compress(bytes(raw_pixel_data))

        # Write to .pd file with metadata
        with open(pd_filename, 'wb') as pd_file:
            # Write width and height as 4-byte integers
            pd_file.write(width.to_bytes(4, 'big'))
            pd_file.write(height.to_bytes(4, 'big'))
            # Write compressed pixel data
            pd_file.write(compressed_pixel_data)

def convert_compressed_pd_to_png(pd_filename, png_filename):
    try:
        with open(pd_filename, "rb") as f:
            # Read width and height (4 bytes each)
            width = int.from_bytes(f.read(4), 'big')
            height = int.from_bytes(f.read(4), 'big')

            # Read and decompress pixel data
            compressed_pixel_data = f.read()
            decompressed_pixel_data = zlib.decompress(compressed_pixel_data)

            # Validate data size
            if len(decompressed_pixel_data) != width * height * 3:
                raise ValueError("Decompressed data size does not match expected pixel data size.")

            # Convert decompressed data to rows
            pixel_data = []
            for row_index in range(height):
                row = []
                for col_index in range(width):
                    start_index = (row_index * width + col_index) * 3
                    row.extend([
                        decompressed_pixel_data[start_index],     # Red
                        decompressed_pixel_data[start_index + 1], # Green
                        decompressed_pixel_data[start_index + 2]  # Blue
                    ])
                pixel_data.append(row)

        # Save as PNG
        with open(png_filename, "wb") as f:
            writer = png.Writer(width, height, greyscale=False)
            writer.write(f, pixel_data)

    except Exception as e:
        print(f"Error converting to PNG: {e}")

def main():
    print("Select an option:")
    print("1. Save PNG as compressed .pd")
    print("2. Convert compressed .pd to PNG")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        # Save PNG as a compressed .pd file
        png_filename = input("Enter the PNG filename to convert (e.g., 'image.png'): ")
        pd_filename = input("Enter the output .pd filename (e.g., 'output_image.pd'): ")
        save_as_compressed_pd(png_filename, pd_filename)
        print(f"PNG saved as compressed .pd file: {pd_filename}")

    elif choice == '2':
        # Convert a compressed .pd file to PNG
        pd_filename = input("Enter the .pd filename to convert (e.g., 'image.pd'): ")
        png_filename = input("Enter the output PNG filename (e.g., 'output_image.png'): ")
        convert_compressed_pd_to_png(pd_filename, png_filename)
        print(f"Compressed .pd file converted to PNG: {png_filename}")
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
