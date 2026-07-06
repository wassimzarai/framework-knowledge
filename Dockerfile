FROM node:20-slim
WORKDIR /app
CMD ["npx", "-y", "supergateway", "--port", "8001", "--stdio", "npx -y mcp-obsidian /vault"]