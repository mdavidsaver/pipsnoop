#ifndef FOO_H
#define FOO_H

#ifdef _WIN32
# ifdef BUILD_FOO
#  define FOO_API __declspec(dllexport)
# else
#  define FOO_API __declspec(dllimport)
# endif
#else
# define FOO_API
#endif

FOO_API int foo(void);

#endif /* FOO_H */
