import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState([]);
  const [selectedCelebrity, setSelectedCelebrity] = useState("All");
  const [trending, setTrending] = useState([]);

  // Load all data
  useEffect(() => {
    fetch("http://127.0.0.1:8000/data")
      .then(res => res.json())
      .then(res => setData(res));
  }, []);

  // Load trending
  useEffect(() => {
    fetch("http://127.0.0.1:8000/trending")
      .then(res => res.json())
      .then(res => setTrending(res));
  }, []);

  // Filter logic
  const filtered =
    selectedCelebrity === "All"
      ? data
      : data.filter(item => item.celebrity === selectedCelebrity);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Celebrity Dashboard 🔥</h1>

      {/* 🔥 Trending Section */}
      <h2>Trending</h2>
      {trending.map((item, index) => (
        <div
          key={index}
          style={{
            cursor: "pointer",
            marginBottom: "5px",
            color: "blue"
          }}
          onClick={() => setSelectedCelebrity(item[0])}
        >
          {item[0]} → {item[1]} mentions
        </div>
      ))}

      {/* Reset Button */}
      <button
        onClick={() => setSelectedCelebrity("All")}
        style={{ marginTop: "10px", padding: "5px 10px" }}
      >
        Show All
      </button>

      <hr />

      {/* Results */}
      <h2>Results</h2>

      {filtered.map((item, index) => (
        <div key={index} style={{ marginTop: "10px" }}>
          <b>{item.celebrity}</b> → {item.reason}
        </div>
      ))}
    </div>
  );
}

export default App;