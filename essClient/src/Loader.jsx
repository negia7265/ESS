import React from "react";
import "./Loader.css";
import { Hourglass } from "react-loader-spinner";
export const Loader = () => {
  return (
    <div
      className="my_loader"
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignContent: "center",
        alignItems: "center",
      }}
    >
      <h1 style={{ color: "black", fontSize: "50px", margin: "30px" }}>Loading...</h1>
      <div>
        {/* <svg
          style={{ width: "70vh" }}
          className="bike"
          viewBox="0 0 48 30"
          width="58px"
          height="40px"
        >
          <g
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1"
          >
            <g transform="translate(9.5,19)">
              <circle
                class="bike__tire"
                r="9"
                stroke-dasharray="56.549 56.549"
              />
              <g
                class="bike__spokes-spin"
                stroke-dasharray="31.416 31.416"
                stroke-dashoffset="-23.562"
              >
                <circle class="bike__spokes" r="5" />
                <circle
                  class="bike__spokes"
                  r="5"
                  transform="rotate(180,0,0)"
                />
              </g>
            </g>
            <g transform="translate(24,19)">
              <g
                class="bike__pedals-spin"
                stroke-dasharray="25.133 25.133"
                stroke-dashoffset="-21.991"
                transform="rotate(67.5,0,0)"
              >
                <circle class="bike__pedals" r="4" />
                <circle
                  class="bike__pedals"
                  r="4"
                  transform="rotate(180,0,0)"
                />
              </g>
            </g>
            <g transform="translate(38.5,19)">
              <circle
                class="bike__tire"
                r="9"
                stroke-dasharray="56.549 56.549"
              />
              <g
                class="bike__spokes-spin"
                stroke-dasharray="31.416 31.416"
                stroke-dashoffset="-23.562"
              >
                <circle class="bike__spokes" r="5" />
                <circle
                  class="bike__spokes"
                  r="5"
                  transform="rotate(180,0,0)"
                />
              </g>
            </g>
            <polyline
              class="bike__seat"
              points="14 3,18 3"
              stroke-dasharray="5 5"
            />
            <polyline
              class="bike__body"
              points="16 3,24 19,9.5 19,18 8,34 7,24 19"
              stroke-dasharray="79 79"
            />
            <path
              class="bike__handlebars"
              d="m30,2h6s1,0,1,1-1,1-1,1"
              stroke-dasharray="10 10"
            />
            <polyline
              class="bike__front"
              points="32.5 2,38.5 19"
              stroke-dasharray="19 19"
            />
          </g>
        </svg> */}
        <Hourglass
          visible={true}
          height="150"
          width="150"
          ariaLabel="hourglass-loading"
          wrapperStyle={{}}
          wrapperClass=""
          colors={["#306cce", "#72a1ed"]}
        />
      </div>
    </div>
  );
};
