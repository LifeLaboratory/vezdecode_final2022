import * as React from "react";
import "./Tabbar.css";
export interface TabbarProps extends React.HTMLAttributes<HTMLDivElement> {
    /**
     * Флаг для показа/скрытия верхней тени (Android) или границы (iOS)
     */
    shadow?: boolean;
    itemsLayout?: "vertical" | "horizontal" | "auto";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Tabbar
 */
export declare const Tabbar: React.FunctionComponent<TabbarProps>;
