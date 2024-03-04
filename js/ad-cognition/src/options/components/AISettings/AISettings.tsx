import React, { useState } from 'react';
import { Category } from '../Category';
import { Option } from '../Option/Option';
import { IconId } from 'Common/constants/icons';
import styles from '../Settings/Settings.module.pcss';

import ModalComp from '../ModalComp/ModelComp';
import { theme } from 'Common/styles';

export const AISettings = () => {
    const [modalOpen, setModalOpen] = useState(
        {
            tresholdCNN: false,
            tresholdCLIP: false,
            serverCNN: false,
            serverCLIP: false,
        }
    );

    const [aiSettings, setAiSettings] = useState(
        {
            tresholdCNN: "",
            tresholdCLIP: "",
            serverCNN: "",
            serverCLIP: "",
        }
    )

    type SettingType = "tCNN" | "tCLIP" | "sCNN" | "sCLIP";

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

            default:
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
                message="CNN Treshold"
                messageDesc="Confidence of the CNN"
                onClick={() => setModalOpen(prevState => ({ ...prevState, tresholdCNN: true }))}
                onChange={() => { }} />
            <Option
                key={14}
                iconId={IconId.CUSTOM_FILTERS}
                id="14"
                className={styles.optionLabel}
                message="CLIP Treshold"
                messageDesc="Confidence of the CLIP"
                onClick={() => setModalOpen(prevState => ({ ...prevState, tresholdCLIP: true }))}
                onChange={() => { }} />
            <Option
                key={15}
                iconId={IconId.CUSTOM_FILTERS}
                id="15"
                className={styles.optionLabel}
                message="CNN Server"
                messageDesc="The URL for the CNN server"
                onClick={() => setModalOpen(prevState => ({ ...prevState, serverCNN: true }))}
                onChange={() => { }} />
            <Option
                key={16}
                iconId={IconId.CUSTOM_FILTERS}
                id="16"
                className={styles.optionLabel}
                message="CLIP Server"
                messageDesc="The URL for the CLIP server"
                onClick={() => setModalOpen(prevState => ({ ...prevState, serverCLIP: true }))}
                onChange={() => { }} />

            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, tresholdCNN: false }))}
                submitMessage='Submit'
                isValid={true}
                onSubmit={() => handleSettingChange("tCNN")}
                title='CNN Treshold'
                isOpen={modalOpen.tresholdCNN}>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={aiSettings.tresholdCNN}
                    onChange={e => setAiSettings(prevState => ({ ...prevState, tresholdCNN: e.target.value }))}
                    placeholder='http://example.com/model.json'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, tresholdCLIP: false }))}
                submitMessage='Submit'
                isValid={true}
                onSubmit={() => handleSettingChange("tCLIP")}
                title='CLIP Treshold'
                isOpen={modalOpen.tresholdCLIP}>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={aiSettings.tresholdCLIP}
                    onChange={e => setAiSettings(prevState => ({ ...prevState, tresholdCLIP: e.target.value }))}
                    placeholder='http://example.com/model.json'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, serverCNN: false }))}
                submitMessage='Submit'
                isValid={true}
                onSubmit={() => handleSettingChange("sCNN")}
                title='CNN Server'
                isOpen={modalOpen.serverCNN}>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={aiSettings.serverCNN}
                    onChange={e => setAiSettings(prevState => ({ ...prevState, serverCNN: e.target.value }))}
                    placeholder='http://example.com/model.json'
                />
            </ModalComp>
            <ModalComp
                onClose={() => setModalOpen(prevState => ({ ...prevState, serverCLIP: false }))}
                submitMessage='Submit'
                isValid={true}
                onSubmit={() => handleSettingChange("sCLIP")}
                title='CLIP Server'
                isOpen={modalOpen.serverCLIP}>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={aiSettings.serverCLIP}
                    onChange={e => setAiSettings(prevState => ({ ...prevState, serverCLIP: e.target.value }))}
                    placeholder='http://example.com/model.json'
                />
            </ModalComp>

        </Category>
    );
};
