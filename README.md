# An integration for weather alerts from weather.gov
This can be used as a severe weather automation system

[![GitHub release (latest by date)][release-badge]][release-link]  [![GitHub][license-badge]][license-link]  [![hacs_badge][hacs-badge]][hacs-link]

[![GitHub stars][stars-badge]][stars-link]  ![GitHub][maintained-badge]


# Breaking changes

### None discovered yet


# Installation Quickstart

This quickstart install guide assumes you are already familiar with custom component installation and with the Home Assistant YAML configuration. If you need more detailed step-by-step instructions, check the links at the bottom for detailed instructions. Troubleshooting information, weatheralerts YAML package information, and Lovelace UI examples are also included in the **Links** at the bottom.

Install the *weatheralerts* integration via *HACS* with custom repository - ddeatrich0407/weatheralerts. After installing via *HACS*, don't restart Home Assistant yet. We will do that after completing the YAML platform configuration.

You will need to find your zone and county codes by looking for your state or marine zone at [https://alerts.weather.gov/](https://alerts.weather.gov/). Once at [https://alerts.weather.gov/](https://alerts.weather.gov/), click the `Land area with zones` link and you will find a list of states with `Public Zones` and `County Zones` links. Once you find your state , click into the `Public Zones` and `County Zones` links and find the respective codes for your county. All you will need are just the first two letters (your state abbreviation) and the last three digits (zone/county ID number) of your zone code and county code to put into the platform configuration. The zone and county ID numbers are not usually the same number, so be sure to look up both codes. For marine zones, go to [https://alerts.weather.gov/](https://alerts.weather.gov/), click the `Marine regions/areas with zones` link and you will find a list of marine areas with `Zones` links. In the `Zones` link for the marine area you are interested in, find the exact marine zone. The first two letters of the marine zone is what will be used for the *state* configuration option, and the last three digits is what will be used for the *zone* configuration option (omit any leading zeros). 

Once installed and you have your state (or marine zone) abbreviation and ID numbers, add the weatheralerts sensor platform to your configuration. If your state is Wisconsin and your county is Outagamie, then the state abbreviation is `WI`, the zone ID number is `038`, and the county ID number is `087`. For the ID numbers, remove any leading zeros and your YAML platform configuration would look something like this:
```yaml
sensor:
  platform: weatheralerts
  state: WI
  zone: 38
  county: 87
```
Once your configuration is saved, restart Home Assistant. 

That completes the integration (custom component) installation.

Check the **Links** below for more detailed instructions, troubleshooting, and for YAML package and Lovelace UI usage and examples.


# Updating via HACS

Check the **Breaking Changes** section of this README to see if you need to manually update the YAML packages or make any changes to your custom YAML or Lovelace UI cards. Simply use the **Update** button for the *weatheralerts* integration within *HACS* if there are no breaking changes and then restart Home Assistant. 


# Links

  * [Detailed Instructions](https://github.com/ddeatrich/weatheralerts/blob/master/documentation/DOCUMENTATION.md)
  * [Troubleshooting](https://github.com/ddeatrich/weatheralerts/blob/master/documentation/TROUBLESHOOTING.md)
  * [YAML Package Info](https://github.com/ddeatrich/weatheralerts/blob/master/documentation/YAML_PACKAGES_DOCS.md)
  * [Lovelace UI Examples](https://github.com/ddeatrich/weatheralerts/blob/master/documentation/LOVELACE_EXAMPLES.md)
  * [GitHub Repository](https://github.com/ddeatrich/weatheralerts)
  * [View Issues/Feature Requests](https://github.com/ddeatrich/weatheralerts/issues)
  * [Report an Issue/Feature Request](https://github.com/ddeatrich/weatheralerts/issues/new/choose)
  * [Changelog](https://github.com/ddeatrich/weatheralerts/blob/master/CHANGELOG.md)




# Todo list
- [x] Add more documentation
- [x] Update code to meet current best practice, clean up code, performance improvements
- [ ] Add backup weather alert source for occasions when weather.gov json feed is experiencing an outage - I can't find any good free ones yet.


[release-badge]: https://img.shields.io/github/v/release/custom-components/weatheralerts?style=plastic
[release-link]: https://github.com/ddeatrich0407/weatheralerts
[license-badge]: https://img.shields.io/github/license/custom-components/weatheralerts?style=plastic
[license-link]: https://github.com/ddeatrich0407/weatheralerts/blob/master/LICENSE
[hacs-badge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=plastic
[hacs-link]: https://github.com/hacs/integration
[stars-badge]: https://img.shields.io/github/stars/custom-components/weatheralerts?style=plastic
[stars-link]: https://github.com/ddeatrich0407/weatheralerts/stargazers
[maintained-badge]: https://img.shields.io/badge/maintenance%20status-actively%20developed-brightgreen

