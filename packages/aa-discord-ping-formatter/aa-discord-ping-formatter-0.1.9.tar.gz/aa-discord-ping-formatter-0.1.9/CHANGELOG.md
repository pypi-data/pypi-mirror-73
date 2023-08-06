# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.1.9] - 2020-07-14
### Added
- Ping creator at the end auf automatic pings via webhooks

## [0.1.8] - 2020-07-09
### Added
- Webhook group restrictions. Webhooks can now be restricted to certain groups (see [README](https://github.com/ppfeufer/aa-discord-ping-formatter#adding-ping-channels)), so not everyone who has access too this module can ping through all webhooks. Webhoos without restrictions are accessible for all with access to the module. (Thanks to Exiom for bringing this up)
- FC name is pre-filled with the users main character name, since the user is most likely te FC pinging for his own fleet.

### Changed
- Formup Time is now a proper date picker so there is a consistent date/time format throughout the pings
- Formup Time disabled by default. To enable it either check the Pre-Ping checkbox or disable the Formup NOW checkbox below the Formup Time field
- Formup Time is set to NOW by default

## [0.1.7] - 2020-07-08
### Added
- Link to timezones conversion on formup time if the [aa-timezones](https://github.com/ppfeufer/aa-timezones) module is installed

## [0.1.6] - 2020-07-04
### Fixed
- Ping for non default roles via Webhook (#9)

## [0.1.5] - 2020-06-24
### Added
- Configurable Discord webhooks to ping channels automagically

## [0.1.4] - 2020-06-18
### Changed
- Ping Type renamed to Ping Target in form

### Fixed
- typo in Additional Information

## [0.1.3] - 2020-06-15
### Added
- Configuration for additional ping targets and fleet types

## [0.1.2] - 2020-06-14
### Fixed
- sanitizing form field input 

## [0.1.1] - 2020-06-13
### Fixed
- there should always be an empty line before Additional Information ...

## [0.1.0] - 2020-06-13
### Added
- initial version
