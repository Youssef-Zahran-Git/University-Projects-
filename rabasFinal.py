import math
def Gauss_Seidal_method():
    """Solving a system of linear equations using the Gauss-Seidel method."""

    # ==================================================
    # =========== step 0 helper functions ==============
    # ==================================================

    # helper function 1: float input validator
    def read_numbers(prompt):
        """Accepting only a real, finite number (int or decimal)."""
        while True:
            text = input(prompt).strip()
            try:
                value = float(text)
            except ValueError:          # empty text, letters, symbols, ...
                print("   [!] Not a number. Valid examples: 4 , -2.5 , 0.001")
                continue
            if not math.isfinite(value):        # reject nan / inf
                print("   [!] The number must be finite (no 'nan' or 'inf').")
                continue
            return value

    # helper function 2: integer input validator (range is now a parameter)
    def read_int(prompt, lo, hi):
        """Accepting only an integer inside [lo, hi]."""
        while True:
            text = input(prompt).strip()
            try:
                value = int(text)
            except ValueError:
                print("   [!] Not an integer. Valid examples: 2 , 4")
                continue                        # <-- was missing
            if not (lo <= value <= hi):
                print("   [!] The number must be >= " + str(lo) + " & <= " + str(hi))
                continue
            return value

    # helper function 3: positive value input validator
    def read_positive(prompt):
        """Reads only a positive real number (used for the accepted error)."""
        while True:
            text = input(prompt).strip()
            try:
                value = float(text)             # <-- was int(text)
            except ValueError:
                print("   [!] Not a number. Valid examples: 0.5 , 0.001")
                continue
            if not math.isfinite(value) or value <= 0:
                print("   [!] The number must be positive and finite.")
                continue
            return value

    # helper function 4: yes/no input
    def read_yes_no(message):
        """Accept only y / n (any capitalisation)."""
        while True:
            text = input(message).strip().lower()
            if text in ("y", "yes"):
                return True
            if text in ("n", "no"):
                return False
            print("   [!] Please answer y or n.")

    # helper function 5: every possible arrangement of the equations
    def all_orders(equations_order):
        """Recursive GENERATOR: yields every permutation, e.g. [0,2,1].
        Yielding (instead of building one huge list) keeps memory small."""
        if len(equations_order) == 0:           # base case
            yield []
            return
        for i in range(len(equations_order)):
            first = equations_order[i]
            rest = equations_order[:i] + equations_order[i + 1:]
            for tail in all_orders(rest):       # recursive step
                yield [first] + tail

    # ===========================================
    # ========= Step 1 reading user input =======
    # ===========================================
    def read_equation():
        """Taking user input and validating the values."""
        print("=" * 30)
        print("===== GAUSS-SEIDEL METHOD =====")
        print("=" * 30)
        n = read_int("How many equations (variables) (2-10): ", 2, 10)
        a = []
        b = []
        for i in range(n):
            print(f"Equation {i+1}: a1*x1 + a2*x2 + ... = b")
            while True:
                row = []
                for j in range(n):
                    row.append(read_numbers(f"The value of x{j+1}: "))   # j, not i
                rhs = read_numbers("The right hand side b: ")
                allZeros = True
                for val in row:                 # iterate the list, not range(list)
                    if val != 0:
                        allZeros = False
                if allZeros:
                    print("   [!] All coefficients are zero. Re-enter this equation.")
                    continue
                break                           # the equation is accepted
            a.append(row)
            b.append(rhs)
        return a, b, n

    # ======================================================================
    # ===== Step 2 checking for diagonal dominance and sorting =============
    # ======================================================================
    def dominance_type(rows):
        """True if every row has |a_ii| > sum of the other |a_ij|."""
        n = len(rows)
        for i in range(n):
            diagonal = abs(rows[i][i])
            others = 0.0
            for j in range(n):
                if j != i:
                    others = others + abs(rows[i][j])
            if diagonal <= others:
                return False
        return True

    def sort_for_dominance(a, b, n):
        """Sorting the equations & starting the solving process."""
        print("\n--- Checking diagonal dominance ---")
        if dominance_type(a):
            print("The equations ARE diagonally dominant (no sorting needed).")
            return a, b, True

        print("The equations are NOT diagonally dominant. Trying to sort them...")
        indexes = []
        for i in range(n):
            indexes.append(i)

        safe_A = None                           # fallback: no zero on the diagonal
        safe_b = None
        for order in all_orders(indexes):
            rows = []
            rhs = []
            for i in order:
                rows.append(a[i])
                rhs.append(b[i])
            if dominance_type(rows):
                print("The equations were SORTED and are now diagonally dominant.")
                return rows, rhs, True
            if safe_A is None:                  # remember a division-safe ordering
                zero_diagonal = False
                for i in range(n):
                    if rows[i][i] == 0:
                        zero_diagonal = True
                if not zero_diagonal:
                    safe_A = rows
                    safe_b = rhs

        print("[!] No ordering of these equations is diagonally dominant.")
        print("    Gauss-Seidel may diverge for this system.")
        if safe_A is None:
            print("[!] Every ordering has a zero on the diagonal (division by zero).")
            return a, b, False
        if read_yes_no("Run the iterations anyway with a safe ordering? (y/n): "):
            return safe_A, safe_b, True
        return a, b, False

    def print_system(A, b, n):
        """Show the system in the order that will really be used."""
        print("\nSystem used by the solver:")
        for i in range(n):
            terms = []
            for j in range(n):
                terms.append("(" + format(A[i][j], "g") + ")*x" + str(j + 1))
            print("   " + " + ".join(terms) + " = " + format(b[i], "g"))

    # =======================================================================
    # ===== Step 3 showing the equation used for each variable ==============
    # =======================================================================
    def show_variable_equations(a, b, n):
        """Showing the user the equation used to solve for each variable."""
        print("\n--- Equation of each variable (Gauss-Seidel form) ---")
        for i in range(n):
            text = "x" + str(i + 1) + " = ( " + format(b[i], "g")
            for j in range(n):
                if j != i and a[i][j] != 0:
                    if a[i][j] < 0:             # - * - = +
                        text = text + " + " + format(abs(a[i][j]), "g") + "*x" + str(j + 1)
                    else:
                        text = text + " - " + format(a[i][j], "g") + "*x" + str(j + 1)
            text = text + " ) / " + format(a[i][i], "g")
            print("   " + text)
        print("   (each new value is used immediately in the next equation "
              "(Gauss-Seidel > Gauss-Jacobi) )")

    # =====================================================================
    # ====== Step 4 iteration table & the solving algorithm ===============
    # =====================================================================
    def print_table_header(n):
        """Prints the header of the solution table with padding."""
        line = "Iter".rjust(5)
        for j in range(n):
            line = line + ("x" + str(j + 1)).rjust(14)
        for j in range(n):
            line = line + ("ea" + str(j + 1) + "(%)").rjust(13)
        line = line + "max ea(%)".rjust(13)
        print(line)
        print("-" * len(line))

    def print_table_row(it, x, errors):
        """One row: width 14 for the values of x, width 13 for the errors."""
        line = str(it).rjust(5)
        for value in x:
            line = line + format(value, "14.6f")
        if errors is None:                      # iteration 0 -> no error yet
            for k in range(len(x) + 1):
                line = line + "-".rjust(13)
        else:
            for e in errors:
                line = line + format(e, "13.6f")
            line = line + format(max(errors), "13.6f")
        print(line)

    def solve(a, b, x, n, tol, max_iter):
        """
        Gauss-Seidel sweep (uses the NEW values inside the same iteration):
            x_i = ( b_i - sum(a_ij * x_j for j != i) ) / a_ii
        Approximate error:  ea_i = |(x_new - x_old) / x_new| * 100
        Stop when the largest error of the iteration is below the tolerance.
        """
        print("\n--- Iteration table ---")
        print_table_header(n)
        print_table_row(0, x, None)
        converged = False
        it = 0
        for it in range(1, max_iter + 1):
            old_x = x[:]                        # copy of the previous iteration
            for i in range(n):
                total = b[i]
                for j in range(n):
                    if j != i:
                        total = total - a[i][j] * x[j]   # x[j] already new if j < i
                x[i] = total / a[i][i]

            errors = []
            for i in range(n):
                if x[i] != 0:
                    errors.append(abs((x[i] - old_x[i]) / x[i]) * 100)
                else:
                    errors.append(abs(x[i] - old_x[i]) * 100)   # avoid dividing by 0
            print_table_row(it, x, errors)

            diverging = False
            for value in x:
                if not math.isfinite(value) or abs(value) > 1e12:
                    diverging = True
            if diverging:
                print("\n[!] The values are blowing up: the method diverges here.")
                return None

            if max(errors) < tol:
                converged = True
                break

        if converged:
            print("\nConverged after " + str(it) + " iterations (max error < " + str(tol) + " %).")
        else:
            print("\n[!] Maximum iterations reached before the tolerance was met.")
        return x

    # =====================================================================
    # MAIN FLOW: input -> dominance/sorting -> variable equations -> table
    # =====================================================================
    while True:                                 # ask again if the system is unusable
        a, b, n = read_equation()
        a, b, ok = sort_for_dominance(a, b, n)
        if ok:
            break
        print("\nPlease enter the equations again.\n")

    print_system(a, b, n)
    show_variable_equations(a, b, n)

    x = []
    for i in range(n):
        x.append(0.0)
    if not read_yes_no("\nUse zeros as the initial guess? (y/n): "):
        for i in range(n):
            x[i] = read_numbers("   initial guess for x" + str(i + 1) + " : ")

    tol = read_positive("\nStopping tolerance in % (e.g. 0.001): ")
    max_iter = read_int("Maximum number of iterations (1-1000): ", 1, 1000)

    solution = solve(a, b, x, n, tol, max_iter)
    if solution is not None:
        print("\nApproximate solution:")
        for i in range(n):
            print("   x" + str(i + 1) + " = " + format(solution[i], ".6f"))


if __name__ == "__main__":
    Gauss_Seidal_method()