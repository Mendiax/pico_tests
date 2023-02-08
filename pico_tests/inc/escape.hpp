#ifndef ESCAPE_HPP
#define ESCAPE_HPP

#define ESC "\x1b"
#define ESC_RESET ESC "[0m"
#define ESC_RED ESC "[1;31m"
#define ESC_GREEN ESC "[1;32m"
#define ESC_WHITE ESC "[1;37m"

#define ESC_PAINT(esc_color, string) esc_color string ESC_RESET

#endif