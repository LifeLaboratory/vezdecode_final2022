import * as React from "react";
import { HasComponent, HasRootRef } from "../../../types";
import "./Paragraph.css";
export interface ParagraphProps extends React.AllHTMLAttributes<HTMLElement>, HasRootRef<HTMLElement>, HasComponent {
    /**
     * Задаёт начертание шрифта, отличное от стандартного.
     */
    weight?: "1" | "2" | "3";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Paragraph
 */
export declare const Paragraph: React.FC<ParagraphProps>;
