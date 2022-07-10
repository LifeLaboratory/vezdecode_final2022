import { DOMProps } from "../../lib/dom";
import * as React from "react";
import "./CustomScrollView.css";
export interface CustomScrollViewProps extends DOMProps {
    windowResize?: boolean;
    boxRef?: React.Ref<HTMLDivElement>;
    className?: HTMLDivElement["className"];
    children: React.ReactNode;
}
export declare const CustomScrollView: ({ className, children, boxRef: externalBoxRef, windowResize, }: CustomScrollViewProps) => JSX.Element;
