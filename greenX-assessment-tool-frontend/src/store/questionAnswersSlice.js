import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  data: [],
};

const questionAnswerSlice = createSlice({
  name: "form",
  initialState,
  reducers: {
    setQuestionAnswerData: (state, action) => {
      return { ...state, ...action.payload };
    },
    resetQuestionAnswerData: () => initialState,
  },
});

export const { setQuestionAnswerData, resetQuestionAnswerData } =
  questionAnswerSlice.actions;

export const questionAnswerReducer = questionAnswerSlice.reducer;
