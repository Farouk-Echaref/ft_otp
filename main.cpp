#include "ft_otp.hpp"

static void	st_error(const std::string& error)
{
	std::cout << "Error: " << error << std::endl;
	exit(1);
}

static std::map<std::string, std::string>	st_create_tokens(char **input)
{
	int					count;
	std::string				current_val;
	std::map<std::string, std::string>	tokens;

	count = 0;
	while (input[count])
	{
		current_val = input[count];
		if (current_val == "-g")
		{
			count++;
			if (tokens.count("G") || !input[count])
				st_error("(format) ./program [-gk]");
			tokens.insert(std::pair<std::string, std::string>("G", input[count]));
		}
		else if (current_val == "-k")
		{
			count++;
			if (tokens.count("K") || !input[count])
				st_error("(format) ./program [-gk]");
			tokens.insert(std::pair<std::string, std::string>("K", input[count]));
		}
		else
			st_error("(format) ./program [-gk]");
		count++;
	}
	return (tokens);
}

static int	st_execute_tokens(std::map<std::string, std::string> &tokens)
{
	std::string	command;
	std::string	generate;
	std::string	store;

	store = tokens.count("G") ? tokens["G"] : "0";
	generate = tokens.count("K") ? tokens["K"] : "0";
	command = "python3 execute.py ";
	command += store + " ";
	command += generate;
	system(command.c_str());
	return (0);
}

int		main(int argc, char *argv[])
{
	std::map<std::string, std::string>	tokens;

	if (argc != 3)
		st_error("(format) ./program [-gk]");
	tokens = st_create_tokens(argv + 1);
	if (st_execute_tokens(tokens))
		st_error("(exec) ft_otp couldn't be executed");
	return (0);
}
