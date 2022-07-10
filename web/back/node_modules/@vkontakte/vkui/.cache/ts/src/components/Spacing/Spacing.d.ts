import * as React from "react";
import "./Spacing.css";
export interface SpacingProps extends React.HTMLAttributes<HTMLDivElement> {
    /**
     * Высота спэйсинга
     */
    size?: number;
    /**
     * @deprecated Это свойство устарело и будет удалено в 5.0.0. Используйте [`Separator`](#/Separator) вместе с Spacing.
     * Настройка положения сепаратора:
     *
     * - separator=false (default) - без сепаратора
     * - separator=true | separator='center' - сепаратор располагается по середине
     * - separator='top'
     * - separator='bottom'
     */
    separator?: boolean | "top" | "bottom" | "center";
    children?: React.ReactNode;
}
/**
 * @see https://vkcom.github.io/VKUI/#/Spacing
 */
export declare const Spacing: ({ size, separator, style, ...restProps }: SpacingProps) => JSX.Element;
