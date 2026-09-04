import { Col, Row } from "antd";
import React from "react";
import img from "../resources/images/a.png";
import { cisco, headings, white } from "../constants/colors";
import CustomButton from "../components/customButton";
import { MdOutlinePhoneInTalk } from "react-icons/md";
import { TbReport } from "react-icons/tb";
import { useNavigate } from "react-router-dom";
const Confirmation = () => {
  const navigate = useNavigate();
  return (
    <div
      style={{
        textAlign: "start",
        padding: "10px 30px",
      }}
    >
      <p
        style={{
          marginBottom: "30px",
          fontSize: "20px",
          fontWeight: 700,
          color: headings,
        }}
      >
        Thank you for completing the assessment using our best-in class
        framework. We trust that this process has provided valuable insights.{" "}
        <br /> Kindly take note of the next steps:
      </p>
      <Row gutter={(30, 30)}>
        <Col xs={24} lg={10}>
          <div style={{ paddingTop: "10px" }}>
            <div
              style={{
                display: "flex",
                gap: "10px",
                color: headings,
                fontWeight: 500,
                marginBottom: "15px",
              }}
            >
              <MdOutlinePhoneInTalk
                style={{
                  fontSize: "60px",
                }}
              />
              <p
                style={{
                  fontSize: "18px",
                }}
              >
                Within the next 5 business days, we will contact you to disscuss
                the assessment results in detail.
              </p>
            </div>
            <div
              style={{
                display: "flex",
                gap: "10px",
                color: headings,
                fontWeight: 500,
              }}
            >
              <TbReport
                style={{
                  fontSize: "60px",
                }}
              />
              <div
                style={{
                  fontSize: "18px",
                }}
              >
                <p
                  style={{
                    marginBottom: "20px",
                  }}
                >
                  Subsequently, you will receive a comprehensive report
                  outlining:
                </p>
                <ul style={{ paddingLeft: "15px" }}>
                  <li style={{ marginBottom: "25px" }}>
                    Your positioning relative to the best in class within your
                    industry.
                  </li>
                  <li style={{ marginBottom: "25px" }}>
                    Identified gaps within your strategic dimensions,
                    accompained by actionable recommendations to address them.
                  </li>
                  <li style={{ marginBottom: "25px" }}>
                    A transformative roadmap showcasing the path forward to
                    achieve your sustainabilty objectives.
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </Col>
        <Col xs={24} lg={14}>
          <img style={{ width: "100%" }} src={img} alt="" />
        </Col>
      </Row>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginTop: "30px",
        }}
      >
        <p
          style={{
            fontStyle: "italic",
            fontSize: "14px",
            color: headings,
          }}
        >
          Please note that these results might change based on the final
          analysis and will be represented in the final result.
        </p>
        {/* <CustomButton
          onClick={() => {
            localStorage.setItem("currentStep", 9);
            navigate("/home/feedback");
          }}
          style={{
            background: cisco,
            color: white,
            borderRadius: "10px",
            width: "100px",
          }}
        >
          Next
        </CustomButton> */}
      </div>
    </div>
  );
};

export default Confirmation;
