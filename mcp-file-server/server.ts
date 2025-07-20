import { McpServer } from "@modelcontextprotocol/sdk/server/mcp";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse";
import express from "express";
import { z } from "zod";
import * as fs from "fs/promises";
import * as path from "path";

const server = new McpServer({
  name: "Local File Access MCP Server",
  version: "1.0.0",
});

// Tool to read file contents
server.tool("readFile", { 
  filePath: z.string().describe("Path to the file to read")
}, async ({ filePath }) => {
  try {
    const resolvedPath = path.resolve(filePath);
    const content = await fs.readFile(resolvedPath, 'utf8');
    return {
      content: [
        { type: "text", text: `File content from ${filePath}:\n\n${content}` },
      ],
    };
  } catch (error) {
    return {
      content: [
        { type: "text", text: `Error reading file ${filePath}: ${error instanceof Error ? error.message : 'Unknown error'}` },
      ],
    };
  }
});

// Tool to list directory contents
server.tool("listDirectory", { 
  dirPath: z.string().describe("Path to the directory to list")
}, async ({ dirPath }) => {
  try {
    const resolvedPath = path.resolve(dirPath);
    const items = await fs.readdir(resolvedPath, { withFileTypes: true });
    const fileList = items.map(item => {
      const type = item.isDirectory() ? 'DIR' : 'FILE';
      return `${type}: ${item.name}`;
    }).join('\n');
    
    return {
      content: [
        { type: "text", text: `Contents of ${dirPath}:\n\n${fileList}` },
      ],
    };
  } catch (error) {
    return {
      content: [
        { type: "text", text: `Error listing directory ${dirPath}: ${error instanceof Error ? error.message : 'Unknown error'}` },
      ],
    };
  }
});

// Tool to write file contents
server.tool("writeFile", { 
  filePath: z.string().describe("Path to the file to write"),
  content: z.string().describe("Content to write to the file")
}, async ({ filePath, content }) => {
  try {
    const resolvedPath = path.resolve(filePath);
    await fs.writeFile(resolvedPath, content, 'utf8');
    return {
      content: [
        { type: "text", text: `Successfully wrote content to ${filePath}` },
      ],
    };
  } catch (error) {
    return {
      content: [
        { type: "text", text: `Error writing file ${filePath}: ${error instanceof Error ? error.message : 'Unknown error'}` },
      ],
    };
  }
});

// Tool to get file/directory info
server.tool("getFileInfo", { 
  filePath: z.string().describe("Path to the file or directory to get info about")
}, async ({ filePath }) => {
  try {
    const resolvedPath = path.resolve(filePath);
    const stats = await fs.stat(resolvedPath);
    const info = {
      path: resolvedPath,
      size: stats.size,
      isFile: stats.isFile(),
      isDirectory: stats.isDirectory(),
      modified: stats.mtime.toISOString(),
      created: stats.birthtime.toISOString()
    };
    
    return {
      content: [
        { type: "text", text: `File info for ${filePath}:\n${JSON.stringify(info, null, 2)}` },
      ],
    };
  } catch (error) {
    return {
      content: [
        { type: "text", text: `Error getting file info for ${filePath}: ${error instanceof Error ? error.message : 'Unknown error'}` },
      ],
    };
  }
});

const app = express();
app.use(express.json());

let transport: SSEServerTransport | null = null;

app.get("/sse", (req, res) => {
  transport = new SSEServerTransport("/messages", res);
  server.connect(transport);
});

app.post("/messages", (req, res) => {
  if (transport) {
    transport.handlePostMessage(req, res);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`MCP File Server is running on http://localhost:${PORT}/sse`);
  console.log("Available tools:");
  console.log("- readFile: Read contents of a file");
  console.log("- listDirectory: List contents of a directory");
  console.log("- writeFile: Write content to a file");
  console.log("- getFileInfo: Get information about a file or directory");
});