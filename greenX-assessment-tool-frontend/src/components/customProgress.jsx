import React from "react";
import { Progress } from "antd";
const CustomProgress = ({ data, strokeColer }) => {
  const prog = localStorage.getItem("progress");

  return (
    <Progress
      strokeColor={strokeColer}
      size={[90, 20]}
      // strokeWidth={8}
      type="circle"
      percent={data}
    />
  );
};

export default CustomProgress;
