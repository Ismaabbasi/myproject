import React from "react";
import styled from "styled-components";
import { Input } from "antd";
import {
  UserOutlined,
  EyeInvisibleOutlined,
  EyeTwoTone,
  LockOutlined,
} from "@ant-design/icons";
import { borderColor } from "../constants/colors";

// Styled component for the input
const StyledInput = styled(Input)`
  ${(props) => props.customStyle && props.customStyle}
  border:1px solid ${borderColor} !important;
  height: 48px !important;
`;

const StyledPasswordInput = styled(Input.Password)`
  ${(props) => props.customStyle && props.customStyle}
  border: 1px solid ${borderColor} !important;
  height: 48px !important;
`;

const CustomInput = ({ placeholder, customStyle, icon, value, ...rest }) => {
  return (
    <StyledInput
      style={{ borderRadius: "4px", ...customStyle }}
      size="large"
      prefix={icon ? icon : <UserOutlined className="site-form-item-icon" />}
      placeholder={placeholder}
      value={value}
      {...rest}
    />
  );
};

// export default CustomInput;
const CustomPasswordInput = ({
  placeholder,
  customStyle,
  icon,
  value,
  ...rest
}) => {
  return (
    <StyledPasswordInput
      style={{ borderRadius: "4px", ...customStyle }}
      size="large"
      iconRender={(visible) =>
        visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />
      }
      prefix={icon ? icon : <LockOutlined className="site-form-item-icon" />}
      placeholder={placeholder}
      value={value}
      {...rest}
    />
  );
};

export default CustomInput;
export { CustomInput, CustomPasswordInput };
