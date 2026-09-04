import React, { useState, useEffect } from "react";
import CustomCard from "../components/customCard";
import { headings, roleBg, textColor } from "../constants/colors";
import { Card, Col, Row, Spin, Table } from "antd";
import CustomTable from "../components/customTable";
import { baseUrl } from "../utills/axios";
import axios from "axios";
const PersonaOverview = () => {
  const storedData = localStorage.getItem("loginData");
  // const [messageApi, contextHolder] = message.useMessage();
  const loginData = JSON.parse(storedData);
  const [userMeasures, setUserMeasures] = useState([]);
  const [loading, setLoading] = useState(false);
  const fetchUserPersona = async () => {
    setLoading(true);
    try {
      const res = await axios.get(baseUrl + `/api/v2/setup/get-persona-all`, {
        headers: {
          Authorization: `Bearer ${loginData?.access_token}`,
        },
      });
      if (res.status === 200) {
        // dispatch(setFormData({ [name]: "" }));
        console.log("persona::", res);
        setUserMeasures(res?.data);
        setLoading(false);
      }
    } catch (error) {
      setLoading(false);

      console.log("error...", error);
    }
  };

  useEffect(() => {
    fetchUserPersona();
  }, []);
  console.log("userMeasures:", userMeasures);
  const tableData = [
    {
      // key: "1",
      profile: userMeasures?.map((item) => item.profile),
      top: userMeasures?.top_of_mind,
      drivers: userMeasures.value_drivers,
      challenges: userMeasures.main_challenges,
    },
  ];
  const colorMap = {
    A: "#add17d",
    B: "#f0a1a8",
    C: "#8dc6ff",
    D: "#ffd700",
    // Add more mappings as needed
  };
  const columns = [
    {
      dataIndex: "profile",
      key: "profile",
      render: (record) => (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "15px",
          }}
        >
          <div
            style={{
              width: "60px",
              height: "60px",
              borderRadius: "100%",
              background: "#add17d",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontWeight: 500,
            }}
          >
            <p>{record?.initials}</p>
          </div>
          <div>
            <p style={{ color: headings, fontSize: "16px", fontWeight: 600 }}>
              {record?.name}
            </p>
            <p style={{ color: textColor }}>{record?.email}</p>
            <p style={{ color: textColor }}>{record?.Company}</p>
            <p
              style={{
                color: textColor,
                background: roleBg,
                borderRadius: "18px",
                height: "22px",
                textAlign: "center",
                fontSize: "12px",
              }}
            >
              {record?.role}
            </p>
          </div>
        </div>
      ),
    },

    {
      title: "Top of Mind",
      dataIndex: "top_of_mind",
      key: "top_of_mind",
      render: (record, text) => (
        <div
          style={{
            padding: "10px",
          }}
        >
          <ul>
            {record?.map((item) => (
              <li style={{ color: textColor }}>{item}</li>
            ))}
          </ul>
        </div>
      ),
    },
    {
      title: "Value Drivers",
      dataIndex: "value_drivers",
      key: "value_drivers",
      render: (record) => (
        <div
          style={{
            padding: "10px",
          }}
        >
          <ul>
            {record?.map((item) => (
              <li style={{ color: textColor }}>{item}</li>
            ))}
          </ul>
        </div>
      ),
    },
    {
      title: "Main Challenges",
      dataIndex: "main_challenges",
      key: "main_challenges",
      render: (record) => (
        <div
          style={{
            padding: "10px",
          }}
        >
          <ul>
            {record?.map((item) => (
              <li style={{ color: textColor }}>{item}</li>
            ))}
          </ul>
        </div>
      ),
    },
  ];
  return (
    <div style={{ margin: "0px 60px 0px 60px" }}>
      <p
        style={{
          fontSize: "20px",
          fontWeight: 600,
          lineHeight: "30px",
          textAlign: "start",
          color: headings,
          marginBottom: "10px",
        }}
      >
        Persona Overview
      </p>
      <Spin spinning={loading}>
        <CustomTable data={userMeasures} columns={columns} />
      </Spin>
    </div>
  );
};

export default PersonaOverview;
