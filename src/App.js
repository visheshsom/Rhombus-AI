import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';


function FileUpload() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [dataFrame, setDataFrame] = useState([]); // Initialize as an empty array

    const handleFileSelect = (event) => {
        setSelectedFile(event.target.files[0]);
    };
  
    useEffect(() => { // This useEffect will log every time dataFrame changes.
        console.log('DataFrame state:', dataFrame);
    }, [dataFrame]);

    
    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await axios.post('/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log('Raw response:', response.data); 
            console.log('DataFrame state:', dataFrame);

            setDataFrame(response.data); // Assuming the backend returns an array directly

        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <div className="App">
            <input type="file" onChange={handleFileSelect} />
            <button onClick={handleUpload}>Upload</button>
            <div className="table-container">
                {dataFrame.length > 0 ? (
                    <table>
                        <thead>
                            <tr>
                                {/* Create table headers dynamically from the first row keys */}
                                {Object.keys(dataFrame[0]).map((key, index) => (
                                    <th key={index}>{key}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {/* Create table rows dynamically */}
                            {dataFrame.map((row, rowIndex) => (
                                <tr key={rowIndex}>
                                    {Object.values(row).map((value, valueIndex) => (
                                        <td key={valueIndex}>{value !== null ? value : "N/A"}</td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No data to display</p>
                )}
            </div>
        </div>
    );
}

export default FileUpload;
