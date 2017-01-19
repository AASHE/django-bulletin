# Change Log

## [Unreleased]
### Changed

## [3.3.1] - 2017-01-19
### Fixed
- ScheduledPosts weren't getting inserted into Issues.

## [3.3] - 2017-01-17
### Changed
- Updated version of django-constant-contact.
- Updated version of Django.
- Updated version of Pillow.

## [3.2.1] - 2016-08-18
### Changed
- Updated version of django-constant-contact used.

## [3.2] - 2016-08-10
### Changed
- Ad images now displayed in editorial ad list.

## [3.1.2] - 2016-08-09
### Changed
- Upgrade version of django-constant-contact.

## [3.1.1] - 2016-08-09
### Changed
- Updated version of django-constant-contact to get
  HTML minification of email sent to Constant Contact.

## [3.1] - 2016-07-28
### Changed
- Allow footer to show on editorial pages.

## [3.0] - 2016-07-25
### Removed
- Django bootstrap breadcrumbs. Weren't using them anyway.

## [2.3] - 2016-07-25
### Added
- Field `display_weight` to `Ad`. Ads are displayed in ascending order
  of `display_weight`.

## [2.2] - 2016-06-28
### Changed
- "Submit an Item" button is shorter.
- Add before and after post hooks (blocks) in list views.
- Add before and after right sidebar hooks (blocks).

## [2.1.1] - 2016-05-24
### Fixed
- Version in setup.py.

## [2.1] - 2016-05-23
### Removed
- Admin scripts. Let users decide which (and how) django-bulletin
  models should be exposed in the admin interface.

## [2.0.8] - 2016-03-18
### Fixed
- Decode HTML before passing it to downstream CSS inliner.
  Bug was previously masked by Mailchimp service, now replaced
  by premailer.

## [2.0.7] - 2016-03-18
### Changed
- Update version of django-constant-contact.

## [2.0.6] - 2016-03-18
### Changed
- Set zip_safe = False in setup.py.

## [2.0.5] - 2016-03-18
### Fixed
- Setup bug fixed.

## [2.0.3] - 2016-03-18
### Changed
- Trimmed some more requirements.

## [2.0.2] - 2016-03-18
### Changed
- Trimmed requirements.

## [2.0.1] - 2016-03-14
### Changed
- Updated Pillow version in setup.py.
