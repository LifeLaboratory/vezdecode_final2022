import * as React from "react";
export interface TransitionContextProps {
    entering: boolean;
}
export declare const useNavTransition: () => TransitionContextProps;
export declare const NavTransitionProvider: React.FC<TransitionContextProps>;
