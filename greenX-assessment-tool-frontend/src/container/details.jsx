import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Form, message } from "antd";
import { useNavigate } from "react-router-dom";
import {
  LockOutlined,
  UserOutlined,
  ContainerOutlined,
  FundProjectionScreenOutlined,
} from "@ant-design/icons";
import { MdOutlineEmail } from "react-icons/md";
import CustomInput from "../components/customInput";
import CustomButton from "../components/customButton";
import CustomSelector from "../components/customSelector";
import { cisco, inputIconColor, textColor, white } from "../constants/colors";
import { setFormData } from "../store/formSlice";
import { useSubmitFormMutation } from "../store/api";
import { baseUrl } from "../utills/axios";
import axios from "axios";

const Details = () => {
  const dispatch = useDispatch();
  const details = useSelector((state) => state.form);
  const [domainsList, setDomainsList] = useState([]);
  const [roles, setRoles] = useState([]);
  const [submitForm, { isLoading }] = useSubmitFormMutation();
  const navigate = useNavigate();
  const [loginData, setLoginData] = useState(null);
  console.log("loginData", loginData);
  const [isNewDomain, setIsNewDomain] = useState(false);
  const [newDomain, setNewDomain] = useState("");
  const [domainId, setDomainId] = useState();

  const [isNewRole, setIsNewRole] = useState(false);
  const [newRole, setNewRole] = useState("");
  const [messageApi, contextHolder] = message.useMessage();

  useEffect(() => {
    const storedData = localStorage.getItem("loginData");
    if (storedData) {
      setLoginData(JSON.parse(storedData));
    }
  }, []);

  useEffect(() => {
    if (loginData && loginData.access_token === "") {
      navigate("/login");
    }
  }, [loginData, navigate]);

  const fetchDomainList = async () => {
    try {
      const res = await axios.get(baseUrl + "/api/v2/domain/get-domain", {
        headers: {
          Authorization: `Bearer ${loginData?.access_token}`,
        },
      });
      if (res.status === 200) {
        console.log(res);

        const formattedData = res.data.domain.map((item) => ({
          label: item.name,
          value: item.name,
          id: item.id,
        }));
        setDomainsList(formattedData);
      }
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (loginData && loginData.access_token) {
      fetchDomainList();
    }
  }, [loginData]);

  const onFinish = (values) => {
    submitForm(values).then(() => {
      // console.log("values::", values);
    });
  };

  const onChange = (e) => {
    const { name, value } = e.target;
    dispatch(setFormData({ [name]: value }));
  };
  const onChangeDomain = (e) => {
    const { name, value } = e.target;
    setNewDomain(value);
  };
  const onChangeRole = (e) => {
    const { name, value } = e.target;
    // console.log("new domain value", value);
    setNewRole(value);
  };

  const createDomain = async () => {
    const payload = {
      name: newDomain,
      description: "string",
      created_by_id: loginData?.user_info?.id,
    };
    try {
      const res = await axios.post(
        baseUrl + "/api/v2/domain/create-domain",
        payload,
        {
          headers: {
            Authorization: `Bearer ${loginData?.access_token}`,
          },
        }
      );
      if (res.status === 200) {
        console.log("create domain:", res);
        messageApi.open({
          type: "success",
          content: "Domain Created Successfully!",
        });
        setIsNewDomain(false);
        fetchDomainList();
      }
    } catch (error) {
      console.log("create domain error:", error);
    }
  };

  const fetchRole = async (id) => {
    try {
      const res = await axios.post(
        `${baseUrl}/api/v2/setup/role-types-id?domain_id=${id}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${loginData?.access_token}`,
          },
        }
      );
      if (res.status === 200) {
        const formattedData = res.data.roles.map((item) => ({
          label: item.name,
          value: item.name,
          id: item.id,
        }));
        setRoles(formattedData);
      }
    } catch (error) {
      console.log(error);
    }
  };
  const createRole = async () => {
    const payload = {
      name: newRole,
      domain_type_id: details?.domain_id,
    };
    try {
      const res = await axios.post(
        baseUrl + "/api/v2/role/create-role",
        payload,
        {
          headers: {
            Authorization: `Bearer ${loginData?.access_token}`,
          },
        }
      );
      if (res.status === 200) {
        console.log("create role:", res);
        messageApi.open({
          type: "success",
          content: "Role Added Successfully!",
        });
        fetchRole(domainId);
        setIsNewRole(false);
      }
    } catch (error) {
      console.log("create domain error:", error);
    }
  };

  const onSelectChange = (value, option) => {
    dispatch(setFormData({ domain_id: option.id, domain_name: value }));
    fetchRole(option.id);
    setDomainId(option.id);
  };

  const onSelectChangeRole = (value, option) => {
    dispatch(setFormData({ role_id: option?.id, role: value }));
  };

  if (!loginData) {
    return <div>Loading...</div>; // or some loading indicator
  }

  return (
    <>
      {contextHolder}

      <div
        className="detail_container"
        style={{ width: "442px", margin: "0 auto", marginBottom: "20px" }}
      >
        <div>
          <p
            style={{
              fontSize: "16px",
              fontWeight: 500,
              lineHeight: "30px",
              textAlign: "start",
              color: textColor,
              marginBottom: "20px",
            }}
          >
            Before we begin, we would like to know more about you and your
            organization. Please fill the form below:
          </p>
        </div>
        <Form
          name="normal_login"
          initialValues={{
            username: loginData?.user_info?.name,
            email: loginData?.user_info?.email,
            company_name: details?.company_name,
            role: details?.role,
            domain_name: details?.domain_name,
            // organization_name: details.company,
            // domain_id: details.domain_id,
            // role_id: details.role_id,
          }}
          onFinish={onFinish}
        >
          <Form.Item
            name="username"
            rules={[
              {
                required: true,
                message: "Please input your name!",
              },
            ]}
          >
            <CustomInput
              disabled
              value={loginData?.user_info?.name}
              onChange={onChange}
              placeholder="Full Name"
              icon={
                <UserOutlined
                  style={{ color: inputIconColor, fontSize: "22px" }}
                />
              }
            />
          </Form.Item>
          <Form.Item
            name="email"
            rules={[
              {
                required: true,
                message: "Please input your email!",
              },
              {
                type: "email",
                message: "The input is not a valid email!",
              },
            ]}
          >
            <CustomInput
              disabled
              value={loginData?.user_info?.email}
              placeholder="Email Address"
              icon={
                <MdOutlineEmail
                  style={{ color: inputIconColor, fontSize: "22px" }}
                />
              }
            />
          </Form.Item>
          <Form.Item
            name="company_name"
            rules={[
              {
                required: true,
                message: "Please input your Company!",
              },
            ]}
          >
            <CustomInput
              name="company_name"
              value={details.company}
              onChange={onChange}
              placeholder="Company"
              icon={
                <ContainerOutlined
                  style={{ color: inputIconColor, fontSize: "22px" }}
                />
              }
            />
          </Form.Item>
          <div style={{ display: "flex", gap: "5px", width: "100%" }}>
            <Form.Item
              style={{ width: "100%" }}
              name={details ? "domain_name" : "domain_id"}
              rules={[
                {
                  required: true,
                  message: "Please select a domain!",
                },
              ]}
            >
              <CustomSelector
                placeholder="Select Domain"
                options={domainsList}
                onChange={onSelectChange}
              />
            </Form.Item>
            <CustomButton
              onClick={() => setIsNewDomain(true)}
              size="large"
              style={{ height: "48px" }}
            >
              +
            </CustomButton>
          </div>
          {isNewDomain ? (
            <div style={{ display: "flex", gap: "5px" }}>
              <Form.Item style={{ width: "100%" }}>
                <CustomInput
                  name="new_domain"
                  // value={details.company}
                  onChange={onChangeDomain}
                  placeholder="Enter New Domain"
                  icon={
                    <ContainerOutlined
                      style={{ color: inputIconColor, fontSize: "22px" }}
                    />
                  }
                />
              </Form.Item>
              <CustomButton
                onClick={createDomain}
                size="large"
                style={{ height: "48px" }}
              >
                Save
              </CustomButton>
            </div>
          ) : null}

          <div
            style={{
              display: "flex",
              gap: "5px",
            }}
          >
            <Form.Item
              style={{
                width: "100%",
              }}
              name={details ? "role" : "role_id"}
              rules={[
                {
                  required: true,
                  message: "Please Select a Role!",
                },
              ]}
            >
              <CustomSelector
                // icon={<FundProjectionScreenOutlined />}
                placeholder="Select Role"
                options={roles}
                onChange={onSelectChangeRole}
              />
            </Form.Item>
            <CustomButton
              onClick={() => setIsNewRole(true)}
              size="large"
              style={{ height: "48px" }}
            >
              +
            </CustomButton>
          </div>
          {isNewRole ? (
            <div style={{ display: "flex", gap: "5px" }}>
              <Form.Item style={{ width: "100%" }}>
                <CustomInput
                  onChange={onChangeRole}
                  placeholder="Enter New Role"
                  icon={
                    <ContainerOutlined
                      style={{ color: inputIconColor, fontSize: "22px" }}
                    />
                  }
                />
              </Form.Item>
              <CustomButton
                onClick={createRole}
                size="large"
                style={{ height: "48px" }}
              >
                Save
              </CustomButton>
            </div>
          ) : null}
          {/* <Form.Item>
          <CustomButton
            htmlType="submit"
            style={{
              width: "100%",
              background: cisco,
              color: white,
              height: "48px",
            }}
            loading={isLoading}
          >
            Submit
          </CustomButton>
        </Form.Item> */}
        </Form>
      </div>
    </>
  );
};

export default Details;
