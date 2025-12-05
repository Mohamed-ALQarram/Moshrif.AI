# URL Fixer

## Overview
Interactive command-line tool to fill missing Telegram URLs in JSON files. This utility scans through JSON files in a directory, identifies entries with empty `telegram_url` fields, and prompts the user to input the correct URLs.

## Purpose
When processing Telegram content, some JSON files may have missing or incomplete `telegram_url` fields. This script provides an efficient way to:
- Identify JSON files with missing URLs
- Interactively collect correct URLs from the user
- Update and save the corrected JSON files
- Maintain data integrity with UTF-8 encoding

## Requirements

### Software Requirements
- **Python**: 3.7 or higher

### Dependencies
- No external packages required (uses Python standard library only)
  - `os` - File system operations
  - `json` - JSON parsing and encoding

## Configuration

### Folder Path
By default, the script looks for JSON files in a folder named `downloaded`:

```python
JSON_FOLDER = "downloaded"   # Change if using a different folder
```

To use a different folder, modify the `JSON_FOLDER` variable in the script.

## Usage

### Basic Usage

1. **Prepare your JSON files**:
   - Place all JSON files in the configured folder (default: `downloaded/`)
   - Ensure each JSON file has a `telegram_url` field (can be empty)

2. **Run the script**:
   ```bash
   python FillMissingURLs.py
   ```

3. **Interactive prompts**:
   - The script will display files with missing URLs
   - Enter the correct URL when prompted
   - Press Enter to confirm each URL

### Example Session

```
[+] Starting URL fixer...

[!] Missing URL in: video_123.json
Enter URL: https://t.me/channel/123

[✔] Updated: video_123.json

[OK] video_456.json already has a URL.

[✔] Done!
```

## JSON File Format

### Expected Structure
Each JSON file should have the following structure:

```json
{
  "filename": "example_video",
  "telegram_url": "",
  "content": "Video transcript..."
}
```

### After Processing
The script will update the file with the provided URL:

```json
{
  "filename": "example_video",
  "telegram_url": "https://t.me/channel/123",
  "content": "Video transcript..."
}
```

## Features

✅ **UTF-8 Support**: Properly handles Arabic and other Unicode characters  
✅ **Non-destructive**: Only updates files with missing URLs  
✅ **Pretty JSON**: Outputs formatted JSON with proper indentation  
✅ **Progress Feedback**: Shows clear status for each file processed  
✅ **Selective Updates**: Skips files that already have URLs

## Error Handling

The script will:
- Skip files that already have a `telegram_url` value
- Preserve all existing JSON fields
- Maintain proper JSON formatting
- Handle file encoding errors gracefully

## Integration with MoshrifAI

This tool is part of the MoshrifAI data processing pipeline:
- **Input**: JSON files exported from Telegram channels
- **Output**: Complete JSON files with valid Telegram URLs
- **Next Step**: Files can be processed by semantic chunker

## Troubleshooting

### File Not Found Error
If you get a "folder not found" error:
- Ensure the `downloaded` folder exists in the same directory as the script
- Or update the `JSON_FOLDER` variable to point to your actual folder

### JSON Decode Error
If a file cannot be parsed:
- Check that the file contains valid JSON
- Ensure proper UTF-8 encoding
- Verify the file is not corrupted

### Permission Errors
If you cannot write to files:
- Check file permissions
- Ensure the folder is not read-only
- Run with appropriate user permissions

## Example Workflow

1. Download content from Telegram → JSON files created
2. Run `FillMissingURLs.py` → URLs added interactively
3. Process with semantic chunker → Content analyzed
4. Build hierarchical index → Ready for retrieval

## Notes

> [!IMPORTANT]
> - Always backup your JSON files before running bulk updates
> - The script modifies files in-place
> - Empty URL fields (`""`) trigger the prompt, `null` or missing fields may cause errors

> [!TIP]
> For batch processing, consider modifying the script to read URLs from a CSV file instead of interactive input
