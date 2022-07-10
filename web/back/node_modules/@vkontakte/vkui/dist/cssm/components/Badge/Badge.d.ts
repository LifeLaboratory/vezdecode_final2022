import * as React from "react";
import "./Badge.css";
export interface BadgeProps extends React.HTMLAttributes<HTMLElement> {
    mode: "new" | "prominent";
}
/**
 * @see https://vkcom.github.io/VKUI/#/Badge
 */
export declare const Badge: React.FC<BadgeProps>;
