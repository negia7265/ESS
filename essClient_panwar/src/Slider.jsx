import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

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

const SimpleSlider = ({ invoiceImages }) => {
  console.log(invoiceImages);
  const images = [
    ...invoiceImages,
    // Add more image URLs as needed
  ];

  return (
    <div>
      <h1>Image Slider</h1>
      <ImageSlider images={images} />
    </div>
  );
};

export default SimpleSlider;

// import React from "react";
// import styled from "styled-components";
// import Slider from "react-slick";
// import "slick-carousel/slick/slick.css";
// import "slick-carousel/slick/slick-theme.css";
// import { nanoid } from "nanoid";

// const ImageContainer = styled.div`
//   max-height: 300px; /* Adjust the maximum height as needed */
//   padding: 0;
//   margin: 0 auto; /* Center the image */
// `;

// const Image = styled.img`
//   max-width: 100%; /* Adjust the maximum width as needed */
//   padding: 0;
//   display: block; /* Ensure the image is treated as a block element */
//   margin: 0 auto; /* Center the image */
// `;

// export const Preview = ({ invoiceImages }) => {
//   const settings = {
//     dots: true,
//     infinite: true,
//     speed: 500,
//     slidesToShow: 1,
//     slidesToScroll: 1,
//   };

//   return (
//     <Slider {...settings}>
//       {invoiceImages.map((image, index) => {
//         return (
//           <ImageContainer key={nanoid()}>
//             <Image src={image} alt="invoice image" />
//           </ImageContainer>
//         );
//       })}
//     </Slider>
//   );
// };
