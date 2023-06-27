import React, { useRef, useEffect } from 'react';

const Slider = ({ handleImageClick }) => {
  const sliderRef = useRef(null);

  const imagesArray = [
    './1210002.png',
    './cropped-1920-1080-652694.jpg',
    './cropped-1920-1080-737474.png',
    './cropped-1920-1080-742320.png',
    './cropped-1920-1080-902399.jpg'
  ];

  useEffect(() => {
    const slider = sliderRef.current;

    const handleScroll = (event) => {
      if (event.deltaY > 0) {
        slider.scrollTop += 100;
      } else {
        slider.scrollTop -= 100;
      }
    };

    slider.addEventListener('wheel', handleScroll);

    return () => {
      slider.removeEventListener('wheel', handleScroll);
    };
  }, []);


    const toDataURL = url => fetch(url)
        .then(response => response.blob())
        .then(blob => new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(blob)
     }))
     
    function dataURLtoFile(dataurl, filename) {
        var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = window.atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
        while(n--){
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new File([u8arr], filename, {type:'image/*'});
    }

    const handleImageClickInternal = async (imageUrl) => {
        toDataURL(imageUrl)
        .then(dataUrl => {
            var file = dataURLtoFile(dataUrl, imageUrl.substring(2));
            handleImageClick(file);
        })

    };

  return (
    <div className="slider" ref={sliderRef}>
      {imagesArray.map((image, index) => (
        <img 
            key={index} 
            src={image} 
            alt={`Image ${index}`} 
            onClick={() => {handleImageClickInternal(imagesArray[index])}}
        />
      ))}
    </div>
  );
};

export default Slider;
