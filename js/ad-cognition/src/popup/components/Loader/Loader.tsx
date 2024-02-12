import React from 'react';

import style from './loader.module.pcss';

export const Loader = () => {
    return (
        // TODO: Maybe add another gif for AdCognition
        <img className={style.loader} src={chrome.runtime.getURL('assets/gifs/loading.gif')} alt="Loading" />
    );
};
