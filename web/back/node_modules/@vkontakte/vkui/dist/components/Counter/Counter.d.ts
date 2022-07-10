import * as React from "react";
import "./Counter.css";
export interface CounterProps extends React.HTMLAttributes<HTMLSpanElement> {
    /**
     * Тип счетчика. При использовании компонента в качестве значения свойства `after` у `Button` эти значения игнорируются
     */
    mode?: "secondary" | "primary" | "prominent" | "contrast";
    size?: "s" | "m";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Counter
 */
export declare const Counter: ({ mode, size, children, ...restProps }: CounterProps) => JSX.Element | null;
