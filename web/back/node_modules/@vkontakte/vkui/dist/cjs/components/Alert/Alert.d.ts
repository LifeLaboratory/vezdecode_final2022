import * as React from "react";
import { ButtonProps } from "../Button/Button";
import "./Alert.css";
export declare type AlertActionInterface = AlertAction & React.AnchorHTMLAttributes<HTMLElement>;
export interface AlertAction extends Pick<ButtonProps, "Component" | "href"> {
    title: string;
    action?: VoidFunction;
    autoclose?: boolean;
    mode: "cancel" | "destructive" | "default";
}
export interface AlertProps extends React.HTMLAttributes<HTMLElement> {
    actionsLayout?: "vertical" | "horizontal";
    actions?: AlertAction[];
    header?: React.ReactNode;
    text?: React.ReactNode;
    onClose?: VoidFunction;
    /**
     * `aria-label` для кнопки закрытия. Необходим, чтобы кнопка была доступной.
     */
    dismissLabel?: string;
}
/**
 * @see https://vkcom.github.io/VKUI/#/Alert
 */
export declare const Alert: React.FC<AlertProps>;
