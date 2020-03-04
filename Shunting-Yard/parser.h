#ifndef PARSER_H_INCLUDED
#define PARSER_H_INCLUDED

#include <string>
#include <vector>
#include <sstream>



// To do: Add error handling


enum TOKEN_TYPE{
    FUNCTION,
    FUNCTION_SEPARATOR,
    LEFT_PARENTHESIS,
    RIGHT_PARENTHESIS,
    OPERATOR,
    NUMBER,
    PARENTHESIS,
    NONE
};



class Parser
{
    public:
        Parser(std::string expression);
        void split();
        bool parse();
        std::vector<std::string> getOutput();
        int order(char op);
        TOKEN_TYPE getType(char character);

    private:
        std::string m_expr;
        std::vector<std::string> m_output;
        std::vector<std::string> m_stack;
        std::vector<std::string> m_split;

};




#endif // PARSER_H_INCLUDED
