import { useState } from "react";
import axios from "axios";

function App() {
  const [userId, setUserId] = useState("");
  const [amount, setAmount] = useState("");
  const [requestId, setRequestId] = useState("");
  const [summary, setSummary] = useState(null);
  const [ranking, setRanking] = useState([]);

  const API = "https://transaction-ranking-api-dw1s.onrender.com";

  const submitTransaction = async () => {
    try {
      await axios.post(`${API}/transaction`, {
        userId,
        amount: Number(amount),
        requestId,
      });

      alert("Transaction Added");
    } catch (err) {
      alert(err.response?.data?.detail || "Error");
    }
  };

  const getSummary = async () => {
    try {
      const res = await axios.get(`${API}/summary/${userId}`);
      setSummary(res.data);
    } catch {
      alert("User not found");
    }
  };

  const getRanking = async () => {
    const res = await axios.get(`${API}/ranking`);
    setRanking(res.data);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Transaction Ranking System</h1>

      <input
        placeholder="User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Request ID"
        value={requestId}
        onChange={(e) => setRequestId(e.target.value)}
      />
      <br /><br />

      <button onClick={submitTransaction}>
        Submit Transaction
      </button>

      <hr />

      <button onClick={getSummary}>
        Get Summary
      </button>

      {summary && (
        <pre>{JSON.stringify(summary, null, 2)}</pre>
      )}

      <hr />

      <button onClick={getRanking}>
        Load Ranking
      </button>

      <pre>{JSON.stringify(ranking, null, 2)}</pre>
    </div>
  );
}

export default App;