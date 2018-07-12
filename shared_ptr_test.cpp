
#include <iostream>

#ifdef __clang__
#  warning __clang__
#endif
#ifdef __APPLE__
#  warning __APPLE__
#endif
#if __cplusplus>=201103L
#  warning c++11
#else
#  warning c++98
#endif
#ifdef __GLIBCXX__
#  warning GNU libstdc++
#endif
#ifdef _LIBCPP_VERSION
#  warning llvm libc++
#endif

#if __cplusplus>=201103L || (defined(_MSC_VER) && (_MSC_VER>=1600)) || (__clang__ && __APPLE__)
// c++11 or MSVC 2010
// clang on linux has tr1/memory, clang on OSX doesn't
#  define SHARED_FROM_STD
#  warning From STD

#elif defined(__GNUC__) && __GNUC__>=4 && !defined(vxWorks)
   // GCC >=4.0.0
#  define SHARED_FROM_TR1
#  warning From TR1

#elif defined(_MSC_VER) && (_MSC_VER>1500 || defined(_HAS_TR1))
   // MSVC > 2008, or 2008 w/ SP1
#  define SHARED_FROM_TR1
#  warning From TR1

#else
#  define SHARED_FROM_BOOST
#  warning From Boost
#endif



#if defined(SHARED_FROM_STD)

#include <memory>

namespace std {
    namespace tr1 {
        using ::std::shared_ptr;
        using ::std::weak_ptr;
        using ::std::static_pointer_cast;
        using ::std::dynamic_pointer_cast;
        using ::std::const_pointer_cast;
        using ::std::enable_shared_from_this;
        using ::std::bad_weak_ptr;
    }
}

#elif defined(SHARED_FROM_TR1)
#  include <tr1/memory>

#elif defined(SHARED_FROM_BOOST)

#if defined(__GNUC__) && __GNUC__ < 3
#define BOOST_EXCEPTION_DISABLE
#define BOOST_NO_TEMPLATE_PARTIAL_SPECIALIZATION
#endif

#  include <boost/tr1/memory.hpp>

#else
#  error No shared_ptr selection
#endif

int main(int argc, char *argv[])
{
    std::tr1::shared_ptr<int> I(new int(0));
    return *I;
}
