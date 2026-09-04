import React from "react";
import { Table } from "antd";
import styled from "styled-components";
import { borderColor, colHeadings } from "../constants/colors";
const StyledTable = styled(Table)`
  .ant-table {
    border: none !important;
    border-right: 1px solid ${borderColor} !important;
    border-radius: 0px;
    overflow: hidden;
  }
  .ant-table-thead > tr > th {
    background-color: #fafafa;
    color:${colHeadings}
    font-weight: 600 !important;
    font-size:18px;
    text-align: center;
    border-radius: 0px !important;
    border: 1px solid ${borderColor};
    border-bottom: unset !important;
    padding:10px 0px;
  }

  .ant-table-tbody > tr > td {
    // text-align: center;
    border: 1px solid ${borderColor};
    border-top: unset !important;
    padding:3px 10px 5px 20px;
  }

  .ant-table-bordered .ant-table-container {
    border: none !important;
  }
     .ant-table-tbody > tr:hover > td {
    background: none !important;
  }
`;
const CustomTable = ({ data, columns, pagination }) => {
  return (
    <StyledTable
      bordered
      dataSource={data}
      columns={columns}
      pagination={{
        defaultPageSize: 3,
        pageSizeOptions: [5, 50, data?.length],
      }}
      scroll={{
        x: 800,
      }}
    />
  );
};

export default CustomTable;
