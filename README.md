# Three free Pydantic validator migration samples

This preview contains exactly three original migration rules for coding
agents and developers. Each rule has structured metadata and separate Pydantic
V1 and V2 Python examples. The samples are free to use under the MIT license.
They were prepared with AI assistance on September 8, 2026 and are not affiliated
with Pydantic.

**Validation passed:** all 12 behavior checks pass in each pinned environment
(24 executions total) in [hosted run 34220636575](https://github.com/sabre-coder/pydantic-validator-migration-samples/actions/runs/34220636575),
testing commit `3667cf0ac7c94fe1f8b0ca9f2ff1f6b4240f19de`.
The examples were executed only on disposable GitHub-hosted runners.

| Rule | V1 pattern | V2 pattern |
| --- | --- | --- |
| `item-validator` | `@validator(..., each_item=True)` after type validation | `Annotated` on the item type with `AfterValidator` |
| `default-validator` | `@validator(..., pre=True, always=True)` | `@field_validator(..., mode="before")` and an explicit default with `validate_default=True` |
| `validation-exception` | Deliberate input rejection using `TypeError` | Deliberate input rejection using `ValueError`; programming `TypeError` still propagates |

Start with [rules.json](rules.json), then follow its `before` and `after` paths.
The JSON includes applicability conditions, example inputs, expected outcomes,
review boundaries and authoritative source links. These are reviewable patterns,
not an automatic codemod or a complete migration guide.

## Version bounds

The prepared validation matrix is deliberately narrow:

- Before examples: Pydantic **1.10.26**.
- After examples: Pydantic **2.13.5**.
- Both: CPython **3.12.14**, Linux on a disposable GitHub-hosted runner.

Pydantic and its runtime dependencies are pinned in `requirements-v1.txt` and
`requirements-v2.txt`. Release metadata was checked on September 8, 2026.
The linked successful run uses exactly these pins.
Other package or Python versions, frameworks, inheritance, assignment validation,
and different coercion policies require their own checks. V1 does not support
Python 3.14 or later.

The examples preserve the explicitly listed cases. They do not promise identical
error dictionaries or all coercion behavior between V1 and V2. In particular,
Pydantic V2 intentionally lets a validator's programming `TypeError` escape;
the third rule demonstrates that distinction instead of hiding it.

## Hosted validation

Run the **Validate three free samples** workflow to reproduce validation.
It also runs on a push to relevant sample files.
On a public repository, each matrix job installs one pinned environment and runs
the same 12 behavioral tests against that version's examples. Its token has only `contents: read`,
checkout credentials are not persisted, and no secrets are used.

The hosted commands are:

```sh
python -m pip install --only-binary=:all: -r requirements-v1.txt
PYDANTIC_LINE=1 python -m unittest discover -s tests -v
```

The second job uses `requirements-v2.txt` and `PYDANTIC_LINE=2` in a fresh runner.
These commands are for the disposable hosted environment; dependency execution
remains outside the local preparation workflow. Before claiming validation,
record the tested commit and successful results for both jobs.

## Authoritative references

- [V2 migration guide: validator changes](https://docs.pydantic.dev/latest/migration/)
- [V2 validator concepts, default validation and exceptions](https://docs.pydantic.dev/latest/concepts/validators/)
- [V1 validators and per-item caveats](https://docs.pydantic.dev/1.10/usage/validators/)
- [V1 Python support](https://docs.pydantic.dev/1.10/)
- [Pydantic version policy](https://docs.pydantic.dev/latest/version-policy/)
- [V1 release metadata](https://pypi.org/pypi/pydantic/1.10.26/json)
- [V2 release metadata](https://pypi.org/pypi/pydantic/2.13.5/json)

The linked documentation is freely available from Pydantic. This preview adds
original examples and explicit behavioral cases; it does not reproduce or sell
the upstream documentation. No larger paid pack, customer order or completed
customer migration is represented by this preview.

## Custom migration help

We are testing a custom pack offer at **0.00040 native ETH on Ethereum mainnet**
for up to three small validator functions. It would include tailored before/after
examples, structured rules, source links and tests for agreed behavior.

Open an issue with your Python/Pydantic versions and a short description of the
needed behavior. Share only code you have permission to disclose, without secrets.
Scope, acceptance cases, payment timing and delivery must be agreed before work
starts. No larger paid pack is already built, and no payment is requested before
an agreement. This is a proposed service, not a Pydantic-affiliated product.
