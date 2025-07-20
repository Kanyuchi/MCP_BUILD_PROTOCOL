# MCP Server Setup Instructions

## Claude Desktop Configuration

1. **Locate Claude Desktop config file:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Add the configuration:**
   Copy the contents from `claude-desktop-config.json` and merge it into your existing Claude Desktop config file.

3. **Restart Claude Desktop** for changes to take effect.

## Cursor IDE Configuration

1. **Open Cursor IDE settings:**
   - Go to File → Preferences → Settings
   - Search for "MCP" or "Model Context Protocol"

2. **Add MCP server configuration:**
   Use the settings from `cursor-config.json` or manually configure:
   - Server name: `file-server`
   - Command: `node`
   - Args: Path to tsx and server.ts (as shown in cursor-config.json)

3. **Restart Cursor IDE** for changes to take effect.

## Alternative: Use HTTP Transport

If the command-based setup doesn't work, you can use the HTTP transport:

1. **Start the server:**
   ```bash
   cd mcp-file-server
   npm start
   ```

2. **Connect via HTTP:**
   - URL: `http://localhost:3000/sse`
   - Use this URL in your MCP client configuration

## Testing the Connection

Once configured, test by asking Claude Desktop or Cursor to:
- List files in a directory
- Read a file's contents  
- Get file information

Example prompts:
- "List the files in my Desktop folder"
- "Read the contents of my README.md file"
- "What files are in the current directory?"

## Troubleshooting

- Ensure Node.js is installed and accessible
- Check that the file paths in the config are correct
- Verify the server is running on port 3000
- Check client logs for connection errors