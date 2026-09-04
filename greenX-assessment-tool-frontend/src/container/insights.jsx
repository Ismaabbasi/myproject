import React, { useState, useEffect } from "react";
import { borderColor, headings, textColor } from "../constants/colors";
import { Col, Row } from "antd";
import CustomCard from "../components/customCard";
import CustomProgress from "../components/customProgress";
import axios from "axios";
import { baseUrl } from "../utills/axios";
const style = {
  background: "#0092ff",
  padding: "8px 0",
};
const Insights = () => {
  const [loading, setLoading] = useState(false);
  const [insights, setInsights] = useState();
  const storedData = localStorage.getItem("loginData");
  // const [messageApi, contextHolder] = message.useMessage();
  const loginData = JSON.parse(storedData);
  console.log("login data in insights", loginData);

  const fetchInsights = async () => {
    setLoading(true);
    try {
      const res = await axios.get(
        baseUrl + `/api/v2/setup/compare-measures/${loginData?.user_info?.id}`,
        {
          headers: {
            Authorization: `Bearer ${loginData?.access_token}`,
          },
        }
      );
      if (res.status === 200) {
        // dispatch(setFormData({ [name]: "" }));
        console.log("insights::", res);
        setInsights(res?.data);
        setLoading(false);
      }
    } catch (error) {
      setLoading(false);

      console.log("error...", error);
    }
  };

  useEffect(() => {
    fetchInsights();
  }, []);
  // style={{ margin: "0 100px" }}
  return (
    <Row justify={"center"}>
      <Col xs={22} lg={21}>
        <p
          style={{
            fontSize: "20px",
            fontWeight: 600,
            lineHeight: "30px",
            textAlign: "start",
            color: headings,
            marginBottom: "5px",
          }}
        >
          Insights and Analysis
        </p>
        <Row gutter={16}>
          <Col
            style={{
              padding: "8px 8px",
            }}
            className="gutter-row"
            xs={24}
            sm={12}
            lg={8}
          >
            <CustomCard
              style={{
                borderRadius: "8px",
                borderColor: "#D1D5DB",
                padding: "0px",
              }}
            >
              <div
                style={{
                  // border: "5.54px solid #F3F4F6",
                  boxShadow: "0px 0px 15.54px #F3F4F6",
                  padding: "20px",
                  width: "100px",
                  margin: "0 auto",
                  height: "100px",
                  borderRadius: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "white",
                }}
              >
                <CustomProgress
                  strokeColer="#3B82F6"
                  data={insights?.value_driver_similar}
                />
              </div>
              <p
                style={{ marginTop: "15px", fontWeight: 500, color: textColor }}
              >
                {/* {item.text} */}
                of industry CTOs <strong>align</strong> with your{" "}
                <strong>CTO's</strong> value drivers, positioning you at the
                forefront of sustainability thought leadership.
              </p>
            </CustomCard>
          </Col>
          <Col
            style={{
              padding: "8px 8px",
            }}
            className="gutter-row"
            xs={24}
            sm={12}
            lg={8}
          >
            <CustomCard
              style={{
                borderRadius: "8px",
                borderColor: "#D1D5DB",
                padding: "0px",
              }}
            >
              <div
                style={{
                  // border: "5.54px solid #F3F4F6",
                  boxShadow: "0px 0px 15.54px #F3F4F6",
                  padding: "0px",
                  width: "100px",
                  margin: "0 auto",
                  background: "white",
                  height: "100px",
                  borderRadius: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <CustomProgress
                  strokeColer="#162543"
                  data={insights?.top_of_mind_similar}
                />
              </div>
              <p
                style={{ marginTop: "15px", fontWeight: 500, color: textColor }}
              >
                {/* {item.text} */}
                <strong>alignment on top of mind</strong> within the team here
                which signifies a cohesive strategy and shared mission.
              </p>
            </CustomCard>
          </Col>
          <Col
            style={{
              padding: "8px 8px",
            }}
            className="gutter-row"
            xs={24}
            sm={12}
            lg={8}
          >
            <CustomCard
              style={{
                borderRadius: "8px",
                borderColor: "#D1D5DB",
                padding: "0px",
              }}
            >
              <div
                style={{
                  // border: "5.54px solid #F3F4F6",
                  boxShadow: "0px 0px 15.54px #F3F4F6",
                  padding: "0px",
                  width: "100px",
                  margin: "0 auto",
                  height: "100px",
                  background: "white",
                  borderRadius: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <CustomProgress
                  strokeColer="#C8362D"
                  data={insights?.value_driver_difference}
                />
              </div>
              <p
                style={{ marginTop: "15px", fontWeight: 500, color: textColor }}
              >
                {/* {item.text} */}
                of industry financial leaders follow{" "}
                <strong>different value drivers</strong>, suggesting a potential
                deviation from e financial practices.
              </p>
            </CustomCard>
          </Col>

          <Col
            style={{
              padding: "8px 8px",
            }}
            className="gutter-row"
            xs={24}
            sm={12}
            lg={8}
          >
            <CustomCard
              style={{
                borderRadius: "8px",
                borderColor: "#D1D5DB",
                padding: "0px",
              }}
            >
              <div
                style={{
                  boxShadow: "0px 0px 15.54px #F3F4F6",
                  padding: "0px",
                  width: "100px",
                  margin: "0 auto",
                  height: "100px",
                  borderRadius: "100%",
                  background: "white",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <CustomProgress
                  strokeColer="#E7A040"
                  data={insights?.top_of_mind_similar}
                />
              </div>
              <p
                style={{ marginTop: "15px", fontWeight: 500, color: textColor }}
              >
                of industry CTOs <strong>align</strong> with your{" "}
                <strong>CTO's</strong> value drivers, positioning you at the
                forefront of sustainability thought leadership.
              </p>
            </CustomCard>
          </Col>
          <Col
            style={{
              padding: "8px 8px",
            }}
            className="gutter-row"
            xs={24}
            sm={12}
            lg={8}
          >
            <CustomCard
              style={{
                borderRadius: "8px",
                borderColor: "#D1D5DB",
                padding: "0px",
              }}
            >
              <div
                style={{
                  boxShadow: "0px 0px 15.54px #F3F4F6",
                  padding: "0px",
                  width: "100px",
                  margin: "0 auto",
                  height: "100px",
                  borderRadius: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "white",
                }}
              >
                <CustomProgress
                  strokeColer="#74AE50"
                  data={insights?.top_of_mind_similar}
                />
              </div>
              <p
                style={{ marginTop: "15px", fontWeight: 500, color: textColor }}
              >
                of sustainability leaders in your sector{" "}
                <strong>reflect the same value drivers</strong> as your
                Sustainability Officer.
              </p>
            </CustomCard>
          </Col>
          <Col
            style={{
              padding: "8px 8px",
            }}
            className="gutter-row"
            xs={24}
            sm={12}
            lg={8}
          >
            <CustomCard
              style={{
                borderRadius: "8px",
                borderColor: "#D1D5DB",
                padding: "0px",
              }}
            >
              <div
                style={{
                  boxShadow: "0px 0px 15.54px #F3F4F6",
                  padding: "0px",
                  width: "100px",
                  margin: "0 auto",
                  height: "100px",
                  background: "white",
                  borderRadius: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <CustomProgress
                  strokeColer="#EF4444"
                  data={insights?.top_of_mind_similar}
                />
              </div>
              <p
                style={{ marginTop: "15px", fontWeight: 500, color: textColor }}
              >
                of sustainability leaders in the sector have{" "}
                <strong>differing top of mind</strong> from your Sustainability
                Officer, suggesting realignment with industry norms.
              </p>
            </CustomCard>
          </Col>
        </Row>
      </Col>
    </Row>
  );
};

export default Insights;
