import React, { useState } from 'react';

const TextProcessor = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith('.md')) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onload = (event) => {
        setText(event.target.result);
      };
      reader.readAsText(selectedFile);
    } else {
      alert('Пожалуйста, выберите файл с расширением .md');
    }
  };

  const handleSubmit = async (useFile = true) => {
    setLoading(true);
    setError('');
    setResponse(null);

    try {
      let payload;
      let endpoint;

      if (useFile && file) {
        const formData = new FormData();
        formData.append('file', file);
        payload = formData;
        endpoint = '/process-file';
      } else {
        payload = { text };
        endpoint = '/process-text';
      }

      const baseUrl = 'http://localhost:8000'; // будем пробрасывать через nginx или прокси
      const res = await fetch(baseUrl + endpoint, {
        method: 'POST',
        body: useFile && file ? payload : JSON.stringify(payload),
        headers: useFile && file ? {} : { 'Content-Type': 'application/json' },
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>📝 AI Text Analyzer</h1>
      <p>Загрузи .md файл или введи текст вручную.</p>

      <div style={{ marginBottom: '20px' }}>
        <input type="file" accept=".md" onChange={handleFileChange} />
        {file && <p style={{ color: 'green' }}>Файл: {file.name}</p>}
      </div>

      <div style={{ marginBottom: '20px' }}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Или вставьте текст здесь..."
          rows="6"
          style={{ width: '100%', padding: '10px', fontSize: '16px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <button
          onClick={() => handleSubmit(true)}
          disabled={!file && !text}
          style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          Обработать файл
        </button>
        <button
          onClick={() => handleSubmit(false)}
          disabled={!text}
          style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          Обработать текст
        </button>
      </div>

      {loading && <p>⏳ Обработка... Ждите ответа от модели...</p>}
      {error && <p style={{ color: 'red' }}>❌ Ошибка: {error}</p>}

      {response && (
        <div style={{ marginTop: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
          <h3>🧠 Ответ от Qwen2:</h3>
          {response.success ? (
            <div>
              <p><strong>Тональность:</strong> {response.data.tone}</p>
              <p><strong>Резюме:</strong> {response.data.summary}</p>
              <p><strong>Ключевые слова:</strong> {response.data.keywords.join(', ')}</p>
            </div>
          ) : (
            <p style={{ color: 'red' }}>{response.error}</p>
          )}
        </div>
      )}

      <hr />
      <p style={{ fontSize: '14px', color: '#666' }}>
        🚀 Работает в Docker: React → FastAPI → Ollama (qwen2:0.5b)
      </p>
    </div>
  );
};

export default TextProcessor;