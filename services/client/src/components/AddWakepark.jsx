import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import { Formik } from "formik";
import * as Yup from "yup";
import axios from "axios";

import localStorage from "../services/localStorage";

class AddWakepark extends Component {
  state = {
    toWakeparks: false
  };

  onHandleAddWakepark = async data => {
    const wakepark = {
      name: data.name,
      description: data.description,
      location: {
        lat: parseInt(data.lat),
        lng: parseInt(data.lng)
      },
      social: {
        instagram: data.instagramHandle
      }
    };

    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/wakeparks/`,
      method: "post",
      data: wakepark,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`
      }
    };
    try {
      const res = await axios(options);
      if (res.status === 201) {
        this.setState({ toWakeparks: true });
      } else {
        // TODO: create message
      }
    } catch (ex) {
      //console.error(ex);
    }
  };

  render() {
    if (this.state.toWakeparks) {
      return <Redirect to="/" data-testid="redirect" />;
    }

    if (!localStorage.isPermitted("post:cableparks")) {
      return <Redirect to="/" data-testid="redirect" />;
    }

    return (
      <div>
        <h3 className="title">Add Wakepark</h3>
        <hr />
        <br />
        <Formik
          initialValues={{
            name: "",
            description: "",
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
            description: Yup.string().required("Please enter a description"),
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
                  <label htmlFor="input-description" className="label">
                    Description
                  </label>
                  <input
                    type="text"
                    name="description"
                    id="input-description"
                    className={errors.description && touched.description ? "input error" : "input"}
                    placeholder="Enter the wakepark description"
                    value={values.description}
                    onChange={handleChange}
                    onBlur={handleBlur}
                  />
                  {errors.description && touched.description && (
                    <div className="input-feedback" data-testid="errors-description">
                      {errors.description}
                    </div>
                  )}
                </div>
                <div className="field">
                  <label htmlFor="input-latitude" className="label">
                    Latitude
                  </label>
                  <input
                    type="text"
                    name="lat"
                    id="input-latitude"
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
                  <label htmlFor="input-longitude" className="label">
                    Longitude
                  </label>
                  <input
                    type="text"
                    name="lng"
                    id="input-longitude"
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
                    name="instagramHandle"
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
