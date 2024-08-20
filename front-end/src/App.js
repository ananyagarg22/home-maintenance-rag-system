import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

import './App.css';

function App() {
  const initMessage = {
    person: "bot",
    message: "Hi there! I'm here to help you connect with top-rated contractors. How can I assist you today?"
  };

  const [query, setQuery] = useState("");
  const [image, setImage] = useState(null);
  const [chatHistory, setChatHistory] = useState([initMessage]);

  const chatEndRef = useRef(null);  // Reference to the end of the chat history

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom(); 
  }, [chatHistory]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    e.target.reset();
    e.target.value = "";
    try {
      let newHistory = [...chatHistory, {
        person: "user",
        message: query,
        image: image ? URL.createObjectURL(image) : null
      }, {
        person: "bot",
        message: "Thinking ..."
      }];
      setChatHistory(newHistory);
      setQuery("");
      setImage(null);
      const formData = new FormData();
      formData.append('user_query', query);
      if (image) {
        formData.append('image', image);
      }
      const response = await axios.post('https://home-maintenance-rag-system.onrender.com/query', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      newHistory.pop();
      newHistory = [...newHistory, {
        person: "bot",
        message: response.data.answer
      }];
      setImage(null);
      setChatHistory(newHistory);
    } catch (error) {
      setChatHistory([...chatHistory, {
        person: "error",
        message: "Could not retrieve an answer."
      }]);
      console.error(error);
    }
  };

  return (
    <div id="chat-window">
      <h1 id="heading">Home Improvement Assistant</h1>
      <div id="chat-history">
        {
          chatHistory.map((chat, index) => {
            return(
              <div key={index} className={`${chat.person}-container`}>
                <img 
                  src={ chat.person === "bot"?
                    "https://img.icons8.com/?size=100&id=37410&format=png&color=000000":
                    "https://img.icons8.com/?size=100&id=23264&format=png&color=000000"
                  }
                  height="3%" width="3%"
                  style={{
                    border: "2px solid grey",
                    borderRadius: "50%",
                    marginTop: "20px",
                    padding: "3px",
                  }}
                  alt="conversationalist"
                />
                <div className={`${chat.person}-message`}>
                  {chat.image && <img src={chat.image} alt="Uploaded" style={{ maxWidth: '100%', marginTop: '10px' }} />}
                  {chat.image && <br/>}
                  {chat.message}
                </div>
              </div>
            );
          })
        }
        <div ref={chatEndRef}/>
      </div>
      <form onSubmit={handleSubmit} id="message-input">
        <label for="upload-file" id="upload">
          <img 
            src={
              image == null?
              "https://img.icons8.com/?size=100&id=86460&format=png&color=000000":
              "https://img.icons8.com/?size=100&id=86460&format=png&color=76D222"
            } 
            alt="upload" 
            height="40%" 
            width="40%"/>
        </label>
        <input
          id="upload-file"
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask your question..."
        />
        <button type="submit" id="submit">
          <img src="https://img.icons8.com/?size=100&id=23365&format=png&color=000000" alt="ask" height="50%" width="50%"/>
        </button>
      </form>
    </div>
  );
}

export default App;
