# Ad Cognition

## How to build

## Requirements

* `nodejs` - **only version 16**.
* `yarn` - nodejs package manager.

### Prepare

* `yarn install` - install necessary dependencies.
* `yarn filters` - download the latest versions of the filter lists built-in the
  extension and convert them to declarative format.

### Build

* `yarn release` - release build.
* `yarn dev` - dev build.
* `yarn dev --watch` - prepare the dev build and monitor the files for changes.
  Note, that this command will not run filters conversion, you'll need to do it
  manually.

### Test

- `yarn test` - run local unit tests using Jest.
- To run the supported [testcases](https://testcases.agrd.dev/) using Playwright:
  - `yarn integration-test dev` for dev build test;
  - `yarn integration-test release` for release build test.

## Permissions required
- `tabs`                          - this permission is required in order to get the URL of the options page tab
- `alarms`                        - this permission is required in order to set the pause protection timer
- `contextMenus`                  - this permission is required in order to create a context menu
- `scripting`                     - this permission is required in order to inject assistant script only in the required pages
- `storage`                       - this permission is required in order to save user settings, user rules and custom filters
- `declarativeNetRequest`         - this permission is required in order to block, redirect and modify URL requests
- `declarativeNetRequestFeedback` - this permission is required in order to create a log of the blocked, redirected or modified URL requests
- `unlimitedStorage`              - this permission is required in order to save large filters
- `webNavigation`                 - this permission is required in order to catch the moment for injecting scriptlets

## Dependencies
1. `nodejs` - https://nodejs.org/en/download/, **only version 16**
2. `yarn`, nodejs package manager - https://classic.yarnpkg.com/lang/en/docs/install
