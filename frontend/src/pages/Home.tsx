import React, { useState } from "react";
import "../styles/Home.css";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [result, setResult] = useState<{ plate: string; state: string }>({ plate: "", state: "" });
  const [loading, setLoading] = useState(false);
  

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] || null;
    setFile(f);
    setResult({ plate: "", state: "" });
    if (f) {
      const url = URL.createObjectURL(f);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);
      setResult({plate: data.plate, state: data.state });
    } catch (err) {
      console.error(err);
      setResult({plate: "", state: "Error"});
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <div>
          <div className="header">Automatic Number Plate Recognition</div>
          <div className="sub">
            Upload an image with a visible license plate. The backend will
            process the image and return detected plate text.
          </div>

          <div className="controls">
            <label className="fileLabel" htmlFor="file-input">
              Choose Image
            </label>
            <input
              id="file-input"
              className="fileInput"
              type="file"
              accept="image/*"
              onChange={onFileChange}
            />

            <div className="fileName">{file?.name ?? "No file chosen"}</div>
          </div>

          <div style={{ display: "flex", gap: 10 }}>
            <button
              className="btn"
              onClick={handleUpload}
              disabled={!file || loading}
            >
              {loading ? "Processing..." : "Upload & Process"}
            </button>

            <button
              className="fileLabel"
              onClick={() => {
                setFile(null);
                setPreviewUrl(null);
                setResult({ plate: "", state: "" });
              }}
            >
              Reset
            </button>
          </div>

          {result && <div className="result">Result: {result.plate}</div>}
          {result && <div className="result">State: {result.state}</div>}
        </div>

        <div className="previewBox">
          {previewUrl ? (
            <img src={previewUrl} alt="preview" className="previewImage" />
          ) : (
            <div style={{ color: "#94a3b8" }}>No preview available</div>
          )}

          <div style={{ fontSize: 12, color: "#64748b" }}>
            Supported formats: JPG, PNG, JPEG
          </div>
        </div>
      </div>
    </div>
  );
}
