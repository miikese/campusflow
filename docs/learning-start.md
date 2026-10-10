# Your first personal actions

Confirm whether you are Engineer A or B and your partner's responsibility.
Supply the shared GitHub repository URL and your partner's real username.
Before implementing your feature, select two topics you do not understand,
describe your current understanding, and predict an experiment's outcome.

The following examples are suggestions. They have not been run by either
fellow and must not be recorded as personal evidence until you run them.

## Suggested topic: Boolean values and integers

`isinstance` recognizes subclasses. Python's Boolean type is an integer
subclass, so a count validator needs a deliberate policy for Boolean input.
Predict each result, run the example yourself, then explain what you learned:

```sh
python3 - <<'PY'
for value in [True, 2, 2.0, "2"]:
    print(repr(value), isinstance(value, int), type(value) is int)
PY
```

## Suggested topic: numeric sorting keys

Strings compare characters, while a key function can extract a number from
each record. Predict both outputs before running this unrelated example:

```sh
python3 - <<'PY'
labels = ["box10", "box2", "box1"]
print(sorted(labels))
print(sorted(labels, key=lambda label: int(label[3:])))
PY
```

Record your actual prompts, predictions, command/output and own explanation
in the log. Pick different topics if these are already familiar. During
implementation, record a third genuine interaction and a real suggestion
you improved or rejected after verification; do not manufacture one.

