import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

// const ImageContainer = styled.div`
//   max-height: 300px; /* Adjust the maximum height as needed */
//   padding: 0;
//   margin: 0 auto;
// `;
// const Image = styled.img`
//   max-width: 100%; /* Adjust the maximum width as needed */
//   padding: 0;
//   display: block; /* Ensure the image is treated as a block element */
//   margin: 0 auto; /* Center the image */
// `;
const ImageSlider = ({ images }) => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };

  return (
    <Slider {...settings}>
      {images.map((image, index) => (
        <div key={index}>
          <img src={image} alt={`Slide ${index}`} />
        </div>
      ))}
    </Slider>
  );
};

const Preview = ({ invoiceImages }) => {
  const images = [...invoiceImages];
  return (
    <div>
      <div>
        <ImageSlider images={images} />
      </div>
    </div>
  );
};

export default Preview;
