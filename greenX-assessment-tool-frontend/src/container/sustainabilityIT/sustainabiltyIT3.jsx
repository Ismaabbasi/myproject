import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Checkbox, Row, Col, Input, Spin, message } from "antd";
import styled from "styled-components";
import { setFormData } from "../../store/formSlice";
import { headings, textColor, cisco } from "../../constants/colors";
import axios from "axios";
import { baseUrl } from "../../utills/axios";
import { MdLightbulbOutline } from "react-icons/md";
import HorizontalProgress from "../../components/horizontalProgress";
import { FaComments } from "react-icons/fa";
import CustomButton from "../../components/customButton";

const { Group: CheckboxGroup } = Checkbox;

const { TextArea } = Input;

const plainOptions = [
  "Ad hoc or reactive: lack of a formal data protection strategy: ad hoc measures to address privacy concerns; basic compliance with relevant data protection regulations (no comprehensive framework in place, limited awareness of data privacy risks and minimal employee training on data protection practices",
  "Initial compliance: some formal data protection practices and policies in place",
  "Meet the minimum requirements of data protection regulations; basic data protection awareness training provided to employees",
  "Defined and managed: well-defined data protection and privacy policies and procedures in place; compliance via constant monitoring of data protection regulations and standards; regular training of employees and communication on data protection",
  "Proactive and continuously improvement: proactive approach to identifying and mitigating data privacy risks and vulnerabilities; adoption of data protection best practices; a strong culture of data protection with ongoing training and the reinforcement of privacy principles",
  "Mature and integrated: data protection and privacy are fully integrated into the business processes and technciogy",
];

const StyledCheckboxGroup = styled(Checkbox.Group)`
  width: 100%;
  display: unset;
`;

const StyledCheckbox = styled(Checkbox)`
  color: ${textColor};
  font-weight: 500;
  font-size: 14px;
  .ant-checkbox-wrapper {
    display: flex;
    align-items: start;
  }

  .ant-checkbox {
    margin-top: 4px;
    margin-right: 10px;
  }
  .ant-checkbox-checked .ant-checkbox-inner {
    background-color: ${cisco}; /* Change this to your desired color */
    border-color: ${cisco}; /* Change this to your desired color */
  }
  &:hover .ant-checkbox-inner,
  &:hover .ant-checkbox-checked .ant-checkbox-inner {
    border-color: ${cisco}; /* Change this to your desired color */
  }
`;

const Container = styled.div`
  width: 95%;
  margin: 0 auto;
  margin-bottom: 50px !important;
  line-height: unset;
`;

const Title = styled.p`
  font-size: 20px;
  font-weight: 600;
  line-height: 30px;
  text-align: start;
  color: ${headings};
  margin-bottom: 30px;
`;

const Question = styled.p`
  font-size: 16px;
  font-weight: 500;
  line-height: 30px;
  text-align: start;
  color: ${headings};
  margin-bottom: 30px;
`;

const SustainabiltyIT3 = () => {
  const [value, setValue] = useState("");
  const dispatch = useDispatch();
  const storedData = localStorage.getItem("loginData");
  const loginData = JSON.parse(storedData);
  const [questionAnswers, setQuestionAnswers] = useState();
  const [loading, setLoading] = useState(false);
  const [index, setIndex] = useState(0);
  const details = useSelector((state) => state.form);
  const [selectedAnswers, setSelectedAnswers] = useState([]);
  const [comments, setComments] = useState({});
  const [messageApi, contextHolder] = message.useMessage();
  const questionAns = useSelector(
    (state) => state.questionAnswers?.data?.question_answer[2]
  );

  const addComment = async (question_id) => {
    console.log("questionAns......", questionAns);

    const payload = {
      user_id: loginData?.user_info?.id,
      question_id,
      comment: comments[question_id],
    };
    try {
      setLoading(true);
      const res = await axios.post(
        baseUrl + "/api/v2/comment/create-comment",
        payload,
        {
          headers: {
            Authorization: `Bearer ${loginData?.access_token}`,
          },
        }
      );
      if (res?.status === 200) {
        setLoading(false);
        setComments({});
        messageApi.open({
          // className: "custom-error-message",
          type: "success",
          content: "Comment Added Successfully",
        });
      }
      console.log("comment res:", res);
    } catch (error) {
      setLoading(false);

      console.log("error::", error);
      messageApi.open({
        // className: "custom-error-message",
        type: "error",
        content: "Something Went Wrong",
      });
    }
  };
  const handleCommentChange = (question_id, value) => {
    setComments((prevComments) => ({
      ...prevComments,
      [question_id]: value,
    }));
  };

  const onChange = (checkedValues, question_id) => {
    // Update the selected answers array
    const updatedAnswers = selectedAnswers.filter(
      (answer) => answer.question_id !== question_id
    );
    updatedAnswers.push({ question_id, answers: checkedValues });

    setSelectedAnswers(updatedAnswers);

    // Prepare the new state
    const newSustainabilityIT = [
      ...(details.sustainabiltyIT || []).filter(
        (answer) =>
          !updatedAnswers.find((upd) => upd.question_id === answer.question_id)
      ),
      ...updatedAnswers,
    ];

    // Dispatch the updated state
    dispatch(
      setFormData({
        sustainabiltyIT: newSustainabilityIT,
      })
    );
  };
  const getCheckedValues = (question_id) => {
    const question = selectedAnswers.find(
      (answer) => answer.question_id === question_id
    );
    return question ? question.answers : [];
  };

  return (
    <>
      {contextHolder}
      <Spin spinning={loading}>
        <Container>
          <div>
            <Title>
              Sustainability Maturity Assessment - {questionAns?.framework_name}
            </Title>
            <HorizontalProgress />
            {questionAns?.subtypes_values?.map((data, index) => (
              <div
                key={index}
                style={{ marginBottom: "20px", marginTop: "20px" }}
              >
                <p
                  style={{
                    textAlign: "start",
                    marginBottom: "30px",
                    color: "black",
                    fontSize: "18px",
                    fontWeight: 600,
                  }}
                >
                  {data?.subtype_name}
                </p>
                <Row>
                  {data?.question_values?.map((question, qIndex) => (
                    <Row>
                      <Col lg={16}>
                        <div
                          key={qIndex}
                          style={{
                            marginBottom: "100px",
                            padding: "0 20px 0 0px",
                          }}
                        >
                          <Question>
                            Q{qIndex + 1}.{question?.question}
                          </Question>
                          <StyledCheckboxGroup
                            value={getCheckedValues(question.question_id)}
                            onChange={(checkedValues) =>
                              onChange(checkedValues, question.question_id)
                            }
                          >
                            <Row justify="center" gutter={[16, 16]}>
                              {question?.answer_values?.map(
                                (option, optionIndex) => (
                                  <Col
                                    style={{ textAlign: "start" }}
                                    span={24}
                                    key={optionIndex}
                                  >
                                    <StyledCheckbox value={option.answer_id}>
                                      {option.answer}
                                    </StyledCheckbox>
                                  </Col>
                                )
                              )}
                            </Row>
                          </StyledCheckboxGroup>
                        </div>
                      </Col>
                      <Col lg={8}>
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
                              Here are some tips for you
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
                            <p
                              style={{
                                marginBottom: "10px",
                                fontWeight: 500,
                                color: headings,
                              }}
                            >
                              Recall any data protection training or workshops
                              attended.
                            </p>
                            <p
                              style={{
                                marginBottom: "10px",
                                fontWeight: 500,
                                color: headings,
                              }}
                            >
                              Consider the technological tools in place for data
                              safeguarding.
                            </p>
                            <p
                              style={{
                                marginBottom: "10px",
                                fontWeight: 500,
                                color: headings,
                              }}
                            >
                              Think about your organization's dedicated
                              cybersecurity team or expert.
                            </p>
                            <p
                              style={{
                                marginBottom: "10px",
                                fontWeight: 500,
                                color: headings,
                              }}
                            >
                              Reflect on past data breaches and the
                              organization's response.
                            </p>
                            <p
                              style={{
                                // marginBottom: "20px",
                                fontWeight: 500,
                                color: headings,
                              }}
                            >
                              Remember how often data protection updates are
                              communicated to employees.
                            </p>
                          </div>
                        </div>

                        <div style={{ padding: "0 0px 0 20px" }}>
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center",
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
                                <FaComments
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
                                Additional Comments:
                              </p>
                            </div>
                            {comments[question.question_id] && (
                              <CustomButton
                                style={{
                                  height: "25px",
                                  fontSize: "12px",
                                  fontWeight: 500,
                                }}
                                onClick={() =>
                                  addComment(question?.question_id)
                                }
                              >
                                Save
                              </CustomButton>
                            )}
                          </div>
                          <div
                            style={{
                              textAlign: "start",

                              borderRadius: "10px",
                            }}
                          >
                            <TextArea
                              value={comments[question.question_id] || ""}
                              placeholder="Add comment here..."
                              onChange={(e) =>
                                handleCommentChange(
                                  question.question_id,
                                  e.target.value
                                )
                              }
                              autoSize={{
                                minRows: 3,
                                maxRows: 5,
                              }}
                              style={{ background: "#f2f4f7" }}
                            />
                          </div>
                        </div>
                      </Col>
                    </Row>
                  ))}
                </Row>
              </div>
            ))}
          </div>
        </Container>
      </Spin>
    </>
  );
};

export default SustainabiltyIT3;
