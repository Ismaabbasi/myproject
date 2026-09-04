import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import CustomButton from "../../components/customButton";
import { useNavigate } from "react-router-dom";
const Index = () => {
  return (
    <div>
      <Outlet />
    </div>
  );
};

export default Index;
