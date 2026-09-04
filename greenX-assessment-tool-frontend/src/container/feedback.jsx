import { Col, Row, Input } from "antd";
import React from "react";
import { headings } from "../constants/colors";
import axios from "axios";
import { baseUrl } from "../utills/axios";
import { setFormData } from "../store/formSlice";
import { useDispatch, useSelector } from "react-redux";
const { TextArea } = Input;
const Feedback = () => {
  const dispatch = useDispatch();

  const onChange = (e, id) => {
    const { name, value } = e.target;
    if (id === 1) {
      dispatch(setFormData({ strength: value }));
    } else {
      dispatch(setFormData({ improvement: value }));
    }
  };

  return (
    <div
      style={{ textAlign: "start", padding: "10px 30px", marginBottom: "40px" }}
    >
      <p
        style={{
          marginBottom: "40px",
          color: headings,
          fontSize: "18px",
          fontWeight: 700,
        }}
      >
        As we conclude the workshop, your insights are invaluable to us. Kindly
        share your feedback regarding the entire workshop and its various
        stages. We are committed to continuous improvement, and your
        observations will directly inform our future enhancements.
      </p>
      <Row gutter={[100]} justify="center">
        <Col xs={24} lg={11}>
          <div>
            <p
              style={{
                fontSize: "16px",
                color: headings,
                marginBottom: "20px",
              }}
            >
              <strong>Strengths</strong> - Please detail aspects you found
              favourable and would like to see more of in the future:
            </p>
            <TextArea
              //   maxLength={150}
              onChange={(e) => onChange(e, 1)}
              placeholder="Type here"
              style={{
                height: 250,
                resize: "none",
                background: "#F3F4F6",
                border: "none",
              }}
            />
          </div>
        </Col>
        <Col xs={24} lg={11}>
          <div>
            <p
              style={{
                fontSize: "16px",
                color: headings,
                marginBottom: "20px",
              }}
            >
              <strong>Areas for Improvement</strong> - Highlight any elements
              that could be refined and provide any specific suggestions:
            </p>
            <TextArea
              //   maxLength={150}
              onChange={(e) => onChange(e, 2)}
              placeholder="Type here"
              style={{
                height: 250,
                resize: "none",
                background: "#F3F4F6",
                border: "none",
              }}
            />
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Feedback;
