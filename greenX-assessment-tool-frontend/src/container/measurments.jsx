// import React, { useEffect, useState } from "react";
// import styled from "styled-components";
// import { useDispatch, useSelector } from "react-redux";
// import { Checkbox, Row, Col, Input } from "antd";
// import { setFormData } from "../store/formSlice";
// import { cisco, headings, textColor } from "../constants/colors";
// import axios from "axios";
// import { baseUrl } from "../utills/axios";
// import { MdLightbulbOutline } from "react-icons/md";

// const { TextArea } = Input;

// const CustomCheckbox = styled(Checkbox)`
//   margin-bottom: 10px;
//   margin-top: 10px;
//   .ant-checkbox-checked .ant-checkbox-inner {
//     background-color: ${cisco}; /* Change this to your desired color */
//     border-color: ${cisco}; /* Change this to your desired color */
//   }

//   .ant-checkbox-inner {
//     width: 20px; /* Adjust size if needed */
//     height: 20px; /* Adjust size if needed */
//   }

//   &:hover .ant-checkbox-inner,
//   &:hover .ant-checkbox-checked .ant-checkbox-inner {
//     border-color: ${cisco}; /* Change this to your desired color */
//   }
// `;
// const Options = () => {
//   const [value, setValue] = useState("");
//   const [measures, setMeasures] = useState();
//   const dispatch = useDispatch();
//   const storedData = localStorage.getItem("loginData");
//   const loginData = JSON.parse(storedData);
//   const selectedOptions = useSelector(
//     (state) => state.form.selectedOptions || []
//   );
//   const details = useSelector((state) => state.form);
//   const filterOther = details?.measures?.filter(
//     (data) => data == "new_measure"
//   );
//   const fetchMeasures = async () => {
//     if (loginData?.has_top_of_mind === true) {
//       try {
//         const payload = {
//           sustainability_types_id: "1",
//           role_id: loginData?.role_id,
//         };
//         const res = await axios.post(
//           baseUrl + `/api/v2/setup/get-measures`,
//           payload,
//           {
//             headers: {
//               Authorization: `Bearer ${loginData?.access_token}`,
//             },
//             params: {
//               user_id: loginData?.user_info?.id,
//             },
//           }
//         );
//         if (res.status === 200) {
//           // dispatch(setFormData({ [name]: "" }));
//           setMeasures(res?.data);
//         }
//       } catch (error) {
//         console.log("error...", error);
//       }
//     } else {
//       try {
//         const payload = {
//           // domain_id: details?.domain_id,
//           sustainability_types_id: "1",
//           role_id: details?.role_id || loginData?.role_id,
//         };
//         const res = await axios.post(
//           baseUrl + "/api/v2/setup/get-measures",
//           payload,
//           {
//             headers: {
//               Authorization: `Bearer ${loginData?.access_token}`,
//             },
//           }
//         );
//         if (res.status === 200) {
//           // dispatch(setFormData({ [name]: "" }));
//           setMeasures(res?.data);
//         }
//       } catch (error) {
//         console.log("error...", error);
//       }
//     }
//   };
//   useEffect(() => {
//     dispatch(setFormData({ new_measure: value }));
//   }, [value]);
//   useEffect(() => {
//     fetchMeasures();
//   }, []);
//   const onChange = (checkedValues) => {
//     if (checkedValues[0] == "Other") {
//       dispatch(setFormData({ measures: checkedValues }));
//     } else {
//       dispatch(setFormData({ measures: checkedValues }));
//     }
//   };

//   console.log("measures....", measures);

//   return (
//     <div
//       style={{
//         width: "95%",
//         margin: "0 auto",
//         marginBottom: "50px",
//         lineHeight: "unset",
//       }}
//     >
//       <div>
//         <p
//           style={{
//             fontSize: "20px",
//             fontWeight: 500,
//             lineHeight: "30px",
//             textAlign: "start",
//             color: headings,
//             marginBottom: "40px",
//           }}
//         >
//           As{" "}
//           <span style={{ fontWeight: 700 }}>
//             {" "}
//             {details?.role || loginData?.role}
//           </span>
//           , which of the following are your top of mind considerations when
//           considering sustainability? <br /> Please select all that apply.
//         </p>
//       </div>
//       <Checkbox.Group
//         style={{ width: "100%", display: "unset" }}
//         defaultValue={[]}
//         onChange={onChange}
//       >
//         <Row>
//           <Col lg={17}>
//             <Row justify={"center"} gutter={[16, 16]}>
//               {measures?.measures?.map((option) => (
//                 <Col
//                   style={{
//                     textAlign: "start",
//                   }}
//                   span={12}
//                   key={option?.id}
//                 >
//                   <CustomCheckbox
//                     style={{
//                       color: textColor,
//                       fontWeight: 500,
//                       fontSize: "14px",
//                     }}
//                     value={option?.id}
//                   >
//                     {option?.name}
//                   </CustomCheckbox>
//                 </Col>
//               ))}
//               <Col
//                 style={{
//                   textAlign: "start",
//                 }}
//                 span={12}
//                 key="new_measure"
//               >
//                 <CustomCheckbox
//                   style={{
//                     color: textColor,
//                     fontWeight: 500,
//                     fontSize: "14px",
//                   }}
//                   value="new_measure"
//                 >
//                   Other
//                 </CustomCheckbox>
//                 {filterOther[0] == "new_measure" ? (
//                   <TextArea
//                     style={{ verticalAlign: "unset", marginTop: "20px" }}
//                     value={value}
//                     onChange={(e) => setValue(e.target.value)}
//                     placeholder="Type here..."
//                     autoSize={{
//                       minRows: 3,
//                       maxRows: 5,
//                     }}
//                   />
//                 ) : null}
//               </Col>
//             </Row>
//           </Col>
//           <Col lg={7}>
//             <div
//               style={{
//                 padding: "0 0px 0 20px",
//                 marginBottom: "20px",
//               }}
//             >
//               <div
//                 style={{
//                   display: "flex",
//                   alignItems: "center",
//                   gap: "10px",
//                   marginBottom: "20px",
//                 }}
//               >
//                 <p
//                   style={{
//                     width: "28px",
//                     height: "28px",
//                     background: cisco,
//                     borderRadius: "100%",
//                     display: "flex",
//                     justifyContent: "center",
//                     alignItems: "center",
//                   }}
//                 >
//                   <MdLightbulbOutline
//                     style={{ color: "white", fontSize: "18px" }}
//                   />
//                 </p>
//                 <p
//                   style={{
//                     fontSize: "20px",
//                     fontWeight: 500,
//                     color: headings,
//                     textAlign: "start",
//                   }}
//                 >
//                   Typical {details?.role || loginData?.role} top of mind:
//                 </p>
//               </div>
//               <div
//                 style={{
//                   textAlign: "start",
//                   background: "#f2f4f7",
//                   padding: "20px 30px",
//                   borderRadius: "10px",
//                 }}
//               >
//                 {measures?.typically_selected_measures?.map((data, index) => (
//                   <p
//                     style={{
//                       marginBottom: "10px",
//                       fontWeight: 500,
//                       color: headings,
//                     }}
//                   >
//                     {index + 1}. {data?.name}
//                   </p>
//                 ))}
//                 {/* <p
//                   style={{
//                     marginBottom: "10px",
//                     fontWeight: 500,
//                     color: headings,
//                   }}
//                 >
//                   1. Energy-efficient data centers and remote technologies to
//                   reduce organizational carbon footprints.
//                 </p>
//                 <p
//                   style={{
//                     marginBottom: "10px",
//                     fontWeight: 500,
//                     color: headings,
//                   }}
//                 >
//                   Consider the technological tools in place for data
//                   safeguarding.
//                 </p>
//                 <p
//                   style={{
//                     marginBottom: "10px",
//                     fontWeight: 500,
//                     color: headings,
//                   }}
//                 >
//                   Think about your organization's dedicated cybersecurity team
//                   or expert.
//                 </p>
//                 <p
//                   style={{
//                     marginBottom: "10px",
//                     fontWeight: 500,
//                     color: headings,
//                   }}
//                 >
//                   Reflect on past data breaches and the organization's response.
//                 </p>
//                 <p
//                   style={{
//                     // marginBottom: "20px",
//                     fontWeight: 500,
//                     color: headings,
//                   }}
//                 >
//                   Remember how often data protection updates are communicated to
//                   employees.
//                 </p> */}
//               </div>
//             </div>
//           </Col>
//         </Row>
//       </Checkbox.Group>
//     </div>
//   );
// };

// export default Options;

import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { useDispatch, useSelector } from "react-redux";
import { Checkbox, Row, Col, Input } from "antd";
import { setFormData } from "../store/formSlice";
import { cisco, headings, textColor } from "../constants/colors";
import axios from "axios";
import { baseUrl } from "../utills/axios";
import { MdLightbulbOutline } from "react-icons/md";

const { TextArea } = Input;

const CustomCheckbox = styled(Checkbox)`
  margin-bottom: 10px;
  margin-top: 10px;
  .ant-checkbox-checked .ant-checkbox-inner {
    background-color: ${cisco}; /* Change this to your desired color */
    border-color: ${cisco}; /* Change this to your desired color */
  }

  .ant-checkbox-inner {
    width: 20px; /* Adjust size if needed */
    height: 20px; /* Adjust size if needed */
  }

  &:hover .ant-checkbox-inner,
  &:hover .ant-checkbox-checked .ant-checkbox-inner {
    border-color: ${cisco}; /* Change this to your desired color */
  }
`;

const Options = () => {
  const [value, setValue] = useState("");
  const [measures, setMeasures] = useState();
  const dispatch = useDispatch();
  const storedData = localStorage.getItem("loginData");
  const loginData = JSON.parse(storedData);

  // Get selected options from Redux store
  const selectedOptions = useSelector((state) => state.form.measures || []);

  const details = useSelector((state) => state.form);

  const filterOther = selectedOptions.includes("new_measure");

  const fetchMeasures = async () => {
    if (loginData?.has_top_of_mind === true) {
      try {
        const payload = {
          sustainability_types_id: "1",
          role_id: loginData?.role_id,
        };
        const res = await axios.post(
          baseUrl + `/api/v2/setup/get-measures`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${loginData?.access_token}`,
            },
            params: {
              user_id: loginData?.user_info?.id,
            },
          }
        );
        if (res.status === 200) {
          setMeasures(res?.data);
        }
      } catch (error) {
        console.log("error...", error);
      }
    } else {
      try {
        const payload = {
          sustainability_types_id: "1",
          role_id: details?.role_id || loginData?.role_id,
        };
        const res = await axios.post(
          baseUrl + "/api/v2/setup/get-measures",
          payload,
          {
            headers: {
              Authorization: `Bearer ${loginData?.access_token}`,
            },
          }
        );
        if (res.status === 200) {
          setMeasures(res?.data);
        }
      } catch (error) {
        console.log("error...", error);
      }
    }
  };

  useEffect(() => {
    fetchMeasures();
  }, []);

  useEffect(() => {
    // Store the 'Other' field value in the Redux store
    dispatch(setFormData({ new_measure: value }));
  }, [value]);

  const onChange = (checkedValues) => {
    dispatch(setFormData({ measures: checkedValues }));
  };

  return (
    <div
      style={{
        width: "95%",
        margin: "0 auto",
        marginBottom: "50px",
        lineHeight: "unset",
      }}
    >
      <div>
        <p
          style={{
            fontSize: "20px",
            fontWeight: 500,
            lineHeight: "30px",
            textAlign: "start",
            color: headings,
            marginBottom: "40px",
          }}
        >
          As{" "}
          <span style={{ fontWeight: 700 }}>
            {details?.role || loginData?.role}
          </span>
          , which of the following are your top of mind considerations when
          considering sustainability? <br /> Please select all that apply.
        </p>
      </div>
      <Checkbox.Group
        style={{ width: "100%", display: "unset" }}
        defaultValue={selectedOptions} // Set initial value from Redux
        onChange={onChange}
      >
        <Row>
          <Col lg={17}>
            <Row justify={"center"} gutter={[16, 16]}>
              {measures?.measures?.map((option) => (
                <Col
                  style={{
                    textAlign: "start",
                  }}
                  span={12}
                  key={option?.id}
                >
                  <CustomCheckbox
                    style={{
                      color: textColor,
                      fontWeight: 500,
                      fontSize: "14px",
                    }}
                    value={option?.id}
                  >
                    {option?.name}
                  </CustomCheckbox>
                </Col>
              ))}
              <Col
                style={{
                  textAlign: "start",
                }}
                span={12}
                key="new_measure"
              >
                <CustomCheckbox
                  style={{
                    color: textColor,
                    fontWeight: 500,
                    fontSize: "14px",
                  }}
                  value="new_measure"
                >
                  Other
                </CustomCheckbox>
                {filterOther ? (
                  <TextArea
                    style={{ verticalAlign: "unset", marginTop: "20px" }}
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    placeholder="Type here..."
                    autoSize={{
                      minRows: 3,
                      maxRows: 5,
                    }}
                  />
                ) : null}
              </Col>
            </Row>
          </Col>
          <Col lg={7}>
            <div
              style={{
                padding: "0 0px 0 20px",
                marginBottom: "20px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  marginBottom: "20px",
                }}
              >
                <p
                  style={{
                    width: "28px",
                    height: "28px",
                    background: cisco,
                    borderRadius: "100%",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                >
                  <MdLightbulbOutline
                    style={{ color: "white", fontSize: "18px" }}
                  />
                </p>
                <p
                  style={{
                    fontSize: "20px",
                    fontWeight: 500,
                    color: headings,
                    textAlign: "start",
                  }}
                >
                  Typical {details?.role || loginData?.role} top of mind:
                </p>
              </div>
              <div
                style={{
                  textAlign: "start",
                  background: "#f2f4f7",
                  padding: "20px 30px",
                  borderRadius: "10px",
                }}
              >
                {measures?.typically_selected_measures?.map((data, index) => (
                  <p
                    key={index}
                    style={{
                      marginBottom: "10px",
                      fontWeight: 500,
                      color: headings,
                    }}
                  >
                    {index + 1}. {data?.name}
                  </p>
                ))}
              </div>
            </div>
          </Col>
        </Row>
      </Checkbox.Group>
    </div>
  );
};

export default Options;
