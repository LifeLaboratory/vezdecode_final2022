import * as React from "react";
import { ConfigProviderContextInterface } from "./ConfigProviderContext";
import { AppearanceScheme } from "../../helpers/scheme";
export interface ConfigProviderProps extends Partial<ConfigProviderContextInterface> {
    /**
     * @deprecated будет удалено в 5.0.0, устанавливать тему следует через appearance
     * Цветовая схема приложения
     */
    scheme?: AppearanceScheme;
    /**
      Локаль ([список](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry))
     */
    locale?: string;
}
/**
 * @see https://vkcom.github.io/VKUI/#/ConfigProvider
 */
export declare const ConfigProvider: React.FC<ConfigProviderProps>;
