import React, { useState, useEffect } from "react";

export const EmailSelect = (props) => {
  const handleSelect = (i) => {
    console.log(i);
    console.log(props.blobArray[i]);
    props.setSelectedBlob(props.blobArray[i]);
    props.handleEmailSelect();
  };
  return (
    <div class="container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">No</th>
            <th scope="col">Subject</th>
            <th scope="col">Sender's id</th>
            <th scope="col">Date Received</th>
            <th scope="col">Time Received</th>
            <th scope="col" colspan="2">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          {props.emailDetails.length > 0 ? (
            props.emailDetails.map((email, i) => (
              <tr key={i}>
                <td>{i + 1}</td>
                <td>{email.subject}</td>
                <td>{email.sender_address}</td>
                <td>{email.date_received}</td>
                <td>{email.time_received}</td>
                <td className="text-right">
                  <button
                    onClick={() => handleSelect(i)}
                    className="btn btn-outline-warning"
                  >
                    Select
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={7}>No Emails</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};
