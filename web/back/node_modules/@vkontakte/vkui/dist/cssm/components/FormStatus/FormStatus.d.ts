import * as React from "react";
import "./FormStatus.css";
export interface FormStatusProps extends React.HTMLAttributes<HTMLDivElement> {
    mode?: "default" | "error";
    header?: React.ReactNode;
}
/**
 * @see https://vkcom.github.io/VKUI/#/FormStatus
 */
export declare const FormStatus: React.FunctionComponent<FormStatusProps>;
