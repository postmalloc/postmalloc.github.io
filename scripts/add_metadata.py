#!/usr/bin/env python3
# Add metadata script for Horcrux photo gallery
# This script allows you to add description, camera, and film information to photos

import json
import os
import sys
import argparse
from pathlib import Path

def get_album_path(album_name):
    """Generate the path to the album JSON file from the album name"""
    data_dir = Path('_data/albums')
    for file in data_dir.glob('*.json'):
        if album_name in file.stem:
            return file
    return None

def update_photo_metadata(album_path, photo_filename, description=None, camera=None, film=None):
    """Update metadata for a specific photo in an album"""
    if not album_path.exists():
        print(f"Error: Album file {album_path} not found.")
        return False
    
    # Load the album data
    with open(album_path, 'r') as f:
        album_data = json.load(f)
    
    # Find the photo
    if photo_filename not in album_data['dict']:
        print(f"Error: Photo {photo_filename} not found in album.")
        return False
    
    # Update the photo metadata
    photo_data = album_data['dict'][photo_filename]
    
    if description:
        photo_data['description'] = description
    if camera:
        photo_data['camera'] = camera
    if film:
        photo_data['film'] = film
    
    # Save the updated album data
    with open(album_path, 'w') as f:
        json.dump(album_data, f, indent=2)
    
    print(f"Updated metadata for {photo_filename} in {album_path}")
    return True

def batch_update_album(album_path, camera=None, film=None):
    """Update all photos in an album with the same camera and film info"""
    if not album_path.exists():
        print(f"Error: Album file {album_path} not found.")
        return False
    
    # Load the album data
    with open(album_path, 'r') as f:
        album_data = json.load(f)
    
    # Update all photos
    count = 0
    for photo_name in album_data['dict']:
        photo_data = album_data['dict'][photo_name]
        if photo_data['type'] == 'photo':
            if camera:
                photo_data['camera'] = camera
            if film:
                photo_data['film'] = film
            count += 1
    
    # Save the updated album data
    with open(album_path, 'w') as f:
        json.dump(album_data, f, indent=2)
    
    print(f"Updated {count} photos in {album_path} with camera: {camera}, film: {film}")
    return True

def list_albums():
    """List all available albums"""
    data_dir = Path('_data/albums')
    if not data_dir.exists():
        print("Error: _data/albums directory not found.")
        return
    
    print("Available albums:")
    for file in sorted(data_dir.glob('*.json')):
        print(f"  - {file.stem}")

def list_photos(album_path):
    """List all photos in an album"""
    if not album_path.exists():
        print(f"Error: Album file {album_path} not found.")
        return
    
    # Load the album data
    with open(album_path, 'r') as f:
        album_data = json.load(f)
    
    print(f"Photos in {album_path.stem}:")
    for photo_name in album_data['order']:
        if photo_name in album_data['dict'] and album_data['dict'][photo_name]['type'] == 'photo':
            photo = album_data['dict'][photo_name]
            description = photo.get('description', '')
            camera = photo.get('camera', '')
            film = photo.get('film', '')
            
            metadata = []
            if description:
                metadata.append(f"Description: {description}")
            if camera:
                metadata.append(f"Camera: {camera}")
            if film:
                metadata.append(f"Film: {film}")
                
            metadata_str = " | ".join(metadata)
            if metadata_str:
                print(f"  - {photo_name} ({metadata_str})")
            else:
                print(f"  - {photo_name}")

def main():
    parser = argparse.ArgumentParser(description='Add metadata to photos in Horcrux gallery')
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List albums command
    list_albums_parser = subparsers.add_parser('list-albums', help='List all available albums')
    
    # List photos command
    list_photos_parser = subparsers.add_parser('list-photos', help='List all photos in an album')
    list_photos_parser.add_argument('album', help='Album name')
    
    # Update single photo command
    update_parser = subparsers.add_parser('update', help='Update metadata for a single photo')
    update_parser.add_argument('album', help='Album name')
    update_parser.add_argument('photo', help='Photo filename (e.g., "Photo-1.jpg")')
    update_parser.add_argument('--description', help='Photo description')
    update_parser.add_argument('--camera', help='Camera used')
    update_parser.add_argument('--film', help='Film used')
    
    # Batch update command
    batch_parser = subparsers.add_parser('batch', help='Update all photos in an album with same metadata')
    batch_parser.add_argument('album', help='Album name')
    batch_parser.add_argument('--camera', help='Camera used')
    batch_parser.add_argument('--film', help='Film used')
    
    args = parser.parse_args()
    
    if args.command == 'list-albums':
        list_albums()
    
    elif args.command == 'list-photos':
        album_path = get_album_path(args.album)
        if album_path:
            list_photos(album_path)
        else:
            print(f"Error: Album '{args.album}' not found.")
    
    elif args.command == 'update':
        if not any([args.description, args.camera, args.film]):
            print("Error: At least one of --description, --camera, or --film must be provided.")
            return
        
        album_path = get_album_path(args.album)
        if album_path:
            update_photo_metadata(album_path, args.photo, args.description, args.camera, args.film)
        else:
            print(f"Error: Album '{args.album}' not found.")
    
    elif args.command == 'batch':
        if not any([args.camera, args.film]):
            print("Error: At least one of --camera or --film must be provided.")
            return
        
        album_path = get_album_path(args.album)
        if album_path:
            batch_update_album(album_path, args.camera, args.film)
        else:
            print(f"Error: Album '{args.album}' not found.")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()