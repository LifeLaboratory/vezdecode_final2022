import * as React from "react";
import "./InfoRow.css";
export interface InfoRowProps extends React.HTMLAttributes<HTMLDivElement> {
    header: React.ReactNode;
}
/**
 * @see https://vkcom.github.io/VKUI/#/InfoRow
 */
export declare const InfoRow: React.FunctionComponent<InfoRowProps>;
