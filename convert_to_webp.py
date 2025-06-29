#!/usr/bin/env python3
"""
WebP Converter Script

Automatically converts all media files in the images directory to WebP format.
Handles both images and videos, preserves filenames, and removes originals.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Supported file extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'}
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
ALL_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

def check_dependencies() -> bool:
    """Check if required tools are installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        subprocess.run(['cwebp', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Required tools not found. Please install:")
        print("  - ffmpeg (for video conversion)")
        print("  - webp tools (for image conversion)")
        print("  brew install ffmpeg webp")
        return False

def get_output_path(input_path: Path, script_dir: Path) -> Path:
    """Determine the correct output path based on filename conventions."""
    filename = input_path.stem
    webp_filename = f"{filename}.webp"
    
    # Cover images go to static/images/
    if filename.endswith('_cover'):
        output_dir = script_dir / 'static' / 'images'
    else:
        # All other images go to static/posts/
        output_dir = script_dir / 'static' / 'posts'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir / webp_filename

def get_media_files(directory: Path, script_dir: Path) -> List[tuple[Path, Path]]:
    """Get all media files that need conversion with their output paths."""
    media_files = []
    
    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in ALL_EXTENSIONS:
            output_path = get_output_path(file_path, script_dir)
            # Check if WebP version already exists at the correct location
            if not output_path.exists():
                media_files.append((file_path, output_path))
    
    return media_files

def convert_image_to_webp(input_path: Path, output_path: Path, quality: int = 80) -> bool:
    """Convert image file to WebP using cwebp."""
    try:
        cmd = ['cwebp', '-q', str(quality)]
        
        # Add animation preservation for GIFs
        if input_path.suffix.lower() == '.gif':
            cmd.extend(['-loop', '0'])  # Infinite loop for animations
        
        cmd.extend([str(input_path), '-o', str(output_path)])
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Converted image: {input_path.name} -> {output_path.name}")
            return True
        else:
            print(f"✗ Failed to convert {input_path.name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error converting {input_path.name}: {e}")
        return False

def get_file_size_mb(file_path: Path) -> float:
    """Get file size in MB."""
    return file_path.stat().st_size / (1024 * 1024)

def convert_video_to_webp(input_path: Path, output_path: Path, quality: int = 80) -> bool:
    """Convert video file to WebP using 2-pass conversion: video -> gif -> webp."""
    try:
        file_size_mb = get_file_size_mb(input_path)
        print(f"  Converting {file_size_mb:.1f}MB video file...")
        
        # Always use 2-pass conversion: mov/mp4 -> gif -> webp for better looping
        temp_gif = input_path.parent / f"{input_path.stem}_temp.gif"
        
        # First pass: convert to GIF with compression
        gif_cmd = [
            'ffmpeg', '-y',
            '-i', str(input_path),
            '-vf', 'fps=10,scale=800:-1:flags=lanczos',
            '-loop', '0',
            str(temp_gif)
        ]
        
        gif_result = subprocess.run(gif_cmd, capture_output=True, text=True, timeout=180)
        if gif_result.returncode != 0:
            print(f"✗ Failed to create temp GIF: {gif_result.stderr}")
            return False
        
        # Second pass: convert GIF to WebP
        webp_cmd = [
            'ffmpeg', '-y',
            '-i', str(temp_gif),
            '-c:v', 'libwebp',
            '-lossless', '0',
            '-compression_level', '6',
            '-q:v', str(quality),
            '-loop', '0',
            str(output_path)
        ]
        
        webp_result = subprocess.run(webp_cmd, capture_output=True, text=True, timeout=180)
        
        # Clean up temp file
        try:
            temp_gif.unlink()
        except:
            pass
        
        if webp_result.returncode == 0:
            # Check if output file is larger than 100MB and needs compression
            output_size_mb = get_file_size_mb(output_path)
            if output_size_mb > 100:
                print(f"  Output is {output_size_mb:.1f}MB (>100MB), re-compressing...")
                
                # Re-compress with lower quality
                compress_cmd = [
                    'ffmpeg', '-y',
                    '-i', str(temp_gif) if temp_gif.exists() else str(input_path),
                    '-c:v', 'libwebp',
                    '-lossless', '0',
                    '-compression_level', '6',
                    '-q:v', '60',  # Lower quality for compression
                    '-loop', '0',
                    str(output_path)
                ]
                
                compress_result = subprocess.run(compress_cmd, capture_output=True, text=True, timeout=180)
                if compress_result.returncode == 0:
                    final_size_mb = get_file_size_mb(output_path)
                    print(f"✓ Converted video with compression: {input_path.name} -> {output_path.name} ({final_size_mb:.1f}MB)")
                else:
                    print(f"✓ Converted video: {input_path.name} -> {output_path.name} (compression failed, using original)")
            else:
                print(f"✓ Converted video: {input_path.name} -> {output_path.name}")
            return True
        else:
            print(f"✗ Failed to convert video {input_path.name}: {webp_result.stderr}")
            return False
                
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout converting {input_path.name}")
        return False
    except Exception as e:
        print(f"✗ Error converting {input_path.name}: {e}")
        return False

def convert_file(input_path: Path, output_path: Path) -> bool:
    """Convert a single file to WebP format."""
    extension = input_path.suffix.lower()
    
    if extension in IMAGE_EXTENSIONS:
        return convert_image_to_webp(input_path, output_path)
    elif extension in VIDEO_EXTENSIONS:
        return convert_video_to_webp(input_path, output_path)
    else:
        print(f"✗ Unsupported file type: {input_path.name}")
        return False

def main():
    """Main function to process all files in images directory."""
    # Get the images directory
    script_dir = Path(__file__).parent
    images_dir = script_dir / 'images'
    
    if not images_dir.exists():
        print(f"Error: Images directory not found at {images_dir}")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Get all media files that need conversion
    media_files = get_media_files(images_dir, script_dir)
    
    if not media_files:
        print("No media files found that need conversion to WebP!")
        return
    
    print(f"Found {len(media_files)} files to convert:")
    for input_path, output_path in media_files:
        try:
            relative_input = input_path.relative_to(script_dir)
        except ValueError:
            relative_input = input_path
        relative_output = output_path.relative_to(script_dir)
        print(f"  - {relative_input} -> {relative_output}")
    
    # Convert files
    converted_count = 0
    failed_files = []
    
    for input_path, output_path in media_files:
        print(f"\nProcessing: {input_path.name}")
        print(f"  Output: {output_path.relative_to(script_dir)}")
        
        if convert_file(input_path, output_path):
            # Remove original file after successful conversion
            try:
                input_path.unlink()
                print(f"✓ Removed original: {input_path.name}")
                converted_count += 1
            except Exception as e:
                print(f"✗ Failed to remove original {input_path.name}: {e}")
                failed_files.append(input_path)
        else:
            failed_files.append(input_path)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Conversion Summary:")
    print(f"  Successfully converted: {converted_count}")
    print(f"  Failed conversions: {len(failed_files)}")
    
    if failed_files:
        print("\nFailed files:")
        for file_path in failed_files:
            print(f"  - {file_path.name}")
    
    print("\nFile placement rules:")
    print("  - Files ending with '_cover' -> static/images/ (for cover images)")
    print("  - All other files -> static/posts/ (for post content)")

if __name__ == "__main__":
    main()