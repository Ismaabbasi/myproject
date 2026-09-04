import React, { useState } from "react";
import { Button, Input, Spin } from "antd";
import { LeftOutlined, MailOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import axios from "axios";
// import { baseUrl } from "../../utils/axios";
// import Swal from "sweetalert2";
import { baseUrl } from "../../utills/axios";
import CustomInput from "../../components/customInput";
import CustomButton from "../../components/customButton";
import { borderColor, cisco, textColor } from "../../constants/colors";
export const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [showOTPFields, setShowOTPFields] = useState(false);
  const [otpDigits, setOtpDigits] = useState(["", "", "", ""]);
  const [token, setToken] = useState("");
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const otpString = otpDigits.join("");

  const handleEmailSubmit = async () => {
    // setShowOTPFields(true);
    setLoading(true);
    const payload = {
      email: email,
    };
    const res = await axios.post(baseUrl + "/api/v2/auth/verify-email", null, {
      params: {
        email: email,
      },
    });
    if (res.status == "200" && res.data.message) {
      setLoading(false);
      setShowOTPFields(true);
    } else {
      setLoading(false);
      //   Swal.fire({
      //     title: res.data.error,
      //     type: "error",
      //     allowOutsideClick: false,
      //   });
    }
  };

  const submitOTP = async () => {
    setLoading(true);

    if (otpString !== "") {
      try {
        const res = await axios.post(baseUrl + "/api/v2/auth/send-otp", {
          code: otpString,
          email: email,
        });
        console.log(res);
        if (res.status === 200) {
          localStorage.setItem("email", email);
          setLoading(false);
          navigate("/new-password");
        } else {
          setLoading(false);
        }
      } catch (error) {
        setLoading(false);

        console.error("Error submitting OTP:", error);
      }
    } else {
      setLoading(false);
    }
  };
  const handleOtpChange = (index, value) => {
    const newOtpDigits = [...otpDigits];
    newOtpDigits[index] = value;
    setOtpDigits(newOtpDigits);
  };
  const goBack = () => {
    if (showOTPFields) {
      setShowOTPFields(false);
    } else {
      navigate("/login");
    }
  };
  return (
    <Spin size="large" spinning={loading}>
      <div style={{ margin: "20px" }}>
        <Button
          style={{
            boxShadow: "none",
            background: "none",
            border: "none",
            fontSize: "18px",
            // fontWeight: 500,
            color: textColor,
          }}
          onClick={goBack}
        >
          <LeftOutlined style={{ fontSize: "14px" }} /> BACK
        </Button>
        <div>
          <div style={{ textAlign: "center" }}>
            <div style={{ marginBottom: "100px", color: "#2F302F" }}>
              <p
                style={{
                  fontSize: "22px",
                  fontWeight: 700,
                  marginBottom: "10px",
                }}
              >
                Forgot password
              </p>
              {showOTPFields ? (
                <>
                  <p>
                    Tokens code has been sent to email address{" "}
                    <span style={{ color: cisco }}> {email}</span>
                  </p>
                </>
              ) : (
                <p>Please enter your email to reset password</p>
              )}
            </div>
            {!showOTPFields && (
              <CustomInput
                style={{
                  width: "400px",
                  height: "40px",
                  margin: "0 auto",
                  borderRadius: "5px",
                  borderColor: "#6EB544",
                  marginBottom: "80px",
                }}
                type="email"
                name="email"
                placeholder="Email"
                //   value={email}
                required
                onChange={(e) => setEmail(e.target.value)}
                suffix={<MailOutlined style={{ color: cisco }} />}
              />
            )}
            <br />
            {showOTPFields && (
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  gap: "20px",
                  marginBottom: "80px",
                }}
              >
                {otpDigits.map((digit, index) => (
                  <>
                    {index === 0 ? "" : "-"}
                    <Input
                      key={index}
                      style={{
                        width: "60px",
                        height: "50px",
                        margin: "0 5px",
                        borderRadius: "10px",
                        borderColor: borderColor,
                        textAlign: "center",
                      }}
                      type="text"
                      name={`otp-${index}`}
                      placeholder="OTP"
                      value={digit}
                      onChange={(e) => handleOtpChange(index, e.target.value)}
                      maxLength={"1"}
                    />
                  </>
                ))}
              </div>
            )}
            <br />
            {showOTPFields ? (
              <>
                <CustomButton
                  style={{
                    width: "395px",
                    height: "48px",
                    // borderRadius: "10px",
                    fontWeight: 700,
                    background: cisco,
                  }}
                  type="primary"
                  block
                  onClick={submitOTP}
                >
                  Submit
                </CustomButton>
              </>
            ) : (
              <>
                <CustomButton
                  style={{
                    width: "395px",
                    height: "48px",
                    // borderRadius: "10px",
                    fontWeight: 700,
                    background: cisco,
                  }}
                  type="primary"
                  block
                  onClick={handleEmailSubmit}
                >
                  Submit
                </CustomButton>
              </>
            )}
          </div>
        </div>
      </div>
    </Spin>
  );
};
