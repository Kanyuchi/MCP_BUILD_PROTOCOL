# PDF Analysis MCP Server - Setup Guide

## Prerequisites

1. **Python 3.8+** installed on your system
2. **spaCy English model** for NLP processing
3. **Claude Desktop** or **Cursor** for MCP integration

## Installation Steps

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd /mnt/c/Users/kutsanzira/OneDrive - Duisburg Business & Innovation GmbH/Desktop/Mcp_Build_Protocol/pdf_analysis_mcp

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_sm
```

### 2. Initialize the Database

The database will be automatically initialized when you first run the server. However, you can test the setup by running:

```bash
python -c "from database import DatabaseManager; db = DatabaseManager(); print('Database initialized successfully')"
```

### 3. Configure Claude Desktop

1. Locate your Claude Desktop configuration file:
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the PDF Analysis MCP server configuration:

```json
{
  "mcpServers": {
    "pdf-analysis": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/mnt/c/Users/kutsanzira/OneDrive - Duisburg Business & Innovation GmbH/Desktop/Mcp_Build_Protocol/pdf_analysis_mcp",
      "env": {
        "PYTHONPATH": "/mnt/c/Users/kutsanzira/OneDrive - Duisburg Business & Innovation GmbH/Desktop/Mcp_Build_Protocol/pdf_analysis_mcp"
      }
    }
  }
}
```

3. Restart Claude Desktop

### 4. Configure Cursor (Optional)

1. Open Cursor settings
2. Navigate to Extensions or MCP Servers section
3. Add a new MCP server with the configuration from `cursor_config.json`
4. Restart Cursor

## Testing the Setup

### 1. Test Server Directly

```bash
python server.py
```

The server should start without errors. Use Ctrl+C to stop.

### 2. Test with Sample PDF

1. Place a sample PDF file in a test directory
2. Open Claude Desktop
3. Try using the MCP tools:

```
Please analyze this PDF file: /path/to/your/sample.pdf using the analyze_pdf tool.
```

### 3. Test Directory Analysis

```
Please analyze all PDFs in this directory: /path/to/your/pdf/directory using the analyze_directory tool.
```

## Available Tools

Once configured, you'll have access to these tools in Claude Desktop/Cursor:

- **analyze_pdf**: Analyze a single PDF file
- **analyze_directory**: Analyze all PDFs in a directory
- **find_relationships**: Find relationships between claims
- **search_claims**: Search for specific claims
- **get_document_summary**: Get document summary
- **generate_literature_review**: Generate literature review
- **export_analysis**: Export results to various formats
- **get_statistics**: Get analysis statistics
- **list_documents**: List all analyzed documents
- **delete_document**: Delete a document and its data

## Configuration Options

You can customize the behavior by modifying `config.py`:

- **MAX_PDF_SIZE_MB**: Maximum PDF file size (default: 100MB)
- **BATCH_SIZE**: Maximum PDFs to process in batch (default: 10)
- **SIMILARITY_THRESHOLD**: Minimum similarity for relationships (default: 0.7)
- **CLAIM_PATTERNS**: Regex patterns for claim extraction
- **EXPORT_FORMATS**: Supported export formats

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed
2. **spaCy model not found**: Run `python -m spacy download en_core_web_sm`
3. **Database errors**: Check that the data directory has write permissions
4. **PDF processing errors**: Verify PDF files are not corrupted or password-protected

### Debug Mode

Enable debug logging by setting the environment variable:

```bash
export PYTHONPATH="/mnt/c/Users/kutsanzira/OneDrive - Duisburg Business & Innovation GmbH/Desktop/Mcp_Build_Protocol/pdf_analysis_mcp"
export LOG_LEVEL=DEBUG
python server.py
```

### Support

For issues or questions:
1. Check the logs in the console output
2. Verify your configuration matches the setup guide
3. Ensure all file paths are correct and accessible
4. Test with a simple PDF file first

## Data Storage

- **Database**: SQLite database stored in `./data/pdf_analysis.db`
- **Cache**: Temporary files in `./cache/`
- **Exports**: Generated exports in `./exports/`

All data is stored locally for complete privacy.

## Security Notes

- All PDF processing happens locally
- No data is sent to external services
- Database is stored locally with no external connections
- Ensure proper file permissions on sensitive documents