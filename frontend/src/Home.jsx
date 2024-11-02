import React, { useState } from "react";
import "./App.css";

function Home() {
  const [patentId, setPatentId] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch("http://localhost:8080/api/check", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patent_id: patentId,
          company_name: companyName,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      setError(error.message);
    }
  };

  const renderJsonFormatted = (obj) => {
    const jsonString = JSON.stringify(obj, null, 2);
    const jsonLines = jsonString.split("\n");

    return (
      <pre>
        {jsonLines.map((line, index) => (
          <div key={index}>{line}</div>
        ))}
      </pre>
    );
  };

  return (
    <div className="App">
      <h1>Patent Infringement Checker</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Patent ID"
          value={patentId}
          onChange={(e) => setPatentId(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Company Name"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          required
        />
        <button type="submit">Check Infringement</button>
      </form>
      {error && <div className="error">Error: {error}</div>}
      {result && (
        <div className="result">
          <h2>Analysis Result</h2>
          {renderJsonFormatted(result)}
        </div>
      )}
    </div>
  );
}

export default Home;
