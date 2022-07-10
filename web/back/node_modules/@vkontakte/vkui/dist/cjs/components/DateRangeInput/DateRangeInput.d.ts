import * as React from "react";
import { CalendarRangeProps } from "../CalendarRange/CalendarRange";
import { Placement } from "../Popper/Popper";
import { HasRootRef } from "../../types";
import "./DateRangeInput.css";
export interface DateRangeInputProps extends Omit<React.InputHTMLAttributes<HTMLDivElement>, "value" | "onChange">, Pick<CalendarRangeProps, "disablePast" | "disableFuture" | "shouldDisableDate" | "onChange" | "value" | "weekStartsOn" | "disablePickers" | "prevMonthAriaLabel" | "nextMonthAriaLabel" | "changeMonthAriaLabel" | "changeYearAriaLabel" | "changeDayAriaLabel" | "prevMonthIcon" | "nextMonthIcon">, HasRootRef<HTMLDivElement> {
    calendarPlacement?: Placement;
    closeOnChange?: boolean;
    clearFieldAriaLabel?: string;
    showCalendarAriaLabel?: string;
    changeStartDayAriaLabel?: string;
    changeStartMonthAriaLabel?: string;
    changeStartYearAriaLabel?: string;
    changeEndDayAriaLabel?: string;
    changeEndMonthAriaLabel?: string;
    changeEndYearAriaLabel?: string;
}
/**
 * @see https://vkcom.github.io/VKUI/#/DateRangeInput
 */
export declare const DateRangeInput: React.FC<DateRangeInputProps>;
