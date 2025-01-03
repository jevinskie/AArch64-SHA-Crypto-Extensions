from yattag import Doc


def generate_table(label, operands, result_label="result"):
    doc, tag, text = Doc().tagtext()

    # Start the table
    # with tag("table", border="0", cellborder="1", cellspacing="0"):
    with tag("table", border="1"):
        # First row: Combined label spanning two cells
        with tag("tr"):
            with tag("td", colspan="2"):
                text(label)

        # Second row: Left cell split into operands, right cell is result
        for i, operand in enumerate(operands, 1):
            with tag("tr"):
                with tag("td"):
                    text(operand)
                if i == 1:
                    with tag("td", rowspan=f"{len(operands)}"):
                        text(result_label)

    return doc.getvalue()


# Example usage
label = "Node Label"
operands = ["Operand 1", "Operand 2", "Operand 3"]  # Adjust this list for 0 < N <= 3
html_table = generate_table(label, operands)
print(html_table)
