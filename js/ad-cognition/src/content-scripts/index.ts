import '@adguard/tswebextension/mv3/content-script';
import { MESSAGE_TYPES } from 'Common/constants/common';
import { log } from 'Common/logger';
import { SETTINGS_NAMES } from 'Common/constants/settings-constants';

import { subscribe } from './subscribe';
import { ImageCollector } from './imagecollector';

// TODO: Temporary construction for keeping alive service worker
// via constantly standing message exchange
if (window.top === window && (document.documentElement instanceof HTMLElement)) {
    setInterval(() => {
        try {
            chrome.runtime.sendMessage({ type: MESSAGE_TYPES.PING });
            // eslint-disable-next-line no-empty
        } catch (e) { }
    }, 10000);

    function getRuleFromUrl(url: string) {
      try {
        // Create a URL object
        const parsedURL = new URL(url);

        // Extract and return the main domain without the 'www' subdomain
        return parsedURL.hostname.replace(/^www\./, '');
      } catch (error) {
        log.error('Invalid URL:', url);
        return null;
      }
    }

    function isRulePresent(rulesString: string, siteRule: string) {
      // Split the rules string into an array of rules
      const rulesArray = rulesString.split('\n');

      // Check if the siteRule is present in the rulesArray
      return rulesArray.includes(siteRule.trim());
    }

    // TODO: HERE WE SEND A MESSAGE TO CHECK IF THE OPTIONS ARE ENABLED
    // SOMETHING LIKE GET_PROTECTION_SETTINGS
    chrome.runtime.sendMessage({ type: MESSAGE_TYPES.GET_PROTECTION_DATA }).then(({ protectionData }) => {
        const debug_enabled = protectionData[SETTINGS_NAMES.DEBUG_ENABLED];
        const cnn_enabled = protectionData[SETTINGS_NAMES.CNN_PROTECTION_ENABLED];
        const clip_enabled = protectionData[SETTINGS_NAMES.CLIP_PROTECTION_ENABLED];

        chrome.runtime.sendMessage({ type: MESSAGE_TYPES.GET_USER_RULES }).then(userRules => {
          const currentRule = getRuleFromUrl(location.href);

          if ((cnn_enabled || clip_enabled) && !isRulePresent(userRules, `@@||${currentRule!}^$document`)) {
            try {
              const imageCollector = new ImageCollector(debug_enabled, cnn_enabled, clip_enabled);
              imageCollector.init();
              // eslint-disable-next-line no-empty
            } catch (e) {
              log.debug(e);
            }
          }
        })

    });
}

subscribe.init();
