import * as React from "react";
import { HasRef, HasRootRef } from "../../types";
import "./SimpleCheckbox.css";
export interface SimpleCheckboxProps extends React.InputHTMLAttributes<HTMLInputElement>, HasRootRef<HTMLLabelElement>, HasRef<HTMLInputElement> {
    indeterminate?: boolean;
    defaultIndeterminate?: boolean;
}
/**
 * @deprecated Этот компонент устарел и будет удален в 5.0.0. Используйте [`Checkbox`](#/Checkbox).
 * @see https://vkcom.github.io/VKUI/#/SimpleCheckbox
 */
export declare const SimpleCheckbox: React.FC<SimpleCheckboxProps>;
