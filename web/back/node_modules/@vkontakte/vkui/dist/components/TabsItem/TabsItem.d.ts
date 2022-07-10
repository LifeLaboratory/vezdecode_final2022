import * as React from "react";
import "./TabsItem.css";
export interface TabsItemProps extends React.HTMLAttributes<HTMLElement> {
    after?: React.ReactNode;
    selected?: boolean;
}
/**
 * @see https://vkcom.github.io/VKUI/#/TabsItem
 */
export declare const TabsItem: React.FC<TabsItemProps>;
