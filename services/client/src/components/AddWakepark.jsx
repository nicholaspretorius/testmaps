import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import { Formik } from "formik";
import * as Yup from "yup";

import localStorage from "../services/localStorage";

class AddWakepark extends Component {
  state = {};

  onHandleAddWakepark(values) {
    console.log("Values: ", values);
  }

  render() {
    if (!localStorage.isPermitted("post:cableparks")) {
      return <Redirect to="/" />;
    }

    return (
      <div>
        <h3 className="title">Add Wakepark</h3>
        <hr />
        <br />
        <Formik
          initialValues={{
            name: "",
            lat: "",
            lng: "",
            instagramHandle: ""
          }}
          onSubmit={(values, { setSubmitting, resetForm }) => {
            this.onHandleAddWakepark(values);
            resetForm();
            setSubmitting(false);
          }}
          validationSchema={Yup.object().shape({
            name: Yup.string().required("Please enter a name"),
            lat: Yup.string().required("Please enter a latitude"),
            lng: Yup.string().required("Please enter a longitude"),
            instagramHandle: Yup.string()
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
                  {errors.name && touched.name && (
                    <div className="input-feedback" data-testid="errors-name">
                      {errors.name}
                    </div>
                  )}
                </div>
                <div className="field">
                  <label htmlFor="input-lat" className="label">
                    Latitude
                  </label>
                  <input
                    type="text"
                    name="lat"
                    id="input-lat"
                    className={errors.lat && touched.lat ? "input error" : "input"}
                    placeholder="Enter the wakepark latitude location"
                    value={values.lat}
                    onChange={handleChange}
                    onBlur={handleBlur}
                  />
                  {errors.lat && touched.lat && (
                    <div className="input-feedback" data-testid="errors-lat">
                      {errors.lat}
                    </div>
                  )}
                </div>
                <div className="field">
                  <label htmlFor="input-lng" className="label">
                    Longitude
                  </label>
                  <input
                    type="text"
                    name="lng"
                    id="input-lng"
                    className={errors.lng && touched.lng ? "input error" : "input"}
                    placeholder="Enter the wakepark longitude location"
                    value={values.lng}
                    onChange={handleChange}
                    onBlur={handleBlur}
                  />
                  {errors.lng && touched.lng && (
                    <div className="input-feedback" data-testid="errors-lng">
                      {errors.lng}
                    </div>
                  )}
                </div>

                <div className="field">
                  <label htmlFor="input-instagram-handle" className="label">
                    Instagram Handle
                  </label>
                  <input
                    type="text"
                    name="instagram-handle"
                    id="input-instagram-handle"
                    className={
                      errors.instagramHandle && touched.instagramHandle ? "input error" : "input"
                    }
                    placeholder="Enter the wakepark Instagram handle"
                    value={values.instagramHandle}
                    onChange={handleChange}
                    onBlur={handleBlur}
                  />
                  {errors.instagramHandle && touched.instagramHandle && (
                    <div className="input-feedback" data-testid="errors-instagram-handle">
                      {errors.instagramHandle}
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
