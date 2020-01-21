import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import { Formik } from "formik";
import * as Yup from "yup";
import axios from "axios";

import localStorage from "../services/localStorage";

class UpdateWakepark extends Component {
  state = {
    id: this.props.match.params.id,
    wakepark: null,
    toWakeparks: false,
    isLoading: true
  };

  componentDidMount() {
    this.getWakeparkDetails(this.state.id);
  }

  async getWakeparkDetails(id) {
    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/wakeparks/${id}`,
      method: "get",
      headers: {
        "Content-Type": "application/json"
      }
    };

    try {
      const res = await axios(options);
      this.setState({ wakepark: res.data, isLoading: false });
    } catch (ex) {
      // ex
    }
  }

  onHandleUpdateWakepark = async data => {
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
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/wakeparks/${this.state.id}`,
      method: "put",
      data: wakepark,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`
      }
    };

    try {
      const res = await axios(options);

      if (res.statusCode === 200) {
        this.setState({ toWakeparks: true });
        this.getWakeparkDetails(this.state.id);
      }
    } catch (ex) {}
  };

  render() {
    const { wakepark, isLoading, toWakeparks } = this.state;

    if (toWakeparks) {
      return <Redirect to="/" data-testid="redirect" />;
    }

    if (!localStorage.isPermitted("put:cableparks")) {
      return <Redirect to="/" data-testid="redirect" />;
    }

    return (
      <div>
        <h3 className="title">Update Wakepark</h3>
        <hr />
        <br />

        {isLoading && <div>Loading...</div>}

        {!isLoading && wakepark && (
          <Formik
            initialValues={{
              name: wakepark.name,
              description: wakepark.description,
              lat: wakepark.location.lat,
              lng: wakepark.location.lng,
              instagramHandle: wakepark.social.instagram
                ? wakepark.social.instagram.split(".com/")[1]
                : ""
            }}
            onSubmit={(values, { setSubmitting, resetForm }) => {
              this.onHandleUpdateWakepark(values);
              resetForm();
              setSubmitting(false);
            }}
            validationSchema={Yup.object().shape({
              name: Yup.string().required("Please enter a name"),
              description: Yup.string().required("Please enter a description"),
              lat: Yup.string().required("Please enter a latitude"),
              lng: Yup.string().required("Please enter a longitude"),
              instagramHandle: wakepark.social.instagram
                ? Yup.string().required("Please enter an instagram handle")
                : Yup.string()
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
                      className={
                        errors.description && touched.description ? "input error" : "input"
                      }
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
        )}
      </div>
    );
  }
}

export default UpdateWakepark;
