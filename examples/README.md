# Examples

Copy these files as a starting point.

| File | What it shows |
| --- | --- |
| [profiles/minimal.md](profiles/minimal.md) | A profile without a workflow file. Rabbit talks and writes in the language you use. |
| [profiles/personal.md](profiles/personal.md) | A profile that points at a workflow file and chats in Turkish but writes documents in English. |
| [workflows/rabbit-workflow.md](workflows/rabbit-workflow.md) | A team workflow file that uses every common stage. |

Your profile lives at `~/.config/rabbit/profile.md`; `/rabbit:setup` writes it
for you. Copy the workflow file anywhere, edit it, and give its path to
`/rabbit:setup`.

Replace `acme.atlassian.net` and `customfield_<id>` with your own values, or let
`/rabbit:setup` find them. See [Your profile](../docs/profile.md) and
[Customizing Rabbit](../docs/customizing.md).
