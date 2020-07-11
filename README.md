# Launchpad

This project aims to provide a quick and easy way to provide newly onboarded AppDynamics applications with well crafted defaults.

<p align="center">
  <img src="https://github.com/AppDynamics/launchpad/blob/master/resources/screencap.png"/>
</p>

## Supported Scenarios

The following scenarios are currently functional.

Basic Configurations
- Disable Service Endpoint Detection
- Enable Business Transaction Lockdown 

## Planned Support 

Advanced Configurations

- Health Rule configurations
- Dashboard deployment

## Usage

Launchpad can be invoked with the command `python3 launchpad.py`

The following switches may be passed. If not, you will be prompted for them.

- --host

- --port

- --ssl/--no-ssl

- --accountname

- --username

- --password

e.g. `python3 launchpad.py --host acme-prod.saas.appdynamics.com --port 443 --ssl --accountname acme-prod --username acme-user --password hunter1`

## Requirements

Launchpad requires python3 as well as a Unix based OS. Windows is not supported at this time.

## Support

Please email bradley.hjelmar@appdynamics.com for any issues.
