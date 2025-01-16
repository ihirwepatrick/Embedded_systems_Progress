const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Hello World");
});
// making IoT requests

app.listen(3000, '10.11.75.77', () => {
  console.log("Server is running on port 3000");
});

