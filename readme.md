# Gemma 3 Function Calling Benchmarks

## Overview

This repository provides the scripts and prompts to benchmark the function calling capabilities of the Gemma 3 family of models. It compares the performance of `1b`, `4b`, `12b`, and `27b` parameter models, as well as their QAT counterparts.

The evaluations have been performed by the Gemini 2.5 Pro Preview model in AI studio using the prompt given in [`prompts/benchmark.md`](prompts/benchmark.md). The test conversations were manually performed using [`scripts/converse.py`](scripts/converse.py) and the test prompts in [`prompts/tests.md`](prompts/tests.md). In the future, I plan to write a script that uses the same Gemini model as a test runner to allow for automated test execution.

## Benchmark Results

### Scores

| Model                 | Instruction Adherence | Function Selection | Parameter Extraction | Graceful Failure | Parallel Calling | Composite Calling | Planning & Reasoning | Output Accuracy | **Overall Score** |
| --------------------- | --------------------- | ------------------ | -------------------- | ---------------- | ---------------- | ----------------- | -------------------- | --------------- | ----------------- |
| **gemma3-27b**        | 4                     | 5                  | 5                    | 5                | **5**            | 5                 | 5                    | 5               | **4.9**           |
| **gemma3-27b-it-qat** | 3                     | 5                  | 5                    | 5                | 3                | 5                 | 4                    | 5               | **4.4**           |
| **gemma3-12b**        | 4                     | 3                  | 5                    | 4                | N/A              | 5                 | 4                    | 5               | **4.0**           |
| **gemma3-12b-it-qat** | 3                     | 4                  | 4                    | 4                | N/A              | 5                 | 3                    | 4               | **3.8**           |
| **gemma3-4b**         | 2                     | 3                  | 4                    | 2                | N/A              | 2                 | 1                    | 2               | **2.0**           |
| **gemma3-4b-it-qat**  | 1                     | 2                  | 2                    | 0                | N/A              | 0                 | 0                    | 0               | **1.0**           |
| **gemma3-1b**         | 0                     | 0                  | 1                    | 0                | N/A              | 0                 | 0                    | 0               | **0.5**           |
| **gemma3-1b-it-qat**  | 1                     | 0                  | 1                    | 0                | N/A              | 0                 | 1                    | 0               | **0.5**           |

> [!NOTE]
> The parallel function calling score for some models is N/A, since the models did not perform parallel calls when expected to. This may be an issue with the wording of the prompt, since only 1 out of 8 invoked the functions in parallel.

### Evaluation of `gemma3-1b`

> `2025-06-13-22-55-29-gemma3-1b.json`

#### **Overall Score: 0.5/5**

This model is not functional as a tool-using agent. It does not understand the fundamental instructions for function calling and resorts to hallucinating responses.

#### Score Breakdown

| Parameter                      | Score | Justification                                                                                                                                                                                 |
| ------------------------------ | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Instruction Adherence**      | 0/5   | The model completely failed to follow the specified format for `thinking` and `function_call`. It produced a hardcoded JSON response instead of invoking a tool.                              |
| **Function Selection**         | 0/5   | The model did not select or call any of the provided functions. It failed Test 1 at the most basic level.                                                                                     |
| **Parameter Extraction**       | 1/5   | It conceptually identified the user's intent ("shipped orders for sara@example.com") in its hallucinated response but failed to use these parameters in an actual function call.              |
| **Graceful Failure**           | 0/5   | When the user pointed out the response was wrong, the model apologized but then repeated the exact same incorrect, hallucinated output, showing no ability to recover or change its strategy. |
| **Parallel Function Calling**  | N/A   | The conversation did not progress far enough to assess this.                                                                                                                                  |
| **Composite Function Calling** | 0/5   | The model failed to execute even a single function call, making composite calling impossible. It failed Test 1 immediately.                                                                   |
| **Planning & Reasoning**       | 0/5   | There was no evidence of planning. The model did not produce a `thinking` block and its actions were not based on a logical sequence of steps to solve the user's problem.                    |
| **Output Accuracy**            | 0/5   | The output was entirely hallucinated and factually incorrect, as confirmed by the user. It was not user-friendly and did not answer the user's question.                                      |

---

### Evaluation of `gemma3-1b-it-qat`

> `2025-06-13-22-56-10-gemma3-1b-it-qat.json`

#### **Overall Score: 0.5/5**

Similar to the base 1b model, this version is non-functional for tool use. While it shows a faint sign of understanding the process by using a `thinking` block, it fails at the critical step of actually calling a function.

#### Score Breakdown

| Parameter                      | Score | Justification                                                                                                                                                                                                                                        |
| ------------------------------ | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Instruction Adherence**      | 1/5   | The model attempted to use the `thinking` block but failed to use the `function_call` format. When corrected by the user, it misunderstood its role and asked the user to name the functions, violating the core instruction of an autonomous agent. |
| **Function Selection**         | 0/5   | No functions were selected or called. It failed Test 1.                                                                                                                                                                                              |
| **Parameter Extraction**       | 1/5   | It correctly identified the necessary parameters in its `thinking` block but failed to apply them in a function call.                                                                                                                                |
| **Graceful Failure**           | 0/5   | The model did not handle its failure gracefully. Instead of attempting to correct its course, it punted the responsibility back to the user, demonstrating a lack of autonomous problem-solving.                                                     |
| **Parallel Function Calling**  | N/A   | The conversation did not provide an opportunity to test this.                                                                                                                                                                                        |
| **Composite Function Calling** | 0/5   | The model failed to execute a single function call.                                                                                                                                                                                                  |
| **Planning & Reasoning**       | 1/5   | It produced a `thinking` block with a rudimentary plan. However, the plan was nonsensical as it involved actions ("Create a list", "Filter the list") that it cannot perform without tools. The reasoning was deeply flawed.                         |
| **Output Accuracy**            | 0/5   | The output was a hallucinated JSON object and did not answer the user's question.                                                                                                                                                                    |

---

### Evaluation of `gemma3-4b`

> `2025-06-13-23-19-26-gemma3-4b.json`

#### **Overall Score: 2/5**

This model understands the basic syntax of function calling but is critically hampered by severe state management issues, causing it to fall into unusable loops. It is too unreliable for practical use.

#### Score Breakdown

| Parameter                      | Score | Justification                                                                                                                                                                                                                                                                        |
| ------------------------------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Instruction Adherence**      | 2/5   | The model used the correct `thinking` and `function_call` formats. However, it got stuck in severe, persistent loops (e.g., calling `get_user_info` repeatedly), failing the implicit instruction to complete the task. This required multiple user interventions to break the loop. |
| **Function Selection**         | 3/5   | It generally selected the correct functions for the task (`get_user_info`, `get_user_orders`). The failure was not in selection but in its inability to stop calling them.                                                                                                           |
| **Parameter Extraction**       | 4/5   | It correctly extracted the necessary parameters like email and order IDs. The main issue was its repeated, unnecessary calls, not its extraction ability.                                                                                                                            |
| **Graceful Failure**           | 2/5   | It showed a good initial recovery in Test 1 by calling `get_user_info` after the first call failed. However, it could not handle its own looping state, which is a critical failure mode it could not escape from gracefully.                                                        |
| **Parallel Function Calling**  | N/A   | The conversation did not provide an opportunity to test this.                                                                                                                                                                                                                        |
| **Composite Function Calling** | 2/5   | It understood the concept of chaining `get_user_info` -> `get_user_orders`. However, its attempt at the more complex chain in Test 2 failed as it fell into a loop, calling `get_user_info` again instead of `get_product_info`.                                                     |
| **Planning & Reasoning**       | 1/5   | The `thinking` blocks revealed the model's broken logic. Its plans were repetitive and it could not maintain a coherent, multi-step strategy, constantly resetting or making illogical choices.                                                                                      |
| **Output Accuracy**            | 2/5   | When it was not looping and finally managed to produce a response (after user help), the summary was accurate. However, it often failed to provide a final response at all due to the loops.                                                                                         |

---

### Evaluation of `gemma3-4b-it-qat`

> `2025-06-13-23-21-38-gemma3-4b-it-qat.json`

#### **Overall Score: 1/5**

This model fails to grasp its role as a function-calling agent. It cannot handle errors and breaks character, making it unsuitable for tool-use tasks.

#### Score Breakdown

| Parameter                      | Score | Justification                                                                                                                                                                                                                                                                  |
| ------------------------------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Instruction Adherence**      | 1/5   | The model failed to use the correct `function_call` format in its first attempt. More critically, it broke character entirely after receiving an error, providing a long, unhelpful technical explanation instead of acting as an agent. This violates the core system prompt. |
| **Function Selection**         | 2/5   | It made a plausible, though incomplete, choice with `get_user_orders` in Test 1. However, it completely abandoned function selection after the first error.                                                                                                                    |
| **Parameter Extraction**       | 2/5   | It correctly identified the user's email but failed to use it in a properly formatted function call.                                                                                                                                                                           |
| **Graceful Failure**           | 0/5   | Its handling of the `UserNotFound` error in Test 4 was a complete failure. Instead of following the user's contingency plan, it stopped and lectured the user about the error's meaning, failing the test entirely.                                                            |
| **Parallel Function Calling**  | N/A   | The conversation did not provide an opportunity to test this.                                                                                                                                                                                                                  |
| **Composite Function Calling** | 0/5   | The model failed at the first step and never attempted to chain calls.                                                                                                                                                                                                         |
| **Planning & Reasoning**       | 0/5   | The initial `thinking` block was malformed. The model showed no evidence of planning or logical reasoning, abandoning the agentic approach after a single error.                                                                                                               |
| **Output Accuracy**            | 0/5   | It never successfully completed a task or provided an accurate, user-friendly response based on tool use.                                                                                                                                                                      |

---

### Evaluation of `gemma3-12b`

> `2025-06-13-23-34-34-gemma3-12b.json`

#### **Overall Score: 4/5**

A very capable and strong model. Its ability to plan, execute complex chains, and handle errors is excellent. Its primary weakness is a tendency to hallucinate functions that don't exist, which impacts its reliability.

#### Score Breakdown

| Parameter                      | Score | Justification                                                                                                                                                                                                           |
| ------------------------------ | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Instruction Adherence**      | 4/5   | Mostly excellent adherence to `thinking` and `function_call` formats. It lost a point for hallucinating functions (`get_order_history`, `get_user_id_by_email`) which violates the rule to only use provided functions. |
| **Function Selection**         | 3/5   | It selected the correct functions for most tests (Tests 1, 2, 3, 7). However, the hallucination of non-existent functions in Test 4 is a significant flaw in its selection capability.                                  |
| **Parameter Extraction**       | 5/5   | Excellent. It correctly parsed emails, status filters, product IDs, and complex query parameters (price ranges, sorting) for Test 7 without issue.                                                                      |
| **Graceful Failure**           | 4/5   | It handled the `UserNotFound` error in Test 4 perfectly by executing the user's fallback plan. It also recovered well when told the function it hallucinated didn't exist.                                              |
| **Parallel Function Calling**  | N/A   | The conversation did not provide an opportunity to test this.                                                                                                                                                           |
| **Composite Function Calling** | 5/5   | Excellent. It flawlessly executed the multi-step reasoning required for Test 2 (`get_user_info` -> `get_user_orders` -> `get_order_details` -> `get_product_info`).                                                     |
| **Planning & Reasoning**       | 4/5   | The `thinking` blocks were clear and logical. It demonstrated a strong ability to formulate and execute multi-step plans. The only deduction is for the instance where its plan involved hallucinated functions.        |
| **Output Accuracy**            | 5/5   | When using the correct functions, the final responses were consistently accurate, user-friendly, and synthesized information correctly.                                                                                 |

---

### Evaluation of `gemma3-12b-it-qat`

> `2025-06-14-00-14-26-gemma3-12b-it-qat.json`, `2025-06-14-00-22-54-gemma3-12b-it-qat.json`, `2025-06-14-00-30-18-gemma3-12b-it-qat.json`

#### **Overall Score: 3.8/5**

A capable model that can handle complex tasks, but its inconsistency and occasional, severe hallucinations make it less reliable than the top performers. It has strong foundational skills but lacks the robust state management of the best models.

#### Score Breakdown

| Parameter                      | Score | Justification                                                                                                                                                                                                                                                                                                                 |
| ------------------------------ | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Instruction Adherence**      | 3/5   | The model's adherence was inconsistent. While it often used the correct formats, it made significant errors. In one instance, after a search, it hallucinated an "add to cart" action. It also violated function specs by using a non-existent `brand` parameter and attempting to call a non-existent `check_time` function. |
| **Function Selection**         | 4/5   | Generally good at selecting the correct function for a given task (e.g., `search_products`, `get_user_info`). The main issue was the hallucinated `check_time` function and the bizarre, unprompted decision to "add to cart".                                                                                                |
| **Parameter Extraction**       | 4/5   | Mostly strong. It correctly handled emails, status filters, and price ranges. It made a mistake by trying to use "Keychron" as a `category` instead of part of the `query`, showing a slight weakness in parsing nuanced requests.                                                                                            |
| **Graceful Failure**           | 4/5   | Handled explicit errors well. It correctly executed the fallback logic in Test 4 and appropriately handled the "out of stock" message in Test 3. However, it handled its _own_ hallucination poorly, doubling down on the "add to cart" error until the user corrected it.                                                    |
| **Parallel Function Calling**  | N/A   | The conversations did not successfully test this. It attempted a related task sequentially in Test 5.                                                                                                                                                                                                                         |
| **Composite Function Calling** | 5/5   | Excellent. It successfully and reliably chained multiple function calls to complete complex tasks like Test 1 and Test 2.                                                                                                                                                                                                     |
| **Planning & Reasoning**       | 3/5   | Highly inconsistent. At times, its `thinking` blocks were clear and logical (e.g., laptop search). At other times, its reasoning completely broke down, as seen with the hallucinated "add to cart" action, which showed a severe lack of situational awareness.                                                              |
| **Output Accuracy**            | 4/5   | When the reasoning was sound, the final output was accurate and user-friendly. The score is lowered due to the instances where it produced confusing and incorrect responses based on its hallucinations.                                                                                                                     |

---

### Evaluation of `gemma3-27b`

> `2025-06-14-00-40-59-gemma3-27b.json`, `2025-06-14-00-49-20-gemma3-27b.json`, `2025-06-14-00-57-14-gemma3-27b.json`

#### **Overall Score: 4.9/5**

An outstanding and highly advanced function-calling model. Its ability to plan, reason, execute parallel and composite calls, and handle errors is top-tier. The single, minor context lapse is the only thing preventing a perfect score.

#### Score Breakdown

| Parameter                      | Score | Justification                                                                                                                                                                                                                                         |
| ------------------------------ | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Instruction Adherence**      | 4/5   | Almost perfect. The only notable error was in Test 3, where it used a hardcoded placeholder `user_id` ("user123") instead of the one it had already retrieved from the conversation context (`789`). This is a minor context retention failure.       |
| **Function Selection**         | 5/5   | Flawless. It consistently chose the correct and most logical function for every step of every test, including complex, multi-step scenarios.                                                                                                          |
| **Parameter Extraction**       | 5/5   | Perfect. It extracted all necessary parameters from user prompts and function outputs, including emails, fallback logic, price ranges, sorting preferences, and product IDs, without any errors or hallucinations.                                    |
| **Graceful Failure**           | 5/5   | Excellent. It handled the `UserNotFound` error in Test 4 perfectly by executing the fallback. It also handled the empty search result for "KeyChron" in Test 6 by clearly explaining the situation and offering helpful alternatives.                 |
| **Parallel Function Calling**  | 5/5   | Excellent. It successfully demonstrated parallel function calling in Test 5. It identified two independent tasks and issued two `function_call` blocks in a single turn, then correctly synthesized the asynchronous responses into one final answer. |
| **Composite Function Calling** | 5/5   | Perfect. It flawlessly executed long and complex chains of function calls to fulfill a series of related user requests, as demonstrated in Test 2 and Test 4.                                                                                         |
| **Planning & Reasoning**       | 5/5   | The `thinking` blocks were exemplary. They were clear, concise, and accurately described a logical, multi-step plan involving both sequential and parallel execution. The reasoning was sound throughout all conversations.                           |
| **Output Accuracy**            | 5/5   | All final responses were accurate, user-friendly, and correctly synthesized information from multiple, sometimes parallel, function calls.                                                                                                            |

---

### Evaluation of `gemma3-27b-it-qat`

> `2025-06-14-02-02-53-gemma3-27b-it-qat.json`, `2025-06-14-02-27-07-gemma3-27b-it-qat.json`, `2025-06-14-02-48-30-gemma3-27b-it-qat.json`, `2025-06-14-02-55-08-gemma3-27b-it-qat.json`


#### **Overall Score: 4.4/5**

An extremely capable model with excellent positive instruction following, planning, and error handling. Its two significant weaknesses are a failure to adhere to negative constraints and occasional context memory lapses, which prevent it from reaching the top tier.

#### Score Breakdown

| Parameter                      | Score | Justification                                                                                                                                                                                                                                                                                                                  |
| ------------------------------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Instruction Adherence**      | 3/5   | The model showed a critical failure in Test 10. It completely ignored the negative constraint ("do not use the `get_product_info` function") and called it anyway. It also demonstrated a significant context memory lapse in Test 3, where it forgot the user's ID it had just fetched, leading to several unnecessary turns. |
| **Function Selection**         | 5/5   | Perfect. In every test case, it selected the correct function or sequence of functions to achieve the user's goal. It did not hallucinate any functions.                                                                                                                                                                       |
| **Parameter Extraction**       | 5/5   | Perfect. It extracted all parameters from user prompts and function outputs with 100% accuracy across all tests.                                                                                                                                                                                                               |
| **Graceful Failure**           | 5/5   | Excellent. It handled the `Forbidden` error in Test 9 perfectly by refusing the action and explaining why. It also handled the `UserNotFound` error in Test 4 by executing the fallback plan. Its self-correction in Test 3 after using the wrong user ID was also very good.                                                  |
| **Parallel Function Calling**  | 3/5   | The model did not successfully demonstrate parallel calling. In Test 5, it correctly identified the two tasks but executed them sequentially, calling `get_current_time` first, waiting for the result, and then proceeding with the order details.                                                                            |
| **Composite Function Calling** | 5/5   | Perfect. It flawlessly executed all sequential and composite calling tests, including the complex chains in Test 2 and Test 4.                                                                                                                                                                                                 |
| **Planning & Reasoning**       | 4/5   | The reasoning is very strong for positive tasks and error handling. The `thinking` blocks are clear and logical. However, its failure to adhere to a negative constraint and its temporary memory lapse indicate a weakness in its reasoning and planning capabilities.                                                        |
| **Output Accuracy**            | 5/5   | All user-facing responses were accurate, well-synthesized, and user-friendly.                                                                                                                                                                                                                                                  |
