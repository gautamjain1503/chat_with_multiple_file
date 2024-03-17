import { useState } from "react";

export default function App() {
  // Define state variables using the useState hook
  const [result, setResult] = useState(); // State for storing the result
  const [question, setQuestion] = useState(""); // State for storing the question
  const [files, setFiles] = useState([]); // State for storing the uploaded files

  // Event handler for updating the question state when input changes
  const handleQuestionChange = (event: any) => {
    setQuestion(event.target.value);
  };

  // Event handler for updating the files state when files are selected
  const handleFileChange = (event: any) => {
    setFiles(event.target.files);
  };

  // Event handler for form submission
  const handleSubmit = (event: any) => {
    event.preventDefault(); // Prevent default form submission behavior

    // Create a new FormData object to store form data
    const formData = new FormData();

    // Loop through selected files and append them to the FormData object
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    // Append the question to the FormData object if it exists
    if (question) {
      formData.append("question", question);
    }

    // Send a POST request to the server with form data
    fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json()) // Parse response as JSON
      .then((data) => {
        setResult(data.result); // Set the result state with the response data
      })
      .catch((error) => {
        console.error("Error", error); // Log any errors to the console
      });
  };

  // Render the component
  return (
    <div className="mx-3">
      <form onSubmit={handleSubmit} className="form">
        {/* Input field for entering the question */}
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
        {/* File input field for uploading files */}
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
        {/* Submit button */}
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

      {/* Display result */}
      <div className="container p-3 mt-4  bg-gradient">
        <h3 className="text-left">Result:</h3>
        <p className="resultOutput">{result}</p>
      </div>
    </div>
  );
}
