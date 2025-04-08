
import typing
class LLMTestGenerator():
    """Generator for the LLM test suite."""

    def __init__(self, model, function:typing.Callable):
        """Initialize the generator."""

        self._name = "LLMTestGenerator"
        self.model = model
        self._func_name = function.__name__

    def generate_assertions(self, prompt:str):
        """
        Generates assertions based on the given prompt.

        Args:
            prompt (str): The input prompt for generating assertions.

        Returns:
            str: The generated assertions as a string.
        """

        '''
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
        generated_ids = self.model.generate(input_ids, max_length=512)
        output_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        '''
        test_code = self.model.generate_content(prompt).text
        #print("LLM output: ", test_code)

        return test_code

    def parse_assertions(self, generated_text):
        """
        Parse the generated text and extract lines that contain assertions.

        Args:
            generated_text (str): The generated text to parse.

        Returns:
            list: A list of lines that contain assertions.
        """
        lines = generated_text.split("\n")
        assertions = [
            line.strip() for line in lines if line.strip().startswith("assert")
        ]
        return assertions

    def create_test_function(self, code_snippet):
        """
        Creates a test function for the given code snippet.

        Args:
            code_snippet (str): The code snippet to generate assertions for.

        Returns:
            tuple: A tuple containing the generated test function code and the test function name.
        """
        function_name = self._func_name
        # Generate text that likely includes assertions
        generated_text = self.generate_assertions(code_snippet)

        # Parse the generated text to extract only assertions
        assertions = self.parse_assertions(generated_text)

        # If no assertions were found, include a placeholder to indicate this
        if not assertions:
            formatted_assertions = "assert False, 'No assertions generated'"
        else:
            formatted_assertions = "\n    ".join(assertions)

        # Create the test function with the extracted or placeholder assertions
        test_function_code = (
            f"def test_{function_name}({function_name}):\n    {formatted_assertions}\n"
        )

        return test_function_code, f"test_{function_name}"

    def write_test_to_file(self, test_function_code, filename="test_generated.py"):
        """
        Writes the test function code to a file.

        Args:
            test_function_code (str): The code of the test function to be written.
            filename (str, optional): The name of the file to write the test function code to. 
                Defaults to "test_generated.py".
        """
        with open(filename, "w") as file:
            file.write(test_function_code)
        print(f"Test function written to {filename}")
        
