1. **Comments**: The code includes both single-line (//) and multi-line (/* */) comments for adding explanatory notes to the code.

2. **Variable Declarations**:
   - Variables are declared using the `let` keyword, followed by the variable name and an initial value.
   - Examples: 
    ```
    let var_name = 10
    let bool_var = true
    let other_bool_var = false
    ```

3. **Function Declarations**:
   - Functions are defined using the `fn` keyword.
   - Only Anonymous functions are defined by specifying parameters and a code block.
   - Example: 
   ```
   let add_function = fn (a, b) => {
        a + b 
    }
   ```

4. **Conditional Statements**:
   - Conditional statements are shown using an `if...else` construct within a function.
   - The code demonstrates a simple if-else function.
   - Example: 
   ```
    let if_else_funtion = fn (size) => { 
        if (size < 100) { "small" } else { "big" } 
    }
   ```

5. **Tuples**:
   - Tuples with two values are created using parentheses.
   - Example: `let some_tuple = (1, 2)`

6. **Global Functions**:
   - The code mentions global functions like `print`, `first`, and `second`.
   - `print` is used to output text.
   - `first` and `second` are used to access the elements of a tuple.
   - Example: `print("The print() global function")`, `print(first((1, 2)))`

7. **Arithmetic Operators**:
   - Basic arithmetic operations are demonstrated, including addition, subtraction, multiplication, and division.
   - Division is shown to truncate decimals.
   - Examples: 
   ```
    let sum = 10 + 10
    let minus = 10 - 10
    let multi = 10 * 10
    let div = 5 / 2
    ```

8. **Logical Operators**:
   - Logical operators such as equality, inequality, less than, greater than, less than or equal, greater than or equal, logical AND, and logical OR are used.
   - Examples: 
   ```
   let equals = "a" == "a" 
   let negation = "a" != "b"
   let less_than = 1 < 2`
   let and = true && false`
   let or = false || true
   ```
   