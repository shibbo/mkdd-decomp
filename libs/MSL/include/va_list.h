#ifndef VA_LIST_H
#define VA_LIST_H

#ifdef __cplusplus              /* hh  971206  */
namespace std {
	extern "C" {
#endif

typedef struct {
    char gpr;
    char fpr;
    char res[2];
    char* input_arg_area;
    char* reg_save_area;
} __va_list[1];

typedef __va_list va_list;

#ifdef __cplusplus
    };
};
#endif

#endif // VA_LIST_H