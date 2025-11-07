import streamlit as st
import json
import base64
from io import BytesIO

# --- (1) DATA INITIALIZATION ---
# This is the "database" of your app.
# It's populated with all the rich content from the study guide.
# It defines the schema for the entire application state.

def get_initial_data():
    """
    Initializes the session state with all syllabus modules, topics,
    definitions, tips, and PYQs.
    This is the master data structure.
    """
    return {
        "modules": {
            "Module 1: Regular Languages": {
                "Introduction to Formal Language Theory": {
                    "definition": """
                    **Alphabet (Σ):** A finite, non-empty set of symbols.
                    * *Example:* `Σ = {0, 1}` (binary alphabet)
                    * *Example:* `Σ = {a, b, c}` (lowercase alphabet)

                    **String (w):** A finite sequence of symbols from an alphabet.
                    * *Example:* `w = 01101` is a string over `Σ = {0, 1}`.
                    * **Empty String (ε):** A string with zero symbols. It is a valid string.
                    * **Length of String (|w|):** The number of symbols in the string. `|01101| = 5`, `|ε| = 0`.

                    **Language (L):** A set of strings over an alphabet. This set can be finite or infinite.
                    * *Example (Finite):* `L = {all binary strings of length 2} = {00, 01, 10, 11}`
                    * *Example (Infinite):* `L = {all binary strings with an even number of 0s}`
                    """,
                    "pyq_focus": "These definitions are used in Part A questions to define a language you need to build a machine for. Understand them perfectly.",
                    "strategy": "This is the foundation. Do not mix up a *string* (a single sequence) with a *language* (a *set* of strings). The empty string `ε` is a string, *not* a language. The language containing only the empty string is `{ε}`.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Deterministic Finite State Automata (DFA)": {
                    "definition": """
                    A DFA is a 5-tuple `(Q, Σ, δ, q₀, F)` where:
                    1.  **Q:** A finite set of states.
                    2.  **Σ:** A finite alphabet.
                    3.  **δ (Transition Function):** `δ: Q × Σ → Q`. This function takes a state and an input symbol and returns *exactly one* next state.
                    4.  **q₀ ∈ Q:** The single start state.
                    5.  **F ⊆ Q:** The set of final/accepting states.

                    

                    **Key Properties:**
                    * **Deterministic:** For every state, there is *exactly one* transition on *every* symbol in the alphabet.
                    * No `ε` (empty string) transitions are allowed.
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* Design a DFA for a given language (e.g., 'binary strings divisible by 3', 'strings containing `aba`', 'strings with even `a`'s and odd `b`'s').\n* Part A questions will ask for simpler DFAs ('starts with 10', 'length is multiple of 3').",
                    "strategy": """
                    Practice is the only way. When designing a DFA, ask yourself: "What does my machine need to *remember*?"
                    * For "even number of `a`'s", you need two states: `q_even` and `q_odd`.
                    * For "divisible by 3", you need three states: `q_rem0`, `q_rem1`, `q_rem2`, representing the remainder so far.
                    * For "contains `aba`", you need states to track the prefix: `q_start` (nothing), `q_a` (saw `a`), `q_ab` (saw `ab`), `q_aba` (saw `aba`, final state).
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Nondeterministic Finite State Automata (NFA)": {
                    "definition": """
                    An NFA is a 5-tuple `(Q, Σ, δ, q₀, F)` where the transition function is:
                    **δ: Q × (Σ ∪ {ε}) → 2^Q** (The power set of Q)

                    **This means:**
                    1.  **Choice:** A state can have *multiple* transitions on one symbol.
                    2.  **No Transition:** A state can have *zero* transitions on one symbol.
                    3.  **ε-Moves:** An NFA can transition to another state *without* reading any input symbol (an `ε` move).

                    

                    An NFA accepts a string if *any* possible path for that string ends in a final state.
                    """,
                    "pyq_focus": "Designing NFAs (which is often easier than DFAs, e.g., 'string whose 3rd-to-last symbol is 1').\n* Understanding `ε-closure`.\n* Being the *input* for the NFA-to-DFA conversion.",
                    "strategy": "Think of NFAs as 'guessers.' For '3rd-to-last symbol is 1', an NFA can just 'guess' which '1' is the 3rd-to-last and then verify there are two more symbols. This is much simpler than the corresponding DFA.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Equivalence of DFA and NFA": {
                    "definition": "For every NFA, there exists an equivalent DFA that accepts the *exact same language*. This is a fundamental theorem proved using **Subset Construction**.",
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* Given an NFA (with or without ε-moves), convert it into an equivalent DFA using the **Subset Construction algorithm**.",
                    "strategy": """
                    This is a pure algorithm. Master the steps.
                    1.  **Start State:** The start state of the DFA is the `ε-closure` of the NFA's start state. `DFA_start = ε-closure(NFA_q₀)`.
                    2.  **New States:** The states in your new DFA will be *sets* of NFA states (e.g., `{q₀, q₁, q₃}`).
                    3.  **Algorithm:**
                        * Create a queue and add your new DFA start state to it.
                        * While the queue is not empty:
                            * Dequeue a state `S` (which is a set of NFA states).
                            * For each symbol `a` in the alphabet:
                                * Find `move(S, a)`: This is the set of all states the NFA could reach from any state in `S` on input `a`.
                                * Find `T = ε-closure(move(S, a))`.
                                * This `T` is your new state.
                                * The transition is `δ(S, a) = T`.
                                * If `T` is a new state you haven't seen, add it to the queue.
                    4.  **Final States:** Any new DFA state (set) that contains *at least one* of the NFA's final states is a final state in the DFA.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Regular Grammar (RG)": {
                    "definition": """
                    A grammar where all production rules are in a specific, restricted format.
                    * **Right-Linear Grammar:** All rules are of the form `A → aB` or `A → a`.
                    * **Left-Linear Grammar:** All rules are of the form `A → Ba` or `A → a`.

                    A grammar must be *either* purely right-linear or purely left-linear to be a Regular Grammar.
                    """,
                    "pyq_focus": "Write a Regular Grammar for a simple language.\n* Convert a DFA/NFA to an equivalent RG and vice-versa.",
                    "strategy": "There is a 1-to-1 mapping:\n* **FA to RG:** A transition `δ(q_i, a) = q_j` becomes a rule `q_i → a q_j`. If `q_j` is a final state, you also add the rule `q_i → a`.\n* **RG to FA:** A rule `A → aB` becomes a transition from state `A` to state `B` on input `a`. A rule `A → a` becomes a transition from `A` to a new, final `accept` state.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            },
            "Module 2: More on Regular Languages": {
                "Regular Expression (RE)": {
                    "definition": """
                    A compact syntax for describing a regular language.
                    **Core Operations:**
                    1.  **Alternation (Union):** `r + s` or `r | s` (matches `r` or `s`)
                    2.  **Concatenation:** `rs` (matches `r` followed by `s`)
                    3.  **Kleene Star:** `r*` (matches zero or more `r`'s)

                    * `r+` (one or more) is shorthand for `rr*`.
                    * `r?` (zero or one) is shorthand for `r + ε`.
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* Given a language description, write the Regular Expression for it.\n* Example: 'Write an RE for all strings over {0,1} that do not contain `11` as a substring.'\n* Example: 'Write an RE for strings with an even number of 0s.'",
                    "strategy": "Break the problem down. \n* 'At least one `a`': `(a+b)* a (a+b)*`\n* 'Even number of 0s': `(1* 0 1* 0)* 1*` (any number of 1s, then a pair of 0s, repeat, then any number of 1s).\n* 'Does not contain 11': `(0+10)* (1?)` (Any number of 0s or 10s, optionally ending in a single 1).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Equivalence of REs and DFA": {
                    "definition": "**Kleene's Theorem:** A language is regular (accepted by a DFA/NFA) if and only if it can be described by a Regular Expression. This is a 3-way equivalence: `DFA ⇔ NFA ⇔ RE`.",
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* **RE to NFA-ε:** Given an RE, convert it to an NFA using **Thompson's Construction**.\n* **DFA to RE:** Given a DFA, convert it to an RE using **state elimination** (or Arden's Theorem).",
                    "strategy": """
                    **Thompson's Construction (RE -> NFA):** This is another algorithm. Learn the building blocks:
                    
                    * You build NFAs for the base symbols, then combine them using `ε` moves.
                    
                    **State Elimination (DFA -> RE):**
                    1.  Add a new unique start state with an `ε` move to the old start state.
                    2.  Add a new unique final state and `ε` moves from all old final states to it.
                    3.  Repeatedly pick a state (that is not the new start or final) and "rip it out."
                    4.  When ripping out state `q`, for every pair of states `p` (in) and `r` (out), you create a new transition from `p` to `r`.
                    5.  If `p -> (a) -> q -> (b) -> r` and `q` has a self-loop `(c)*`, the new transition is `p -> (a c* b) -> r`. You add this (using `+`) to any existing `p -> (d) -> r` transition, making it `p -> (d + a c* b) -> r`.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Pumping Lemma for Regular Languages": {
                    "definition": """
                    A theorem used to prove that a language is **NOT** regular.
                    
                    **The Lemma:** If `L` is a regular language, then there exists a "pumping length" `p` (a magic number) such that for *any* string `s` in `L` with `|s| ≥ p`, `s` can be split into three parts, `s = xyz`, satisfying:
                    1.  `|y| > 0` (the part to be pumped is not empty)
                    2.  `|xy| ≤ p` (the pumpable part is near the beginning)
                    3.  `xyⁱz ∈ L` for all `i ≥ 0` (you can pump `y` 0, 1, 2, ... times and the string stays in the language)
                    """,
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* 'Use the Pumping Lemma to prove that L = {aⁿbⁿ | n ≥ 0} is NOT regular.'\n* Other common languages: {aᵖ | p is prime}, {ww | w ∈ {a,b}*}, {aⁿ!}",
                    "strategy": """
                    This is a proof by contradiction. **MEMORIZE THIS TEMPLATE:**
                    1.  **Assume:** Assume `L` *is* regular (to find a contradiction).
                    2.  **Lemma:** The Pumping Lemma must hold. Let `p` be the pumping length.
                    3.  **Choose String:** **You** must choose a specific, clever string `s` in `L` such that `|s| ≥ p`.
                        * *Good choice for {aⁿbⁿ}:* `s = aᵖbᵖ`.
                    4.  **Split:** The lemma says `s` can be split into `xyz` where `|y| > 0` and `|xy| ≤ p`.
                        * Because `|xy| ≤ p`, for our string `s = a...a b...b`, `x` and `y` must *both* consist *only* of `a`'s. So `x = aʲ`, `y = aᵏ`, `z = aˡbᵖ`, where `j+k+l = p` and `k > 0`.
                    5.  **Pump:** The lemma says `xyⁱz` must be in `L` for all `i`. Let's test `i = 2` (or `i = 0`).
                        * `xy²z = x y y z = aʲ aᵏ aᵏ aˡ bᵖ = aʲ⁺²ᵏ⁺ˡ bᵖ = aᵖ⁺ᵏ bᵖ`.
                    6.  **Contradiction:** Since `k > 0`, `p+k ≠ p`. This string `aᵖ⁺ᵏ bᵖ` does *not* have an equal number of `a`'s and `b`'s. Therefore, `xy²z ∉ L`.
                    7.  **Conclusion:** This is a contradiction. Our initial assumption that `L` is regular must be false.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Closure Properties of Regular Languages": {
                    "definition": "A set is 'closed' under an operation if applying that operation to members of the set always results in another member of the set.\n\nRegular Languages are **closed** under:\n* Union (`L₁ U L₂`)\n* Intersection (`L₁ ∩ L₂`)\n* Complementation (`L̅`)\n* Concatenation (`L₁L₂`)\n* Kleene Star (`L*`)\n* Difference (`L₁ - L₂`)\n* Reverse (`Lᴿ`)",
                    "pyq_focus": "Part A: 'List three closure properties.'\n* Part B: 'Prove that Regular Languages are closed under Union (or Intersection, etc.).'",
                    "strategy": "Know the proofs. \n* **Union/Concat/Star:** Easy. Use Thompson's construction on the REs, or `ε`-move constructions on the NFAs.\n* **Complementation:** Easy for DFAs. Just flip all final states to non-final and all non-final states to final. (This only works on a *complete* DFA, so add a 'dead state' if needed).\n* **Intersection:** Easy. Use the Complementation proof and De Morgan's Law: `L₁ ∩ L₂ = (L₁̅ U L₂̅)̅`. Or, by *product construction* (a DFA whose states are pairs of states from the two original DFAs).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "DFA State Minimization": {
                    "definition": "The algorithm to find the *unique* minimal DFA (the one with the fewest possible states) for a given regular language. The most common method is the **Table-Filling Algorithm** (based on Myhill-Nerode).",
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* 'Minimize the following DFA.' [A diagram of a DFA is given].",
                    "strategy": """
                    This is another pure algorithm.
                    1.  **Remove Unreachable States:** Do a simple graph traversal (like BFS) from the start state. Any state you don't reach can be deleted.
                    2.  **Create the Table:** Draw a grid with all pairs of states `(q_i, q_j)` where `i > j`.
                    3.  **Step 1 (Initial Mark):** Mark any pair `(q_i, q_j)` where one state is final and the other is not. These are "distinguishable".
                    4.  **Step 2 (Iterative Mark):** Loop through all unmarked pairs `(p, q)`:
                        * For each symbol `a` in the alphabet, find their transitions: `p' = δ(p, a)` and `q' = δ(q, a)`.
                        * Look up the pair `(p', q')` in your table (or `(q', p')` if it's in the other order).
                        * **If the pair `(p', q')` is already marked**, then `(p, q)` is also distinguishable. Mark `(p, q)`.
                    5.  **Repeat Step 2:** Keep looping until a full pass of the table results in *no new marks*.
                    6.  **Merge:** All remaining *unmarked* pairs are equivalent. Merge them into a single state. Redraw the DFA.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            },
            "Module 3: CFGs and Myhill-Nerode": {
                "Myhill-Nerode Theorem": {
                    "definition": """
                    A powerful theorem that gives a different characterization of regular languages.
                    
                    It defines an "indistinguishability relation" `R_L`: Two strings `x` and `y` are indistinguishable (written `x R_L y`) if for *all* possible suffixes `z`, either *both* `xz` and `yz` are in `L`, or *neither* is.
                    
                    **The Theorem:** A language `L` is regular **if and only if** the number of equivalence classes of `R_L` is **finite**.
                    
                    **Bonus:** The number of states in the minimal DFA for `L` is *exactly* the number of these equivalence classes.
                    """,
                    "pyq_focus": "State the Myhill-Nerode Theorem.\n* List its applications (DFA minimization, proving non-regularity).\n* (Harder) Show the equivalence classes for a given language.",
                    "strategy": "This theorem is the *theory* behind the table-filling minimization algorithm. The algorithm is just a practical way of finding these 'indistinguishable' equivalence classes.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Context Free Grammar (CFG)": {
                    "definition": """
                    A more powerful type of grammar than a Regular Grammar.
                    A CFG is a 4-tuple `(V, T, P, S)` where:
                    1.  **V (Variables):** A finite set of non-terminal symbols (e.g., `S`, `A`, `B`).
                    2.  **T (Terminals):** A finite set of terminal symbols (the alphabet, e.g., `a`, `b`).
                    3.  **P (Productions):** A set of rules of the form `A → w`, where `A` is a *single* variable and `w` is *any string* of variables and terminals (`w ∈ (V U T)*`).
                    4.  **S ∈ V:** The start symbol.

                    **Key Property:** The rule `A → w` can be applied *regardless of the context* in which `A` appears. This is why it's "Context-Free".
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* Write a CFG for a given language.\n* Common examples: `L = {aⁿbⁿ}`, `L = {palindromes}`, `L = {equal number of a's and b's}`.",
                    "strategy": """CFGs allow for *recursion* and *nesting*, which regular languages don't.
                    * For `L = {aⁿbⁿ}`: `S → aSb | ε`. This rule perfectly captures the "one `a` for every one `b`" and "nesting" structure.
                    * For Palindromes: `S → aSa | bSb | a | b | ε`.
                    * For Equal `a`'s and `b`'s: `S → aSbS | bSaS | ε`.""",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Derivation Trees and Ambiguity": {
                    "definition": """
                    **Derivation Tree (Parse Tree):** A graphical way to show how a string is derived from a CFG's start symbol.
                    * The root is the start symbol.
                    * Internal nodes are variables.
                    * Leaves are terminals.
                    * Reading the leaves from left to right yields the final string.

                    **Ambiguity:** A grammar is **ambiguous** if there exists at least one string in its language that has:
                    1.  Two or more different **leftmost derivations**, OR
                    2.  Two or more different **rightmost derivations**, OR
                    3.  Two or more different **parse trees**.

                    (All three are equivalent definitions).
                    """,
                    "pyq_focus": "Given a grammar and a string, show two parse trees to prove it is ambiguous.\n* The classic example is the arithmetic expression grammar: `E → E+E | E*E | id`.",
                    "strategy": "For the grammar `E → E+E | id`, the string `id+id+id` has two parse trees: one for `(id+id)+id` and one for `id+(id+id)`. This ambiguity is bad for programming language compilers, as it means 'what to do first' is unclear. This is why operator precedence (e.g., `*` before `+`) is defined.",
                    "done": False ,"my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Normal Forms for CFGs": {
                    "definition": """
                    Standard formats for CFGs that make them easier to work with.
                    
                    **Chomsky Normal Form (CNF):** All productions are of the form:
                    * `A → BC` (two variables)
                    * `A → a` (one terminal)
                    * (Optionally, `S → ε` is allowed if the language contains `ε`)
                    
                    **Greibach Normal Form (GNF):** All productions are of the form:
                    * `A → aβ` (one terminal, followed by zero or more *variables*)
                    """,
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* 'Convert the following CFG into Chomsky Normal Form.'\n* 'Convert the following CFG into Greibach Normal Form.'",
                    "strategy": """
                    These are pure, multi-step algorithms. They are long and tedious, but are "free marks" if you memorize the steps.
                    
                    **CNF Conversion (in order):**
                    1.  **START:** Add a new start symbol `S₀ → S`.
                    2.  **TERM (Terminate):** Get rid of terminals in "mixed" rules. `A → aB` becomes `A → X_a B` and `X_a → a`.
                    3.  **BIN (Binarize):** Shorten long rules. `A → BCD` becomes `A → BZ` and `Z → CD`.
                    4.  **DEL (Delete):** Eliminate `ε`-productions (e.g., `A → ε`). This is the hardest step. If `B → AC` and `A` can go to `ε`, you must add a new rule `B → C`.
                    5.  **UNIT (Unit):** Eliminate unit productions (e.g., `A → B`). Replace the rule with `A → [all of B's productions]`.
                    
                    **GNF Conversion:** This is more complex. The main idea is to eliminate left-recursion and then use substitution to get a terminal at the start of every rule.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            },
            "Module 4: Context-Free Languages": {
                "Nondeterministic Pushdown Automata (PDA)": {
                    "definition": """
                    An NFA with a **stack**. This stack provides infinite memory, but it can only be accessed in a LIFO (Last-In, First-Out) manner.
                    
                    A PDA is a 7-tuple `(Q, Σ, Γ, δ, q₀, Z₀, F)` where:
                    * `Q, Σ, q₀, F` are like in an NFA.
                    * **Γ (Gamma):** The finite stack alphabet.
                    * **Z₀ ∈ Γ:** The initial stack symbol.
                    * **δ (Transition Function):** `δ: Q × (Σ ∪ {ε}) × (Γ ∪ {ε}) → 2^(Q × (Γ ∪ {ε}))`
                    
                    This means a transition is based on:
                    1.  Current state
                    2.  Input symbol (or `ε`)
                    3.  What's on top of the stack (or `ε` for "don't care/don't pop")
                    
                    The transition results in:
                    1.  A new state
                    2.  A symbol (or `ε` for "don't push") to be pushed onto the stack.
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* Design a PDA for a given language.\n* Common examples: `L = {aⁿbⁿ}`, `L = {wcwᴿ}` (palindromes with center marker), `L = {wwᴿ}` (even-length palindromes).",
                    "strategy": """
                    The stack is your memory.
                    * For `L = {aⁿbⁿ}`:
                        1.  In `q₀`, for every `a` you read, PUSH an `X` onto the stack.
                        2.  When you read the first `b`, transition to state `q₁`.
                        3.  In `q₁`, for every `b` you read, POP one `X` from the stack.
                        4.  If the input ends and the stack is empty (you see `Z₀`), move to a final state `q_f`.
                    * PDAs are non-deterministic. For `L = {wwᴿ}`, the PDA has to "guess" where the middle of the string is.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Deterministic Pushdown Automata (DPDA)": {
                    "definition": "A PDA that is 'deterministic.' This means that for any given state, input symbol, and stack symbol, there is *at most one* valid transition. DPDAs cannot have 'choice.'\n\nDPDAs recognize the set of **Deterministic Context-Free Languages**, which is a *proper subset* of all Context-Free Languages. For example, `L = {aⁿbⁿ}` is a DCFL, but `L = {wwᴿ}` is *not* (the PDA has to non-deterministically guess the midpoint).",
                    "pyq_focus": "Differentiate between PDA and DPDA.\n* Give an example of a CFL that is not a DCFL.",
                    "strategy": "The key limitation is 'choice.' If the machine ever has to 'guess,' it's not deterministic. The `wwᴿ` (palindromes) language is the classic example of a non-DPDA language.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Equivalence of PDAs and CFGs": {
                    "definition": "A fundamental theorem: A language `L` is Context-Free (generated by a CFG) **if and only if** it is accepted by some PDA. `CFG ⇔ PDA`.",
                    "pyq_focus": "State the theorem.\n* (Harder) Convert a given CFG to an equivalent PDA.\n* (Harder) Convert a given PDA to an equivalent CFG.",
                    "strategy": "The algorithm to convert **CFG -> PDA** is fairly standard: Create a PDA that simulates the grammar's derivations. It starts by pushing the Start symbol `S` on the stack. It then non-deterministically applies production rules. If it sees a variable `A` on the stack, it pops it and pushes one of `A`'s productions (e.g., `aBb`). If it sees a terminal `a` on the stack, it must match it with the input.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Pumping Lemma for Context-Free Languages": {
                    "definition": """
                    The tool to prove a language is **NOT** Context-Free.
                    
                    **The Lemma:** If `L` is a CFL, there exists a pumping length `p` such that for any string `s` in `L` with `|s| ≥ p`, `s` can be split into *five* parts, `s = uvwxy`, satisfying:
                    1.  `|vwx| ≤ p` (the "pumpable" part is of limited length)
                    2.  `|vx| > 0` (at least one of `v` or `x` is not empty)
                    3.  `uvⁱwxⁱy ∈ L` for all `i ≥ 0` (you can pump `v` and `x` in tandem)
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* 'Use the Pumping Lemma for CFLs to prove that L = {aⁿbⁿcⁿ | n ≥ 0} is NOT Context-Free.'\n* Other example: `L = {aⁱbʲcᵏ | i < j < k}`.",
                    "strategy": """
                    Another proof by contradiction. **MEMORIZE THIS TEMPLATE:**
                    1.  **Assume:** Assume `L` *is* a CFL.
                    2.  **Lemma:** The Pumping Lemma must hold. Let `p` be the pumping length.
                    3.  **Choose String:** **You** choose a clever string `s` in `L`.
                        * *Good choice for {aⁿbⁿcⁿ}:* `s = aᵖbᵖcᵖ`.
                    4.  **Split:** The lemma says `s = uvwxy` where `|vwx| ≤ p` and `|vx| > 0`.
                        * Because `|vwx| ≤ p`, the substring `vwx` *cannot* span all three groups of letters. It can only contain `a`'s and `b`'s, OR `b`'s and `c`'s, OR just one letter type. It *cannot* contain `a`'s, `b`'s, *and* `c`'s.
                        * Also, `v` and `x` cannot *both* be empty.
                    5.  **Pump:** Let's pump `i = 2`. `uv²wx²y`.
                        * **Case 1:** `vwx` is all `a`'s. Then `v` and/or `x` are `a`'s. Pumping gives `aᵖ⁺ᵏbᵖcᵖ`. This is not in `L`.
                        * **Case 2:** `vwx` contains `a`'s and `b`'s. Then `v` and `x` can contain `a`'s and `b`'s, but *no c's*. Pumping `i=2` adds `a`'s and `b`'s, but no `c`'s. The string is `aᵖ⁺ᵏbᵖ⁺ᵐcᵖ`. This is not in `L`.
                        * **Case 3:** `vwx` contains `b`'s and `c`'s. Pumping adds `b`'s and `c`'s, but no `a`'s. Not in `L`.
                    6.  **Contradiction:** In all possible cases, pumping `i=2` (or `i=0`) results in a string not in `L`.
                    7.  **Conclusion:** This is a contradiction. `L` is not a CFL.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Closure Properties of Context-Free Languages": {
                    "definition": "CFLs are **closed** under:\n* Union\n* Concatenation\n* Kleene Star\n\nCFLs are **NOT** closed under:\n* Intersection\n* Complementation",
                    "pyq_focus": "List closure properties of CFLs.\n* Prove CFLs are closed under Union.\n* Prove CFLs are *not* closed under Intersection.",
                    "strategy": "Proof for **not closed under Intersection**:\n1.  Let `L₁ = {aⁿbⁿcᵐ | n,m ≥ 0}`. This is a CFL. (You push `a`'s, pop `b`'s, then ignore `c`'s).\n2.  Let `L₂ = {aᵐbⁿcⁿ | n,m ≥ 0}`. This is a CFL. (You ignore `a`'s, then push `b`'s, pop `c`'s).\n3.  `L₁ ∩ L₂ = {aⁿbⁿcⁿ | n ≥ 0}`.\n4.  We just proved using the Pumping Lemma that `{aⁿbⁿcⁿ}` is **NOT** a CFL.\n5.  Since we intersected two CFLs and got a non-CFL, the set of CFLs is not closed under intersection.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            },
            "Module 5: Turing Machines": {
                "Context Sensitive Languages (CSL)": {
                    "definition": "A language generated by a **Context-Sensitive Grammar (CSG)**. \nA CSG has rules of the form `αAβ → αγβ`, where `A` can only be replaced by `γ` in the 'context' of `α` and `β`. \nA simpler definition is that for any rule `u → v`, `|u| ≤ |v|` (rules never shrink the string, except `S → ε`).\n\nCSLs are recognized by **Linear Bounded Automata (LBA)**, which is a Turing Machine that can only use the tape space occupied by the *original input*.",
                    "pyq_focus": "Write a CSG for `L = {aⁿbⁿcⁿ}`.\n * Define LBA.",
                    "strategy": "The CSG for `aⁿbⁿcⁿ` is a classic example to know, but complex. The key idea is that CSLs can handle the 'counting' of `aⁿbⁿcⁿ` which CFLs cannot.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Turing Machines (TM)": {
                    "definition": """
                    The most powerful model of computation. It is a finite automaton (like a DFA) with a "head" that can read and write symbols on an *infinite* tape, and move left or right.

                    

                    A TM is a 7-tuple `(Q, Σ, Γ, δ, q₀, q_accept, q_reject)`:
                    * `Q, Σ, q₀` are as before.
                    * **Γ (Gamma):** The tape alphabet (contains `Σ` and a blank symbol `B`).
                    * **δ (Transition Function):** `δ: Q × Γ → Q × Γ × {L, R}`
                    * `q_accept` and `q_reject` are special halting states.

                    A transition `δ(q, a) = (p, b, L)` means: "If in state `q` reading an `a`, change to state `p`, write a `b` on the tape, and move the head Left."
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* Design a Turing Machine for a given language or function.\n* Examples: `L = {aⁿbⁿcⁿ}`, `L = {ww}`.\n* Function computation: 'Design a TM to compute 2's complement', 'Design a TM to add two unary numbers'.",
                    "strategy": """
                    Designing a TM is like writing a low-level program.
                    **Strategy for `L = {aⁿbⁿcⁿ}`:**
                    1.  Start at the leftmost `a`. Mark it (e.g., write `X`) and move right.
                    2.  Scan right, past all `a`'s and `Y`'s, until you find the first `b`. Mark it (write `Y`) and move right.
                    3.  Scan right, past all `b`'s and `Z`'s, until you find the first `c`. Mark it (write `Z`).
                    4.  **Rewind:** Move the head all the way left until you hit the first symbol after the start marker.
                    5.  **Loop:** Go back to step 1 (find the next `a`).
                    6.  **Check:** If you scan for an `a` and find a `Y` (a marked `b`), it means you ran out of `a`'s. Now, you must check if you also ran out of `b`'s and `c`'s. Scan right. If you see only `Y`'s, then `Z`'s, then a blank, you accept.
                    7.  If at any point you can't find the `a`, `b`, or `c` you're looking for, you go to `q_reject`.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Universal Turing Machine (UTM)": {
                    "definition": "A UTM, `U`, is a specific Turing Machine that can *simulate* any other Turing Machine `M` on any input `w`. \n\nThe UTM takes as input a description (encoding) of `M` and the input `w` (e.g., `Tape = <M>#<w>`). It then simulates `M`'s steps on `w`.",
                    "pyq_focus": "Explain the Universal Turing Machine.",
                    "strategy": "This is the **theoretical foundation of the stored-program computer**. Your CPU is a 'real-world' (fixed) UTM. The programs you run (Chrome, Python, etc.) are the 'encodings' `<M>` that the CPU simulates.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "The Halting Problem": {
                    "definition": """
                    The most famous **undecidable** problem.
                    
                    **The Problem:** "Is there a Turing Machine `H` (a 'Halting' checker) that can take *any* TM `M` and *any* input `w` and decide, in a finite amount of time, whether `M` will halt (accept or reject) on input `w`?"
                    
                    **The Answer:** No. Such a machine `H` **cannot exist**. The problem is *undecidable*.
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* 'Explain the Halting Problem.'\n* 'Prove that the Halting Problem is undecidable.'",
                    "strategy": """
                    The proof is a brilliant **proof by contradiction** (a "diagonalization" argument):
                    1.  **Assume:** Assume such a "Halting" checker `H` *does* exist. `H(M, w)` outputs 'HALT' or 'LOOP'.
                    2.  **Construct `D`:** We use `H` to build a new, paradoxical TM `D` ("Diagonal"). `D` takes one input: the encoding of a TM, `<M>`.
                    3.  **`D`'s Logic:**
                        * `D` runs `H` on the input `(M, <M>)`. (It asks `H`, "Will machine M halt if given its own code as input?")
                        * **If `H` says 'HALT'**: `D`'s code says "then *loop* forever."
                        * **If `H` says 'LOOP'**: `D`'s code says "then *halt*."
                    4.  **The Paradox:** Now, what happens when we run `D` on its *own* encoding, `<D>`?
                        * `D(<D>)` must either halt or loop.
                        * **Case 1:** If `D(<D>)` *halts*, it means `H(<D>, <D>)` must have said 'LOOP'. But `D`'s logic says if `H` says 'LOOP', `D` must *halt*. This is correct. Wait...
                        * **Let's re-check `D`'s logic:**
                            * `D(<M>)`:
                                1.  Run `H(<M>, <M>)`.
                                2.  If `H` outputs 'HALT', `D` *loops*.
                                3.  If `H` outputs 'LOOP', `D` *halts*.
                        * **Now, run `D(<D>)`:**
                            * **Case A: Assume `D(<D>)` halts.** By `D`'s logic, this can only happen if `H(<D>, <D>)` outputted 'LOOP'. But if `H` says `D(<D>)` loops, it's wrong, because we *assumed* `D(<D>)` halts. **Contradiction.**
                            * **Case B: Assume `D(<D>)` loops.** By `D`'s logic, this can only happen if `H(<D>, <D>)` outputted 'HALT'. But if `H` says `D(<D>)` halts, it's wrong, because we *assumed* `D(<D>)` loops. **Contradiction.**
                    5.  **Conclusion:** Both possibilities lead to a contradiction. The machine `D` cannot exist. Since `D` is built from `H`, `H` also cannot exist. The problem is undecidable.
                    """,
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Recursive and Recursively Enumerable (RE) Languages": {
                    "definition": """
                    This is about how a TM "accepts" a language.
                    
                    **Recursively Enumerable (RE):** A language `L` is RE if there exists a TM `M` that **halts and accepts** every string `w` in `L`.
                    * If `w ∈ L`: `M` *halts* and says 'yes'.
                    * If `w notin L`: `M` might *halt* and say 'no', OR it might *loop forever*.
                    (This is also called "Turing-recognizable")
                    
                    **Recursive (R) / Decidable:** A language `L` is Recursive if there exists a TM `M` (a "decider") that **halts on all inputs**.
                    * If `w ∈ L`: `M` *halts* and says 'yes'.
                    * If `w notin L`: `M` *halts* and says 'no'.
                    (This TM is an "algorithm" in the true sense).
                    """,
                    "pyq_focus": "**(HIGHLY LIKELY)**\n* 'Differentiate between Recursive and Recursively Enumerable Languages.'",
                    "strategy": "The key difference is **guaranteed halting**. \n* **Recursive = Decidable.** An algorithm exists. The TM *always* stops with a 'yes' or 'no' answer. \n* **RE = Recognizable.** The TM *only* guarantees to stop on 'yes' answers. It might loop on 'no' answers.\n* **Relationship:** All `R` languages are `RE`. Not all `RE` languages are `R`. \n* **The Halting Problem** is the classic example of a language that is `RE` (you can simulate `M` on `w` and 'accept' if it halts) but **not** `Recursive` (you can't *decide* if it will loop).",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                },
                "Chomsky classification of formal languages": {
                    "definition": """
                    The grand hierarchy that ties everything together.
                    
                    * **Type-0: Recursively Enumerable**
                        * **Grammar:** Unrestricted Grammar
                        * **Machine:** Turing Machine
                    
                    * **Type-1: Context-Sensitive**
                        * **Grammar:** Context-Sensitive Grammar (e.g., `|u| ≤ |v|`)
                        * **Machine:** Linear Bounded Automaton (LBA)
                    
                    * **Type-2: Context-Free**
                        * **Grammar:** Context-Free Grammar (e.g., `A → w`)
                        * **Machine:** Pushdown Automaton (PDA)
                    
                    * **Type-3: Regular**
                        * **Grammar:** Regular Grammar (e.g., `A → aB`)
                        * **Machine:** Finite Automaton (DFA/NFA)
                    
                    This is a proper hierarchy: `Type-3 ⊂ Type-2 ⊂ Type-1 ⊂ Type-0`.
                    
                    """,
                    "pyq_focus": "**(GUARANTEED QUESTION)**\n* 'Explain the Chomsky Hierarchy.' (3 or 7 marks).",
                    "strategy": "**Memorize this table.** Know the four types, their names, their grammar, and their machine. This is one of the most fundamental concepts of the entire course and a very common question.",
                    "done": False, "my_notes": "", "my_links": [], "my_photos_bytes": [], "survey": None
                }
            }
        },
        "pyqs": {
            "Module 1: Regular Languages": [
                {"q": "Design a DFA for the language L = {x ∈ {a, b}* | 'aba' is not a substring in x}.", "my_text": "", "my_files": []},
                {"q": "Draw the state-transition diagram showing an NFA N for L = {x ∈ {a, b}* | the second digit from the end is 'b'}. Then, obtain the DFA D equivalent to N by applying the subset construction algorithm.", "my_text": "", "my_files": []},
                {"q": "Design a DFA for recognizing binary numbers which are a multiple of 5.", "my_text": "", "my_files": []},
                {"q": "Write a Regular Grammar for the language: L = {aⁿx | x ∈ {a, b}*, n ≥ 1}", "my_text": "", "my_files": []}
            ],
            "Module 2: More on Regular Languages": [
                {"q": "Using pumping lemma for regular languages, prove that the language L = {aⁿ! | n ∈ N} is not regular.", "my_text": "", "my_files": []},
                {"q": "Obtain the minimum-state DFA from the following DFA. ", "my_text": "", "my_files": []},
                {"q": "Using Kleen’s construction (state elimination), obtain the regular expression for the language represented by the following NFA. ", "my_text": "", "my_files": []},
                {"q": "Write a Regular Expression for the language: L = {x ∈ {0,1}* | there are no consecutive 1's in x}", "my_text": "", "my_files": []}
            ],
            "Module 3: CFGs and Myhill-Nerode": [
                {"q": "Convert the Context-Free Grammar with productions: {S → ASB | ε , A->aAS | a, B->SbS | A | bb} into Chomsky Normal form.", "my_text": "", "my_files": []},
                {"q": "Write a Context-Free Grammar for the language L = {x ∈ {a, b}* | #a(x) = #b(x)} (equal number of a's and b's).", "my_text": "", "my_files": []},
                {"q": "Convert the Context-Free Grammar with productions: {S → aS b | ε} into Greibach Normal form.", "my_text": "", "my_files": []},
                {"q": "Show the equivalence classes of the canonical Myhill-Nerode relation for the language of binary strings with an odd number of 1's.", "my_text": "", "my_files": []}
            ],
            "Module 4: Context-Free Languages": [
                {"q": "Design a PDA for the language L = {w wᴿ | w ∈ {a, b}*} (even length palindromes).", "my_text": "", "my_files": []},
                {"q": "Design a PDA for the language L = {aⁱ bʲ cᵏ | i + j = k, i,j,k >= 0}.", "my_text": "", "my_files": []},
                {"q": "Using pumping lemma for context-free languages, prove that the language: L = {ww | w ∈ {a, b}*} is not a context-free language.", "my_text": "", "my_files": []},
                {"q": "Prove that Context Free Languages are closed under set union.", "my_text": "", "my_files": []}
            ],
            "Module 5: Turing Machines": [
                {"q": "Design a Turing Machine for the language L = {aⁿbⁿcⁿ | n ≥ 1}.", "my_text": "", "my_files": []},
                {"q": "Design a Turing machine to obtain the sum of two natural numbers a and b, both represented in unary on the alphabet set {1}. Assume tape is `⊢1ᵃ01ᵇ...` and should halt with `⊢1ᵃ⁺ᵇ...`", "my_text": "", "my_files": []},
                {"q": "Differentiate between Recursive and Recursively Enumerable Languages.", "my_text": "", "my_files": []},
                {"q": "Explain the Halting Problem and argue that it is undecidable.", "my_text": "", "my_files": []},
                {"q": "Write a Context Sensitive Grammar for the language L = {aⁿbⁿcⁿ | n ≥ 1}", "my_text": "", "my_files": []}
            ]
        }
    }

# --- (2) HELPER FUNCTIONS ---
# These handle file/data conversions

def get_state_as_json():
    """Converts the entire session state to a JSON string for downloading."""
    # We can't serialize Streamlit's UploadedFile objects, but we already
    # converted them to b64 strings, so we are good to go.
    return json.dumps(st.session_state.study_data, indent=2)

def create_download_link(json_string, filename="cst301_progress.json"):
    """Generates a base64-encoded download link for the JSON data."""
    b64 = base64.b64encode(json_string.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}" style="background-color: #0068c9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Save My Progress</a>'
    return href

def file_to_b64(file):
    """Converts an UploadedFile object to a base64 string."""
    file_bytes = file.getvalue()
    b64_string = base64.b64encode(file_bytes).decode()
    return b64_string

def display_b64_file(b64_string, file_name):
    """Displays a base64 file (image or PDF) in Streamlit."""
    try:
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            st.image(base64.b64decode(b64_string), caption=file_name, use_column_width=True)
        elif file_name.lower().endswith('.pdf'):
            # This is a common workaround to embed PDFs
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_string}" width="700" height="500" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.warning(f"Can't preview file type: {file_name}")
    except Exception as e:
        st.error(f"Error displaying file {file_name}: {e}")

# --- (3) MAIN APP LOGIC ---

# Set wide mode and a title
st.set_page_config(layout="wide", page_title="CST 301 Study Tracker")

# Initialize session state
if 'study_data' not in st.session_state:
    st.session_state.study_data = get_initial_data()

# Get the master data object
study_data = st.session_state.study_data

# --- Sidebar Navigation ---
st.sidebar.title("CST 301 Study Tracker")
st.sidebar.header("Navigation")

# Calculate progress for the sidebar
total_topics = 0
completed_topics = 0
for mod, topics in study_data["modules"].items():
    total_topics += len(topics)
    for topic_name, topic_data in topics.items():
        if topic_data["done"]:
            completed_topics += 1

if total_topics > 0:
    progress_percent = completed_topics / total_topics
    st.sidebar.progress(progress_percent)
    st.sidebar.caption(f"{completed_topics} / {total_topics} Topics Completed")
else:
    st.sidebar.progress(0)
    st.sidebar.caption("0 / 0 Topics Completed")

view_options = ["📈 Dashboard"] + list(study_data["modules"].keys()) + ["✍️ PYQ Practice"]
view = st.sidebar.radio("Go to:", view_options)

st.sidebar.divider()
st.sidebar.warning("Your progress is saved in this browser session. **Use the 'Save My Progress' button on the Dashboard to download a file** you can load later.")


# --- View 1: Progress Dashboard ---
if view == "📈 Dashboard":
    st.title("📈 CST 301 Progress Dashboard")
    st.markdown("Welcome to your study tracker! Use the sidebar to navigate to a module or practice PYQs.")

    col1, col2 = st.columns(2)
    with col1:
        st.header("Overall Progress")
        if total_topics > 0:
            st.progress(progress_percent)
            st.metric(label="Topics Completed", value=f"{completed_topics} / {total_topics}")
        else:
            st.info("No topics found.")

    with col2:
        st.header("Self-Assessment")
        confidence_counts = {"Not Confident": 0, "Somewhat Confident": 0, "Very Confident": 0}
        for mod, topics in study_data["modules"].items():
            for topic_name, topic_data in topics.items():
                if topic_data["done"] and topic_data["survey"]:
                    if topic_data["survey"].startswith("Not Confident"):
                        confidence_counts["Not Confident"] += 1
                    elif topic_data["survey"].startswith("Somewhat Confident"):
                        confidence_counts["Somewhat Confident"] += 1
                    elif topic_data["survey"].startswith("Very Confident"):
                        confidence_counts["Very Confident"] += 1
        
        st.bar_chart(confidence_counts)


    st.divider()

    # --- Save/Load Section ---
    st.header("Save & Load Your Progress")
    st.warning("🚨 **IMPORTANT:** This app does not have a database. Your progress is lost when you close this tab. **Save your progress by downloading the JSON file** and load it when you return.")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Save Progress")
        json_data = get_state_as_json()
        st.markdown(create_download_link(json_data), unsafe_allow_html=True)
        st.info("Click the button above to save a JSON file of all your notes, links, and progress.")

    with col2:
        st.subheader("Load Progress")
        uploaded_file = st.file_uploader("Upload your `cst301_progress.json` file", type="json")
        if uploaded_file is not None:
            try:
                loaded_data = json.load(uploaded_file)
                # Basic validation
                if "modules" in loaded_data and "pyqs" in loaded_data:
                    # Overwrite the session state with the loaded data
                    st.session_state.study_data = loaded_data
                    st.success("Progress loaded successfully!")
                    st.info("The page will now reload to reflect your data.")
                    st.rerun() 
                else:
                    st.error("This does not appear to be a valid progress file.")
            except Exception as e:
                st.error(f"Error loading file: {e}")

# --- View 2: Module Study View ---
elif view in study_data["modules"].keys():
    module_key = view
    module_data = study_data["modules"][module_key]
    st.title(f"📚 {module_key}")

    # Topic selection
    topic_name = st.selectbox("Select a topic to study:", module_data.keys())
    
    # Get the data for the selected topic
    topic_data = module_data[topic_name]
    
    st.divider()
    
    # --- Checkbox to mark as done ---
    # This is the "production-level" way to handle state updates in Streamlit.
    # The widget's value is set *from* the state.
    # When the widget is changed by the user, the script reruns.
    # *After* the widget is rendered, we update the state with the new value.
    is_done = st.checkbox(
        "Mark as Done", 
        value=topic_data["done"], 
        key=f"{module_key}_{topic_name}_done"
    )
    st.session_state.study_data["modules"][module_key][topic_name]["done"] = is_done
    
    # --- Pre-filled Content ---
    st.header("🎓 Core Content")
    tab_def, tab_pyq, tab_strat = st.tabs(["📜 Definition", "🎯 PYQ Focus", "💡 Strategy"])
    with tab_def:
        st.markdown(topic_data["definition"])
    with tab_pyq:
        st.info(topic_data["pyq_focus"])
    with tab_strat:
        st.success(topic_data["strategy"])

    # --- User's Study Hub ---
    st.divider()
    st.header("My Study Hub")
    tab_notes, tab_links, tab_media = st.tabs(["My Notes", "My Links", "My Media (Photos/Diagrams)"])

    with tab_notes:
        notes = st.text_area(
            "Add your personal notes, summaries, and questions here...", 
            value=topic_data["my_notes"], 
            height=300, 
            key=f"{module_key}_{topic_name}_notes"
        )
        st.session_state.study_data["modules"][module_key][topic_name]["my_notes"] = notes

    with tab_links:
        st.markdown("Add links to useful YouTube videos, articles, or tutorials.")
        new_link = st.text_input("Paste a URL:", key=f"{module_key}_{topic_name}_link_input")
        
        if st.button("Add Link", key=f"{module_key}_{topic_name}_link_btn"):
            if new_link and new_link.startswith("http"):
                st.session_state.study_data["modules"][module_key][topic_name]["my_links"].append(new_link)
                st.rerun() # Refresh to clear input and show new link
            else:
                st.warning("Please enter a valid URL (starting with http).")
        
        st.subheader("My Saved Links:")
        for i, link in enumerate(topic_data["my_links"]):
            col1, col2 = st.columns([0.9, 0.1])
            col1.markdown(f"- [{link}]({link})")
            if col2.button("X", key=f"{module_key}_{topic_name}_link_del_{i}", help="Delete this link"):
                st.session_state.study_data["modules"][module_key][topic_name]["my_links"].pop(i)
                st.rerun()

    with tab_media:
        st.markdown("Upload your own diagrams, mind maps, or photos of handwritten notes.")
        
        # File uploader for adding new media
        uploaded_files = st.file_uploader(
            "Upload files (PNG, JPG, PDF)", 
            accept_multiple_files=True, 
            type=["png", "jpg", "jpeg", "pdf"],
            key=f"{module_key}_{topic_name}_photos_uploader"
        )
        
        if uploaded_files:
            for file in uploaded_files:
                file_b64 = file_to_b64(file)
                st.session_state.study_data["modules"][module_key][topic_name]["my_photos_bytes"].append({
                    "name": file.name,
                    "b64": file_b64
                })
            # We must rerun to clear the file uploader and show the new files
            st.rerun()

        st.subheader("My Saved Media:")
        if not topic_data["my_photos_bytes"]:
            st.info("No media uploaded for this topic yet.")
        
        # Display saved media with delete buttons
        for i, file_data in enumerate(topic_data["my_photos_bytes"]):
            st.markdown(f"**{file_data['name']}**")
            display_b64_file(file_data['b64'], file_data['name'])
            
            if st.button(f"Delete {file_data['name']}", key=f"{module_key}_{topic_name}_media_del_{i}"):
                st.session_state.study_data["modules"][module_key][topic_name]["my_photos_bytes"].pop(i)
                st.rerun()
            st.divider()

            
    # --- Survey (as requested) ---
    if is_done:
        st.divider()
        st.header("🧠 Self-Assessment")
        st.write("Now that you've marked this topic as done, how confident do you feel?")
        
        survey_options = ["---", "Not Confident (Need Review)", "Somewhat Confident", "Very Confident (Ready for Exam)"]
        
        # Find index for radio button
        current_survey_val = topic_data.get("survey") # Use .get for safety
        if current_survey_val in survey_options:
            survey_index = survey_options.index(current_survey_val)
        else:
            survey_index = 0

        response = st.radio(
            "Confidence Level:", 
            survey_options, 
            index=survey_index, 
            key=f"{module_key}_{topic_name}_survey"
        )
        
        if response != "---":
            st.session_state.study_data["modules"][module_key][topic_name]["survey"] = response
        else:
            st.session_state.study_data["modules"][module_key][topic_name]["survey"] = None


# --- View 3: PYQ Practice ---
elif view == "✍️ PYQ Practice":
    st.title("✍️ PYQ Practice Portal")
    st.info("Test your knowledge with questions from previous years. Your answers are saved with your progress file.")
    
    pyq_module = st.selectbox("Select Module:", study_data["pyqs"].keys())
    
    st.divider()
    
    questions = study_data["pyqs"][pyq_module]
    
    for i, q_data in enumerate(questions):
        st.header(f"Question {i+1}")
        st.markdown(f"**{q_data['q']}**")
        
        with st.expander(f"Show/Hide My Answer for Q{i+1}"):
            # Text Answer
            answer_text = st.text_area(
                "Type your answer, notes, or solution plan:", 
                value=q_data["my_text"], 
                key=f"{pyq_module}_q{i}_text"
            )
            st.session_state.study_data["pyqs"][pyq_module][i]["my_text"] = answer_text
            
            # File Answer
            st.subheader("My Solution Files")
            
            # File uploader for adding new files
            uploaded_solution = st.file_uploader(
                "Upload your handwritten solution (PDF, PNG, JPG)", 
                type=["pdf", "png", "jpg", "jpeg"], 
                key=f"{pyq_module}_q{i}_file_uploader"
            )
            
            if uploaded_solution:
                file_b64 = file_to_b64(uploaded_solution)
                st.session_state.study_data["pyqs"][pyq_module][i]["my_files"].append({
                    "name": uploaded_solution.name,
                    "b64": file_b64
                })
                st.rerun()

            # Display saved files
            if not q_data["my_files"]:
                st.info("No solution files uploaded for this question yet.")

            for file_index, file_data in enumerate(q_data["my_files"]):
                st.markdown(f"**{file_data['name']}**")
                display_b64_file(file_data['b64'], file_data['name'])
                
                if st.button(f"Delete {file_data['name']}", key=f"{pyq_module}_q{i}_file_del_{file_index}"):
                    st.session_state.study_data["pyqs"][pyq_module][i]["my_files"].pop(file_index)
                    st.rerun()
                st.divider()