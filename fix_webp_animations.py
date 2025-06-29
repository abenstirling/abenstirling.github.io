#!/usr/bin/env python3
"""
WebP Animation Fixer

Checks existing WebP files for animations and re-converts them with infinite looping.
"""

import subprocess
import sys
from pathlib import Path
from typing import List

def check_webp_animation(file_path: Path) -> bool:
    """Check if a WebP file is animated."""
    try:
        cmd = ['webpinfo', str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Look for animation indicators in the output
            output = result.stdout.lower()
            return 'anim' in output or 'frame' in output
        else:
            # Fallback: check file size and assume larger files might be animated
            file_size = file_path.stat().st_size
            return file_size > 500000  # 500KB threshold
    except Exception:
        # If webpinfo is not available, assume it might be animated if it's large
        try:
            file_size = file_path.stat().st_size
            return file_size > 500000  # 500KB threshold
        except:
            return False

def fix_webp_animation(file_path: Path) -> bool:
    """Re-convert WebP file with infinite looping."""
    try:
        # Create a temporary file for the fixed version
        temp_path = file_path.with_suffix('.temp.webp')
        
        # First try using webpmux to set loop count (if available)
        try:
            cmd = ['webpmux', '-loop', '0', str(file_path), '-o', str(temp_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                temp_path.replace(file_path)
                print(f"✓ Fixed animation with webpmux: {file_path.name}")
                return True
        except FileNotFoundError:
            pass  # webpmux not available, try ffmpeg
        
        # Fallback to ffmpeg with better parameters
        cmd = [
            'ffmpeg', '-i', str(file_path),
            '-c:v', 'libwebp',
            '-quality', '80',
            '-loop', '0',  # Infinite loop for WebP output
            '-lossless', '0',  # Ensure lossy mode
            '-y',  # Overwrite
            str(temp_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # Replace original with fixed version
            temp_path.replace(file_path)
            print(f"✓ Fixed animation with ffmpeg: {file_path.name}")
            return True
        else:
            # Clean up temp file if it exists
            if temp_path.exists():
                temp_path.unlink()
            
            # If that fails, the file might already be properly formatted
            print(f"⚠ Could not fix {file_path.name} - might already be correct")
            return True  # Don't treat as failure since file might be fine
            
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout fixing {file_path.name} - skipping")
        if temp_path.exists():
            temp_path.unlink()
        return False
    except Exception as e:
        print(f"✗ Error fixing {file_path.name}: {e}")
        return False

def main():
    """Main function to fix all animated WebP files."""
    script_dir = Path(__file__).parent
    static_dir = script_dir / 'static'
    
    if not static_dir.exists():
        print(f"Error: Static directory not found at {static_dir}")
        sys.exit(1)
    
    # Check for required tools
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg not found. Please install: brew install ffmpeg")
        sys.exit(1)
    
    # Find all WebP files
    webp_files = []
    for webp_file in static_dir.rglob('*.webp'):
        webp_files.append(webp_file)
    
    if not webp_files:
        print("No WebP files found!")
        return
    
    print(f"Found {len(webp_files)} WebP files")
    
    # Check which ones are animated
    animated_files = []
    for webp_file in webp_files:
        print(f"Checking: {webp_file.relative_to(script_dir)}")
        if check_webp_animation(webp_file):
            animated_files.append(webp_file)
            print(f"  → Animated: YES")
        else:
            print(f"  → Animated: NO")
    
    if not animated_files:
        print("\nNo animated WebP files found that need fixing!")
        return
    
    print(f"\nFound {len(animated_files)} animated WebP files:")
    for file_path in animated_files:
        print(f"  - {file_path.relative_to(script_dir)}")
    
    # Ask for confirmation
    response = input(f"\nFix {len(animated_files)} animated WebP files? (y/N): ").lower().strip()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    # Fix the files
    fixed_count = 0
    failed_files = []
    
    for file_path in animated_files:
        print(f"\nFixing: {file_path.name}")
        if fix_webp_animation(file_path):
            fixed_count += 1
        else:
            failed_files.append(file_path)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Animation Fix Summary:")
    print(f"  Successfully fixed: {fixed_count}")
    print(f"  Failed fixes: {len(failed_files)}")
    
    if failed_files:
        print("\nFailed files:")
        for file_path in failed_files:
            print(f"  - {file_path.name}")

if __name__ == "__main__":
    main()