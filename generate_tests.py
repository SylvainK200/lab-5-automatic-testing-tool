from time import sleep

import google.generativeai as genai
import pickle
from common.abstract_seed import AbstractSeed
from common.llm_test_generator import LLMTestGenerator
from common.prompt_generator import PromptGenerator
from common.abstract_executor import AbstractExecutor
from fuzzers.mutation_fuzzer import MutationFuzzer
from power_schedules.abstract_power_schedule import AbstractPowerSchedule
from to_test.number_to_words import number_to_words
from to_test.strong_password_checker import strong_password_checker
import importlib
from extract_parameter import extract_params, get_type

key = "API_KEY"

def generate_inital_tests_with_llm(model, function_to_test):
    # Create an LLMTestGenerator object with the generative model and the function to test
    llm_generator = LLMTestGenerator(model, function=function_to_test)

    # Create a PromptGenerator object with the function to test
    prompt_generator = PromptGenerator(function_to_test)

    # Generate a prompt for the function
    prompt = prompt_generator.generate_prompt()

    # Print the prompt
    #print(prompt)

    # Create a test function using the LLMTestGenerator
    test, test_name = llm_generator.create_test_function(prompt)

    print("Tests produced by LLM:")

    # Define the filename for the generated test file
    filename = "test_generated.py"

    # Write the test function to the file
    llm_generator.write_test_to_file(test, filename=filename)

    # Get the module name and function name from the filename
    module_name = filename.split(".")[0]
    function_name = test_name

    # Import the module dynamically
    module = importlib.import_module(module_name)

    # Get the function from the module
    function = getattr(module, function_name)

    executor = AbstractExecutor(function)

    # Execute the input function and get the coverage date
    coverage_data = executor._execute_input(input=function_to_test)


    # Print the coverage date
    return function, coverage_data
    

if __name__ == "__main__":

    results = []
    # Configure the generative AI with the API key
    for j in range(5):
        genai.configure(api_key=key)

        # Create a generative model
        model = genai.GenerativeModel('gemini-1.5-pro')

        function_to_test = strong_password_checker #file_name_check
        #function_to_test = strongPasswordChecker


        ######Generate intial tests with LLM

        test, coverage_data = generate_inital_tests_with_llm(model, function_to_test)

        initial_coverage = coverage_data

        # define the executor to be used with your test generator
        executor = AbstractExecutor(function_to_test)
        new_inputs_list = []
        try:

            f  = open('test_generated.py', 'r')
            content = f.readlines()
            parameters = extract_params(content)
            is_a_number = get_type(parameters)
            refined_tests = []
            max_coverage = 0
            max_branches = 0
            to_test = []
            for param in parameters:
                new_param = int(param) if get_type([param]) else param
                to_test.append(new_param)
                coverage = executor._execute_input(input_list = to_test)
                if coverage['coverage']['percent_covered'] > max_coverage or coverage['coverage']['covered_branches'] > max_branches :
                    refined_tests.append(new_param)
                    max_coverage = coverage['coverage']['percent_covered']
                    max_branches = coverage['coverage']['covered_branches']
                to_test = refined_tests.copy()
            list_seeds = [AbstractSeed(str(param)) for param in refined_tests]
            power_schedule = AbstractPowerSchedule()
            min_mutations = 1
            max_mutations = 5
            character_list = ['1','2', '3', '4', '5', '6','7', '8', '9', '0'] if is_a_number else list('@#$%^&*()_+=[]{}|\\/<>.,!?-:;')
            mutation_fuzzer = MutationFuzzer(executor=executor,
                                             power_schedule = power_schedule,
                                             min_mutations = min_mutations,
                                             max_mutations = max_mutations,
                                             seeds=list_seeds,
                                             character_list = character_list)

            refined_to_test  = []
            max_branches = 0
            for i in range(50):
                new_input = mutation_fuzzer.generate_input()

                if(is_a_number):
                    new_input = int(new_input)
                    refined_to_test.extend([new_input])
                    coverage = executor._execute_input(input_list=refined_to_test)

                else:
                    refined_to_test.extend([new_input])
                    coverage = executor._execute_input(input_list=refined_to_test)

                if coverage['coverage']['percent_covered'] > max_coverage or coverage['coverage']['covered_branches'] > max_branches :
                    refined_tests.append(new_input)
                    max_coverage = coverage['coverage']['percent_covered']
                    max_branches = coverage['coverage']['covered_branches']
                refined_to_test = refined_tests.copy()

            final_inputs = []
            to_test  = []
            max_coverage = 0
            max_branches = 0
            i = len(refined_tests) -1
            while i >0 :
                to_test.append(refined_tests[i])
                coverage = executor._execute_input(input_list=to_test)
                if coverage['coverage']['percent_covered'] > max_coverage or coverage['coverage']['covered_branches'] > max_branches :
                    final_inputs.append(refined_tests[i])
                    max_coverage = coverage['coverage']['percent_covered']
                    max_branches = coverage['coverage']['covered_branches']
                to_test = final_inputs.copy()
                i -=1
            new_inputs_list = final_inputs
            print(f"Final inputs : {final_inputs} ")
        except Exception as e:
            print(f"Exception occured: {e}")

        coverage_data = executor._execute_input(input_list=new_inputs_list)
        print(f"Initial number of tests {len(parameters)} and final inputs {len(new_inputs_list)}")
        print(f"Initial coverage: {initial_coverage['coverage']}")
        print(f"Final coverage: {coverage_data['coverage']}")

        line_coverage_improment = coverage_data["coverage"]["percent_covered"] - initial_coverage["coverage"]["percent_covered"]
        branch_coverage_improment = coverage_data["coverage"]["covered_branches"]/coverage_data["coverage"]["num_branches"] - initial_coverage["coverage"]["covered_branches"]/initial_coverage["coverage"]["num_branches"]
        total_tests = len(new_inputs_list)
        final_score = (line_coverage_improment + branch_coverage_improment) / total_tests
        print(f"Final score: {final_score}")
        result = dict()
        result['function_test'] = 'strong_password_checker' if j < 5 else 'number_to_words'
        result['runs'] = (j % 5)+1
        result['generator'] = coverage_data
        result['llm'] = initial_coverage
        result['improvement'] = final_score
        results.append(result)
        sleep(45)
    with open('results_strong_password.pkl', 'wb') as f:  # open a text file
        pickle.dump(results, f)





    




    