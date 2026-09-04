import React from "react";
import { createBrowserRouter } from "react-router-dom";
import { Navigate } from "react-router-dom";
import LogIn from "../container/logIn";
import SignUp from "../container/signUp";
import Home from "../container/home";
import Details from "../container/details";
import Options from "../container/measurments";
import PersonaOverview from "../container/personaOverview";
import Insights from "../container/insights";
import EnterOTP from "../container/forgotPassword/enterOTP";
import { ForgotPassword } from "../container/forgotPassword/forgotPassword";
import NewPassword from "../container/forgotPassword/newPassword";
import HeaderComp from "../components/header";
import MyAccount from "../container/myAccount";
import Drivers from "../container/drivers";
import Challenges from "../container/challenges";
import Sustainability from "../container/sustainabilityIT";
import SustainabiltyIT from "../container/sustainabilityIT/sustainabiltyIT";
import SustainabiltyIT2 from "../container/sustainabilityIT/sustainabiltyIT2";
import SustainabiltyIT3 from "../container/sustainabilityIT/sustainabiltyIT3";
import SustainabiltyIT4 from "../container/sustainabilityIT/sustainabiltyIT4";
import SustainabiltyIT5 from "../container/sustainabilityIT/sustainabiltyIT5";
import SustainabiltyIT6 from "../container/sustainabilityIT/sustainabiltyIT6";
import Variations from "../container/variations";
import EditSubType from "../container/editSubType";
import Variations2 from "../container/variations/variations2";
import Variations1 from "../container/variations/variations1";
import Variations3 from "../container/variations/variations3";
import Variations4 from "../container/variations/variations4";
import Variations5 from "../container/variations/variations5";
import Variations6 from "../container/variations/variations6";
import Confirmation from "../container/confirmation";
import Feedback from "../container/feedback";
const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="login" replace />,
  },
  {
    path: "login",
    element: <LogIn />,
  },
  {
    path: "sign-up",
    element: <SignUp />,
  },
  {
    path: "my-account",
    element: <MyAccount />,
  },
  {
    path: "enter-otp",
    element: <EnterOTP />,
  },
  {
    path: "forgot-password",
    element: <ForgotPassword />,
  },
  {
    path: "new-password",
    element: <NewPassword />,
  },
  {
    path: "header",
    element: <HeaderComp />,
  },
  {
    path: "home",
    element: <Home />,
    children: [
      {
        path: "",
        element: <Navigate to="details" replace />,
      },
      {
        path: "details",
        element: <Details />,
      },
      {
        path: "measurments",
        element: <Options />,
      },
      {
        path: "drivers",
        element: <Drivers />,
      },
      {
        path: "challenges",
        element: <Challenges />,
      },
      {
        path: "persona-overview",
        element: <PersonaOverview />,
      },
      {
        path: "insights",
        element: <Insights />,
      },
      {
        path: "sustainability",
        element: <Sustainability />,
        children: [
          {
            path: "",
            element: <Navigate to="sustainabilty-IT" replace />,
          },
          {
            path: "sustainabilty-IT",
            element: <SustainabiltyIT />,
          },
          {
            path: "sustainabilty-IT-2",
            element: <SustainabiltyIT2 />,
          },
          {
            path: "sustainabilty-IT-3",
            element: <SustainabiltyIT3 />,
          },
          {
            path: "sustainabilty-IT-4",
            element: <SustainabiltyIT4 />,
          },
          {
            path: "sustainabilty-IT-5",
            element: <SustainabiltyIT5 />,
          },
          {
            path: "sustainabilty-IT-6",
            element: <SustainabiltyIT6 />,
          },
        ],
      },

      {
        path: "variations",
        element: <Variations />,
        children: [
          {
            path: "",
            element: <Navigate to="variations-1" replace />,
          },
          {
            path: "variations-1",
            element: <Variations1 />,
          },
          {
            path: "variations-2",
            element: <Variations2 />,
          },
          {
            path: "variations-3",
            element: <Variations3 />,
          },
          {
            path: "variations-4",
            element: <Variations4 />,
          },
          {
            path: "variations-5",
            element: <Variations5 />,
          },
          {
            path: "variations-6",
            element: <Variations6 />,
          },
        ],
      },

      {
        path: "confirmation",
        element: <Confirmation />,
      },
      {
        path: "feedback",
        element: <Feedback />,
      },
    ],
  },
  {
    path: "edit-subtype",
    element: <EditSubType />,
  },
]);

export default router;
