import * as React from "react";
import { HoverPopperProps } from "../HoverPopper/HoverPopper";
import "./RichTooltip.css";
export declare type RichTooltipProps = Omit<HoverPopperProps, "arrowClassName">;
/**
 * @see https://vkcom.github.io/VKUI/#/RichTooltip
 */
export declare const RichTooltip: React.FC<RichTooltipProps>;
