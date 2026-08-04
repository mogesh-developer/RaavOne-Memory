def build_context(
    memories,
    query: str,
):
    lines = []

    lines.append(
        "Relevant User Memories:\n"
    )

    for memory in memories:

        lines.append(
            f"- {memory}"
        )

    lines.append(
        "\nCurrent User Question:\n"
    )

    lines.append(query)

    return "\n".join(lines)