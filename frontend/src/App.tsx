import { useState } from "react";

export default function App() {
  const [result, setResult] = useState();
  const [question, setQuestion] = useState("");
  const [files, setFiles] = useState([]);

  const handleQuestionChange = (event: any) => {
    setQuestion(event.target.value);
  };

  const handleFileChange = (event: any) => {
    setFiles(event.target.files);
  };

  const handleSubmit = (event: any) => {
    event.preventDefault();

    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }
    if (question) {
      formData.append("question", question);
    }

    fetch("https://18.206.174.134/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data.result);
      })
      .catch((error) => {
        console.error("Error", error);
      });
  };

  return (
    <div className="mx-3">
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group row mb-2">
          <label className="questionLabel col-sm-2 col-form-label" htmlFor="question">
            Question
          </label>
          <div className="col-sm-10">
            <input
              className="questionInput form-control"
              id="question"
              type="text"
              value={question}
              onChange={handleQuestionChange}
              placeholder="Ask your question here"
            />
          </div>
        </div>
        <div className="custom-file">
          <label className="fileLabel custom-file-label col-sm-2" htmlFor="file">
            Choose File
          </label>
          <input
            type="file"
            id="file"
            name="file"
            accept=".csv, .pdf, .docx, .txt"
            onChange={handleFileChange}
            className="fileInput custom-file-input"
            multiple
            required
          />
          <div className="invalid-feedback">Example invalid custom file feedback</div>
        </div>
        <div className="form-group row mt-4">
          <div className="col-sm-10">
            <button
              className="submitBtn btn btn-primary"
              type="submit"
              disabled={!files.length || !question}
            >
              Submit
            </button>
          </div>
        </div>
      </form>

      <div className="container p-3 mt-4  bg-gradient">
        <h3 className="text-left">Result:</h3>
        <p className="resultOutput">{result}</p>
      </div>
    </div>
  );
}
