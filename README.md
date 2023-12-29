# Advisobot
Automated course registration (for University of Louisiana - Lafayette).

## Configuration

In order for the tool to operate properly, it requires two configuration files:

### drivers.yaml
This file will contain paths to WebDrivers needed to operate the tool. It will follow this format:
```
firefox: ./conf/drivers/geckodriver
chrome: ./conf/drivers/chromedriver
```
You will need to download the respective driver needed for your situation.
* [Firefox](https://github.com/mozilla/geckodriver/releases)
* [Chrome](https://googlechromelabs.github.io/chrome-for-testing/)

### credentials.ini
This file will contain the credentials for you UL account. Upon the first run of the tool, the contents will be encrypted for protection.

Keys & values:
* CLID: Your school-assigned CLID# (i.e., C000#####)
* PSWD: Password for your account

### courses.yaml
This file will contain the term and courses for which you are registering, and will follow this format:

```
courses:
  course1:
    subject: CSCE
    number: 500
    section: 001
  course2:
    subject: CSCE
    number: 509
    section: 001
  ...

term: Spring 2024
```
Templates are provided for each of these files. Simply copy the template, rename it appropriately, and fill in the values. 

## Actions
Advisobot facilitates two primary actions to aid you in your registration automation:

### Verification
Prior to registration, it's imperative that the user verifies their information and configurations. To verify the information, use the following commands:

* `python main.py verify credentials`: Verify that credentials are valid by logging in
* `python main.py verify term`: Verify that term is valid by locating it in the registration dashboard's term selection drop down
* `python main.py verify courses`: Verify that courses contain required information and that they are valid classes by looking them up in ULink
* `python main.py verify plan {PLAN NAME}`: Verify that plan name is valid by locating it in user's ULink registration plans

### Registration
The primary motivation for this tool is that it registers your classes for you. There are two different ways to execute this process:

#### Course Info
Register a list of courses using their subject, number, and section number. All three pieces of information are required, to ensure the tool does not register the user for the wrong class. Do so using the following command:
```
python main.py register courses
```

#### Plan
Register courses from a plan that the user has saved in their ULink account. As one might guess, the plan must be configured and saved in ULink prior to the tool using it to register. Do so using the following command:
```
python main.py register plan {PLAN NAME}
```

## Disclaimer(s)

This tool was written/tested using:
* Linux Mint (5.15.0-88-generic)
* Python 3.11.5
* Firefox 119.0.1 (64-bit)

---
Should you find a bug, please [report it](https://github.com/theokoles7/Advisobot/issues/new)!