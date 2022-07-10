import * as React from "react";
import { HasPlatform } from "../../types";
import { ConfigProviderContextInterface } from "../ConfigProvider/ConfigProviderContext";
import "./ModalRoot.css";
export interface ModalRootProps extends HasPlatform {
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
    /**
     * @ignore
     */
    configProvider?: ConfigProviderContextInterface;
}
export declare const ModalRootTouch: React.FC<Pick<ModalRootProps, "configProvider" | "onOpen" | "onOpened" | "onClose" | "onClosed" | "activeModal">>;
