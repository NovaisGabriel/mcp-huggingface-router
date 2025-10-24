import React, {useState} from 'react'
import axios from 'axios'

export default function App(){
  const [text,setText] = useState("")
  const [mode,setMode] = useState("auto")
  const [result,setResult] = useState(null)
  const [loading,setLoading] = useState(false)

  async function submit(e){
    e.preventDefault()
    setLoading(true)
    setResult(null)
    try{
      const res = await axios.post("http://localhost:7860/api/analyze", {text, mode: mode==="auto"?null:mode})
      setResult(res.data)
    }catch(err){
      setResult({error: err.toString()})
    }finally{
      setLoading(false)
    }
  }

  return (
    <div style={{maxWidth:800, margin:'20px auto', fontFamily:'Arial, sans-serif'}}>
      <h1>MCP (Hugging Face) — Demo</h1>
      <form onSubmit={submit}>
        <textarea value={text} onChange={e=>setText(e.target.value)} rows={8} style={{width:'100%'}} placeholder="Paste text here..." />
        <div style={{marginTop:8}}>
          <label>
            Mode:
            <select value={mode} onChange={e=>setMode(e.target.value)} style={{marginLeft:8}}>
              <option value="auto">Auto (router)</option>
              <option value="summary">Summary</option>
              <option value="sentiment">Sentiment</option>
              <option value="keywords">Keywords</option>
              <option value="all">All</option>
            </select>
          </label>
        </div>
        <button style={{marginTop:12}} disabled={loading}>Analyze</button>
      </form>

      <div style={{marginTop:20}}>
        {loading && <div>Processing…</div>}
        {result && <div>
          <h3>Decision: {result.decision}</h3>
          {result.summary && <>
            <h4>Summary</h4><p>{result.summary}</p>
          </>}
          {result.sentiment && <>
            <h4>Sentiment</h4><pre>{JSON.stringify(result.sentiment,null,2)}</pre>
          </>}
          {result.keywords && <>
            <h4>Keywords</h4><ul>{result.keywords.map(k=><li key={k}>{k}</li>)}</ul>
          </>}
          {result.error && <div style={{color:'red'}}>{result.error}</div>}
        </div>}
      </div>
    </div>
  )
}
