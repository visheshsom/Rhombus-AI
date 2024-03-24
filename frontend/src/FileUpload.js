import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
    const [file, setFile] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleFormSubmit = (event) => {
        event.preventDefault();
        if (!file) {
            alert('Please select a file first!');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        axios.post('http://localhost:8000/data/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            console.log('File successfully uploaded and processed', response.data);
            
        })
        .catch(error => console.log(error));
    };

    return (
        <div>
            <form onSubmit={handleFormSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
        </div>
    );
}

export default FileUpload;
