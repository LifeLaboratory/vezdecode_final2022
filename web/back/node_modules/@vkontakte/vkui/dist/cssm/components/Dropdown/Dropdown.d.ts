import * as React from "react";
import { HoverPopperProps } from "../HoverPopper/HoverPopper";
import { ClickPopperProps } from "../ClickPopper/ClickPopper";
import "./Dropdown.css";
export interface DropdownProps extends Omit<ClickPopperProps, "arrow" | "arrowClassName">, Omit<HoverPopperProps, "arrow" | "arrowClassName"> {
    action?: "click" | "hover";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Dropdown
 */
export declare const Dropdown: React.FC<DropdownProps>;
