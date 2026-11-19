import { createServer } from "./app.js";

const port = Number.parseInt(process.env.PORT ?? "3000", 10);
const server = createServer();

server.listen(port, "0.0.0.0", () => {
  console.log(`MTS Node demo listening on ${port}`);
});

