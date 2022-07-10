import * as React from "react";
import { HasRootRef } from "../../types";
import { RemovableProps } from "../Removable/Removable";
import "./FormLayoutGroup.css";
export interface FormLayoutGroupProps extends React.HTMLAttributes<HTMLDivElement>, RemovableProps, HasRootRef<HTMLDivElement> {
    mode?: "vertical" | "horizontal";
    /**
     * Только для режима horizontal. Дает возможность удалить всю группу `FormItem`.
     */
    removable?: boolean;
}
/**
 * @see https://vkcom.github.io/VKUI/#/FormLayoutGroup
 */
export declare const FormLayoutGroup: React.FC<FormLayoutGroupProps>;
