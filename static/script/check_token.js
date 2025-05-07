/**
 * A simple script that forces user to logout if the session token is
 * invalid or not set properly (needs to login again)
 */

import { clearAllCookies } from "./modules/cookie_clear.js";

(async function () {
  try {
    // requests token check in the backend using the cookie i have
    const response = await fetch("/api/token-check", {
      credentials: "include", // include the cookie during request
      headers: {
        "Content-Type": "application/json",
      },
    });

    // checks if the auth token is active (redirect if not)
    const response_data = await response.json();
    if (response_data.active) {
      console.log("This token is active");
    } else {
      alert("You are not logged in currently");
      clearAllCookies();
      window.location.href = "/";
    }
  } catch (err) {
    alert("You are not logged in currently");
    clearAllCookies();
    window.location.href = "/";
  }
})();
