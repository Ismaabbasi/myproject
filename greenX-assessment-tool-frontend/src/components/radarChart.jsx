import React, { useEffect, useState } from "react";
import ReactEcharts from "echarts-for-react";
import axios from "axios";
import { baseUrl } from "../utills/axios";
import { useNavigate } from "react-router-dom";
import { headings } from "../constants/colors";
const RadarChart = ({ chartData }) => {
  const storedData = localStorage.getItem("loginData");
  const loginData = JSON.parse(storedData);
  const [frameworkName, setFrameworkName] = useState("");
  const navigate = useNavigate();
  // const [chartData, setChartData] = useState({
  //   subtypes: [], // Change this to store both name and ID
  //   leadersMaturity: [],
  //   userMaturity: [],
  // });

  // useEffect(() => {
  //   const fetchData = async () => {
  //     const payload = {
  //       user_id: loginData?.user_info?.id,
  //       framework_id: 1,
  //     };
  //     try {
  //       const response = await axios.post(
  //         baseUrl + "/api/v2/chart/get-spider-chart",
  //         payload,
  //         {
  //           headers: {
  //             Authorization: `Bearer ${loginData?.access_token}`,
  //           },
  //         }
  //       );
  //       const data = response.data;
  //       console.log("data res:", data);

  //       if (
  //         data.subtypes &&
  //         data.leaders_maturity_level &&
  //         data.user_maturity_level
  //       ) {
  //         setChartData({
  //           subtypes: data.subtypes.map((subtype) => ({
  //             name: subtype.name,
  //             id: subtype.id, // Store the ID along with the name
  //           })),
  //           leadersMaturity: data.leaders_maturity_level,
  //           userMaturity: data.user_maturity_level,
  //           framework_name: data.framework_name,
  //         });
  //         setFrameworkName(data.framework_name);
  //       }
  //     } catch (error) {
  //       console.error("Error fetching data:", error);
  //     }
  //   };

  //   fetchData();
  // }, []);

  const handleChartClick = (params) => {
    if (params.componentType === "radar" && params.name) {
      // Find the subtype with the clicked name
      const clickedSubtype = chartData.subtypes.find(
        (subtype) => subtype.name === params.name
      );
      if (clickedSubtype) {
        console.log("Clicked subtype ID:", clickedSubtype.id);
        navigate("/edit-subtype", {
          state: {
            id: clickedSubtype.id,
          },
        });
      } else {
        console.log("Subtype not found");
      }
    }
  };

  const isDataValid =
    chartData.subtypes.length > 0 &&
    chartData.leadersMaturity.length > 0 &&
    chartData.userMaturity.length > 0;

  const option = {
    title: {
      text: `Maturity Levels`,
    },
    legend: {
      orient: "vertical",
      right: 10,
      top: 10,
      data: ["Leaders Maturity", "User Maturity"],
    },
    radar: {
      indicator: isDataValid
        ? chartData.subtypes.map((subtype) => ({
            name: subtype.name,
            max: 5, // Assuming the maximum maturity level is 5
            triggerEvent: true,
          }))
        : [],
    },
    series: [
      {
        name: "Leaders vs User Maturity",
        type: "radar",
        data: isDataValid
          ? [
              {
                value: chartData.leadersMaturity,
                name: "Leaders Maturity",
                label: {
                  show: true,
                  formatter: (params) => `${params.value}`, // Show the value on each point
                },
              },
              {
                value: chartData.userMaturity,
                name: "User Maturity",
                label: {
                  show: true,
                  formatter: (params) => `${params.value}`, // Show the value on each point
                },
              },
            ]
          : [],
        itemStyle: {
          emphasis: {
            lineStyle: {
              width: 2,
            },
          },
        },
        lineStyle: {
          width: 2,
        },
      },
    ],
  };

  return (
    <>
      {/* <p
        className=""
        style={{
          color: headings,
          textAlign: "start",
          fontSize: "18px",
          marginBottom: "100px",
        }}
      >
        Below are the versions per sub-dimension for the{" "}
        <strong>{frameworkName}</strong> dimension. The average answer per each
        sub-dimension <br /> will determine your Maturity Level. Click on the
        sub-dimension name to change your answers.
      </p> */}
      <ReactEcharts
        option={option}
        onEvents={{
          click: handleChartClick, // Handle clicks on the radar chart
        }}
      />
    </>
  );
};

export default RadarChart;
