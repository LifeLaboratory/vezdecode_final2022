import * as React from "react";
import { TappableProps } from "../Tappable/Tappable";
import "./PanelHeaderButton.css";
export interface PanelHeaderButtonProps extends Omit<TappableProps, "label"> {
    primary?: boolean;
    label?: React.ReactNode;
}
/**
 * @see https://vkcom.github.io/VKUI/#/PanelHeaderButton
 */
export declare const PanelHeaderButton: React.FC<PanelHeaderButtonProps>;
