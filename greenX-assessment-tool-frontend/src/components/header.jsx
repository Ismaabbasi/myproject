import React, { useEffect, useState } from "react";
import {
  DesktopOutlined,
  FileOutlined,
  PieChartOutlined,
  TeamOutlined,
  UserOutlined,
  LogoutOutlined,
  ExclamationCircleFilled,
} from "@ant-design/icons";
import { DownOutlined } from "@ant-design/icons";
import { Dropdown, Avatar, Space } from "antd";
import { Breadcrumb, Layout, Menu, theme, message, Modal } from "antd";
import {
  headings,
  lightredBg,
  placeholderColor,
  red,
  textColor,
} from "../constants/colors";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { baseUrl } from "../utills/axios";
const { Header, Content, Footer, Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}

const HeaderComp = () => {
  const [collapsed, setCollapsed] = useState(false);
  const storedData = localStorage.getItem("loginData");
  const loginData = JSON.parse(storedData);
  const [messageApi, contextHolder] = message.useMessage();
  const { confirm } = Modal;

  const navigate = useNavigate();
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const logOut = async () => {
    localStorage.clear();

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
        navigate("/login");
      }
    } catch (error) {}
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
      okText: "Yes",
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
  const items = [
    {
      label: (
        <div style={{ textAlign: "center" }}>
          <Avatar
            size={64}
            style={{
              backgroundColor: "#87d068",
            }}
            icon={<UserOutlined />}
          />
        </div>
      ),
      key: "0",
    },
    {
      label: (
        <div style={{ textAlign: "center" }}>
          <p style={{ fontWeight: 500 }}>{loginData?.user_info?.name}</p>
          <p>{loginData?.user_info?.email}</p>
        </div>
      ),
      key: "1",
    },
    {
      label: (
        <div style={{ textAlign: "center" }}>
          {/* <p>shahmasood.dev@gmail.com</p> */}
        </div>
      ),
      key: "2",
    },
    {
      label: (
        <div
          style={{
            fontWeight: 500,
            display: "flex",
            alignItems: "center",
            gap: "10px",
          }}
        >
          <UserOutlined />
          <p
            style={{ fontWeight: 500 }}
            onClick={() => navigate("/my-account")}
          >
            My Profile
          </p>
        </div>
      ),
      key: "3",
    },
    {
      type: "divider",
    },
    {
      label: (
        <div
          onClick={showConfirm}
          style={{
            fontWeight: 500,
            display: "flex",
            //   justifyContent: "space-between",
            alignItems: "center",
            gap: "10px",
            color: red,
            // background: lightredBg,
            // padding: "5px 10px",
            borderRadius: "4px",
            width: "200px",
            marginBottom: "10px",
          }}
        >
          <LogoutOutlined />
          <p>Logout</p>
        </div>
      ),
      key: "4",
    },
  ];
  return (
    <>
      {contextHolder}

      <Header
        style={{
          background: colorBgContainer,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "0 30px",
        }}
      >
        <p className="project_title" style={{ fontWeight: 700 }}>
          Sustainability Priority Assessment Tool
        </p>
        <div>
          <Dropdown
            menu={{
              items,
            }}
            trigger={["click"]}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "5px",
              }}
            >
              <Avatar
                style={{
                  backgroundColor: "#87d068",
                }}
                icon={<UserOutlined />}
              />

              <div className="mobile_none" style={{ lineHeight: "100px" }}>
                <p
                  style={{
                    lineHeight: "20px",
                    color: headings,
                    fontWeight: 600,
                  }}
                >
                  {loginData?.user_info?.name}
                </p>
                <p
                  style={{
                    lineHeight: "20px",
                    color: textColor,
                    fontSize: "12px",
                  }}
                >
                  {loginData?.user_info?.email}
                </p>
              </div>
            </div>
          </Dropdown>
        </div>
      </Header>
    </>
  );
};
export default HeaderComp;
