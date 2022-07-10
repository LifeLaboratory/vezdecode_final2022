import * as React from "react";
import "./PanelHeaderContent.css";
export interface PanelHeaderContentProps extends React.HTMLAttributes<HTMLDivElement> {
    aside?: React.ReactNode;
    before?: React.ReactNode;
    status?: React.ReactNode;
}
/**
 * @see https://vkcom.github.io/VKUI/#/PanelHeaderContent
 */
export declare const PanelHeaderContent: React.FunctionComponent<PanelHeaderContentProps>;
