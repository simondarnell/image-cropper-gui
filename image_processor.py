"""Image processing module for crop and mirror operations."""
try:
    from PIL import Image
except ImportError as e:
    raise ImportError("Pillow library is required; install it with: pip install pillow") from e
from pathlib import Path


def crop_and_mirror(
    image_path: str,
    top_pixels: int = 0,
    bottom_pixels: int = 0,
    left_pixels: int = 0,
    right_pixels: int = 0,
) -> Image.Image:
    """
    Crop specified pixels from sides and mirror them to opposite sides.
    
    Args:
        image_path: Path to the image file
        top_pixels: Pixels to crop from top and mirror to bottom
        bottom_pixels: Pixels to crop from bottom and mirror to top
        left_pixels: Pixels to crop from left and mirror to right
        right_pixels: Pixels to crop from right and mirror to left
    
    Returns:
        Modified PIL Image object
    """
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    
    # Validate inputs
    top_pixels = max(0, min(top_pixels, height // 2))
    bottom_pixels = max(0, min(bottom_pixels, height // 2))
    left_pixels = max(0, min(left_pixels, width // 2))
    right_pixels = max(0, min(right_pixels, width // 2))
    
    # Crop from each side and mirror to opposite
    result = img.copy()
    
    # Handle top -> bottom mirroring
    if top_pixels > 0:
        top_section = img.crop((0, 0, width, top_pixels))
        result.paste(top_section, (0, height - top_pixels))
    
    # Handle bottom -> top mirroring
    if bottom_pixels > 0:
        bottom_section = img.crop((0, height - bottom_pixels, width, height))
        result.paste(bottom_section, (0, 0))
    
    # Handle left -> right mirroring
    if left_pixels > 0:
        left_section = img.crop((0, 0, left_pixels, height))
        result.paste(left_section, (width - left_pixels, 0))
    
    # Handle right -> left mirroring
    if right_pixels > 0:
        right_section = img.crop((width - right_pixels, 0, width, height))
        result.paste(right_section, (0, 0))
    
    return result


def batch_process_images(
    input_folder: str,
    output_folder: str,
    top_pixels: int = 0,
    bottom_pixels: int = 0,
    left_pixels: int = 0,
    right_pixels: int = 0,
    extensions: list = None,
    progress_callback=None,
) -> tuple:
    """
    Batch process all images in a folder.
    
    Args:
        input_folder: Path to input folder containing images
        output_folder: Path to output folder for processed images
        top_pixels: Pixels to crop from top
        bottom_pixels: Pixels to crop from bottom
        left_pixels: Pixels to crop from left
        right_pixels: Pixels to crop from right
        extensions: List of file extensions to process (default: common image formats)
        progress_callback: Optional callback function(current, total, filename)
    
    Returns:
        Tuple of (successful_count, failed_count, error_messages)
    """
    if extensions is None:
        extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]
    
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all matching image files
    image_files = []
    for ext in extensions:
        image_files.extend(input_path.glob(f"*{ext}"))
        image_files.extend(input_path.glob(f"*{ext.upper()}"))
    
    image_files = sorted(set(image_files))  # Remove duplicates and sort
    
    successful = 0
    failed = 0
    errors = []
    
    for idx, image_file in enumerate(image_files, 1):
        try:
            if progress_callback:
                progress_callback(idx, len(image_files), image_file.name)
            
            # Process the image
            processed = crop_and_mirror(
                str(image_file),
                top_pixels=top_pixels,
                bottom_pixels=bottom_pixels,
                left_pixels=left_pixels,
                right_pixels=right_pixels,
            )
            
            # Save with original filename
            output_file = output_path / image_file.name
            processed.save(output_file, quality=95)
            successful += 1
        except Exception as e:
            failed += 1
            error_msg = f"{image_file.name}: {str(e)}"
            errors.append(error_msg)
    
    return successful, failed, errors
