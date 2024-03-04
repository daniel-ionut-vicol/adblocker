import { Modal } from 'Common/components/Modal'
import { theme } from 'Common/styles'
import React, { ReactElement } from 'react'
import cn from 'classnames';

type ModalCompProps = {
    children: ReactElement,
    title: string,
    isOpen: boolean,
    description?: string,
    submitMessage: string,
    isValid?: boolean,
    onClose: () => void,
    onSubmit: () => void
}

const ModalComp = (
    {
        children,
        title,
        isOpen,
        description,
        isValid,
        submitMessage,
        onClose,
        onSubmit,
    }: ModalCompProps) => {
    return (
        <Modal isOpen={isOpen} handleClose={onClose} >
            <div className={theme.modal.container}>
                <div className={theme.modal.header}>
                    <h1 className={theme.modal.title}>{title}</h1>
                </div>
                <div className={theme.modal.itemWrapper}>
                    {children}
                </div>
            </div>
            {description &&
                <div className={theme.modal.description}>
                    {description}
                </div>
            }
            <div className={theme.modal.footer}>
                <button
                    className={cn(
                        theme.button.middle,
                        theme.button.green,
                        theme.modal.leftBtn,
                    )}
                    type="submit"
                    disabled={!isValid}
                    onClick={onSubmit}
                >
                    {submitMessage}
                </button>
            </div>
        </Modal>
    )
}

export default ModalComp