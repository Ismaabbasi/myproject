import React from "react";
import styled from "styled-components";
import logo from "../resources/images/logo.png";
import { headings, textColor, white } from "../constants/colors";
import { Col, Row, QRCode } from "antd";
import SignUpForm from "../components/signUpForm";
// Styled components
const Container = styled.div`
  text-align: center;
  width: 500px;
  margin: 0 auto;
  margin-top: 70px;
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

const SignUp = () => {
  return (
    <Container>
      <Logo src={logo} alt="Logo" />
      <WelcomeText>
        Welcome to Sustainability <br /> Priority Assessment Tool
      </WelcomeText>
      <Row>
        <Col xs={24}>
          <p
            style={{
              textAlign: "start",
              marginBottom: "20px",
              color: textColor,
            }}
          >
            Fill form below to register
          </p>
          <SignUpForm />
        </Col>
      </Row>
    </Container>
  );
};

export default SignUp;
