import * as React from "react";
import { HasRootRef } from "../../types";
import "./CustomSelectOption.css";
export interface CustomSelectOptionProps extends React.HTMLAttributes<HTMLDivElement>, HasRootRef<HTMLDivElement> {
    /**
     * Вставляет основной контент.
     */
    option?: any;
    /**
     * Добавляет описание под основным блоком.
     */
    description?: React.ReactNode;
    /**
     * Вставляет элемент в начало блока перед основным контентом.
     * Например, можно передать компонент `Avatar`, `Icon<Name>` или другие изображения.
     */
    before?: React.ReactNode;
    /**
     * Вставляет элемент в конец блока после основного контента.
     * Например, можно передать компонент `Avatar`, `Icon<Name>` или другие изображения.
     */
    after?: React.ReactNode;
    /**
     * Позволяет создавать вложенность.
     */
    hierarchy?: number;
    /**
     * Включает состояние выбранного элемента списка.
     */
    selected?: boolean;
    /**
     * Включает состояние наведения.
     */
    hovered?: boolean;
    /**
     * Включает состояние фокуса.
     */
    focused?: boolean;
    /**
     * Блокирует весь блок.
     */
    disabled?: boolean;
}
/**
 * @see https://vkcom.github.io/VKUI/#/CustomSelectOption
 */
export declare const CustomSelectOption: React.FC<CustomSelectOptionProps>;
