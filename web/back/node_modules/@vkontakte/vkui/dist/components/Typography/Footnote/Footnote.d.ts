import * as React from "react";
import { HasComponent } from "../../../types";
import "./Footnote.css";
export interface FootnoteProps extends React.AllHTMLAttributes<HTMLElement>, HasComponent {
    /**
     * Задаёт начертание шрифта отличное от стандартного.
     */
    weight?: "1" | "2" | "3";
    caps?: boolean;
}
/**
 * @see https://vkcom.github.io/VKUI/#/Footnote
 */
export declare const Footnote: ({ children, weight, caps, Component, ...restProps }: FootnoteProps) => JSX.Element;
