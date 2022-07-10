import * as React from "react";
import "./Spinner.css";
export interface SpinnerProps extends React.HTMLAttributes<HTMLSpanElement> {
    size?: "small" | "regular" | "medium" | "large";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Spinner
 */
export declare const Spinner: React.MemoExoticComponent<({ size, "aria-label": ariaLabel, ...restProps }: SpinnerProps) => JSX.Element>;
