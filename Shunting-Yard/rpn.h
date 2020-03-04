#ifndef RPN_H_INCLUDED
#define RPN_H_INCLUDED

#include <stdlib.h>
#include <vector>
#include <string>
#include <sstream>



class RPN
{
    public:
        RPN(std::vector<std::string> in);
        double evaluate();
        std::vector<double> getArguments(int numberOfArguments);
        bool isValue(std::string in, int pos);
        void replace(std::string oldVal, double newVal);
        void goBack();


    private:
        std::vector<std::string> m_input;
        std::vector<double> m_stack;
        std::vector<std::string> m_backup;
        bool m_isReplaced;
};

#endif // RPN_H_INCLUDED
