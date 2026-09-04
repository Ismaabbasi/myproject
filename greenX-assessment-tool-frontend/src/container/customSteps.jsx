import React from "react";
import styled from "styled-components";
import { Steps } from "antd";
import { progressLine } from "../constants/colors";

const StyledSteps = styled(Steps)`
  display: flex;
  height: 7px;
  margin-top: 10px;
  .ant-steps-item {
    flex: 1;
    min-width: 0; /* Ensure steps shrink */
  }

  .ant-steps-item-finish .ant-steps-icon-dot,
  .ant-steps-item-process .ant-steps-icon-dot,
  .ant-steps-item-process .ant-steps-item-icon,
  .ant-steps-item-finish .ant-steps-item-tail::after {
    background-color: ${progressLine} !important;
    border-color: ${progressLine} !important;
  }

  .ant-steps-item-wait .ant-steps-item-icon,
  .ant-steps-item-process .ant-steps-item-tail::after {
    background-color: #yourColor !important;
    border-color: #yourColor !important;
    color: green !important;
  }

  .ant-steps-item-icon {
    display: flex;
    align-items: center;
    justify-content: center;
  }
`;

const CustomSteps = ({ current, items }) => {
  return <StyledSteps current={current} progressDot="dot" items={items} />;
};

export default CustomSteps;
