import * as React from "react";
import "./Separator.css";
export interface SeparatorProps extends React.HTMLAttributes<HTMLDivElement> {
    /**
     * С этим свойством компонент не будет иметь отступы слева и справа
     */
    wide?: boolean;
    /**
     * @deprecated Это свойство устарело и будет удалено в 5.0.0. Используйте [`Spacing`](#/Spacing).
     */
    expanded?: boolean;
}
/**
 * @see https://vkcom.github.io/VKUI/#/Separator
 */
export declare const Separator: React.FC<SeparatorProps>;
