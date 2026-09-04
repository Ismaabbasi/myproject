// src/Chatbot.js
import React, { useState } from "react";
import axios from "axios";

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await axios.post(
        "https://api.openai.com/v1/chat/completions",
        {
          model: "gpt-4",
          messages: [{ role: "user", content: input }],
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer YOUR_OPENAI_API_KEY`,
          },
        }
      );

      const botMessage = response.data.choices[0].message.content;
      setMessages([...newMessages, { sender: "bot", text: botMessage }]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div style={styles.chatbot}>
      <div style={styles.chatbox}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={
              msg.sender === "user" ? styles.userMessage : styles.botMessage
            }
          >
            {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={styles.input}
          placeholder="Type your message..."
        />
        <button type="submit" style={styles.button}>
          Send
        </button>
      </form>
    </div>
  );
};

const styles = {
  chatbot: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    width: "300px",
    height: "400px",
    border: "1px solid #ccc",
    borderRadius: "5px",
    padding: "10px",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)",
  },
  chatbox: {
    flex: 1,
    overflowY: "auto",
    marginBottom: "10px",
  },
  form: {
    display: "flex",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "5px 0 0 5px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px",
    borderRadius: "0 5px 5px 0",
    border: "1px solid #ccc",
    backgroundColor: "#007BFF",
    color: "#fff",
    cursor: "pointer",
  },
  userMessage: {
    textAlign: "right",
    margin: "10px 0",
    padding: "10px",
    backgroundColor: "#DCF8C6",
    borderRadius: "5px",
  },
  botMessage: {
    textAlign: "left",
    margin: "10px 0",
    padding: "10px",
    backgroundColor: "#F1F0F0",
    borderRadius: "5px",
  },
};

export default ChatBot;
