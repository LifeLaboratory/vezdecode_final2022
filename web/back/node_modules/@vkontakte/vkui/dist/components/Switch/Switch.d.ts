import * as React from "react";
import { HasRootRef } from "../../types";
import { VisuallyHiddenInputProps } from "../VisuallyHiddenInput/VisuallyHiddenInput";
import "./Switch.css";
export interface SwitchProps extends VisuallyHiddenInputProps, HasRootRef<HTMLLabelElement> {
}
/**
 * @see https://vkcom.github.io/VKUI/#/Switch
 */
export declare const Switch: React.FC<SwitchProps>;
