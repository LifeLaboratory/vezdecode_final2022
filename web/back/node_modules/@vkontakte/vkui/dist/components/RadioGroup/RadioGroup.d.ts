import * as React from "react";
import "./RadioGroup.css";
export interface RadioGroupProps extends React.HTMLAttributes<HTMLDivElement> {
    mode?: "vertical" | "horizontal";
}
/**
 * @see https://vkcom.github.io/VKUI/#/RadioGroup
 */
export declare const RadioGroup: React.FC<RadioGroupProps>;
