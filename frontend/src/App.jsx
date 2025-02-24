import React, { useState } from "react";
import axios from "axios";

function App() {
    const [question, setQuestion] = useState("");
    const [response, setResponse] = useState(null);

    const askQuestion = async () => {
        if (!question) return alert("Please enter a question!");

        setResponse("Thinking...");

        try {
            const res = await axios.post("http://localhost:5000/ask", { question });
            setResponse(res.data.answer);
        } catch (error) {
            setResponse("Error: Unable to process your request.");
        }
    };

    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center", 
          justifyContent: "center",  
          minHeight: "100vh",
          width: "100%",
          textAlign: "center",
          backgroundColor: "#222",  
          color: "white", 
        }}
      >
            <h1>AI Product Assistant</h1>
            <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask about a product..."
                style={{
                    width: "60%",
                    padding: "10px",
                    marginBottom: "10px",
                    borderRadius: "5px",
                    border: "1px solid #ccc",
                    fontSize: "16px",
                }}
            />
            <button
                onClick={askQuestion}
                style={{
                    padding: "10px 20px",
                    marginLeft: "10px",
                    cursor: "pointer",
                    backgroundColor: "#007bff",
                    color: "white",
                    border: "none",
                    borderRadius: "5px",
                    fontSize: "16px",
                }}
            >
                Ask
            </button>
            <div
                style={{
                    marginTop: "20px",
                    padding: "10px",
                    background: "#f1f1f1",
                    borderRadius: "5px",
                    minHeight: "50px",
                    width: "800px",
                    maxWidth: "800px",
                    color: "#333",
                    fontSize: "18px",
                    marginLeft: "auto",
                    marginRight: "auto"
                }}
            >
                <strong>Response:</strong>
                <p>{response}</p>
            </div>
        </div>
    );
}

export default App;
