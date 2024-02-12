export enum SETTINGS_NAMES {
    /* VERSION */
    VERSION = 'version',

    /* GLOBAL FILTERING */
    PROTECTION_PAUSE_EXPIRES = 'protection.pause.expires',
    PROTECTION_ENABLED = 'protection.enabled',
    CNN_PROTECTION_ENABLED = 'protection.cnn.enabled',
    CLIP_PROTECTION_ENABLED = 'protection.clip.enabled',
    DEBUG_ENABLED = 'debug.enabled',

    POPUP_V3_WIZARD_ENABLED = 'popup.v3.wizard.enabled',
    NOTICE_HIDDEN = 'notice.hidden',

    FILTERS_CHANGED = 'filters.changed',
}

export const SCHEME_VERSION = 3;

export const DEFAULT_SETTINGS = {
    [SETTINGS_NAMES.VERSION]: SCHEME_VERSION,

    [SETTINGS_NAMES.PROTECTION_ENABLED]: true,
    [SETTINGS_NAMES.CNN_PROTECTION_ENABLED]: true,
    [SETTINGS_NAMES.CLIP_PROTECTION_ENABLED]: true,
    [SETTINGS_NAMES.DEBUG_ENABLED]: false,
    [SETTINGS_NAMES.PROTECTION_PAUSE_EXPIRES]: 0,

    [SETTINGS_NAMES.POPUP_V3_WIZARD_ENABLED]: true,
    [SETTINGS_NAMES.NOTICE_HIDDEN]: false,

    [SETTINGS_NAMES.FILTERS_CHANGED]: [] as number[],
};

export type SettingsType = typeof DEFAULT_SETTINGS;

export type SettingsValueType = SettingsType[keyof SettingsType];

export type OPTION_SETTINGS = Pick<SettingsType,
SETTINGS_NAMES.NOTICE_HIDDEN
| SETTINGS_NAMES.FILTERS_CHANGED
>;

export type POPUP_SETTINGS = Pick<SettingsType,
SETTINGS_NAMES.PROTECTION_ENABLED
| SETTINGS_NAMES.PROTECTION_PAUSE_EXPIRES
| SETTINGS_NAMES.POPUP_V3_WIZARD_ENABLED
| SETTINGS_NAMES.FILTERS_CHANGED
>;
