import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [filesUsed, setFilesUsed] = useState([]);
  const [fileContent, setFileContent] = useState('');

  const askQuestion = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    setAnswer('');
    setFilesUsed([]);
    setFileContent('');

    try {
      const response = await axios.post('http://localhost:8000/api/ask', {
        question: question
      });
      
      setAnswer(response.data.answer);
      setFilesUsed(response.data.files_used || []);
      
      // Показываем содержание первого файла для примера
      if (response.data.files_used && response.data.files_used.length > 0) {
        const contentResponse = await axios.get(
          `http://localhost:8000/api/files/${response.data.files_used[0]}`
        );
        setFileContent(contentResponse.data.content);
      }

    } catch (error) {
      console.error('Error:', error);
      setAnswer('Произошла ошибка при обработке запроса');
    } finally {
      setLoading(false);
    }
  };

  const exampleQuestions = [
    "Что содержится в файле test.md?",
    "Расскажи об основной идее документа test.md",
    "Какая тональность текста в test.md?",
    "О чем этот документ?",
    "Какие инструкции содержатся в файле?"
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1>📁 Интеллектуальный анализатор файлов</h1>
        <p>Задайте вопрос о содержимом файлов в папке shared-data</p>
      </header>

      <div className="container">
        <div className="question-section">
          <h2>💬 Задайте вопрос о файлах</h2>
          
          <div className="examples">
            <h4>Примеры вопросов:</h4>
            {exampleQuestions.map((q, index) => (
              <button
                key={index}
                className="example-btn"
                onClick={() => setQuestion(q)}
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>

          <div className="input-group">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Например: Что содержится в test.md? Какая основная идея документа?"
              rows="3"
              disabled={loading}
            />
            <button 
              onClick={askQuestion} 
              disabled={loading || !question.trim()}
            >
              {loading ? '⏳ Анализируем...' : '🚀 Задать вопрос'}
            </button>
          </div>
        </div>

        {answer && (
          <div className="results-section">
            <div className="answer">
              <h2>🤖 Ответ на основе анализа файлов</h2>
              <div className="answer-content">
                {answer}
              </div>
              
              {filesUsed.length > 0 && (
                <div className="files-used">
                  <h4>📋 Проанализированные файлы:</h4>
                  <div className="files-list">
                    {filesUsed.map((file, index) => (
                      <span key={index} className="file-tag">{file}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {fileContent && (
              <div className="file-info">
                <h2>📄 Содержимое файла: {filesUsed[0]}</h2>
                <div className="file-content">
                  <pre>{fileContent}</pre>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;