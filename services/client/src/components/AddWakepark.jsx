import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import PropTypes from "prop-types";
import { Formik } from "formik";
import * as Yup from "yup";

class AddWakepark extends Component {
  state = {};
  render() {
    return (
      <div>
        <h3 className="title">Add Wakepark</h3>
        <hr />
        <br />
        <Formik
          initialValues={{
            name: ""
          }}
          onSubmit={(values, { setSubmitting, resetForm }) => {
            onHandleAddWakepark(values);
            resetForm();
            setSubmitting(false);
          }}
          validationSchema={Yup.object().shape({
            name: Yup.string().required("Please enter a name")
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
                  <label htmlFor="input-name" className="label">
                    Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    id="input-name"
                    className={errors.name && touched.name ? "input error" : "input"}
                    placeholder="Enter the wakepark name"
                    value={values.name}
                    onChange={handleChange}
                    onBlur={handleBlur}
                  />
                  {errors.name & touched.name && (
                    <div className="input-feedback" data-testid="errors-name">
                      {errors.name}
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
  }
}

export default AddWakepark;
