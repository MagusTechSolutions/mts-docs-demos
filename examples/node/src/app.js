import http from "node:http";

export function createServer() {
  return http.createServer((request, response) => {
    response.setHeader("Content-Type", "application/json");

    if (request.url === "/health") {
      response.end(JSON.stringify({ status: "ok" }));
      return;
    }

    response.end(JSON.stringify({ message: "Hello from MTS Node.js" }));
  });
}

