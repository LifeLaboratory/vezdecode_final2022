import * as React from "react";
import { SimpleCellProps } from "../SimpleCell/SimpleCell";
import { HasPlatform, HasRootRef } from "../../types";
import { RemovableProps } from "../Removable/Removable";
import "./Cell.css";
export interface CellProps extends Omit<SimpleCellProps, "getRootRef">, HasPlatform, RemovableProps, HasRootRef<HTMLDivElement> {
    mode?: "removable" | "selectable";
    /**
     * В режиме перетаскивания ячейка перестает быть кликабельной, то есть при клике переданный onClick вызываться не будет
     */
    draggable?: boolean;
    /**
     * @deprecated Будет удалено в 5.0.0. Используйте mode="removable"
     */
    removable?: boolean;
    /**
     * Имя для input в режиме selectable
     */
    name?: string;
    /**
     * @deprecated Будет удалено в 5.0.0. Используйте mode="selectable"
     */
    selectable?: boolean;
    /**
     * В режиме selectable реагирует на входящие значения пропса checked, как зависящий напрямую от входящего значения
     */
    checked?: boolean;
    /**
     * В режиме selectable реагирует на входящие значения пропса defaultChecked как неконтролируемый компонент
     */
    defaultChecked?: boolean;
    /**
     * Коллбэк срабатывает при завершении перетаскивания.
     * **Важно:** режим перетаскивания не меняет порядок ячеек в DOM. В коллбэке есть объект с полями `from` и `to`.
     * Эти числа нужны для того, чтобы разработчик понимал, с какого индекса на какой произошел переход. В песочнице
     * есть рабочий пример с обработкой этих чисел и перерисовкой списка.
     */
    onDragFinish?: ({ from, to }: {
        from: number;
        to: number;
    }) => void;
    /**
     * aria-label для кнопки перетаскивания ячейки
     */
    draggerLabel?: string;
}
/**
 * @see https://vkcom.github.io/VKUI/#/Cell
 */
export declare const Cell: React.FC<CellProps>;
