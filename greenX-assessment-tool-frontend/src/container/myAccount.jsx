import React, { useState, useEffect } from "react";
import {
  headings,
  inputIconColor,
  red,
  roleBg,
  textColor,
  white,
} from "../constants/colors";
import { Dropdown, Avatar, Space, Row, Col, message, Spin, Modal } from "antd";
import {
  DesktopOutlined,
  FileOutlined,
  PieChartOutlined,
  TeamOutlined,
  UserOutlined,
  LogoutOutlined,
  MailOutlined,
  FundProjectionScreenOutlined,
  ContainerOutlined,
  ExclamationCircleFilled,
  EditOutlined,
} from "@ant-design/icons";
import axios from "axios";
import { baseUrl } from "../utills/axios";
import { useNavigate } from "react-router-dom";
import CustomButton from "../components/customButton";
import { MdKeyboardBackspace } from "react-icons/md";
import HeaderComp from "../components/header";
const CustomDiv = ({ icon, title, onClick }) => {
  return (
    <div
      onClick={onClick}
      style={{
        width: "442px",
        height: "42px",
        display: "flex",
        alignItems: "center",
        gap: "10px",
        background: "#F3F4F6",
        border: "1px solid #D1D5DB",
        paddingLeft: "10px",
        borderRadius: "4px",
        margin: "0 auto",
        marginBottom: "25px",

        color: title == "Logout" ? red : inputIconColor,
      }}
    >
      <p style={{ fontSize: "18px" }}>{icon}</p>
      <p style={{ fontWeight: 500 }}>{title}</p>
    </div>
  );
};

const CustomAssessmentList = ({ list }) => {
  return (
    <div
      style={{
        background: "#F3F4F6",
        border: "1px solid #F3F4F6",
        borderRadius: "8px",
        padding: "20px 40px",
        marginBottom: "30px",
      }}
    >
      <ul>
        {list?.map((data) => (
          <li
            style={{
              marginBottom: "15px",
              textAlign: "start",
              color: textColor,
              fontWeight: 500,
            }}
          >
            {data}
          </li>
        ))}
      </ul>
    </div>
  );
};

const MyAccount = () => {
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const storedData = localStorage.getItem("loginData");

  const [messageApi, contextHolder] = message.useMessage();
  const { confirm } = Modal;
  const loginData = JSON.parse(storedData);

  const navigate = useNavigate();
  const fetchProfile = async () => {
    try {
      const res = await axios.post(
        `${baseUrl}/api/v2/setup/user-profile-id?user_id=${loginData?.user_info?.id}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${loginData?.access_token}`,
          },
        }
      );
      setProfileData(res.data);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    fetchProfile();
  }, []);

  const logOut = async () => {
    localStorage.clear();
    setLoading(true);
    try {
      const res = await axios.post(
        baseUrl + "/api/v2/auth/logout",
        {},
        {
          headers: {
            Authorization: `Bearer ${loginData?.access_token}`,
          },
        }
      );
      if (res?.status === 200) {
        messageApi.open({
          type: "success",
          content: res?.data?.message,
        });
        localStorage.clear("all");
        setLoading(false);
        navigate("/login");
      }
    } catch (error) {
      setLoading(false);
    }
  };

  const showConfirm = () => {
    confirm({
      title: (
        <span style={{ color: "gray" }}>Are you sure you want to log-out?</span>
      ),
      icon: <ExclamationCircleFilled />,
      content: (
        <span style={{ color: "gray" }}>
          Logging out will end your current session. Are you sure you want to
          proceed?
        </span>
      ),
      okText: "yes",
      okType: "primary",
      okButtonProps: {
        // disabled: true,
      },
      cancelText: "No",
      onOk() {
        logOut();
      },
      onCancel() {
        console.log("Cancel");
      },
    });
  };

  const assList = [
    "Community and Social Impact",
    "Water Conservation and Sustainable Resource Use",
    "Other",
  ];
  return (
    <>
      <HeaderComp />
      <Spin size="large" spinning={loading}>
        <div style={{ marginTop: "0px", width: "98%", margin: "0 auto" }}>
          <CustomButton
            style={{
              background: "none",
              boxShadow: "none",
              border: "none",
              fontWeight: 500,
              marginTop: "0px",
              color: textColor,
              display: "flex",
              alignItems: "center",
              gap: "5px",
            }}
            onClick={() => navigate(-1)}
          >
            <MdKeyboardBackspace style={{ fontWeight: 700 }} />
            <p>Back</p>
          </CustomButton>
          <Row>
            <Col
              xs={24}
              lg={9}
              // offset={4}
              style={{
                textAlign: "center",
                padding: "0 10px",
              }}
            >
              <div
                style={{
                  background: white,
                  padding: "20px 20px 1px 20px",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "10px",
                  }}
                >
                  <p
                    style={{
                      fontWeight: 600,
                      fontSize: "20px",
                      color: headings,
                    }}
                  >
                    Personal Information
                  </p>
                  <EditOutlined
                    style={{ color: inputIconColor, fontSize: "20px" }}
                  />
                </div>
                {/* <Avatar
                  size={98}
                  style={{
                    backgroundColor: "#87d068",
                    marginBottom: "50px",
                  }}
                  icon={<UserOutlined />}
                /> */}
                <Avatar
                  size={98}
                  style={{
                    backgroundColor: "#87d068",
                    marginBottom: "50px",
                    fontSize: "30px",
                    fontWeight: 500,
                  }}
                >
                  {profileData?.initials}
                </Avatar>
                <CustomDiv icon={<UserOutlined />} title={profileData?.name} />
                <CustomDiv icon={<MailOutlined />} title={profileData?.email} />

                <CustomDiv
                  icon={<FileOutlined />}
                  title={profileData?.Company}
                />
                <CustomDiv
                  icon={<ContainerOutlined />}
                  title={profileData?.domain}
                />
                <CustomDiv
                  icon={<FundProjectionScreenOutlined />}
                  title={profileData?.role}
                />
                <CustomDiv
                  onClick={showConfirm}
                  icon={<LogoutOutlined />}
                  title="Logout"
                />
              </div>
            </Col>
            <Col
              xs={24}
              lg={15}
              // span={14}
              // offset={4}
              style={{
                textAlign: "center",
                padding: "0 10px",
              }}
            >
              <div
                style={{
                  background: white,
                  padding: "20px",
                  height: "100%",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "30px",
                  }}
                >
                  <p
                    style={{
                      fontWeight: 600,
                      fontSize: "20px",
                      color: headings,
                    }}
                  >
                    My Assessment
                  </p>
                </div>
                <p
                  style={{
                    fontSize: "16px",
                    fontWeight: 500,
                    color: headings,
                    textAlign: "start",
                    marginBottom: "30px",
                  }}
                >
                  1- As {profileData?.role}, which of the following are your top
                  of mind considerations when considering <br /> sustainability?
                  Please select all that apply
                </p>
                <CustomAssessmentList list={profileData?.top_of_mind} />
                <p
                  style={{
                    fontSize: "16px",
                    fontWeight: 500,
                    color: headings,
                    textAlign: "start",
                    marginBottom: "30px",
                  }}
                >
                  2- How do you-ensure data protection and privacy and protect
                  your organization against breaches <br /> and unauthorised
                  access?
                </p>
                <CustomAssessmentList list={profileData?.value_drivers} />
              </div>
            </Col>
          </Row>
        </div>
      </Spin>
    </>
  );
};

export default MyAccount;
