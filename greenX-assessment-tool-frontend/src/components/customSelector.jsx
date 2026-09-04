import React from "react";
import { DownOutlined } from "@ant-design/icons";
import { Select } from "antd";
import styled from "styled-components";
import { borderColor } from "../constants/colors";

const StyledSelect = styled(Select)`
  .ant-select-selector {
    height: ${(props) => props.height || "48px"} !important;
    border-radius: ${(props) => props.borderRadius || "4px"} !important;
    background-color: ${(props) =>
      props.backgroundColor || "#ffffff"} !important;
    color: ${(props) => props.color || "#000000"} !important;
    border: 1px solid ${borderColor} !important;

    &:hover {
      border-color: ${(props) => props.hoverBorderColor || ""} !important;
    }

    .ant-select-selection-placeholder {
      color: ${(props) => props.placeholderColor || "#bfbfbf"} !important;
      opacity: 1 !important; /* Ensure placeholder is visible */
      display: flex;
      align-items: center;
    }

    .ant-select-selection-item {
      color: ${(props) => props.color || "#000000"} !important;
      display: flex;
      align-items: center;
    }
  }
`;

const CustomSelector = ({ options, onChange, style, icon, ...rest }) => {
  return (
    <StyledSelect
      size="large"
      defaultValue={options?.label}
      onChange={onChange}
      options={options}
      style={style}
      // dropdownClassName="custom-dropdown"
      suffixIcon={icon || <DownOutlined />}
      {...rest}
    />
  );
};

export default CustomSelector;
