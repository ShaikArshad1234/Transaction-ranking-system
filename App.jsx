import { useState } from "react";
import API_URL from "./api";

function App() {

  const [userId, setUserId] =
    useState("");

  const [amount, setAmount] =
    useState("");

  const [transactionId, setTransactionId] =
    useState("");

  const [summary, setSummary] =
    useState(null);

  const [ranking, setRanking] =
    useState([]);

  const createTransaction = async () => {

    const response = await fetch(
      `${API_URL}/transaction`,
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/json"
        },
        body: JSON.stringify({
          userId,
          amount: Number(amount),
          transactionId
        })
      }
    );

    const data =
      await response.json();

    alert(
      data.message ||
      data.detail
    );
  };

  const getSummary = async () => {

    const response = await fetch(
      `${API_URL}/summary/${userId}`
    );

    const data =
      await response.json();

    setSummary(data);
  };

  const getRanking = async () => {

    const response = await fetch(
      `${API_URL}/ranking`
    );

    const data =
      await response.json();

    setRanking(data);
  };

  return (
    <div style={{padding:"20px"}}>

      <h1>
        Transaction Ranking System
      </h1>

      <input
        placeholder="User ID"
        value={userId}
        onChange={(e)=>
          setUserId(e.target.value)
        }
      />

      <br/><br/>

      <input
        placeholder="Amount"
        value={amount}
        onChange={(e)=>
          setAmount(e.target.value)
        }
      />

      <br/><br/>

      <input
        placeholder="Transaction ID"
        value={transactionId}
        onChange={(e)=>
          setTransactionId(e.target.value)
        }
      />

      <br/><br/>

      <button
        onClick={createTransaction}
      >
        Create Transaction
      </button>

      <button
        onClick={getSummary}
      >
        Get Summary
      </button>

      <button
        onClick={getRanking}
      >
        Get Ranking
      </button>

      {summary && (
        <div>
          <h2>Summary</h2>

          <pre>
            {JSON.stringify(
              summary,
              null,
              2
            )}
          </pre>
        </div>
      )}

      {ranking.length > 0 && (
        <div>

          <h2>
            Ranking
          </h2>

          <table border="1">

            <thead>
              <tr>
                <th>User</th>
                <th>Score</th>
                <th>Total</th>
                <th>Count</th>
              </tr>
            </thead>

            <tbody>

              {ranking.map(
                (item) => (

                <tr
                  key={item.userId}
                >
                  <td>
                    {item.userId}
                  </td>

                  <td>
                    {item.score}
                  </td>

                  <td>
                    {item.totalAmount}
                  </td>

                  <td>
                    {item.transactionCount}
                  </td>
                </tr>

              ))}
            </tbody>

          </table>

        </div>
      )}

    </div>
  );
}

export default App;