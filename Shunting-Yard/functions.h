#ifndef FUNCTIONS_H_INCLUDED
#define FUNCTIONS_H_INCLUDED

#include <string>
#include <vector>
#include <cmath>

struct function
{
    std::string name;
    int numberOfArguments;
    double (*eval)(std::vector<double> args);
};


double add(std::vector<double> args)
{
    return args[1]+args[0];
}

double substract(std::vector<double> args)
{
    return args[1]-args[0];
}

double multiply(std::vector<double> args)
{
    return args[1]*args[0];
}

double divide(std::vector<double> args)
{
    return args[1]/args[0];
}

double power(std::vector<double> args)
{
    return pow(args[1], args[0]);
}



int functions_size = 5;
function functions[] =
{
    {"+", 2, &add},
    {"-", 2, &substract},
    {"*", 2, &multiply},
    {"/", 2, &divide},
    {"^", 2, &power}
};



#endif // FUNCTIONS_H_INCLUDED
