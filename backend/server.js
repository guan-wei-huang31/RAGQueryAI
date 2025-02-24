const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// 🛠️ 修正 `/ask` 只處理 POST 請求
app.post("/ask", async (req, res) => {
    try {
        console.log("Received request:", req.body);  // ✅ Debug
        const response = await axios.post("http://localhost:5001/ask", req.body);
        res.json(response.data);
    } catch (error) {
        console.error("Error:", error);  // ✅ Debug
        res.status(500).json({ error: "Python RAG API error", details: error.message });
    }
});

// 🛠️ 讓 `/` 顯示 API 狀態，避免 `Cannot GET /`
app.get("/", (req, res) => {
    res.send("Express.js API is running...");
});

// 啟動 Express 伺服器
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
