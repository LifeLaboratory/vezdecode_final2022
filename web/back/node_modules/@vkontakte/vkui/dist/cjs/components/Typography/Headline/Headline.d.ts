import * as React from "react";
import { HasComponent } from "../../../types";
import "./Headline.css";
export interface HeadlineProps extends React.AllHTMLAttributes<HTMLElement>, HasComponent {
    /**
     * Задаёт начертание шрифта отличное от стандартного.
     *
     * > ⚠️ Начертания `"semibold"`, `medium` и `"regular"` устарели и будут удалены в 5.0.0. Используйте значения `"1"`, `"2"` и `"3"`.
     */
    weight?: "regular" | "medium" | "semibold" | "1" | "2" | "3";
    level?: "1" | "2";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Headline
 */
export declare const Headline: React.FC<HeadlineProps>;
