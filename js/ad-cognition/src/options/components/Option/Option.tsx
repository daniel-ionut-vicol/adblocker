import React from 'react';
import cn from 'classnames';

import { Icon, IconId } from 'Common/components/ui';
import { reactTranslator } from 'Common/translators/reactTranslator';
import { Checkbox } from 'Common/components/Checkbox';

import { HighlightSearch } from '../HighlightSearch';

import styles from '../SwitcherOption/SwitcherOption.module.pcss';

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
}

export const Option = ({
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
}: IProps) => {
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
                <button
                    className={styles.button}
                    type="button"
                    onClick={onClick}
                >
                    {content()}
                </button>
        </label>
    );
};
