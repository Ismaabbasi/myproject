import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  endpoints: (builder) => ({
    // Define your endpoints here
    submitForm: builder.mutation({
      query: (formData) => ({
        url: "/submit",
        method: "POST",
        body: formData,
      }),
    }),
  }),
});

export const { useSubmitFormMutation } = api;
