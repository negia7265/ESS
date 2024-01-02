import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import styled from "styled-components";
// const ImageContainer = styled.div`
//   max-height: 300px; /* Adjust the maximum height as needed */
//   padding: 0;
//   margin: 0 auto;
// `;
// const CenteredContainer = styled.div`
//   display: flex;
//   justify-content: center;
//   align-items: center;
//   height: 100vh; /* Adjust the height as needed */
// `;
const Image = styled.img`
  width: 100%; /* Adjust the maximum width as needed */
  max-width: 90vh;
  max-height: 100vh;
  padding: 0;
  display: block; /* Ensure the image is treated as a block element */
`;
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
        <div key={index} style={{ display: "flex", justifyContent: "center" }}>
          {/* <img src={image} alt={`Slide ${index}`} /> */}
          <Image src={image} alt={`Slide ${index}`} />
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
