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
// const Challenges = () => {
//   const [value, setValue] = useState("");
//   const [measures, setMeasures] = useState();
//   const [tips, setTips] = useState();
//   const dispatch = useDispatch();
//   const storedData = localStorage.getItem("loginData");
//   const loginData = JSON.parse(storedData);
//   const selectedOptions = useSelector(
//     (state) => state.form.selectedOptions || []
//   );
//   const details = useSelector((state) => state.form);
//   const filterOther = details?.challenges?.filter((data) => data == "other");
//   const fetchMeasures = async () => {
//     if (loginData?.has_measures === true) {
//       try {
//         const payload = {
//           sustainability_types_id: "3",
//           // role_id: loginData?.role_id,
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
//           // setMeasures(res?.data?.measures);
//           const updatedMeasures = [
//             ...res?.data?.measures,
//             {
//               id: "other",
//               name: "Other",
//             },
//           ];

//           setMeasures(updatedMeasures);
//           setTips(res?.data);
//         }
//       } catch (error) {
//         console.log("error...", error);
//       }
//     } else {
//       try {
//         const payload = {
//           // domain_id: details?.domain_id,
//           sustainability_types_id: "3",
//           // role_id: details?.role_id,
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
//           // setMeasures(res?.data?.measures);
//           const updatedMeasures = [
//             ...res?.data?.measures,
//             {
//               id: "other",
//               name: "Other",
//             },
//           ];

//           setMeasures(updatedMeasures);
//           setTips(res?.data);
//         }
//       } catch (error) {
//         console.log("error...", error);
//       }
//     }
//   };
//   useEffect(() => {
//     dispatch(setFormData({ new_measure_challenges: value }));
//   }, [value]);
//   useEffect(() => {
//     fetchMeasures();
//   }, []);
//   const onChange = (checkedValues) => {
//     if (checkedValues[0] == "Other") {
//       dispatch(setFormData({ challenges: checkedValues }));
//     } else {
//       dispatch(setFormData({ challenges: checkedValues }));
//     }
//   };

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
//             {details?.role || loginData?.role}
//           </span>
//           , which of the following are your challenges when considering
//           sustainability? Please select all that apply.
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
//               {measures?.map((option) => (
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
//                   {option?.id == "other" && filterOther == "other" ? (
//                     <TextArea
//                       style={{ verticalAlign: "unset", marginTop: "20px" }}
//                       value={value}
//                       onChange={(e) => setValue(e.target.value)}
//                       placeholder="Type here..."
//                       autoSize={{
//                         minRows: 3,
//                         maxRows: 5,
//                       }}
//                     />
//                   ) : null}
//                 </Col>
//               ))}
//               {/* <Col
//             style={{
//               textAlign: "start",
//             }}
//             span={12}
//             key="new_measure"
//           >
//             <CustomCheckbox
//               style={{
//                 color: textColor,
//                 fontWeight: 500,
//                 fontSize: "14px",
//               }}
//               value="new_measure"
//             >
//               Other
//             </CustomCheckbox>

//           </Col> */}
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
//                   Typical {details?.role || loginData?.role} challenges:
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
//                 {tips?.typically_selected_measures?.map((data, index) => (
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
//               </div>
//             </div>
//           </Col>
//         </Row>
//       </Checkbox.Group>
//     </div>
//   );
// };

// export default Challenges;

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

// Styled Components
const Container = styled.div`
  width: 95%;
  margin: 0 auto;
  margin-bottom: 50px;
  line-height: unset;
`;

const Title = styled.p`
  font-size: 20px;
  font-weight: 500;
  line-height: 30px;
  text-align: start;
  color: ${headings};
  margin-bottom: 40px;
`;

const Highlight = styled.span`
  font-weight: 700;
`;

const TipsContainer = styled.div`
  padding: 0 0 0 20px;
  margin-bottom: 20px;
`;

const TipsHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
`;

const TipsCircle = styled.div`
  width: 28px !important;
  height: 28px;
  background: ${cisco};
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const TipsTitle = styled.p`
  font-size: 18px;
  font-weight: 500;
  color: ${headings};
  text-align: start;
`;

const TipsList = styled.div`
  text-align: start;
  background: #f2f4f7;
  padding: 20px 30px;
  border-radius: 10px;
`;

const TipItem = styled.p`
  margin-bottom: 10px;
  font-weight: 500;
  color: ${headings};
`;

const CustomCheckbox = styled(Checkbox)`
  margin-bottom: 10px;

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

const Challenges = () => {
  const [value, setValue] = useState("");
  const [measures, setMeasures] = useState([]);
  const [tips, setTips] = useState({});
  const dispatch = useDispatch();
  const storedData = localStorage.getItem("loginData");
  const loginData = JSON.parse(storedData);
  const details = useSelector((state) => state.form);
  const selectedOptions = useSelector((state) => state.form.challenges || []);

  // Filter to check if "other" is selected
  const isOtherSelected = selectedOptions.includes("other");

  const fetchMeasures = async () => {
    try {
      const payload = { sustainability_types_id: "3" };
      const res = await axios.post(
        `${baseUrl}/api/v2/setup/get-measures`,
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
        const updatedMeasures = [
          ...res.data.measures,
          {
            id: "other",
            name: "Other",
          },
        ];
        setMeasures(updatedMeasures);
        setTips(res.data);
      }
    } catch (error) {
      console.error("Error fetching measures:", error);
    }
  };

  useEffect(() => {
    dispatch(setFormData({ new_measure_challenges: value }));
  }, [value, dispatch]);

  useEffect(() => {
    fetchMeasures();
  }, []);

  const onChange = (checkedValues) => {
    dispatch(setFormData({ challenges: checkedValues }));
  };

  return (
    <Container>
      <Title>
        As <Highlight>{details?.role || loginData?.role}</Highlight>, which of
        the following are your challenges when considering sustainability?
        Please select all that apply.
      </Title>
      <Checkbox.Group
        style={{ width: "100%", display: "unset" }}
        value={selectedOptions}
        onChange={onChange}
      >
        <Row>
          <Col lg={17}>
            <Row justify="center" gutter={[16, 16]}>
              {measures.map((option) => (
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
                      textTransform: "capitalize",
                    }}
                    value={option.id}
                  >
                    {option.name}
                  </CustomCheckbox>
                  {option.id === "other" && isOtherSelected && (
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
                  )}
                </Col>
              ))}
            </Row>
          </Col>
          <Col lg={7}>
            <TipsContainer>
              <TipsHeader>
                <TipsCircle>
                  <MdLightbulbOutline
                    style={{ color: "white", fontSize: "18px" }}
                  />
                </TipsCircle>
                <TipsTitle>
                  Typical {details?.role || loginData?.role} <br /> challenges:
                </TipsTitle>
              </TipsHeader>
              <TipsList>
                {tips?.typically_selected_measures?.map((data, index) => (
                  <TipItem key={index}>
                    {index + 1}. {data?.name}
                  </TipItem>
                ))}
              </TipsList>
            </TipsContainer>
          </Col>
        </Row>
      </Checkbox.Group>
    </Container>
  );
};

export default Challenges;
