# Reporting errors

[日本語](CONTRIBUTING.ja.md)

The proof of the main theorem is partly computational. Reports of errors and of failed reproductions are very welcome, in English or Japanese.

## How to report

Open an [issue](https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/issues/new/choose) and choose a template:

- **Mathematical error**: a gap or an error in a proof, a statement or a computation. Give the version (tag) you read, the location, and why the step fails. A counterexample or the missing case is welcome but not required.
- **Verification fails or cannot be run**: a check that fails, a computed result that does not agree with the paper, or instructions that do not work. Include the command, its full output, `out/<step>.json` if one was written, and your environment. A failing check of `proof.sh` or `full.sh` is treated as a possible error in the proof until it is explained.
- **Text, references or documentation**: unclear wording, a wrong citation, a missing explanation, or a difference between the English and Japanese versions.

## What happens after a report

1. The report is acknowledged in the issue, and its effect on Theorem A, Theorem B and the supplement is assessed there.
2. A correction is made in a pull request that refers to the issue. Only the sources change in a pull request; the PDFs are regenerated at the next release.
3. The correction appears in the next dated release. [CHANGELOG.md](CHANGELOG.md) states for every release whether a mathematical statement changed, and names the issue. Earlier tags and releases are kept unchanged, so every version that has been cited stays available.

## Pull requests

Pull requests are welcome for documentation and code. For a change that affects a mathematical statement or proof, please open an issue first. Pull requests change sources only (`.typ`, code, Lean, Markdown), not the committed PDFs. CI runs the input checks, the tests, the container build, the Typst build, `paper/tools/check-paper.py` and the Lean check on every pull request.
