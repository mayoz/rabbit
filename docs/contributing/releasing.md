# Releasing

Users get a new version when `version` in `.claude-plugin/plugin.json` changes
on `main`; the tag only publishes the GitHub release. Tagging needs a GPG or SSH
signing key set up in git (`user.signingkey`).

1. In a pull request to `main`, bump `version` in `.claude-plugin/plugin.json`
   and add a `## [<version>] - <YYYY-MM-DD>` section to `CHANGELOG.md`.
2. Run the checks and the evals ([development](development.md)), and pull one
   real sprint and take one task to its brief with your development copy.
3. After the pull request merges, tag `main`:

   ```bash
   git switch main && git pull
   ```

   ```bash
   git tag -s v<version> -m v<version>
   ```

   ```bash
   git push origin v<version>
   ```

   The tag must match `version` in `.claude-plugin/plugin.json`; the
   `release` workflow stops when it does not.
4. The `release` workflow publishes a GitHub release with that CHANGELOG
   section.
5. On a clean machine, run the install commands from the README and check that
   `/rabbit` lists the four commands.
