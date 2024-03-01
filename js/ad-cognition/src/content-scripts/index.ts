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
            const parsedURL = new URL(url);
            return `@@||${parsedURL.hostname.replace(/^www\./, '')}^$document`;
        } catch (error) {
            log.error('Invalid URL:', url);
            return null;
        }
    }

    function isRulePresent(rulesString: string, siteRule: string) {
        const rulesArray = rulesString.split('\n');

        return rulesArray.includes(siteRule.trim());
    }

    document.addEventListener('DOMContentLoaded', function () {

        const imgTags = document.querySelectorAll('img');

        const imgArray = Array.from(imgTags);

        chrome.runtime.sendMessage({ type: MESSAGE_TYPES.GET_PROTECTION_DATA }).then(({ protectionData }) => {
            log.debug(protectionData)
            const debug_enabled = protectionData[SETTINGS_NAMES.DEBUG_ENABLED];
            const cnn_enabled = protectionData[SETTINGS_NAMES.CNN_PROTECTION_ENABLED];
            const clip_enabled = protectionData[SETTINGS_NAMES.CLIP_PROTECTION_ENABLED];

            chrome.runtime.sendMessage({ type: MESSAGE_TYPES.GET_USER_RULES }).then(userRules => {
                const currentRule = getRuleFromUrl(location.href);

                if ((cnn_enabled || clip_enabled) && !isRulePresent(userRules, currentRule!)) {
                    try {
                        const imageCollector = new ImageCollector(debug_enabled, cnn_enabled, clip_enabled, imgArray);
                        imageCollector.init();
                        // eslint-disable-next-line no-empty
                    } catch (e) {
                        log.debug(e);
                    }
                }
            })
        });
    });
}

subscribe.init();
