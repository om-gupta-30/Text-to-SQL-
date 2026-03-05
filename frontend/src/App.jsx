import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const sampleQueries = [
    "Show all customers from USA",
    "What are the top 5 best-selling products?",
    "List all pending or processing orders",
    "Show customers with more than 2 orders",
    "What is the total revenue from delivered orders?",
    "Show all products in Electronics category",
    "Which customers have never placed an order?",
    "Show order details for customer Alice Johnson",
    "What is the average order value?",
    "List products with low stock (less than 50)",
    "Show orders shipped in March 2024",
    "What are the top 3 customers by total spending?",
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
    setQuestion(query)
    setError(null)
    setResult(null)
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
                className="suggestion-btn"
                onClick={() => handleSuggestionClick(query)}
              >
                {query}
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
            <h3>Generated SQL</h3>
            <pre className="sql-code">{result.sql}</pre>
          </div>

          <div className="table-section">
            <h3>Results ({result.results.length} rows)</h3>
            
            {result.results.length > 0 ? (
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
                          <td key={i}>{value !== null ? value : 'NULL'}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="no-results">No results found</p>
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
