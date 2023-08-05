from funcy import is_seq


def join(words):
    words = list(words)
    if not words:
        return ""

    return (
        "{before} and {after}".format(
            before=", ".join(words[:-1]), after=words[-1],
        )
        if len(words) > 1
        else words[0]
    )


def get_summary(stats):
    status = (
        (state, len(data) if is_seq(data) else data)
        for state, data in stats
        if data
    )
    return join(
        "{} file{} {}".format(num, "s" if num > 1 else "", state)
        for state, num in status
    )
