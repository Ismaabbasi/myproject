import React, { useState, useEffect } from "react";
import { cisco, headings, white } from "../../constants/colors";
import RadarChart from "../../components/radarChart";
import { Outlet } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import CustomButton from "../../components/customButton";
const Variations = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [count, setCount] = useState(1);
  useEffect(() => {
    navigate(`variations-${count}`);
  }, [count]);
  const next = () => {
    if (count == "6") {
      localStorage.setItem("currentStep", 8);
      navigate("/home/confirmation");
    } else {
      setCount(count + 1);
    }
  };
  const prev = () => {
    if (count > 1) {
      setCount(count - 1);
    } else {
      localStorage.setItem("currentStep", 6);

      navigate("/home/sustainability/sustainabilty-IT-6");
    }
  };
  return (
    <div style={{ width: "95%", margin: "0 auto" }}>
      <Outlet />
      {/* <div
        className="detail_container"
        style={{
          width: "93%",
          margin: "0 auto",
          marginTop: 10,
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <CustomButton
          style={{
            background: cisco,
            color: white,
            width: "136px",
            height: "44px",
          }}
          onClick={() => prev()}
        >
          Back
        </CustomButton>

        <CustomButton
          loading={loading}
          style={{ background: cisco, width: "136px", height: "44px" }}
          type="primary"
          onClick={() => next()}
        >
          Next
        </CustomButton>
      </div> */}
    </div>
  );
};

export default Variations;
