import React from 'react';

import { reactTranslator } from 'Common/translators/reactTranslator';
import { theme } from 'Common/styles';

import styles from './About.module.pcss';

export const About = () => {
    return (
        <section className={styles.container}>
            <h2 className={theme.common.headingMain}>
                {reactTranslator.getMessage('options_about_title')}
            </h2>
            <div className={theme.common.headingSecondary}>
                <div>
                    {reactTranslator.getMessage('options_about_product')}
                </div>
                <div>
                    {`${reactTranslator.getMessage('options_about_version')} ${chrome.runtime.getManifest().version} `}
                </div>
            </div>
            <div className={theme.common.headingSecondary}>
                <div>
                    {`© 2009-${new Date().getFullYear()} AdCognition Software Ltd.`}
                </div>
                <div>
                    {reactTranslator.getMessage('options_about_rights_reserved')}
                </div>
            </div>
        </section>
    );
};
