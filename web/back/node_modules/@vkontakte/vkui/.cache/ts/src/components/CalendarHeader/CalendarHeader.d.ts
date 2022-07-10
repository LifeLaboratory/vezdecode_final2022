import * as React from "react";
import "./CalendarHeader.css";
export interface CalendarHeaderProps extends Pick<React.HTMLAttributes<HTMLDivElement>, "className"> {
    viewDate: Date;
    prevMonth?: boolean;
    nextMonth?: boolean;
    disablePickers?: boolean;
    prevMonthAriaLabel?: string;
    nextMonthAriaLabel?: string;
    changeMonthAriaLabel?: string;
    changeYearAriaLabel?: string;
    prevMonthIcon?: React.ReactNode;
    nextMonthIcon?: React.ReactNode;
    onChange(viewDate: Date): void;
    /**
     * Нажатие на кнопку переключения на следующий месяц.
     */
    onNextMonth?(): void;
    /**
     * Нажатие на кнопку переключения на предыдущий месяц.
     */
    onPrevMonth?(): void;
}
export declare const CalendarHeader: React.FC<CalendarHeaderProps>;
