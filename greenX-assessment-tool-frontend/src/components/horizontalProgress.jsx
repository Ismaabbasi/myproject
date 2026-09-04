import React, { useState, useEffect } from "react";
import axios from "axios";
import { baseUrl } from "../utills/axios";
import { Progress } from "antd";
import { cisco } from "../constants/colors";
import { useSelector } from "react-redux";
const HorizontalProgress = () => {
  const total_questions = useSelector(
    (state) => state.questionAnswers?.data?.total_questions
  );
  const details = useSelector((state) => state.form);
  const updatedDetails =
    details?.sustainabiltyIT?.flatMap((data) => data?.answers) || [];

  console.log("totalQuestions", total_questions);

  const answeredQuestions = updatedDetails?.length;

  // Calculate the progress percentage
  const progressPercent = ((answeredQuestions / total_questions) * 100).toFixed(
    2
  );

  return (
    <div>
      <Progress percent={progressPercent} strokeColor={cisco} />
    </div>
  );
};

export default HorizontalProgress;
