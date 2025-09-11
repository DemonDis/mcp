FROM node:20-slim

WORKDIR /app
RUN npm install -g @modelcontextprotocol/server-filesystem

ENTRYPOINT ["mcp-server-filesystem"]