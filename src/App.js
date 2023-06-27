import LoadingDot from './LoadingDot'; 
import './App.css';
import React, { useState } from 'react';
import Slider from './Slider';
import Image0 from './1210002.png';
import Image1 from './cropped-1920-1080-652694.jpg';
import Image2 from './cropped-1920-1080-737474.png';
import Image3 from './cropped-1920-1080-742320.png';
import Image4 from './cropped-1920-1080-902399.jpg';

function App() {

  const images = [
    Image0,
    Image1,
    Image2,
    Image3,
    Image4
  ];

  const [selectedFile, setSelectedFile] = useState(null);
  const [backgroundStyle, setBackgroundStyle] = useState();
  const [isLoading, setIsLoading] = useState(false);
  const [fetchedColors, setFetchedColors] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [isInputDisabled, setIsInputDisabled] = useState(false);  

  // Function to update the background style with the fetched colors
  const updateBackground = (colors) => {
    const gradientColors = colors.join(', ');
    const newBackgroundStyle = `linear-gradient(to right, ${gradientColors})`;
    document.body.style.setProperty('--gradient-background', newBackgroundStyle);
    setBackgroundStyle(newBackgroundStyle);
    setFetchedColors(colors);
  };

  const processAndEvaluate = async (file, imagePath) => {
    setSelectedFile(file);
    setIsLoading(true);
    setIsInputDisabled(true);

    let formData = new FormData();
    formData.append('file', file);
    formData.append('imagePath', imagePath);

    try {
      const response = await fetch('https://mohitkambli.pythonanywhere.com/upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        let tempFetchedColors = data.colors;
        const fetchedColors = JSON.parse(tempFetchedColors.replace(/'/g, "\""));
        updateBackground(fetchedColors);
      } else {
        console.log('Request failed with status:', response.status);
      }
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          setSelectedImage(reader.result);
        };
        reader.readAsDataURL(file);
      }
    } catch (error) {
      console.log('Error: ', error);
    } finally {
      setIsLoading(false);
      setIsInputDisabled(false);
    }
  }

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    const imagePath = URL.createObjectURL(file);
    processAndEvaluate(file, imagePath);
  };

  const handleImageClick = async (file) => {
    processAndEvaluate(file, URL.createObjectURL(file));
  };

  return (
    <div className="App">
      <div className="Content">
        <h1 className="heading-style">ColorJam{isLoading && <LoadingDot/>}</h1>
        <div className="div-file-input-label">
          <label htmlFor="file" className="file-input-label">
            <input
              type="file"
              id="file"
              onChange={handleFileChange}
              accept="image/*"
              style={{ display: 'none' }}
              disabled={isInputDisabled}
            />
            Browse an Image
          </label>
        </div>
      </div>
      <div className="color-list">
        {
          fetchedColors.length === 0 ? (
            <p>Dominant colors will be loaded here...</p>
          ) : (
            fetchedColors.map((color, index) => (
              <div key={index} className="color-item">
                <div className="color-box" style={{ backgroundColor: color }}></div>
                <span className="color-code">{color}</span>
              </div>
            ))
          )
        }
      </div>
      <div className="image-container">
        {selectedImage ? (
          <img src={selectedImage} alt="Selected" />
        ) : (
          <p className="color-text">Image will be displayed here...</p>
        )}
      </div>
      <div className="slider-container">
        <Slider images={images} handleImageClick={handleImageClick} />
      </div>
    </div>
  );
}

export default App;
