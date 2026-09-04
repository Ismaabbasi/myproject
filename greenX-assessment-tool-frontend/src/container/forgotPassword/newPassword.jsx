import React, { useState } from "react";
import { LockOutlined, UserOutlined } from "@ant-design/icons";
import { Button, Checkbox, message, Form, Input, Spin, Row, Col } from "antd";
import { useNavigate } from "react-router-dom";
import CustomInput from "../../components/customInput";
import { MdOutlineEmail } from "react-icons/md";
import {
  cisco,
  inputIconColor,
  textColor,
  white,
} from "../../constants/colors";
import { baseUrl } from "../../utills/axios";
import axios from "axios";
import CustomButton from "../../components/customButton";
import Password from "antd/es/input/Password";
const NewPassword = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();
  const email = localStorage.getItem("email");
  const onFinish = async (values) => {
    setLoading(true);
    console.log("Received values of form: ", values);
    try {
      const res = await axios.post(baseUrl + "/api/v2/auth/reset-password", {
        email: email,
        password: values.password,
        password_repeat: values.password_repeat,
      });
      if (res?.status == "200") {
        messageApi.open({
          type: "success",
          content: res?.data?.message,
        });
        setLoading(false);
        setTimeout(() => {
          navigate("/login");
        }, 1000);
      } else {
        setLoading(false);
      }
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  };
  return (
    <>
      {contextHolder}
      <div style={{ marginTop: "60px" }}>
        <p style={{ textAlign: "center", marginBottom: "40px" }}>
          Enter below your new password to reset
        </p>
        <Row justify={"center"}>
          <Col xs={20} sm={18} md={8}>
            <Spin size="large" spinning={loading}>
              <Form
                name="normal_login"
                className="login-form"
                initialValues={{
                  remember: true,
                }}
                onFinish={onFinish}
              >
                <Form.Item
                  name="password"
                  rules={[
                    {
                      required: true,
                      message: "Please input your Password!",
                    },
                  ]}
                >
                  <CustomInput
                    placeholder="Enter new password"
                    type="password"
                    icon={
                      <LockOutlined
                        className="site-form-item-icon"
                        style={{ color: inputIconColor, fontSize: "22px" }}
                      />
                    }
                  />
                </Form.Item>
                <Form.Item
                  name="password_repeat"
                  rules={[
                    {
                      required: true,
                      message: "Please input your Password!",
                    },
                  ]}
                >
                  <CustomInput
                    placeholder="Repeat password"
                    type="password"
                    icon={
                      <LockOutlined
                        className="site-form-item-icon"
                        style={{ color: inputIconColor, fontSize: "22px" }}
                      />
                    }
                  />
                </Form.Item>

                <Form.Item>
                  <CustomButton
                    htmlType="submit"
                    style={{
                      width: "100%",
                      background: cisco,
                      color: white,
                      height: "48px",
                    }}
                  >
                    Log in
                  </CustomButton>
                </Form.Item>
              </Form>
            </Spin>
          </Col>
        </Row>
      </div>
    </>
  );
};
export default NewPassword;
