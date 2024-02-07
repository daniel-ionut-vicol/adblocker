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
    // TODO: HERE WE SEND A MESSAGE TO CHECK IF THE OPTIONS ARE ENABLED
    // SOMETHING LIKE GET_PROTECTION_SETTINGS
    chrome.runtime.sendMessage({ type: MESSAGE_TYPES.GET_PROTECTION_DATA }).then(({ protectionData }) => {
        const debug_enabled = protectionData[SETTINGS_NAMES.DEBUG_ENABLED];
        const cnn_enabled = protectionData[SETTINGS_NAMES.CNN_PROTECTION_ENABLED];
        const clip_enabled = protectionData[SETTINGS_NAMES.CLIP_PROTECTION_ENABLED];

        log.debug('GOT THE SETTINGS FROM BACKGROUND', protectionData);

        if (cnn_enabled || clip_enabled) {
            try {
                const imageCollector = new ImageCollector(debug_enabled, cnn_enabled, clip_enabled);
                imageCollector.init();
                // eslint-disable-next-line no-empty
            } catch (e) {
                log.debug(e);
            }
        }
    });
}

subscribe.init();
