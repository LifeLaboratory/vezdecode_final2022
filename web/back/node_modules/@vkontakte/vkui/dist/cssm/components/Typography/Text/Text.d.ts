import * as React from "react";
import { HasComponent, HasRootRef } from "../../../types";
import "./Text.css";
export interface TextProps extends React.AllHTMLAttributes<HTMLElement>, HasRootRef<HTMLElement>, HasComponent {
    /**
     * Задаёт начертание шрифта, отличное от стандартного.
     *
     * > ⚠️ Начертания `"semibold"`, `medium` и `"regular"` устарели и будут удалены в 5.0.0. Используйте значения `"1"`, `"2"` и `"3"`.
     */
    weight?: "regular" | "medium" | "semibold" | "1" | "2" | "3";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Text
 */
export declare const Text: React.FC<TextProps>;
