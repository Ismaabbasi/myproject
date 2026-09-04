import React, { useState, useEffect } from "react";
import { Button, message, Steps, theme } from "antd";

import { useDispatch, useSelector } from "react-redux";
import { useNavigate, Outlet, useLocation } from "react-router-dom";
import { cisco, white } from "../constants/colors";
import CustomButton from "../components/customButton";
import axios from "axios";
import { baseUrl } from "../utills/axios";
import CustomSteps from "./customSteps";
import HeaderComp from "../components/header";
const steps = [
  {
    path: "details",
  },
  {
    // title: "Options",
    path: "measurments",
  },
  {
    // title: "Options",
    path: "drivers",
  },
  {
    // title: "Options",
    path: "challenges",
  },

  {
    // title: "persona-overview",
    path: "persona-overview",
  },
  {
    // title: "Insights",
    path: "insights",
  },
  {
    // title: "sustainabilty-IT",
    path: "sustainability",
  },

  {
    path: "variations",
  },
  {
    path: "confirmation",
  },
  {
    path: "feedback",
  },
];

const Home = () => {
  const navigate = useNavigate();
  const [count, setCount] = useState(1);
  const [count2, setCount2] = useState(0);
  const [loading, setLoading] = useState(false);
  const { token } = theme.useToken();
  // const [current, setCurrent] = useState(0);
  const [current, setCurrent] = useState(
    parseInt(localStorage.getItem("currentStep")) || 0
  );
  const currentInStorage = localStorage.getItem("currentStep");
  console.log("current step:", current);

  const location = useLocation();
  const details = useSelector((state) => state.form);
  console.log("stored values before", details);

  const updatedDetails =
    details?.sustainabiltyIT?.flatMap((data) => data?.answers) || [];
  // console.log("stored values after", updatedDetails);
  const storedData = localStorage.getItem("loginData");
  const [messageApi, contextHolder] = message.useMessage();
  const loginData = JSON.parse(storedData);
  useEffect(() => {
    if (!loginData || !loginData.access_token) {
      navigate("/login");
    }
  }, [loginData, navigate]);
  // useEffect(() => {
  //   navigate(steps[current].path);
  // }, [current, navigate]);
  useEffect(() => {
    localStorage.setItem("currentStep", current);
    navigate(steps[current].path);
  }, [current, navigate]);

  useEffect(() => {
    if (count >= 2 && current === 6) {
      navigate(`/home/sustainability/sustainabilty-IT-${count}`);
    } else if (count > 1 && current === 7) {
      navigate(`/home/variations/variations-${count}`);
    }
  }, [count]);
  const next = async () => {
    // setCurrent(current + 1);
    // console.log("hello", current);

    if (current === 0) {
      if (details?.company_name == "") {
        messageApi.open({
          type: "error",
          content: "Please! enter company name",
        });
      } else if (details?.domain_id == "") {
        messageApi.open({
          type: "error",
          content: "Please! select domain",
        });
      } else if (details?.role_id == "") {
        messageApi.open({
          type: "error",
          content: "Please, select your role!",
        });
      } else {
        setLoading(true);
        try {
          const payload = {
            user_id: loginData?.user_info?.id,
            company_name: details?.company_name,
            domain_id: details?.domain_id,
            role_id: details?.role_id,
          };
          const res = await axios.post(
            baseUrl + "/api/v2/setup/user-profile-create",
            payload,
            {
              headers: {
                Authorization: `Bearer ${loginData?.access_token}`,
              },
            }
          );
          if (res.status === 200) {
            setLoading(false);
            messageApi.open({
              type: "success",
              content: res?.data?.message,
            });
            // setTimeout(() => {
            //   setCurrent(current + 1);
            // }, 1000);
            setTimeout(() => {
              setCurrent((prev) => prev + 1);
            }, 1000);
          }
        } catch (error) {
          setLoading(false);
          console.log("error...", error);
        }
      }
    } else if (current === 1) {
      if (details?.measures?.length < 1) {
        messageApi.open({
          type: "error",
          content: "Select at least one option",
        });
      } else {
        try {
          const payload = {
            user_id: loginData?.user_info?.id,
            measures: details?.measures?.filter(
              (item) => item !== "new_measure"
            ),
            new_measure: details?.new_measure,
            sustainability_types_id: 1,
          };
          const res = await axios.post(
            baseUrl + "/api/v2/setup/save-measures",
            payload,
            {
              headers: {
                Authorization: `Bearer ${loginData?.access_token}`,
              },
            }
          );
          if (res.status === 200) {
            messageApi.open({
              type: "success",
              content: res?.data?.message,
            });
            // setTimeout(() => {
            //   setCurrent(current + 1);
            // }, 1000);
            setTimeout(() => {
              setCurrent((prev) => prev + 1);
            }, 1000);
          }
        } catch (error) {
          console.log("error...", error);
        }
      }
    } else if (current === 2) {
      if (details?.drivers?.length < 1) {
        messageApi.open({
          type: "error",
          content: "Select at least one option",
        });
      } else {
        try {
          const payload = {
            user_id: loginData?.user_info?.id,
            measures: details?.drivers?.filter((item) => item !== "other"),
            new_measure: details?.new_measure_driver,
            sustainability_types_id: 2,
          };
          const res = await axios.post(
            baseUrl + "/api/v2/setup/save-measures",
            payload,
            {
              headers: {
                Authorization: `Bearer ${loginData?.access_token}`,
              },
            }
          );
          if (res.status === 200) {
            messageApi.open({
              type: "success",
              content: res?.data?.message,
            });
            // setTimeout(() => {
            //   setCurrent(current + 1);
            // }, 1000);
            setTimeout(() => {
              setCurrent((prev) => prev + 1);
            }, 1000);
          }
        } catch (error) {
          console.log("error...", error);
        }
      }
    } else if (current === 3) {
      if (details?.challenges?.length < 1) {
        messageApi.open({
          type: "error",
          content: "Select at least one option",
        });
      } else {
        try {
          const payload = {
            user_id: loginData?.user_info?.id,
            measures: details?.challenges?.filter((item) => item !== "other"),
            new_measure: details?.new_measure_challenges,
            sustainability_types_id: 3,
          };
          const res = await axios.post(
            baseUrl + "/api/v2/setup/save-measures",
            payload,
            {
              headers: {
                Authorization: `Bearer ${loginData?.access_token}`,
              },
            }
          );
          if (res.status === 200) {
            messageApi.open({
              type: "success",
              content: res?.data?.message,
            });
            // setTimeout(() => {
            //   setCurrent(current + 1);
            // }, 1000);
            setTimeout(() => {
              setCurrent((prev) => prev + 1);
            }, 1000);
          }
        } catch (error) {
          console.log("error...", error);
        }
      }
    } else if (current === 6) {
      window.scrollTo({
        top: 0,
        behavior: "smooth", // Optional: for smooth scrolling
      });
      if (count === 6) {
        try {
          const payload = {
            user_id: loginData?.user_info?.id,
            selected_answers: updatedDetails,
          };
          const res = await axios.post(
            baseUrl + "/api/v2/setup/save-user-answers",
            payload,
            {
              headers: {
                Authorization: `Bearer ${loginData?.access_token}`,
              },
            }
          );
          if (res.status === 200) {
            console.log("save answers:", res);
            messageApi.open({
              type: "success",
              content: res?.data?.message,
            });
            setTimeout(() => {
              setCurrent((prev) => prev + 1);
              // navigate("/home");
            }, 1000);
            setCount(1);
          }
        } catch (error) {
          console.log("error...", error);
        }
      } else {
        if (count === 4 || count === 5) {
          localStorage.setItem("progress", count2 + 20);
          setCount2(count2 + 20);
        } else {
          localStorage.setItem("progress", count2 + 15);
          setCount2(count2 + 15);
        }
        setCount(count + 1);
      }
    } else if (current === 7) {
      if (count === 6) {
        setCurrent((prev) => prev + 1);
      } else {
        setCount(count + 1);
      }
    } else if (current === 9) {
      try {
        setLoading(true);
        const payload = {
          strength: details?.strength,
          improvement: details?.improvement,
          user_id: loginData?.user_info?.id,
        };
        const res = await axios.post(
          baseUrl + "/api/v2/feedback/create-feedback",
          payload,
          {
            headers: {
              Authorization: `Bearer ${loginData?.access_token}`,
            },
          }
        );
        console.log("feedback res:", res);
        if (res.status === 200) {
          setLoading(false);
          messageApi.open({
            type: "success",
            content: res?.data,
          });
        }
        setTimeout(() => {
          setCurrent(4);
        }, 1000);
      } catch (error) {
        setLoading(false);
      }
    } else {
      setCurrent((prev) => prev + 1);
    }
  };

  const prev = () => {
    if (current === 6 && count >= 2) {
      setCount(count - 1);
      navigate(`/home/sustainability/sustainabilty-IT`);
      window.scrollTo({
        top: 0,
        behavior: "smooth", // Optional: for smooth scrolling
      });
    }
    if (current === 7 && count > 1) {
      setCount(count - 1);
    } else {
      setCurrent((prev) => prev - 1);
      window.scrollTo({
        top: 0,
        behavior: "smooth", // Optional: for smooth scrolling
      });
    }
  };

  const items = steps.map((item) => ({
    key: item.title,
    title: item.title,
  }));
  // const items = steps.map((item) => ({
  //   key: item.path,
  //   title: item.path,
  // }));

  const contentStyle = {
    textAlign: "center",
    color: token.colorTextTertiary,
    backgroundColor: white,
    width: current === 7 ? "98%" : "90%",
    minHeight: current === 0 ? "75vh" : current === 2 ? "60vh" : "auto",
    margin: "0 auto",
    marginTop: "0px",
    paddingTop: "15px",
    paddingBottom: "20px",
  };

  return (
    <>
      {contextHolder}

      <HeaderComp />

      <div style={{ padding: "0px 10px" }}>
        <CustomSteps current={current} items={items} />

        <div style={contentStyle}>
          {/* <div style={{ padding: "0 17px" }}> */}
          {/* </div> */}
          <Outlet />
          <div
            className="detail_container"
            style={{
              width:
                current === 1
                  ? "95%"
                  : current === 2
                  ? "95%"
                  : current === 3
                  ? "95%"
                  : current === 4
                  ? "91%"
                  : current === 5
                  ? "87.5%"
                  : current === 9
                  ? "87%"
                  : "93%",
              margin: "0 auto",
              marginTop: 10,
              display: "flex",
              justifyContent: current === 0 ? "end" : "space-between",
            }}
          >
            {current > 0 ? (
              <CustomButton
                style={{
                  background: cisco,
                  color: white,
                  width: "136px",
                  height: "44px",
                }}
                onClick={() => prev()}
              >
                Back
              </CustomButton>
            ) : null}

            <CustomButton
              loading={loading}
              style={{ background: cisco, width: "136px", height: "44px" }}
              type="primary"
              onClick={() => next()}
            >
              {current === 6 && count === 6 ? "Submit" : "Next"}
            </CustomButton>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
