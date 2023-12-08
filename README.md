# Advisobot
Automated course registration (for University of Louisiana - Lafayette).

## Configuration

In order for the tool to operate properly, it requires two configuration files:

### credentials.ini
This file will contain the credentials for you UL account. During run time, the contents will be encrypted for protection.

Keys & values:
* CLID: Your school-assigned CLID# (i.e., C000#####)
* PSWD: Password for your account

### courses.yaml
This file will contain the courses for which you are registering, and will follow this format:

```
course#:
  subject:  CSCE
  number:   500
  crn:      44523
```
Templates are provided for each of these files. Simply copy the template, rename it appropriately, and fill in the values. 

## Disclaimer(s)

This tool was written/tested using:
* Linux Mint (5.15.0-88-generic)
* Python 3.11.5
* Firefox 119.0.1 (64-bit)

---
Should you find a bug, please [report it](https://github.com/theokoles7/Advisobot/issues/new)!