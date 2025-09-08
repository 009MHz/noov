# Mobile E2E — Run & Debug Guide (Android & iOS, Appium + pytest)

**Audience:** QA/Developers running the mobile test suite locally and in CI  
**Stack:** Python, pytest, Allure, Appium 2 (UiAutomator2 / XCUITest)  
**Scope:** Android (Windows/macOS/Linux), iOS (macOS), local + GitHub Actions

---

## Quick Start (TL;DR)
```bash
# 1) Create venv & install deps
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r mobile-tests/requirements.txt

# 2) Start an Android emulator & Appium 2
emulator -avd Pixel_7_API_34 -gpu host -no-snapshot -netdelay none -netspeed full
appium driver install uiautomator2
appium --base-path /wd/hub

# 3) Run smoke tests with Allure output
pytest -m smoke --config mobile-tests/configs/android.local.yaml \
  --alluredir=reports/
```

To **view Allure locally** after a run:
```bash
# If you have Allure CLI
allure serve reports/
```
If not, open the zip artifact produced by CI (GitHub Actions) — it contains the raw results and the generated static site if configured.

---

## 1) Prerequisites

### 1.1 Core tools
- **Python 3.11+** (and `pip`)
- **Node.js 18+** (for Appium 2)
- **Java 17+** (Temurin/OpenJDK; needed by Android tooling)
- **Android SDK** + platform tools (for Android)
- **Xcode** (for iOS, macOS only)

### 1.2 Environment variables
- `ANDROID_SDK_ROOT` (or `ANDROID_HOME`) → points to your Android SDK folder
- Add `<SDK>/platform-tools` and `<SDK>/emulator` to your `PATH`
- Optional app creds for tests: `APP_USER`, `APP_PASS`

---

## 2) Android — Local Run

### 2.1 Install SDK components (first time)
```bash
sdkmanager --install "platform-tools" "platforms;android-34" "build-tools;34.0.0" \
  "emulator" "system-images;android-34;google_apis;x86_64"
```

### 2.2 Create & boot an emulator (first time)
```bash
avdmanager create avd -n Pixel_7_API_34 -k "system-images;android-34;google_apis;x86_64" -d pixel_7
emulator -avd Pixel_7_API_34 -netdelay none -netspeed full &
adb devices    # verify device is listed
```

### 2.3 Start Appium 2
```bash
npm i -g appium@2.x
appium driver install uiautomator2
appium --base-path /wd/hub
```

### 2.4 Configure your APK path
Edit `mobile-tests/configs/android.local.yaml`:
```yaml
appium:
  url: "http://127.0.0.1:4723/wd/hub"
capabilities:
  platformName: "Android"
  automationName: "UiAutomator2"
  deviceName: "Android Emulator"
  app: "/ABSOLUTE/PATH/TO/your-app-debug.apk"
  appWaitActivity: "*"
  newCommandTimeout: 120
  autoGrantPermissions: true
```

### 2.5 Run tests
```bash
# Smoke
pytest -m smoke --config mobile-tests/configs/android.local.yaml \
  --alluredir=reports/allure-results

# Specific file or test
pytest mobile-tests/tests/auth/test_login.py::test_valid_login \
  --config mobile-tests/configs/android.local.yaml \
  --alluredir=reports/allure-results

# Parallel (example)
pytest -n 2 --config mobile-tests/configs/android.local.yaml \
  --alluredir=reports/allure-results

# With env creds
APP_USER=qa@example.com APP_PASS='secret' pytest -m smoke --config mobile-tests/configs/android.local.yaml \
  --alluredir=reports/allure-results
```

---

## 3) iOS — Local Run (macOS)

> iOS requires Xcode and macOS.

### 3.1 Prepare simulator
```bash
xcrun simctl list devices
xcrun simctl boot "iPhone 15"
```

### 3.2 Appium (XCUITest)
```bash
appium driver install xcuitest
appium --base-path /wd/hub
```

### 3.3 Configure `mobile-tests/configs/ios.local.yaml`
```yaml
appium:
  url: "http://127.0.0.1:4723/wd/hub"
capabilities:
  platformName: "iOS"
  automationName: "XCUITest"
  deviceName: "iPhone 15"
  platformVersion: "18.0"
  app: "/ABSOLUTE/PATH/TO/your-app.app"
  newCommandTimeout: 120
```

### 3.4 Run tests
```bash
pytest -m smoke --config mobile-tests/configs/ios.local.yaml \
  --alluredir=reports/allure-results
```

---

## 4) Debugging Toolkit

### 4.1 Appium Inspector (optional but recommended)
- Install Appium Inspector (desktop app) to **inspect elements**, verify locators, and test actions.  
- Connect to `http://127.0.0.1:4723/wd/hub` using the same capabilities YAML.

### 4.2 Logs & artifacts
- **Appium server logs**: capture with `appium --base-path /wd/hub > appium.log 2>&1`
- **Android logcat**: `adb logcat -d > reports/logcat.txt`
- **iOS simulator logs**: Xcode’s Devices and Simulators or `log show --predicate ...`
- **On failure** (recommended hooks in `conftest.py`): take **screenshot** and **page source**:
  - `driver.get_screenshot_as_file(...)`
  - `driver.page_source` → save to file
- **Allure attachments**: attach screenshots, logs, and page source for any failure.

### 4.3 Useful adb commands
```bash
adb devices
adb shell dumpsys activity | head -50
adb shell am start -W -a android.intent.action.VIEW -d "myapp://deeplink/path"
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0
```

### 4.4 WebView / hybrid apps
- Switch context to `WEBVIEW_*` if you need DOM locators:
  - `driver.contexts`, `driver.switch_to.context(name)`
- Ensure webview is debuggable in your build settings.

### 4.5 Locators strategy (flake reduction)
- Prefer **`ACCESSIBILITY_ID`** (Android `content-desc`, iOS `accessibilityLabel`) with a team-wide `testid:*` convention.
- Avoid brittle XPath (indices). If needed, use Android `uiautomator` or iOS `-ios predicate string` judiciously.
- Work with devs to add/standardize stable IDs.

### 4.6 VS Code debugging
- Use the provided `vscode-launch-mobile.json` (see below) to step-debug tests.  
- In VS Code, copy it to `.vscode/launch.json`, select **"Pytest: Mobile (Android smoke)"**, press **F5**.

---

## 5) CI (GitHub Actions) — Android Emulator

- Use `ReactiveCircus/android-emulator-runner@v2` to spin up emulators on `ubuntu-latest`.
- Start Appium in background, run pytest, upload Allure + logs as artifacts.
- Example workflow name: `mobile-e2e-android.yml`.

> See pipeline snippet in your repository’s CI folder or use the draft shared alongside this guide.

---

## 6) Troubleshooting (Common Issues)

| Symptom | Likely Cause | Fix |
|---|---|---|
| `WebDriverException: Could not proxy command to remote server` | Appium driver not installed / server not running | `appium driver install uiautomator2`, ensure `appium --base-path /wd/hub` is running |
| `No devices/emulators found` | Emulator not started or adb not on PATH | Start emulator; check `adb devices`; verify `ANDROID_SDK_ROOT` |
| App freezes on launch | Wrong `appWaitActivity` or permissions | Set `appWaitActivity: "*"`; enable `autoGrantPermissions: true` |
| Locator not found | Missing or unstable testIDs | Verify with Appium Inspector; ask devs to add `content-desc`/`accessibilityLabel` |
| WebView actions fail | Not in `WEBVIEW_*` context | List contexts and `switch_to.context` |
| Flaky waits | Implicit sleeps | Replace with explicit waits and state checks (activity/element visible) |
| iOS app won’t run | Signing or simulator mismatch | Use `.app` for simulator, `.ipa` for devices; match `platformVersion` and `deviceName` |

---

## 7) Quality Gates & Conventions
- **Tags:** `@smoke`, `@android`, `@ios`, `@regression` (custom markers in `pytest.ini`)
- **Retry transient steps only** (not assertions) via `pytest-rerunfailures` if needed.
- **Artifacts:** Always keep Allure results, screenshots, and logs on failures.
- **Data:** Seed/reset test data deterministically (API helpers or in-app toggles).

---

## 8) Appendix — VS Code Launch Config (Pytest)
Save the following as `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Pytest: Mobile (Android smoke)",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "-m", "smoke",
        "--config", "mobile-tests/configs/android.local.yaml",
        "--maxfail=1",
        "--alluredir=reports/allure-results",
        "-q"
      ],
      "console": "integratedTerminal",
      "justMyCode": false,
      "env": {
        "APP_USER": "qa@example.com",
        "APP_PASS": "secret123!"
      }
    },
    {
      "name": "Pytest: Single Test (focused)",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "mobile-tests/tests/auth/test_login.py::test_valid_login",
        "--config", "mobile-tests/configs/android.local.yaml",
        "--alluredir=reports/allure-results",
        "-q"
      ],
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```
