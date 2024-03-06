import React, { useContext, useState } from 'react';
import { Category } from '../Category';
import { Option } from '../Option/Option';
import { IconId } from 'Common/constants/icons';
import styles from '../Settings/Settings.module.pcss';

import ModalComp from '../ModalComp/ModelComp';
import { theme } from 'Common/styles';
import { rootStore } from 'Options/stores';
import { OPTION_SETTINGS, SETTINGS_NAMES } from 'Common/constants/settings-constants';

type SettingType = "tCNN" | "tCLIP" | "sCNN" | "sCLIP";

type AI_SETTINGS = {
    tCNN: number,
    tCLIP: number,
    sCNN: string,
    sCLIP: string
}

export const AISettings = () => {
    const { settingsStore, uiStore } = useContext(rootStore);

    const [modalOpen, setModalOpen] = useState(
        {
            tCNN: false,
            tCLIP: false,
            sCNN: false,
            sCLIP: false,
        }
    );

    const [aiSettings, setAiSettings] = useState<AI_SETTINGS>(
        {
            tCNN: settingsStore.settings[SETTINGS_NAMES.CNN_PROTECTION_TRESHOLD as keyof OPTION_SETTINGS],
            tCLIP: settingsStore.settings[SETTINGS_NAMES.CLIP_PROTECTION_TRESHOLD as keyof OPTION_SETTINGS],
            sCNN: settingsStore.settings[SETTINGS_NAMES.CNN_PROTECTION_SERVER as keyof OPTION_SETTINGS],
            sCLIP: settingsStore.settings[SETTINGS_NAMES.CLIP_PROTECTION_SERVER as keyof OPTION_SETTINGS]
        }
    )
    const handleSettingChange = (type: SettingType) => {
        switch (type) {
            case "tCNN":

                break;
            case "tCLIP":

                break;
            case "sCNN":

                break;
            case "sCLIP":

                break;
        }
    };

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

            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, tCNN: false }))}
                submitMessage='Submit'
                isValid={true}
                onSubmit={() => handleSettingChange("tCNN")}
                title='CNN treshold'
                isOpen={modalOpen.tCNN}>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={aiSettings.tCNN}
                    onChange={e => setAiSettings(prevState => ({ ...prevState, tCNN: e.target.value }))}
                    placeholder='Confidence percentage'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, tCLIP: false }))}
                submitMessage='Submit'
                isValid={true}
                onSubmit={() => handleSettingChange("tCLIP")}
                title='CLIP treshold'
                isOpen={modalOpen.tCLIP}>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={aiSettings.tCLIP}
                    onChange={e => setAiSettings(prevState => ({ ...prevState, tCLIP: e.target.value }))}
                    placeholder='Confidence percentage'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, sCNN: false }))}
                submitMessage='Submit'
                isValid={true}
                onSubmit={() => handleSettingChange("sCNN")}
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
                isValid={true}
                onSubmit={() => handleSettingChange("sCLIP")}
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

        </Category>
    );
};
