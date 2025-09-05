### ✅ **Test Case 1: Successful Login without 2FA**

* **Priority:** Critical
* **Pre-Condition:**

  * 2FA is **disabled** for the test user.
  * Valid email and password credentials are known.
* **Steps:**

  1. Open `https://manage-qa.noovoleum.com/login`.
  2. Fill the email input with a valid email (e.g., `harits.satriyo@noovoleum.com`).
  3. Fill the password input with the correct password (e.g., `Halo123456`).
  4. Leave the 2FA field empty.
  5. Click the "Log In" button.
* **Expected Result:**

  * User is redirected to the dashboard/home page.
  * Session is stored (e.g., via cookies or local storage).
  * 2FA banner warning is displayed (.getByText('Please Enable 2FA (2 Factor'))
  * OTP Warning text is displayed (.getByText('OTP / 2FA Enabled : No'))

---

### ✅ **Test Case 2: Successful Login with 2FA Enabled**

* **Priority:** Critical
* **Pre-Condition:**

  * 2FA is **enabled** for the test user.
  * Valid credentials and a valid 6-digit 2FA code from the authenticator app are available.
* **Steps:**

  1. Open `https://manage-qa.noovoleum.com/login`.
  2. Enter valid email and password.
  3. Enter valid 2FA code in the "2FA Code (if enabled)" field.
  4. Click "Log In".
* **Expected Result:**

  * Login succeeds and user is redirected to the secure area.
  * User redirected to /dashboard
  * Session is established correctly.
  * The 2FA banner is not displayed

---

### ❌ **Test Case 3: Login with Invalid Credentials**

* **Priority:** High
* **Pre-Condition:**

  * Email and/or password is incorrect.
* **Steps:**

  1. Open the login page.
  2. Enter an invalid email or password.
  3. Leave 2FA empty or provide random code.
  4. Click "Log In".
* **Expected Result:**

  * Error message is displayed
    * Invalid email / password is displayed
  * User remains on login page.
  * No session is created.

---

### ❌ **Test Case 4: Login with Invalid 2FA Code**

* **Priority:** High
* **Pre-Condition:**

  * 2FA is enabled.
  * User enters correct email/password but incorrect 2FA code.
* **Steps:**

  1. Enter valid email and password.
  2. Enter invalid 2FA code (e.g., `123000`).
  3. Click "Log In".
* **Expected Result:**

  * Error shown (e.g., “Invalid 2FA code”).
  * User remains on login page.
  * No session is created.

---

### 🔒 **Test Case 5: Login Form Validation – Empty Fields**

* **Priority:** Medium
* **Pre-Condition:**

  * None.
* **Steps:**

  1. Open login page.
  2. Do not enter any input.
  3. Click "Log In".
* **Expected Result:**

  * Required field validation appears for Email and Password.
    * "Please Enter Your Email" text displayed for email field
    * "Please Enter Your Password" text displayed for password field
  * Login is blocked.
  * No API call or page redirect happens.

---

### 🔒 **Test Case 6: Login Form Validation – Invalid Email Format**

* **Priority:** Medium
* **Pre-Condition:**

  * None.
* **Steps:**

  1. Enter an invalid email format (e.g., `user@noovoleum`) in the Email field.
  2. Fill in any password.
  3. Click "Log In".
* **Expected Result:**

  * Invalid email message appears
  * Form does not submit.

---

### 🔁 **Test Case 7: Login Page Refresh – Inputs Are Cleared**

* **Priority:** Minor
* **Pre-Condition:**

  * Login form is filled.
* **Steps:**

  1. Enter email and password.
  2. Refresh the page.
* **Expected Result:**

  * All inputs (Email, Password, 2FA) are cleared.
  * No autofill remains (unless browser-level autofill is triggered).

---

### 🔐 **Test Case 8: Login Session Persistence After Redirect**

* **Priority:** High
* **Pre-Condition:**

  * User has logged in successfully.
* **Steps:**

  1. Login successfully.
  2. Refresh the browser.
  3. Reopen the login page manually.
* **Expected Result:**

  * User is redirected away from the login page
  * Session remains valid.

---
