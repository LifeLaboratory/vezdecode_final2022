import * as React from "react";
export interface ScrollSaverProps {
    initialScroll?: number;
    saveScroll: (scroll: number) => any;
}
/**
 * @see https://vkcom.github.io/VKUI/#/ScrollSaver
 */
export declare const ScrollSaver: React.FC<ScrollSaverProps>;
