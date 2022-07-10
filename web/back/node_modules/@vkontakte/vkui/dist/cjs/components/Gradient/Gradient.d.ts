import * as React from "react";
import "./Gradient.css";
export interface GradientProps extends React.HTMLAttributes<HTMLDivElement> {
    mode?: "tint" | "white" | "black";
    to?: "top" | "bottom";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Gradient
 */
export declare const Gradient: React.FC<GradientProps>;
