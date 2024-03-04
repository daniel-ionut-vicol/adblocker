import React, { useState } from 'react';
import cn from 'classnames';

import { Icon, IconId } from 'Common/components/ui';

import { HighlightSearch } from '../HighlightSearch';

import styles from './Option.module.pcss';
import { theme } from 'Common/styles';

interface ChangeHandler {
    (e: React.ChangeEvent<HTMLInputElement>): void;
}

interface IProps {
    id: string;
    iconId?: IconId;
    messageDesc?: string;
    message?: string;
    onClick?: () => void;
    onChange?: ChangeHandler;
    className?: string,
    iconClass?: string,
    containerClass?: string,
    integrated?: boolean,
    title?: string,
    value?: string
}

export const InputOption = ({
    id,
    iconId,
    messageDesc,
    message,
    onClick,
    onChange,
    className = '',
    iconClass = '',
    containerClass = '',
    integrated = false,
    title = '',
    value = ''
}: IProps) => {
    const [isValidForm, setIsValidForm] = useState(false);
    const handleValueChange = (v: string) => {
        value = v;
        if (value.length > 0) {
            setIsValidForm(true);
        } else {
            setIsValidForm(false);
        }
    }

    const content = () => {
        return (
            <>
                {iconId && (
                    <span className={styles.icon}>
                        <Icon id={iconId} className={iconClass} />
                    </span>
                )}
                <div className={cn(styles.optionLabel, className)}>
                    {message && (
                        <HighlightSearch str={message} />
                    )}
                    {messageDesc && (
                        <div className={styles.optionLabelDesc}>
                            {messageDesc}
                        </div>
                    )}
                </div>
                <input
                    className={theme.modal.modalInput}
                    type="text"
                    value={value}
                    onChange={e => handleValueChange(e.target.value)}
                    placeholder='Confidence %'
                />
                <button
                    className={cn(
                        theme.button.middle,
                        theme.button.green,
                        theme.modal.leftBtn,
                    )}
                    type="submit"
                    disabled={!isValidForm}
                    onClick={onClick}
                >
                    Update
                </button>
            </>
        );
    };
    return (
        <label
            className={cn(
                styles.optionItem, containerClass, { [styles.disabled]: integrated },
            )}
            htmlFor={id}
            key={id}
            title={title}
        >
            {content()}
        </label>
    );
};
