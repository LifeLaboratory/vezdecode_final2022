import * as React from "react";
export interface ScrollContextInterface {
    getScroll(): {
        x: number;
        y: number;
    };
    scrollTo(x?: number, y?: number): void;
    isScrollLock: boolean;
    enableScrollLock(): void;
    disableScrollLock(): void;
    beforeScrollLockFnSetRef?: React.RefObject<Set<() => void>>;
}
export declare const ScrollContext: React.Context<ScrollContextInterface>;
export declare const useScroll: () => ScrollContextInterface;
export interface ScrollControllerProps {
    elRef: React.RefObject<HTMLElement>;
}
export declare const GlobalScrollController: React.FC<ScrollControllerProps>;
export declare const ElementScrollController: React.FC<ScrollControllerProps>;
/**
 * Вызывает функцию effect, до блокировки прокрутки
 * @param effect функция, которая может возвращать функцию очистки
 * @param deps effect обновится только при изменении значений в списке.
 */
export declare const useScrollLockEffect: (effect: React.EffectCallback, deps: React.DependencyList) => void;
export declare const useScrollLock: (enabled?: boolean) => void;
