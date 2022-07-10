import * as React from "react";
import { AvatarProps } from "../Avatar/Avatar";
import { HasRootRef } from "../../types";
import "./GridAvatar.css";
export interface GridAvatarProps extends React.HTMLAttributes<HTMLDivElement>, HasRootRef<HTMLDivElement>, Pick<AvatarProps, "size" | "shadow" | "badge"> {
    /**
     * Массив со ссылками. От 1 до 4 элементов.
     */
    src?: string[];
}
export declare const MAX_GRID_LENGTH = 4;
/**
 * @see https://vkcom.github.io/VKUI/#/GridAvatar
 */
export declare const GridAvatar: ({ src, ...restProps }: GridAvatarProps) => JSX.Element;
