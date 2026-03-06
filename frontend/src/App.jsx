import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const sampleQueries = [
    { label: "Show all customers from USA", type: "select" },
    { label: "What are the top 5 best-selling products?", type: "select" },
    { label: "What is the total revenue from delivered orders?", type: "select" },
    { label: "What are the top 3 customers by total spending?", type: "select" },
    { label: "Add a new customer named John Doe with email john@example.com from New York, USA", type: "dml" },
    { label: "Update all pending orders to processing status", type: "dml" },
    { label: "Delete all cancelled orders", type: "dml" },
    { label: "Upsert a product named Webcam HD in Electronics at $79.99 with 70 in stock", type: "dml" },
    { label: "Create a table called notes with id, content, and created_at columns", type: "ddl" },
    { label: "Add a discount_percent column to the products table", type: "ddl" },
    { label: "Show the column info for the orders table", type: "pragma" },
    { label: "Show the query plan for selecting all delivered orders", type: "pragma" },
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!question.trim()) {
      setError('Please enter a question')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail?.error || 'Failed to process query')
      }

      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSuggestionClick = (query) => {
    setQuestion(query.label)
    setError(null)
    setResult(null)
  }

  const queryTypeBadge = (type) => {
    const map = {
      select: { label: 'SELECT', color: '#3b82f6' },
      dml: { label: 'DML', color: '#f59e0b' },
      ddl: { label: 'DDL', color: '#8b5cf6' },
      pragma: { label: 'PRAGMA', color: '#10b981' },
      other: { label: 'OTHER', color: '#6b7280' },
    }
    const badge = map[type] ?? map.other
    return (
      <span style={{
        background: badge.color,
        color: '#fff',
        borderRadius: '4px',
        padding: '2px 8px',
        fontSize: '11px',
        fontWeight: 700,
        letterSpacing: '0.05em',
        marginLeft: '8px',
        verticalAlign: 'middle',
      }}>
        {badge.label}
      </span>
    )
  }

  return (
    <div className="container">
      <header>
        <h1>Text-to-SQL AI</h1>
        <p>Ask questions about customers, orders, and products in natural language</p>
      </header>

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., Show all customers from USA"
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Processing...' : 'Submit'}
          </button>
        </div>
      </form>

      {!result && !loading && (
        <div className="suggestions">
          <h3>Try these example queries:</h3>
          <div className="suggestion-grid">
            {sampleQueries.map((query, idx) => (
              <button
                key={idx}
                className={`suggestion-btn suggestion-btn--${query.type}`}
                onClick={() => handleSuggestionClick(query)}
              >
                {query.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="results">
          <div className="sql-section">
            <h3>
              Generated SQL
              {queryTypeBadge(result.query_type)}
            </h3>
            <pre className="sql-code">{result.sql}</pre>
          </div>

          <div className="table-section">
            {(result.query_type === 'select' || result.query_type === 'pragma') && result.results.length > 0 ? (
              <>
                <h3>{result.message}</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        {Object.keys(result.results[0]).map((key) => (
                          <th key={key}>{key}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {result.results.map((row, idx) => (
                        <tr key={idx}>
                          {Object.values(row).map((value, i) => (
                            <td key={i}>{value !== null ? String(value) : 'NULL'}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            ) : result.query_type === 'select' || result.query_type === 'pragma' ? (
              <p className="no-results">No results found</p>
            ) : (
              <div className="exec-result">
                <span className="exec-result__icon">
                  {result.query_type === 'dml' ? '✓' : '⬡'}
                </span>
                <p className="exec-result__message">{result.message}</p>
                {result.rows_affected !== null && (
                  <p className="exec-result__detail">{result.rows_affected} row(s) affected</p>
                )}
              </div>
            )}
          </div>

          <button
            className="new-query-btn"
            onClick={() => {
              setResult(null)
              setQuestion('')
              setError(null)
            }}
          >
            Ask Another Question
          </button>
        </div>
      )}
    </div>
  )
}

export default App
