import React, { useEffect, useState } from "react";
import "./App.css";

function Reports() {
  const [reports, setReports] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await fetch("http://localhost:8080/api/reports");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setReports(data);
      } catch (error) {
        console.error("Error fetching reports:", error);
        setError(error.message);
      }
    };

    fetchReports();
  }, []);

  return (
    <div className="reports-container">
      <h1>Saved Reports</h1>
      {error && <div className="error">Error: {error}</div>}
      {reports.length > 0 ? (
        reports.map((report, index) => (
          <div key={index} className="report">
            <h2>Report {index + 1}</h2>
            <pre>{JSON.stringify(report, null, 2)}</pre>
          </div>
        ))
      ) : (
        <p>No reports available.</p>
      )}
    </div>
  );
}

export default Reports;
