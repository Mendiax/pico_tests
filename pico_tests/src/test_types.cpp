#include "test_types.hpp"

TestCaseStats TestCaseStats::operator-(const TestCaseStats& rhs)
{
    TestCaseStats result;
    result.asserts_passed = this->asserts_passed - rhs.asserts_passed;
    result.asserts_failed = this->asserts_failed - rhs.asserts_failed;
    result.asserts_checked = this->asserts_checked - rhs.asserts_checked;
    return result;
}

bool TestCaseStats::check_assert(bool expr)
{
    this->asserts_checked++;
    if(expr)
    {
        this->asserts_passed++;
        return true;
    }
    else
    {
        this->asserts_failed++;
        return false;
    }
}

