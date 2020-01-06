import React from "react";
import { Redirect } from "react-router-dom";
import PropTypes from "prop-types";
import { Formik } from "formik";
import * as Yup from "yup";

const LoginForm = props => {
  const { onHandleLoginFormSubmit, isAuthenticated } = props;

  if (isAuthenticated()) {
    return <Redirect to="/" />;
  }

  return (
    <div>
      <h1 className="title is-1">Login</h1>
      <hr />
      <br />
      <Formik
        initialValues={{
          email: "",
          password: ""
        }}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          onHandleLoginFormSubmit(values);
          resetForm();
          setSubmitting(false);
        }}
        validationSchema={Yup.object().shape({
          email: Yup.string()
            .email("Please enter a valid email.")
            .required("Email is required.")
            .min(6, "Email must be 6 or more characters."),
          password: Yup.string()
            .required("Password is required.")
            .min(8, "Password must be 8 or more characters.")
        })}
      >
        {props => {
          const {
            values,
            touched,
            errors,
            isSubmitting,
            handleChange,
            handleBlur,
            handleSubmit
          } = props;
          return (
            <form onSubmit={handleSubmit}>
              <div className="field">
                <label htmlFor="input-email" className="label">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  id="input-email"
                  className={
                    errors.email && touched.email ? "input error" : "input"
                  }
                  placeholder="Enter your email address"
                  value={values.email}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
                {errors.email && touched.email && (
                  <div className="input-feedback" data-testid="errors-email">
                    {errors.email}
                  </div>
                )}
              </div>
              <div className="field">
                <label htmlFor="input-password" className="label">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  id="input-password"
                  className={
                    errors.password && touched.password
                      ? "input error"
                      : "input"
                  }
                  placeholder="Enter your password"
                  value={values.password}
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
                {errors.password && touched.password && (
                  <div className="input-feedback" data-testid="errors-password">
                    {errors.password}
                  </div>
                )}
              </div>

              <input
                type="submit"
                className="button is-primary"
                value="Submit"
                disabled={isSubmitting}
              />
            </form>
          );
        }}
      </Formik>
    </div>
  );
};

LoginForm.propTypes = {
  onHandleLoginFormSubmit: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired
};

export default LoginForm;
