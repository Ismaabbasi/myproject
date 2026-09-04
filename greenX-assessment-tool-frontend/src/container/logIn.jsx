import React, { useState } from "react";
import styled from "styled-components";
import logo from "../resources/images/logo.png";
import {
  borderColor,
  headings,
  inputIconColor,
  textColor,
  white,
} from "../constants/colors";
import { Col, Row, QRCode, Spin, Modal } from "antd";
import LoginForm from "../components/loginForm";
import CustomInput from "../components/customInput";
import { MdOutlineEmail } from "react-icons/md";
import CustomButton from "../components/customButton";
import { useNavigate } from "react-router-dom";
// Styled components
const Container = styled.div`
  text-align: center;
  width: 60%;
  margin: 0 auto;
  margin-top: 70px;
  @media (max-width: 768px) {
    width: 90%;
    margin-top: 40px;
  }
`;

const Logo = styled.img`
  width: contain;
  height: auto;
  margin-bottom: 20px;
`;

const WelcomeText = styled.p`
  font-size: 18px !important;
  font-weight: 600 !important;
  color: ${headings} !important;
  margin-bottom: 40px;
  letter-spacing: 1px;
`;

const LogIn = () => {
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();
  const showModal = () => {
    setIsModalOpen(true);
  };
  const handleOk = () => {
    // setIsModalOpen(false);
    // navigate("/enter-otp");
    navigate("/forgot-password");
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };
  return (
    <>
      <Modal
        title="Enter your email"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
        footer={[
          <CustomButton key="back" onClick={handleCancel}>
            Cancel
          </CustomButton>,

          <CustomButton
            key="link"
            type="primary"
            loading={loading}
            onClick={handleOk}
          >
            Submit
          </CustomButton>,
        ]}
      >
        <CustomInput
          placeholder="Email Address"
          icon={
            <MdOutlineEmail
              style={{ color: inputIconColor, fontSize: "22px" }}
            />
          }
        />
      </Modal>
      <Spin size="large" spinning={loading}>
        <Container>
          <Logo src={logo} alt="Logo" />
          <WelcomeText>
            Welcome to Sustainability <br /> Priority Assessment Tool
          </WelcomeText>
          <Row justify={"center"}>
            <Col xs={24} lg={11}>
              <p
                style={{
                  textAlign: "start",
                  marginBottom: "20px",
                  color: textColor,
                }}
              >
                Enter your credentials below to login.
              </p>
              <LoginForm showModal={showModal} setLoading={setLoading} />
            </Col>

            <Col
              xs={24}
              lg={11}
              style={{
                paddingTop: "20px 10px 20px 0px",
                display: "flex",
                justifyContent: "end",
                alignItems: "center",
              }}
            >
              <div>
                <p
                  style={{
                    fontWeight: 500,
                    marginBottom: "20px",
                    fontSize: "12px",
                  }}
                >
                  Please scan below QR code to Login
                </p>
                <QRCode
                  style={{
                    width: "250px",
                    height: "auto",
                    marginLeft: "auto",
                    borderColor: "#D1D5DB",
                    padding: "20px",
                  }}
                  bgColor={`${white}`}
                  type="canvas"
                  value="http://192.168.10.76:3000/"
                />
              </div>
            </Col>
          </Row>
        </Container>
      </Spin>
    </>
  );
};

export default LogIn;
