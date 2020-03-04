#include "rpn.h"
#include "functions.h"



int values_size=11;
char values[] = "1234567890.";

RPN::RPN(std::vector<std::string> in)
{
    m_isReplaced = false;
    m_input = in;
}

std::vector<double> RPN::getArguments(int numberOfArguments)
{
    std::vector<double> temp;
    for(int i=0; i<numberOfArguments; i++)
    {
        temp.push_back(m_stack.back());
        m_stack.pop_back();
    }
    return temp;
}

void RPN::goBack()
{
    m_isReplaced = false;
    m_input = m_backup;
}


void RPN::replace(std::string oldVal, double newVal)
{
    if(!m_isReplaced)// Prepare a backup
    {
        m_backup = m_input;
        m_isReplaced = true;
    }
    // Conversion into string
    std::ostringstream strs;
    strs << newVal;
    std::string newValString = strs.str();

    for(int i=0; i<m_input.size(); i++)
    {
        if (m_input[i]==oldVal)
        {
            m_input[i] = newValString;
        }
    }
}

double RPN::evaluate()
{

    for(int i=0; i<m_input.size(); i++)
    {
        if(isValue(m_input[i], 0))
        {
            m_stack.push_back(atof(m_input[i].c_str()));
        }
        else
        {
            double answer=0;
            std::vector<double> args;
            for(int j=0; j<functions_size; j++)
            {
                if(m_input[i]==functions[j].name)
                {
                    args = getArguments(functions[j].numberOfArguments);
                    answer = (*functions[j].eval)(args);
                }
            }

            m_stack.push_back(answer);
        }
    }
    return m_stack.back();
}

bool RPN::isValue(std::string in, int pos)
{
    if(in[pos]=='+' or in[pos]=='-')
    {
        if(in.size()>pos+1)
        {
            if(isValue(in, pos+1))
                return true;
        }
    }
    for(int i=0;i<values_size;i++)
    {
        if(in[pos]==values[i])
            return true;
    }
    return false;
}
