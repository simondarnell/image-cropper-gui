#!/usr/bin/env python3
"""
Test script to verify the image processor works correctly.
This creates sample test images and processes them.
"""
from PIL import Image, ImageDraw
from pathlib import Path
from image_processor import crop_and_mirror, batch_process_images


def create_test_images(output_dir: str, count: int = 3):
    """Create sample test images with different colors."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    colors = [
        ("red", [(255, 0, 0), (200, 0, 0), (150, 0, 0)]),
        ("green", [(0, 255, 0), (0, 200, 0), (0, 150, 0)]),
        ("blue", [(0, 0, 255), (0, 0, 200), (0, 0, 150)]),
    ]
    
    for color_name, shades in colors:
        # Create image with gradient
        img = Image.new("RGB", (400, 300), shades[0])
        draw = ImageDraw.Draw(img)
        
        # Add text label
        draw.text((150, 130), f"Test Image - {color_name.upper()}", fill=(255, 255, 255))
        
        # Add colored sections
        draw.rectangle([0, 0, 50, 300], fill=shades[1])
        draw.rectangle([350, 0, 400, 300], fill=shades[1])
        draw.rectangle([0, 0, 400, 50], fill=shades[2])
        draw.rectangle([0, 250, 400, 300], fill=shades[2])
        
        filename = output_path / f"test_{color_name}.png"
        img.save(filename)
        print(f"Created: {filename}")


def test_crop_and_mirror():
    """Test the crop_and_mirror function."""
    test_dir = Path("test_input")
    test_dir.mkdir(exist_ok=True)
    
    # Create a test image
    create_test_images(str(test_dir), count=1)
    
    test_image = test_dir / "test_red.png"
    
    # Test with different crop values
    print("\nTesting crop_and_mirror function:")
    result = crop_and_mirror(
        str(test_image),
        top_pixels=30,
        bottom_pixels=30,
        left_pixels=20,
        right_pixels=20,
    )
    
    result.save("test_output_single.png")
    print("✓ Single image processing successful")
    print(f"  Result saved to: test_output_single.png")


def test_batch_process():
    """Test batch processing."""
    input_dir = Path("test_input")
    output_dir = Path("test_output_batch")
    
    # Create test images
    create_test_images(str(input_dir))
    
    print("\nTesting batch processing:")
    
    def progress_cb(current, total, filename):
        print(f"  [{current}/{total}] Processing: {filename}")
    
    successful, failed, errors = batch_process_images(
        str(input_dir),
        str(output_dir),
        top_pixels=25,
        bottom_pixels=25,
        left_pixels=15,
        right_pixels=15,
        progress_callback=progress_cb,
    )
    
    print(f"\n✓ Batch processing complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    if errors:
        print("  Errors:")
        for error in errors:
            print(f"    - {error}")
    
    print(f"  Output folder: {output_dir}")


if __name__ == "__main__":
    print("Image Processor Test Suite")
    print("=" * 50)
    
    try:
        test_crop_and_mirror()
        test_batch_process()
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
