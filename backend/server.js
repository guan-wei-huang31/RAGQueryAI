/**
 * Filename: server.js
 * Author: Guan-Wei Huang
 * Created: 2025-02-24
 * Version: 1.0.0
 * License: MIT
 * Description:
 *     This script sets up an Express.js server that acts as a middleware
 *     between the frontend and the Python RAG API. It handles requests and
 *     forwards them to the Python backend.
 *
 * Contact: gwhuang24@gmail.com
 * GitHub: https://github.com/guan-wei-huang31
 */
 
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

//  Ensure `/ask` only handles POST requests
app.post("/ask", async (req, res) => {
    try {
        console.log("Received request:", req.body);
        const response = await axios.post("http://localhost:5001/ask", req.body);
        res.json(response.data);
    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({ error: "Python RAG API error", details: error.message });
    }
});

//  Root route to display API status, preventing `Cannot GET /` error
app.get("/", (req, res) => {
    res.send("Express.js API is running...");
});

// Start the Express server
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
