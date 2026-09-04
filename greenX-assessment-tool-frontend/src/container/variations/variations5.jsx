import React, { useState, useEffect } from "react";
import { headings } from "../../constants/colors";
import RadarChart from "../../components/radarChart";
import axios from "axios";
import { baseUrl } from "../../utills/axios";
const Variations5 = () => {
  const storedData = localStorage.getItem("loginData");
  const loginData = JSON.parse(storedData);
  const [frameworkName, setFrameworkName] = useState("");

  // const navigate = useNavigate();
  const [chartData, setChartData] = useState({
    subtypes: [], // Change this to store both name and ID
    leadersMaturity: [],
    userMaturity: [],
  });

  useEffect(() => {
    const fetchData = async () => {
      const payload = {
        user_id: loginData?.user_info?.id,
        framework_id: 5,
      };
      try {
        const response = await axios.post(
          baseUrl + "/api/v2/chart/get-spider-chart",
          payload,
          {
            headers: {
              Authorization: `Bearer ${loginData?.access_token}`,
            },
          }
        );
        const data = response.data;
        console.log("data res:", data);

        if (
          data.subtypes &&
          data.leaders_maturity_level &&
          data.user_maturity_level
        ) {
          setChartData({
            subtypes: data.subtypes.map((subtype) => ({
              name: subtype.name,
              id: subtype.id, // Store the ID along with the name
            })),
            leadersMaturity: data.leaders_maturity_level,
            userMaturity: data.user_maturity_level,
            framework_name: data.framework_name,
          });
          setFrameworkName(data.framework_name);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);
  return (
    <div style={{ width: "95%", margin: "0 auto" }}>
      <p
        className=""
        style={{
          color: headings,
          textAlign: "start",
          fontSize: "18px",
          marginBottom: "100px",
          marginTop: "20px",
        }}
      >
        Below are the versions per sub-dimension for the{" "}
        <strong>{frameworkName}</strong> dimension. The average answer per each
        sub-dimension <br /> will determine your Maturity Level. Click on the
        sub-dimension name to change your answers.
      </p>
      <RadarChart chartData={chartData} />
    </div>
  );
};

export default Variations5;
