import * as React from "react";
import { AdaptivityContextInterface, AdaptivityProps } from "../AdaptivityProvider/AdaptivityContext";
export interface ModalRootProps extends AdaptivityProps {
    activeModal?: string | null;
    /**
     * Будет вызвано при начале открытия активной модалки с её id
     */
    onOpen?(modalId: string): void;
    /**
     * Будет вызвано при окончательном открытии активной модалки с её id
     */
    onOpened?(modalId: string): void;
    /**
     * Будет вызвано при начале закрытия активной модалки с её id
     */
    onClose?(modalId: string): void;
    /**
     * Будет вызвано при окончательном закрытии активной модалки с её id
     */
    onClosed?(modalId: string): void;
}
/**
 * @see https://vkcom.github.io/VKUI/#/ModalRoot
 */
export declare const ModalRoot: React.FC<Pick<ModalRootProps & AdaptivityContextInterface, "onOpen" | "onOpened" | "onClose" | "onClosed" | "activeModal"> & import("../AdaptivityProvider/AdaptivityContext").SizeProps>;
