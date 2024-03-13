import React, { useContext, useState } from 'react';
import { Category } from '../Category';
import { Option } from '../Option/Option';
import { IconId } from 'Common/constants/icons';
import styles from '../Settings/Settings.module.pcss';

import ModalComp from '../ModalComp/ModelComp';
import { theme } from 'Common/styles';
import { rootStore } from 'Options/stores';
import { SETTINGS_NAMES } from 'Common/constants/settings-constants';

type SettingType = "tCNN" | "tCLIP" | "sCNN" | "sCLIP" | "minImgWidth";

type AI_SETTINGS = {
    tCNN: number,
    tCLIP: number,
    sCNN: string,
    sCLIP: string,
    minImgWidth: number
}

export const AISettings = () => {
    const { settingsStore, uiStore } = useContext(rootStore);
    const [modalOpen, setModalOpen] = useState(
        {
            tCNN: false,
            tCLIP: false,
            sCNN: false,
            sCLIP: false,
            minImgWidth: false
        }
    );

    const [aiSettings, setAiSettings] = useState<AI_SETTINGS>(
        {
            tCNN: settingsStore.settings[SETTINGS_NAMES.CNN_PROTECTION_TRESHOLD],
            tCLIP: settingsStore.settings[SETTINGS_NAMES.CLIP_PROTECTION_TRESHOLD],
            sCNN: settingsStore.settings[SETTINGS_NAMES.CNN_PROTECTION_SERVER],
            sCLIP: settingsStore.settings[SETTINGS_NAMES.CLIP_PROTECTION_SERVER],
            minImgWidth: settingsStore.settings[SETTINGS_NAMES.MIN_IMG_WIDTH]
        }
    )

    const handleSettingSave = (type: SettingType, value: number | string) => {
        switch (type) {
            case "tCNN":
                settingsStore.setSetting(SETTINGS_NAMES.CNN_PROTECTION_TRESHOLD, value)
                break;
            case "tCLIP":
                settingsStore.setSetting(SETTINGS_NAMES.CLIP_PROTECTION_TRESHOLD, value)
                break;
            case "sCNN":
                settingsStore.setSetting(SETTINGS_NAMES.CNN_PROTECTION_SERVER, value)
                break;
            case "sCLIP":
                settingsStore.setSetting(SETTINGS_NAMES.CLIP_PROTECTION_SERVER, value)
                break;
            case "minImgWidth":
                settingsStore.setSetting(SETTINGS_NAMES.MIN_IMG_WIDTH, value)
                break;
        }
        uiStore.addNotification("Setting saved!")
        setModalOpen({ tCLIP: false, sCLIP: false, sCNN: false, tCNN: false, minImgWidth: false })
    };

    function validateUrl(string: string) {
        try {
            new URL(string);
            return true;
        } catch (err) {
            return false;
        }
    }

    return (
        <Category
            navLink="/"
            headerName="AI Settings"
            headerDesc="Edit the prediction tresholds and the servers links"
        >
            <Option
                key={13}
                iconId={IconId.CUSTOM_FILTERS}
                id="13"
                className={styles.optionLabel}
                message="CNN treshold"
                messageDesc="Confidence of the CNN"
                onClick={() => setModalOpen(prevState => ({ ...prevState, tCNN: true }))}
            />
            <Option
                key={14}
                iconId={IconId.CUSTOM_FILTERS}
                id="14"
                className={styles.optionLabel}
                message="CLIP treshold"
                messageDesc="Confidence of the CLIP"
                onClick={() => setModalOpen(prevState => ({ ...prevState, tCLIP: true }))}
            />
            <Option
                key={15}
                iconId={IconId.CUSTOM_FILTERS}
                id="15"
                className={styles.optionLabel}
                message="CNN server"
                messageDesc="The URL for the CNN server"
                onClick={() => setModalOpen(prevState => ({ ...prevState, sCNN: true }))}
            />
            <Option
                key={16}
                iconId={IconId.CUSTOM_FILTERS}
                id="16"
                className={styles.optionLabel}
                message="CLIP server"
                messageDesc="The URL for the CLIP server"
                onClick={() => setModalOpen(prevState => ({ ...prevState, sCLIP: true }))}
            />
            <Option
                key={17}
                iconId={IconId.CUSTOM_FILTERS}
                id="17"
                className={styles.optionLabel}
                message="Minimum image width"
                messageDesc="The size of the image that will be scanned by AI blockers"
                onClick={() => setModalOpen(prevState => ({ ...prevState, minImgWidth: true }))}
            />

            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, tCNN: false }))}
                submitMessage='Submit'
                isValid={!!aiSettings.tCNN}
                onSubmit={() => handleSettingSave("tCNN", aiSettings.tCNN)}
                title='CNN treshold'
                isOpen={modalOpen.tCNN}>
                <input
                    className={theme.modal.modalInput}
                    type="number"
                    step="0.01"
                    value={aiSettings.tCNN.toString()}
                    onChange={e => {
                        const value = parseFloat(e.target.value);
                        setAiSettings(prevState => ({ ...prevState, tCNN: isNaN(value) ? 0 : value }));
                    }}
                    placeholder='Confidence percentage'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, tCLIP: false }))}
                submitMessage='Submit'
                isValid={!!aiSettings.tCLIP}
                onSubmit={() => handleSettingSave("tCLIP", aiSettings.tCLIP)}
                title='CLIP treshold'
                isOpen={modalOpen.tCLIP}>
                <input
                    className={theme.modal.modalInput}
                    type="number"
                    step="0.01"
                    value={aiSettings.tCLIP.toString()}
                    onChange={e => {
                        const value = parseFloat(e.target.value);
                        setAiSettings(prevState => ({ ...prevState, tCLIP: isNaN(value) ? 0 : value }));
                    }}
                    placeholder='Confidence percentage'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, sCNN: false }))}
                submitMessage='Submit'
                isValid={validateUrl(aiSettings.sCNN)}
                onSubmit={() => handleSettingSave("sCNN", aiSettings.sCNN)}
                title='CNN server'
                isOpen={modalOpen.sCNN}>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={aiSettings.sCNN}
                    onChange={e => setAiSettings(prevState => ({ ...prevState, sCNN: e.target.value }))}
                    placeholder='Link to the model.json'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, sCLIP: false }))}
                submitMessage='Submit'
                isValid={validateUrl(aiSettings.sCLIP)}
                onSubmit={() => handleSettingSave("sCLIP", aiSettings.sCLIP)}
                title='CLIP server'
                isOpen={modalOpen.sCLIP}>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={aiSettings.sCLIP}
                    onChange={e => setAiSettings(prevState => ({ ...prevState, sCLIP: e.target.value }))}
                    placeholder='Link to the CLIP server'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, minImgWidth: false }))}
                submitMessage='Submit'
                isValid={!!aiSettings.minImgWidth}
                onSubmit={() => handleSettingSave("minImgWidth", aiSettings.minImgWidth)}
                title='Minim image width'
                isOpen={modalOpen.minImgWidth}>
                <input
                    className={theme.modal.modalInput}
                    type="number"
                    value={aiSettings.minImgWidth.toString()}
                    onChange={e => {
                        const value = parseFloat(e.target.value);
                        setAiSettings(prevState => ({ ...prevState, minImgWidth: isNaN(value) ? 0 : value }));
                    }}
                    placeholder='Confidence percentage'
                />
            </ModalComp>
        </Category>
    );
};
